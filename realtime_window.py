import wx

yellow = (235, 243, 190, 0)
green1 = (147, 245, 161, 0)
greencontrol = (153, 245, 198, 0)
greenlight = (219, 245, 214, 0)
blue1 = (152, 245, 228, 0)
bluepowder = (152, 231, 245, 0)  
bluefresh = (86, 245, 216)  
bluesky = (167, 233, 245)
orange = (245, 175, 81, 0)
orangelight = (245, 220, 162, 0)


range_box_color = (250,150,255)
range_box_pen_color = (153, 245, 198)
# --- Color configuration (reuse or adjust as needed) ---
COLOR_VEL_HANDLE       =                    wx.Colour(245, 175, 81)
COLOR_VEL_FADE_BOX     =                    wx.Colour(152, 231, 245)
COLOR_VEL_FADE_HANDLE  =                    wx.Colour(160, 160,   0)
COLOR_TEXT             =                    wx.Colour( 50, 205,  50)
COLOR_FADE_BOX_BASE    =                    wx.Colour(153, 245, 198)
COLOR_FADE_HANDLE      =                    wx.Colour(167, 233, 245)
# custom grid‐line color for VelocityStrip
COLOR_VEL_GRID_LINE = wx.Colour(150, 150, 150)

class RealtimeTopStrip(wx.Panel):
    def __init__(self, parent, height=40):
        super().__init__(parent, style=wx.TRANSPARENT_WINDOW, size=(-1, height))
        self.SetMinSize((-1, height))
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        try: self.SetTransparent(200)
        except: pass
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, evt):
        dc = wx.AutoBufferedPaintDC(self)
        w, h = self.GetClientSize()
        unit = w / 128.0

        # background
        dc.SetBrush(wx.Brush(wx.Colour(250,235,225)))
        dc.SetPen(wx.Pen(wx.Colour(125,135,150), 3))
        dc.DrawRectangle(0, 0, w, h)

        # minor ticks every 8
        dc.SetPen(wx.Pen(COLOR_VEL_GRID_LINE, 1))
        for v in range(0, 128, 8):
            x = int(v * unit)
            length = h * 0.3
            dc.DrawLine(x, 0, x, int(length))

        # major ticks & labels at 16,32,48,64,80,96,112
        major = [16, 32, 48, 64, 80, 96, 112]
        dc.SetPen(wx.Pen(wx.BLACK, 2))
        dc.SetTextForeground(wx.BLACK)
        dc.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        for v in major:
            x = int(v * unit)
            length = h * 0.6
            dc.DrawLine(x, 0, x, int(length))
            label = str(v)
            tw, th = dc.GetTextExtent(label)
            dc.DrawText(label, x - tw//2, int(length) + 2)




class RealtimeWindowStrip(wx.Panel):
    HANDLE_SIZE = 10

    def __init__(self, parent, vel_low, vel_high, low_fade, high_fade, voice_index, zone_index, group_num, main):
        super().__init__(parent, style=wx.TRANSPARENT_WINDOW, size=(-1, 60))
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        try: self.SetTransparent(200)
        except: pass
        self.voice_index = voice_index
        self.zone_index  = zone_index
        self.group_num   = group_num
        self.main        = main
        # map each handle name to its MIDI PID:
        self._handle_map = {
            'low':     (53, 'low'),
            'high':    (55, 'high'),
            'lowfade': (54, 'low_fade'),
            'highfade':(56, 'high_fade'),
        }

        # parameters
        self.low, self.high       = vel_low, vel_high
        self.low_fade, self.high_fade = low_fade, high_fade
        self.selected             = None

        # bind events
        self.Bind(wx.EVT_PAINT,     self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        self.Bind(wx.EVT_MOTION,    self.OnMouseDrag)
        self.Bind(wx.EVT_LEFT_UP,   self.OnMouseUp)

    def OnPaint(self, _):
        dc = wx.AutoBufferedPaintDC(self)
        w, h = self.GetClientSize()
        key_w = w / 128.0
        pad   = 2

        

         # background
        dc.SetBrush(wx.Brush(wx.Colour(225,235,250)))
        dc.SetPen(wx.Pen(wx.Colour(125,135,150), 3))
        dc.DrawRectangle(0, 0, w, h)

        span = max(1, self.high - self.low)


        x_low  = int(self.low  * key_w)
        x_high = int(self.high * key_w)
        
        dc.SetBrush(wx.Brush(wx.Colour(range_box_color)))
        dc.SetPen(wx.Pen(wx.Colour(range_box_pen_color), 0))
        dc.DrawRectangle(x_low, 0, x_high - x_low, h)
            
            
        # 3) low‐fade triangle
        lf = min(self.low_fade, span)
        x0 = int(self.low * key_w)
        x1 = int((self.low + lf) * key_w)
        pts_low = [(x0, h), (x0, 0), (x1, h)]
        alpha = int(255 * (lf/span))
        col_low = wx.Colour(*COLOR_FADE_BOX_BASE.Get()[:3], alpha)
        dc.SetBrush(wx.Brush(col_low))
        dc.SetPen(wx.Pen(COLOR_FADE_BOX_BASE, 3))
        dc.DrawPolygon(pts_low)
        
        

        # 4) high‐fade triangle
        hf = min(self.high_fade, span)
        x2 = int(self.high * key_w)
        x3 = int((self.high - hf) * key_w)
        pts_high = [(x2, 0), (x2, h), (x3, 0)]
        alpha = int(255 * (hf/span))
        col_high = wx.Colour(*COLOR_FADE_BOX_BASE.Get()[:3], alpha)
        dc.SetBrush(wx.Brush(col_high))
        dc.SetPen(wx.Pen(COLOR_FADE_BOX_BASE, 1))
        dc.DrawPolygon(pts_high)
        
        # 1) background grid lines
        dc.SetPen(wx.Pen(COLOR_VEL_GRID_LINE, 1, style=wx.PENSTYLE_SHORT_DASH))
        for val in (16, 32, 48, 64, 80, 96, 112):
            x = int(val * key_w)
            dc.DrawLine(x, 0, x, h)

        dc.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT,
                           wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

        # 5) low/high handles + numeric labels at .25/.75 heights
        for name, y_frac in (('low',0.25), ('high',0.75)):
            val = getattr(self, name)
            x   = int(val * key_w)
            yc  = int(y_frac * h) - self.HANDLE_SIZE//2

            # handle
            dc.SetBrush(wx.Brush(COLOR_VEL_HANDLE))
            dc.SetPen(wx.Pen(wx.BLACK,1))
            dc.DrawRectangle(x-self.HANDLE_SIZE//2, yc,
                             self.HANDLE_SIZE, self.HANDLE_SIZE)

            # label
            txt = str(val)
            tw, th = dc.GetTextExtent(txt)
            rx = x + self.HANDLE_SIZE//2 + pad
            ry = yc - pad
            dc.SetBrush(wx.Brush(wx.BLACK))
            dc.SetPen(wx.Pen(wx.BLACK,0))
            dc.DrawRectangle(rx, ry, tw+2*pad, th+2*pad)
            dc.SetTextForeground(COLOR_TEXT)
            dc.DrawText(txt, rx+pad, ry+pad)

        # 6) low‐fade handle at bottom + label
        y_low_fh = h - self.HANDLE_SIZE - 2
        dc.SetBrush(wx.Brush(COLOR_FADE_HANDLE))
        dc.SetPen(wx.Pen(wx.BLACK,1))
        dc.DrawRectangle(x1-self.HANDLE_SIZE//2, y_low_fh,
                         self.HANDLE_SIZE, self.HANDLE_SIZE)
        lf_txt = str(self.low_fade)
        tw, th = dc.GetTextExtent(lf_txt)
        rx = x1 + self.HANDLE_SIZE//2 + pad
        ry = y_low_fh - pad
        dc.SetBrush(wx.Brush(wx.BLACK)); dc.SetPen(wx.Pen(wx.BLACK,0))
        dc.DrawRectangle(rx, ry, tw+2*pad, th+2*pad)
        dc.SetTextForeground(COLOR_TEXT)
        dc.DrawText(lf_txt, rx+pad, ry+pad)

        # 7) high‐fade handle at top + label
        y_high_fh = 2
        dc.SetBrush(wx.Brush(COLOR_FADE_HANDLE))
        dc.SetPen(wx.Pen(wx.BLACK,1))
        dc.DrawRectangle(x3-self.HANDLE_SIZE//2, y_high_fh,
                         self.HANDLE_SIZE, self.HANDLE_SIZE)
        hf_txt = str(self.high_fade)
        tw, th = dc.GetTextExtent(hf_txt)
        rx = x3 + self.HANDLE_SIZE//2 + pad
        ry = y_high_fh - pad
        dc.SetBrush(wx.Brush(wx.BLACK)); dc.SetPen(wx.Pen(wx.BLACK,0))
        dc.DrawRectangle(rx, ry, tw+2*pad, th+2*pad)
        dc.SetTextForeground(COLOR_TEXT)
        dc.DrawText(hf_txt, rx+pad, ry+pad)
        



    def OnMouseDown(self, evt):
        w, h = self.GetClientSize()
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
        w,h = self.GetClientSize(); key_w=w/128.0
        x   = evt.GetX()
        key = max(0, min(127, int(x/key_w)))
        span= max(1, self.high-self.low)

        sel = self.selected
        if sel=='lowfade':
            self.low_fade  = max(0, min(span, key-self.low))
        elif sel=='highfade':
            self.high_fade = max(0, min(span, self.high-key))
        elif sel=='low':
            self.low = key
            # clamp high >= low
            if self.low > self.high:
                self.high = self.low
        elif sel=='high':
            self.high = key
            if self.high < self.low:
                self.low = self.high

        # **now enforce your rule: fades never exceed new span**
        span = max(1, self.high - self.low)
        self.low_fade  = min(self.low_fade,  span)
        self.high_fade = min(self.high_fade, span)

        self.Refresh()
        pid, attr = self._handle_map[self.selected]
        val = getattr(self, attr)
        self.main.send_parameter_edit(pid, val) #===========================================================================================
 

    def OnMouseUp(self, evt):
        self.selected = None
        for name, (pid, attr) in self.HANDLE_MAP.items():
            val = getattr(self, attr)
            self.main.send_parameter_edit(pid, val)

    def update_params(self, vel_low=None, vel_high=None,
                      low_fade=None, high_fade=None):
        if vel_low   is not None: self.low       = vel_low
        if vel_high  is not None: self.high      = vel_high
        if low_fade  is not None: self.low_fade  = low_fade
        if high_fade is not None: self.high_fade = high_fade
        # clamp in case external values > span
        span = max(1, self.high - self.low)
        self.low_fade  = min(self.low_fade,  span)
        self.high_fade = min(self.high_fade, span)
        self.Refresh()
        
    def _on_param_click(self, evt):
        """First click: select preset/voice/zone once."""
        # preset = self.main.parsed_preset['E4_PRESET_NUMBER']
        # self.main.send_parameter_edit(223, preset)            # PRESET_SELECT
        self.main.send_parameter_edit(225, self.voice_index)  # VOICE_SELECT
        # self.main.send_parameter_edit(227, self.group_num)    # GROUP_SELECT
        # self.main.send_parameter_edit(226, self.zone_index)   # SAMPLE_ZONE_SELECT
        # allow the drag to continue
        evt.Skip()