import wx
import wx.lib.scrolledpanel as scrolled
from custom_widgets import DraggableNumber, DraggableNumberEvent
# --- Constants for note names and black-key positions ---
NOTE_NAMES = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
BLACK_KEYS = {1, 3, 6, 8, 10}

def midi_to_note(n: int) -> str:
    """Convert 0–127 to 'C 3' style with C3 at 60."""
    octave = (n // 12) - 2
    name   = NOTE_NAMES[n % 12]
    return f"{name} {octave}"


yellow = (235, 243, 190, 0)
purple = (210, 164, 237, 0)
greencontrol = (153, 245, 198, 0)
salmon = (237, 164, 164, 0)
cyanish = (164, 198, 237, 0)
greeny= (73, 245, 102, 0)  
bluefresh = (86, 245, 216)  
bluesky = (167, 233, 245)
orange = (245, 175, 81, 0)
orangelight = (245, 220, 162, 0)
key_color = (200,200,200)
key_color_ol = (130,130,130)
grey = wx.Colour(153, 245, 198)
bg_color = (157, 134, 134)
bkey = (193, 245, 238)
range_box_color = (250,150,255)
fade_box_color = wx.Colour(153, 245, 198)
# --- Color configuration ---
COLOR_LOWKEY_HANDLE     = wx.Colour(  0, 128,   0)
COLOR_ORIGKEY_HANDLE    = wx.Colour(73, 245, 102)
COLOR_HIGHKEY_HANDLE    = wx.Colour(  0,   0, 128)

COLOR_LOWFADE_BOX_BASE  = wx.Colour(153, 245, 198)
COLOR_HIGHFADE_BOX_BASE = wx.Colour(153, 245, 198)

COLOR_LOWFADE_HANDLE    = wx.Colour(  0, 160,   0)
COLOR_HIGHFADE_HANDLE   = wx.Colour(  0,   0, 160)

COLOR_ORIGKEY_LINE      = wx.Colour(40, 255, 70)

COLOR_TEXT              = wx.Colour( 50, 205,  50)

# --- Top strip: full 0–127 keyboard, transparent window style ---
class KeyTopStrip(wx.Panel):
    def __init__(self, parent, height=40):
        super().__init__(
            parent,
            style=wx.TRANSPARENT_WINDOW,
            size=(-1, height)
        )
        self.SetMinSize((-1, height))
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.SetBackgroundColour(wx.Colour(bg_color))
        # try:
        #     self.SetTransparent(200)
        # except Exception:
        #     pass
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, evt):
        dc = wx.AutoBufferedPaintDC(self)
        w, h = self.GetClientSize()
        key_w = w / 128

        # # draw white keys
        # dc.SetPen(wx.Pen(wx.Colour(180,180,180), 1))
        # for i in range(128):
        #     x = int(i * key_w)
        #     dc.SetBrush(wx.Brush(wx.Colour(key_color)))
        #     dc.DrawRectangle(x, 0, int(key_w) + 1, h)


        dc.SetBrush(wx.Brush(wx.Colour(key_color)))
        dc.SetPen(wx.Pen(wx.Colour(180,180,180), 1))
        dc.DrawRectangle(0, 0, w, h)

        # draw black keys
        dc.SetBrush(wx.BLACK_BRUSH)
        for i in range(128):
            if (i % 12) in BLACK_KEYS:
                x = int(i * key_w)
                dc.DrawRectangle(x, 0, int(key_w) + 1, int(h * 0.6))

        # label each C
        dc.SetTextForeground(wx.Colour(0, 0, 0))
        for i in range(0, 128, 12):
            x = int(i * key_w)
            dc.DrawText(midi_to_note(i), x + 2, h // 2 + 5)





# --- Zone strip: handles + triangular fade zones with colored handles/lines/text ---
class KeyWindowStrip(wx.Panel):
    HANDLE_SIZE = 10

    # handle → (MIDI PID, attribute name)
    HANDLE_MAP = {
        'lowfade':  (46, 'low_fade'),
        'highfade': (48, 'high_fade'),
        'low':      (45, 'low'),
        'high':     (47, 'high'),
        'orig':     (44, 'orig'),
    }

    def __init__(self, parent,
                 orig, low, high, low_fade, high_fade,
                 voice_index, zone_index, group_num, main):
        super().__init__(parent)
        self.main        = main
        self.voice_index = voice_index
        self.zone_index  = zone_index
        self.group_num   = group_num

        # model
        self.orig      = orig
        self.low       = low
        self.high      = high
        self.low_fade  = low_fade
        self.high_fade = high_fade
        self.selected  = None

        # ── LAYOUT ────────────────────────────────────────────────────
        vs = wx.BoxSizer(wx.VERTICAL)

        # 1) drawing panel
        self.canvas = wx.Panel(self, style=wx.TRANSPARENT_WINDOW, size=(-1, 60))
        self.canvas.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.canvas.Bind(wx.EVT_PAINT,     self.OnPaint)
        self.canvas.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        self.canvas.Bind(wx.EVT_MOTION,    self.OnMouseDrag)
        self.canvas.Bind(wx.EVT_LEFT_UP,   self.OnMouseUp)
        vs.Add(self.canvas, 0, wx.EXPAND)

        # 2) numeric row
        hs = wx.BoxSizer(wx.HORIZONTAL)
        self._num_controls = {}
        for name, (pid, attr) in self.HANDLE_MAP.items():
            val = getattr(self, attr)
            dn = DraggableNumber(
                self, id=pid, value=val, min_val=0, max_val=127,
                callback=self._on_number_change
            )
            dn.SetMinSize((60, 30))
            dn.SetToolTip(f"{name}")
            hs.Add(dn, 0, wx.ALL, 2)
            self._num_controls[name] = dn
        vs.Add(hs, 0, wx.EXPAND)

        self.SetSizer(vs)

    # ── PAINTING ────────────────────────────────────────────────────
    def OnPaint(self, evt):
        dc = wx.AutoBufferedPaintDC(self.canvas)
        w, h = self.canvas.GetClientSize()
        key_w = w / 128.0
        pad   = 2

        # background
        dc.SetBrush(wx.Brush(wx.Colour(*key_color)))
        dc.SetPen(wx.Pen(wx.Colour(*key_color_ol), 1))
        dc.DrawRectangle(0, 0, w, h)

        span = max(1, self.high - self.low)

        # range box
        x_low  = int(self.low  * key_w)
        x_high = int(self.high * key_w)
        dc.SetBrush(wx.Brush(wx.Colour(*range_box_color)))
        dc.SetPen(wx.Pen(wx.Colour(*range_box_color), 0))
        dc.DrawRectangle(x_low, 0, x_high - x_low, h)

        # black-key overlay
        dc.SetBrush(wx.Brush(wx.Colour(bkey)))
        dc.SetPen(wx.Pen(wx.Colour(*key_color_ol), 1))
        for i in range(128):
            if (i % 12) in BLACK_KEYS:
                x = int(i * key_w)
                dc.DrawRectangle(x, 0, int(key_w)+1, int(h*0.6))

        # fade triangles
        self._draw_fade(dc, h, key_w, span, low=True)
        self._draw_fade(dc, h, key_w, span, low=False)

        
        # ─── draw vertical lines at low & high ───────────────────────
        x_low  = int(self.low  * key_w)
        x_high = int(self.high * key_w)
        line_col = wx.Colour(12,100,12) 
        dc.SetPen(wx.Pen(line_col, 4))
        
        # draw the two vertical lines
        dc.DrawLine(x_low,  0, x_low,  h)
        dc.DrawLine(x_high, 0, x_high, h)
        
                # orig line
        xo = int(self.orig * key_w)
        dc.SetPen(wx.Pen(wx.BLACK, 4))
        dc.DrawLine(xo, 0, xo, h)
        dc.SetPen(wx.Pen(COLOR_ORIGKEY_LINE, 2))
        dc.DrawLine(xo, 0, xo, h)
        
        # handles + labels
        for name in ('low','high','orig','lowfade','highfade'):
            self._draw_handle(dc, name, key_w, h, pad)

    def _draw_fade(self, dc, h, key_w, span, low):
        if low:
            lf = min(self.low_fade, span)
            x0 = int(self.low * key_w)
            x1 = int((self.low + lf) * key_w)
            pts = [(x0,h),(x0,0),(x1,h)]
            col = COLOR_LOWFADE_BOX_BASE
        else:
            hf = min(self.high_fade, span)
            x2 = int(self.high * key_w)
            x3 = int((self.high - hf) * key_w)
            pts = [(x2,0),(x2,h),(x3,0)]
            col = COLOR_HIGHFADE_BOX_BASE

        alpha = int(255 * ((lf if low else hf)/span))
        fade_col = wx.Colour(col.Red(),col.Green(),col.Blue(),alpha)
        dc.SetBrush(wx.Brush(fade_col))
        dc.SetPen(wx.Pen(col,1))
        dc.DrawPolygon(pts)

    def _draw_handle(self, dc, name, key_w, h, pad):
        pid, attr = self.HANDLE_MAP[name]
        # compute x,y
        if name=='lowfade':
            x = int((self.low + self.low_fade) * key_w); y = h-self.HANDLE_SIZE-2
        elif name=='highfade':
            x = int((self.high - self.high_fade) * key_w); y = 2
        else:
            val = getattr(self,attr)
            frac = {'low':0.30, 'orig':0.50, 'high':0.70}[name]
            x = int(val * key_w); y = int(frac*h)-self.HANDLE_SIZE//2

        # box
        col = {
            'lowfade':  COLOR_LOWFADE_HANDLE,
            'highfade': COLOR_HIGHFADE_HANDLE,
            'low':      COLOR_LOWKEY_HANDLE,
            'high':     COLOR_HIGHKEY_HANDLE,
            'orig':     COLOR_ORIGKEY_HANDLE
        }[name]
        dc.SetBrush(wx.Brush(col)); dc.SetPen(wx.Pen(wx.BLACK,1))
        dc.DrawRectangle(x-self.HANDLE_SIZE//2,y,self.HANDLE_SIZE,self.HANDLE_SIZE)

        # label
        label = ( str(getattr(self,attr))
                 if name.endswith('fade')
                 else midi_to_note(getattr(self,attr)) )
        tw,th = dc.GetTextExtent(label)
        rx, ry = x+self.HANDLE_SIZE//2+pad, y-pad
        dc.SetBrush(wx.Brush(wx.BLACK)); dc.SetPen(wx.Pen(wx.BLACK,0))
        dc.DrawRectangle(rx,ry,tw+pad*2,th+pad*2)
        dc.SetTextForeground(COLOR_TEXT)
        dc.DrawText(label, rx+pad, ry+pad)

    # ── USER INTERACTION ─────────────────────────────────────────────
    def OnMouseDown(self, evt):
        w, h = self.canvas.GetClientSize()
        key_w = w / 128.0
        x, y = evt.GetPosition()
        span = max(1, self.high - self.low)

        checks = [
            ('highfade', self.high - min(self.high_fade, span), self.HANDLE_SIZE//2+2),
            ('lowfade',  self.low  + min(self.low_fade,  span), h - self.HANDLE_SIZE//2 - 2),
            ('high',     self.high, int(0.70 * h)),
            ('low',      self.low,  int(0.30 * h)),
            ('orig',      self.orig,  int(0.50 * h)),
        ]

        half = self.HANDLE_SIZE / 2
        for name, key_val, y_center in checks:
            xpos = key_val * key_w
            if abs(x - xpos) <= half and abs(y - y_center) <= half:
                self.selected = name
                self._on_param_click(evt)
                return

        self.selected = None


    def OnMouseDrag(self, evt):
        if not (self.selected and evt.Dragging()): return
        w,h = self.canvas.GetClientSize()
        key_w = w/128.0
        x = evt.GetX()
        key = max(0, min(127, int(x/key_w)))
        span = max(1, self.high-self.low)

        sel = self.selected
        if sel=='lowfade':
            self.low_fade = max(0, min(span, key-self.low))
        elif sel=='highfade':
            self.high_fade= max(0, min(span, self.high-key))
        elif sel=='low':
            self.low = key
            if self.low>self.orig: self.orig=self.low
        elif sel=='high':
            self.high=key
            if self.high<self.orig:self.orig=self.high
        elif sel=='orig':
            self.orig=key
            if self.orig<self.low: self.low=self.orig
            if self.orig>self.high:self.high=self.orig

        # clamp
        span = max(1, self.high-self.low)
        self.low_fade  = min(self.low_fade,  span)
        self.high_fade = min(self.high_fade, span)

        # update numeric control too
        self._num_controls[self.selected].set_value(
            getattr(self, self.HANDLE_MAP[self.selected][1])
        )

        self.canvas.Refresh()
        pid, attr = self.HANDLE_MAP[self.selected]
        val = getattr(self, attr)
        self.main.send_parameter_edit(pid, val) #===========================================================================================


    def OnMouseUp(self, evt):
        self.selected = None
        for name, (pid, attr) in self.HANDLE_MAP.items():
            val = getattr(self, attr)
            self.main.send_parameter_edit(pid, val)
        

    def _on_param_click(self, evt):
        # select voice + zone
        self.main.send_parameter_edit(225, self.voice_index)
        self.main.send_parameter_edit(226, self.zone_index)
        evt.Skip()

    def _on_number_change(self, evt):
        pid = evt.GetId()
        val = evt.GetInt()
        # find which handle this is
        for name,(hpid,attr) in self.HANDLE_MAP.items():
            if hpid==pid:
                setattr(self, attr, val)
                # if it's low/high/orig, maintain ordering
                if name=='low' and self.low>self.orig: self.orig=self.low
                if name=='high'and self.high<self.orig:self.orig=self.high
                # clamp fades
                span = max(1, self.high-self.low)
                self.low_fade  = min(self.low_fade,  span)
                self.high_fade = min(self.high_fade, span)
                break

        # send your sysex param edit
        self.main.send_parameter_edit(pid, val)
        # repaint
        self.canvas.Refresh()

























class MultisampleKeyWindowStrip(wx.Panel):
    HANDLE_SIZE = 10

    # handle → (MIDI PID, attribute name)
    HANDLE_MAP = {
        'lowfade':  (46, 'low_fade'),
        'highfade': (48, 'high_fade'),
        'low':      (45, 'low'),
        'high':     (47, 'high'),
        # 'orig' removed
    }

    def __init__(self, parent,
                 orig, low, high, low_fade, high_fade,
                 voice_index, zone_index, group_num, main):
        super().__init__(parent)
        self.main        = main
        self.voice_index = voice_index
        self.zone_index  = zone_index
        self.group_num   = group_num

        # model
        # self.orig still set but never used
        self.orig      = orig
        self.low       = low
        self.high      = high
        self.low_fade  = low_fade
        self.high_fade = high_fade
        self.selected  = None

        # ── LAYOUT ────────────────────────────────────────────────────
        vs = wx.BoxSizer(wx.VERTICAL)

        # 1) drawing panel
        self.canvas = wx.Panel(self, style=wx.TRANSPARENT_WINDOW, size=(-1, 60))
        self.canvas.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.canvas.Bind(wx.EVT_PAINT,     self.OnPaint)
        self.canvas.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        self.canvas.Bind(wx.EVT_MOTION,    self.OnMouseDrag)
        self.canvas.Bind(wx.EVT_LEFT_UP,   self.OnMouseUp)
        vs.Add(self.canvas, 0, wx.EXPAND)

        # 2) numeric row
        hs = wx.BoxSizer(wx.HORIZONTAL)
        self._num_controls = {}
        for name, (pid, attr) in self.HANDLE_MAP.items():
            val = getattr(self, attr)
            dn = DraggableNumber(
                self, id=pid, value=val, min_val=0, max_val=127,
                callback=self._on_number_change
            )
            dn.SetMinSize((60, 30))
            dn.SetToolTip(f"{name}")
            hs.Add(dn, 0, wx.ALL, 2)
            self._num_controls[name] = dn
        vs.Add(hs, 0, wx.EXPAND)

        self.SetSizer(vs)

    # ── PAINTING ────────────────────────────────────────────────────
    def OnPaint(self, evt):
        dc = wx.AutoBufferedPaintDC(self.canvas)
        w, h = self.canvas.GetClientSize()
        key_w = w / 128.0
        pad   = 2

        # background
        dc.SetBrush(wx.Brush(wx.Colour(*key_color)))
        dc.SetPen(wx.Pen(wx.Colour(*key_color_ol), 1))
        dc.DrawRectangle(0, 0, w, h)

        span = max(1, self.high - self.low)

        # range box
        x_low  = int(self.low  * key_w)
        x_high = int(self.high * key_w)
        dc.SetBrush(wx.Brush(wx.Colour(*range_box_color)))
        dc.SetPen(wx.Pen(wx.Colour(*range_box_color), 0))
        dc.DrawRectangle(x_low, 0, x_high - x_low, h)

        # black-key overlay
        dc.SetBrush(wx.Brush(wx.Colour(153, 245, 198)))
        dc.SetPen(wx.Pen(wx.Colour(*key_color_ol), 1))
        for i in range(128):
            if (i % 12) in BLACK_KEYS:
                x = int(i * key_w)
                dc.DrawRectangle(x, 0, int(key_w)+1, int(h*0.6))

        # fade triangles
        self._draw_fade(dc, h, key_w, span, low=True)
        self._draw_fade(dc, h, key_w, span, low=False)

        # handles + labels (no 'orig')
        for name in ('low','high','lowfade','highfade'):
            self._draw_handle(dc, name, key_w, h, pad)

    def _draw_fade(self, dc, h, key_w, span, low):
        if low:
            lf = min(self.low_fade, span)
            x0 = int(self.low * key_w)
            x1 = int((self.low + lf) * key_w)
            pts = [(x0,h),(x0,0),(x1,h)]
            col = COLOR_LOWFADE_BOX_BASE
        else:
            hf = min(self.high_fade, span)
            x2 = int(self.high * key_w)
            x3 = int((self.high - hf) * key_w)
            pts = [(x2,0),(x2,h),(x3,0)]
            col = COLOR_HIGHFADE_BOX_BASE

        alpha = int(255 * ((lf if low else hf)/span))
        fade_col = wx.Colour(col.Red(),col.Green(),col.Blue(),alpha)
        dc.SetBrush(wx.Brush(fade_col))
        dc.SetPen(wx.Pen(col,1))
        dc.DrawPolygon(pts)

    def _draw_handle(self, dc, name, key_w, h, pad):
        pid, attr = self.HANDLE_MAP[name]
        if name=='lowfade':
            x = int((self.low + self.low_fade) * key_w); y = h-self.HANDLE_SIZE-2
        elif name=='highfade':
            x = int((self.high - self.high_fade) * key_w); y = 2
        else:
            val = getattr(self,attr)
            frac = {'low':0.30, 'high':0.70}[name]
            x = int(val * key_w); y = int(frac*h)-self.HANDLE_SIZE//2

        col = {
            'lowfade':  COLOR_LOWFADE_HANDLE,
            'highfade': COLOR_HIGHFADE_HANDLE,
            'low':      COLOR_LOWKEY_HANDLE,
            'high':     COLOR_HIGHKEY_HANDLE,
        }[name]
        dc.SetBrush(wx.Brush(col)); dc.SetPen(wx.Pen(wx.BLACK,1))
        dc.DrawRectangle(x-self.HANDLE_SIZE//2,y,self.HANDLE_SIZE,self.HANDLE_SIZE)

        label = str(getattr(self,attr)) if name.endswith('fade') else midi_to_note(getattr(self,attr))
        tw,th = dc.GetTextExtent(label)
        rx, ry = x+self.HANDLE_SIZE//2+pad, y-pad
        dc.SetBrush(wx.Brush(wx.BLACK)); dc.SetPen(wx.Pen(wx.BLACK,0))
        dc.DrawRectangle(rx,ry,tw+pad*2,th+pad*2)
        dc.SetTextForeground(COLOR_TEXT)
        dc.DrawText(label, rx+pad, ry+pad)

    # ── USER INTERACTION ─────────────────────────────────────────────
    def OnMouseDown(self, evt):
        w, h = self.canvas.GetClientSize()
        key_w = w / 128.0
        x, y = evt.GetPosition()
        span = max(1, self.high - self.low)

        checks = [
            ('highfade', self.high - min(self.high_fade, span), self.HANDLE_SIZE//2+2),
            ('lowfade',  self.low  + min(self.low_fade,  span), h - self.HANDLE_SIZE//2 - 2),
            ('high',     self.high, int(0.70 * h)),
            ('low',      self.low,  int(0.30 * h)),
        ]

        half = self.HANDLE_SIZE / 2
        for name, key_val, y_center in checks:
            xpos = key_val * key_w
            if abs(x - xpos) <= half and abs(y - y_center) <= half:
                self.selected = name
                self._on_param_click(evt)
                return

        self.selected = None

    def OnMouseDrag(self, evt):
        if not (self.selected and evt.Dragging()): return
        w,h = self.canvas.GetClientSize()
        key_w = w/128.0
        x = evt.GetX()
        key = max(0, min(127, int(x/key_w)))
        span = max(1, self.high-self.low)

        sel = self.selected
        if sel=='lowfade':
            self.low_fade = max(0, min(span, key-self.low))
        elif sel=='highfade':
            self.high_fade= max(0, min(span, self.high-key))
        elif sel=='low':
            self.low = key
            if self.low>self.high: self.high=self.low
        elif sel=='high':
            self.high=key
            if self.high<self.low: self.low=self.high

        span = max(1, self.high-self.low)
        self.low_fade  = min(self.low_fade,  span)
        self.high_fade = min(self.high_fade, span)

        self._num_controls[self.selected].set_value(
            getattr(self, self.HANDLE_MAP[self.selected][1])
        )
        self.canvas.Refresh()
        # lookup the PID and the attribute name
        pid, attr = self.HANDLE_MAP[self.selected]
        # pull the current model value (so for 'highfade' this is self.high_fade)
        val = getattr(self, attr)
        # print(pid, attr, val)
        self.main.send_parameter_edit(pid, val)

    def OnMouseUp(self, evt):
        self.selected = None
        for name, (pid, attr) in self.HANDLE_MAP.items():
            val = getattr(self, attr)
            self.main.send_parameter_edit(pid, val)

    def _on_param_click(self, evt):
        # print("self.voice_index, self.zone_index", self.voice_index, self.zone_index)
        self.main.send_parameter_edit(225, self.voice_index)
        # self.main.send_parameter_edit(226, -1)
        evt.Skip()

    def _on_number_change(self, evt):
        pid = evt.GetId()
        val = evt.GetInt()
        for name,(hpid,attr) in self.HANDLE_MAP.items():
            if hpid==pid:
                setattr(self, attr, val)
                break

        self.main.send_parameter_edit(pid, val)
        self.canvas.Refresh()


























class LinkKeyWindowStrip(wx.Panel):
    HANDLE_SIZE = 10

    # handle → (MIDI PID, attribute name)
    HANDLE_MAP = {
        'lowfade':  (29, 'low_fade'),
        'highfade': (31, 'high_fade'),
        'low':      (28, 'low'),
        'high':     (30, 'high')
    }

    def __init__(self, parent, link_index, main, controls,):
        super().__init__(parent)
        self.main        = main
    


        self.orig      = 0
        self.low       = 0
        self.high      = 127
        self.low_fade  = 0
        self.high_fade = 0
        self.selected  = None
        
        self.link_index = link_index
        
        controls["E4_LINK_KEY_LOW"] = self.low
        controls["E4_LINK_KEY_LOWFADE"] = self.low_fade
        controls["E4_LINK_KEY_HIGH"] = self.high
        controls["E4_LINK_KEY_HIGHFADE"] = self.high_fade
        

        # ── LAYOUT ────────────────────────────────────────────────────
        vs = wx.BoxSizer(wx.VERTICAL)

        # 1) drawing panel
        self.canvas = wx.Panel(self, style=wx.TRANSPARENT_WINDOW, size=(-1, 60))
        self.canvas.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.canvas.Bind(wx.EVT_PAINT,     self.OnPaint)
        self.canvas.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        self.canvas.Bind(wx.EVT_MOTION,    self.OnMouseDrag)
        self.canvas.Bind(wx.EVT_LEFT_UP,   self.OnMouseUp)
        vs.Add(self.canvas, 0, wx.EXPAND)

        # 2) numeric row
        hs = wx.BoxSizer(wx.HORIZONTAL)
        self._num_controls = {}
        for name, (pid, attr) in self.HANDLE_MAP.items():
            val = getattr(self, attr)
            dn = DraggableNumber(
                self, id=pid, value=val, min_val=0, max_val=127,
                callback=self._on_number_change
            )
            dn.SetMinSize((60, 30))
            dn.SetToolTip(f"{name}")
            hs.Add(dn, 0, wx.ALL, 2)
            self._num_controls[name] = dn
        vs.Add(hs, 0, wx.EXPAND)

        self.SetSizer(vs)

    # ── PAINTING ────────────────────────────────────────────────────
    def OnPaint(self, evt):
        dc = wx.AutoBufferedPaintDC(self.canvas)
        w, h = self.canvas.GetClientSize()
        key_w = w / 128.0
        pad   = 2

        # background
        dc.SetBrush(wx.Brush(wx.Colour(*key_color)))
        dc.SetPen(wx.Pen(wx.Colour(*key_color_ol), 1))
        dc.DrawRectangle(0, 0, w, h)

        span = max(1, self.high - self.low)

        # range box
        x_low  = int(self.low  * key_w)
        x_high = int(self.high * key_w)
        dc.SetBrush(wx.Brush(wx.Colour(*range_box_color)))
        dc.SetPen(wx.Pen(wx.Colour(*range_box_color), 0))
        dc.DrawRectangle(x_low, 0, x_high - x_low, h)

        # black-key overlay
        dc.SetBrush(wx.Brush(wx.Colour(153, 245, 198)))
        dc.SetPen(wx.Pen(wx.Colour(*key_color_ol), 1))
        for i in range(128):
            if (i % 12) in BLACK_KEYS:
                x = int(i * key_w)
                dc.DrawRectangle(x, 0, int(key_w)+1, int(h*0.6))

        # fade triangles
        self._draw_fade(dc, h, key_w, span, low=True)
        self._draw_fade(dc, h, key_w, span, low=False)

        # handles + labels (no 'orig')
        for name in ('low','high','lowfade','highfade'):
            self._draw_handle(dc, name, key_w, h, pad)

    def _draw_fade(self, dc, h, key_w, span, low):
        if low:
            lf = min(self.low_fade, span)
            x0 = int(self.low * key_w)
            x1 = int((self.low + lf) * key_w)
            pts = [(x0,h),(x0,0),(x1,h)]
            col = COLOR_LOWFADE_BOX_BASE
        else:
            hf = min(self.high_fade, span)
            x2 = int(self.high * key_w)
            x3 = int((self.high - hf) * key_w)
            pts = [(x2,0),(x2,h),(x3,0)]
            col = COLOR_HIGHFADE_BOX_BASE

        alpha = int(255 * ((lf if low else hf)/span))
        fade_col = wx.Colour(col.Red(),col.Green(),col.Blue(),alpha)
        dc.SetBrush(wx.Brush(fade_col))
        dc.SetPen(wx.Pen(col,1))
        dc.DrawPolygon(pts)

    def _draw_handle(self, dc, name, key_w, h, pad):
        pid, attr = self.HANDLE_MAP[name]
        if name=='lowfade':
            x = int((self.low + self.low_fade) * key_w); y = h-self.HANDLE_SIZE-2
        elif name=='highfade':
            x = int((self.high - self.high_fade) * key_w); y = 2
        else:
            val = getattr(self,attr)
            frac = {'low':0.30, 'high':0.70}[name]
            x = int(val * key_w); y = int(frac*h)-self.HANDLE_SIZE//2

        col = {
            'lowfade':  COLOR_LOWFADE_HANDLE,
            'highfade': COLOR_HIGHFADE_HANDLE,
            'low':      COLOR_LOWKEY_HANDLE,
            'high':     COLOR_HIGHKEY_HANDLE,
        }[name]
        dc.SetBrush(wx.Brush(col)); dc.SetPen(wx.Pen(wx.BLACK,1))
        dc.DrawRectangle(x-self.HANDLE_SIZE//2,y,self.HANDLE_SIZE,self.HANDLE_SIZE)

        label = str(getattr(self,attr)) if name.endswith('fade') else midi_to_note(getattr(self,attr))
        tw,th = dc.GetTextExtent(label)
        rx, ry = x+self.HANDLE_SIZE//2+pad, y-pad
        dc.SetBrush(wx.Brush(wx.BLACK)); dc.SetPen(wx.Pen(wx.BLACK,0))
        dc.DrawRectangle(rx,ry,tw+pad*2,th+pad*2)
        dc.SetTextForeground(COLOR_TEXT)
        dc.DrawText(label, rx+pad, ry+pad)

    # ── USER INTERACTION ─────────────────────────────────────────────
    def OnMouseDown(self, evt):
        w, h = self.canvas.GetClientSize()
        key_w = w / 128.0
        x, y = evt.GetPosition()
        span = max(1, self.high - self.low)

        checks = [
            ('highfade', self.high - min(self.high_fade, span), self.HANDLE_SIZE//2+2),
            ('lowfade',  self.low  + min(self.low_fade,  span), h - self.HANDLE_SIZE//2 - 2),
            ('high',     self.high, int(0.70 * h)),
            ('low',      self.low,  int(0.30 * h)),
        ]

        half = self.HANDLE_SIZE / 2
        for name, key_val, y_center in checks:
            xpos = key_val * key_w
            if abs(x - xpos) <= half and abs(y - y_center) <= half:
                self.selected = name
                self._on_param_click(evt)
                return

        self.selected = None

    def OnMouseDrag(self, evt):
        if not (self.selected and evt.Dragging()): return
        w,h = self.canvas.GetClientSize()
        key_w = w/128.0
        x = evt.GetX()
        key = max(0, min(127, int(x/key_w)))
        span = max(1, self.high-self.low)

        sel = self.selected
        if sel=='lowfade':
            self.low_fade = max(0, min(span, key-self.low))
        elif sel=='highfade':
            self.high_fade= max(0, min(span, self.high-key))
        elif sel=='low':
            self.low = key
            if self.low>self.high: self.high=self.low
        elif sel=='high':
            self.high=key
            if self.high<self.low: self.low=self.high

        span = max(1, self.high-self.low)
        self.low_fade  = min(self.low_fade,  span)
        self.high_fade = min(self.high_fade, span)

        self._num_controls[self.selected].set_value(
            getattr(self, self.HANDLE_MAP[self.selected][1])
        )
        self.canvas.Refresh()
        # lookup the PID and the attribute name
        pid, attr = self.HANDLE_MAP[self.selected]
        # pull the current model value (so for 'highfade' this is self.high_fade)
        val = getattr(self, attr)
        # print(pid, attr, val)
        self.main.send_parameter_edit(pid, val)

    def OnMouseUp(self, evt):
        self.selected = None
        for name, (pid, attr) in self.HANDLE_MAP.items():
            val = getattr(self, attr)
            self.main.send_parameter_edit(pid, val)
            
    def _on_param_click(self, evt):
        # select link
        self.main.send_parameter_edit(224, self.link_index)

        evt.Skip()


    def _on_number_change(self, evt):
        pid = evt.GetId()
        val = evt.GetInt()
        for name,(hpid,attr) in self.HANDLE_MAP.items():
            if hpid==pid:
                setattr(self, attr, val)
                break

        self.main.send_parameter_edit(pid, val)
        self.canvas.Refresh()