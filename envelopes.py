import wx
from wx.lib.scrolledpanel import ScrolledPanel

from custom_widgets import EVT_DRAGGABLENUMBER

yellow = (235, 243, 190, 0)
green1 = (147, 245, 161, 0)
greencontrol = (153, 245, 198, 120)
greenlight = (219, 245, 214, 0)
blue1 = (152, 245, 228, 0)
bluepowder = (152, 231, 245, 120)  
bluefresh = (86, 245, 216)  
bluesky = (167, 233, 245)
orange = (245, 175, 81, 120)
orangelight = (245, 220, 162, 0)


#====================================================================================================================================
#====================================================================================================================================
#====================================================================================================================================



class AmpEnvelopeDisplay(wx.Panel):
    def __init__(self, parent, min_width=600, min_height=150, on_change=None, main = None):
        # remove the fixed size; let sizers do the work
        super().__init__(parent)
        self.main = main
        self.on_change = on_change
        self.SetBackgroundColour("black")
        self.SetDoubleBuffered(True)
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        # enforce a minimum size if you like
        self.SetMinSize((min_width, min_height))

        self.mouse_down = False

        # margins
        self.left_margin   = 10
        self.right_margin  = 10
        self.top_margin    = 10
        self.bottom_margin = 10

        # default envelope parameters
        self.attack_1_rate, self.attack_1_level   = 50, 100
        self.attack_2_rate, self.attack_2_level   = 50, 100
        self.decay_1_rate,  self.decay_1_level    = 50, 50
        self.decay_2_rate,  self.decay_2_level    = 50, 50
        self.release_1_rate,self.release_1_level  = 50, 0
        self.release_2_rate,self.release_2_level  = 50, 0
        self._raw_depth = 16       # for example
        self.depth     = (100/16)*self._raw_depth

        # internals for dragging
        self._pts    = []
        self._drag_i = None
        self.point_r = 4

        # events
        self.Bind(wx.EVT_PAINT,      self._on_paint)
        self.Bind(wx.EVT_LEFT_DOWN,  self._on_left_down)
        self.Bind(wx.EVT_LEFT_UP,    self._on_left_up)
        self.Bind(wx.EVT_MOTION,     self._on_mouse_move)
        self.Bind(wx.EVT_SIZE,       lambda e: (self.Refresh(), e.Skip()))


    def update_parameters(self,
            a1r, a1l, a2r, a2l,
            d1r, d1l, d2r, d2l,
            r1r, r1l, r2r, r2l,
            depth):
        # store & redraw
        (self.attack_1_rate,  self.attack_1_level,
         self.attack_2_rate,  self.attack_2_level,
         self.decay_1_rate,   self.decay_1_level,
         self.decay_2_rate,   self.decay_2_level,
         self.release_1_rate, self.release_1_level,
         self.release_2_rate, self.release_2_level) = (
            a1r, a1l, a2r, a2l,
            d1r, d1l, d2r, d2l,
            r1r, r1l, r2r, r2l
        )
        self.depth = (100 / 16) * depth
        self.Refresh()

        # push back to controls
        if self.on_change:
            rates  = [0,
                self.attack_1_rate,
                self.attack_2_rate,
                self.decay_1_rate,
                self.decay_2_rate,
                self.release_1_rate,
                self.release_2_rate
            ]
            levels = [0,
                self.attack_1_level,
                self.attack_2_level,
                self.decay_1_level,
                self.decay_2_level,
                self.release_1_level,
                self.release_2_level
            ]
            self.on_change(rates, levels)


    def _on_paint(self, evt):
        dc = wx.PaintDC(self)
        dc.Clear()

        w, h = self.GetClientSize()
        left    = self.left_margin
        avail_w = w - self.left_margin - self.right_margin

        # recompute y‐axis extremes each time
        y_full = self.top_margin
        y_zero = h - self.bottom_margin
        span   = y_zero - y_full

        # effective levels
        eff = lambda lvl: lvl * (self.depth/100.0)
        ea1, ea2 = eff(self.attack_1_level),  eff(self.attack_2_level)
        ed1, ed2 = eff(self.decay_1_level),   eff(self.decay_2_level)
        er1, er2 = eff(self.release_1_level), eff(self.release_2_level)

        # segment rates
        rates = [
            self.attack_1_rate, self.attack_2_rate,
            self.decay_1_rate,  self.decay_2_rate,
            self.release_1_rate,self.release_2_rate
        ]
        total_t = sum(rates) or 1

        # build x positions
        xs = [left]
        for r in rates:
            xs.append(xs[-1] + (r/total_t) * avail_w)

        # build y positions
        ys = [
            y_zero,
            y_zero - ea1/100.0 * span,
            y_zero - ea2/100.0 * span,
            y_zero - ed1/100.0 * span,
            y_zero - ed2/100.0 * span,
            y_zero - er1/100.0 * span,
            y_zero - er2/100.0 * span
        ]

        # cache for dragging
        self._pts = list(zip(xs, ys))

        # draw fill
        gc = wx.GraphicsContext.Create(dc)
        brush = gc.CreateLinearGradientBrush(
            left, y_full,
            left, y_full + span,
            wx.Colour(50,150,255,120),
            wx.Colour(50,150,255,10)
        )
        path = gc.CreatePath()
        path.MoveToPoint(xs[0], ys[0])
        for x,y in zip(xs[1:], ys[1:]):
            path.AddLineToPoint(x,y)
        path.AddLineToPoint(xs[-1], y_zero)
        path.AddLineToPoint(xs[0],  y_zero)
        path.CloseSubpath()
        gc.SetBrush(brush)
        gc.FillPath(path)

        # stroke
        pen = gc.CreatePen(wx.Pen(wx.Colour("green"),2))
        gc.SetPen(pen)
        stroke = gc.CreatePath()
        stroke.MoveToPoint(xs[0], ys[0])
        for x,y in zip(xs[1:], ys[1:]):
            stroke.AddLineToPoint(x,y)
        gc.StrokePath(stroke)
        
        # draw 2 vertical grid lines
        pen_vert = wx.Pen(wx.Colour(200,200,200), 1, wx.PENSTYLE_DOT)
        dc.SetPen(pen_vert)
        # y_full is your top_margin, y_zero is bottom line
        for idx in (2, 4):
            x = xs[idx]
            dc.DrawLine(int(x), int(y_full), int(x), int(y_zero))

        # handles
        for x,y in zip(xs, ys):
            gc.SetBrush(wx.Brush(wx.Colour("blue")))
            gc.DrawEllipse(x-self.point_r, y-self.point_r,
                           self.point_r*2, self.point_r*2)


    def _on_left_down(self, evt):
        self.mouse_down = True
        x,y = evt.GetPosition()
        for i,(px,py) in enumerate(self._pts):
            # skip the very first point (i==0), allow all others
            if i>0 and (x-px)**2 + (y-py)**2 < (self.point_r*1.5)**2:
                self._drag_i = i
                self.CaptureMouse()
                return

    def _on_left_up(self, evt):
        self.mouse_down = False
        if self._drag_i is not None:
            self._drag_i = None
            if self.HasCapture(): self.ReleaseMouse()

    def _on_mouse_move(self, evt):
        if self._drag_i is None or not(evt.LeftIsDown() and evt.Dragging()):
            return

        x,y = evt.GetPosition()
        w,h = self.GetClientSize()
        left    = self.left_margin
        avail_w = w - self.left_margin - self.right_margin
        y_full  = self.top_margin
        y_zero  = h - self.bottom_margin
        span    = y_zero - y_full

        i = self._drag_i
        rates = [
            self.attack_1_rate, self.attack_2_rate,
            self.decay_1_rate,  self.decay_2_rate,
            self.release_1_rate,self.release_2_rate
        ]
        total_t = sum(rates) or 1

        xs = [left]
        for r in rates:
            xs.append(xs[-1] + (r/total_t)*avail_w)

        # update rate
        seg_idx = i-1
        new_r = round((x - xs[i-1]) / avail_w * total_t)
        new_r = max(0, min(127, new_r))
        if seg_idx==0:   #======================================================================================================
            self.attack_1_rate   = new_r
            self.main.send_parameter_edit(70 , new_r)
        elif seg_idx==1: 
            self.attack_2_rate   = new_r
            self.main.send_parameter_edit(72 , new_r)
        elif seg_idx==2: 
            self.decay_1_rate    = new_r
            self.main.send_parameter_edit(74 , new_r)
        elif seg_idx==3: 
            self.decay_2_rate    = new_r
            self.main.send_parameter_edit(76 , new_r)
        elif seg_idx==4: 
            self.release_1_rate = new_r
            self.main.send_parameter_edit(78 , new_r)
        elif seg_idx==5: 
            self.release_2_rate = new_r
            self.main.send_parameter_edit(80 , new_r)
        

        # update level
        new_l = round((1 - (y-y_full)/span) * 100)
        new_l = max(0, min(100, new_l))
        if i==1:   
            self.attack_1_level   = new_l  # and send sysex from here
            self.main.send_parameter_edit(71 , new_l)
        elif i==2: 
            self.attack_2_level   = new_l
            self.main.send_parameter_edit(73 , new_l)
        elif i==3: 
            self.decay_1_level    = new_l
            self.main.send_parameter_edit(75 , new_l)
        elif i==4: 
            self.decay_2_level    = new_l
            self.main.send_parameter_edit(77 , new_l)
        elif i==5: 
            self.release_1_level = new_l
            self.main.send_parameter_edit(79 , new_l)
        elif i==6: 
            self.release_2_level = new_l
            self.main.send_parameter_edit(81 , new_l)


        # push back + redraw
        self.update_parameters(
            self.attack_1_rate,  self.attack_1_level,
            self.attack_2_rate,  self.attack_2_level,
            self.decay_1_rate,   self.decay_1_level,
            self.decay_2_rate,   self.decay_2_level,
            self.release_1_rate, self.release_1_level,
            self.release_2_rate, self.release_2_level,
            self._raw_depth
        )




#=====================================================================================================
#=====================================================================================================
#=====================================================================================================

amp_env_depths_conv= {
    "-96":0, "-93":1, "-90":2, "-87":3, "-84":4, "-81":5, "-78":6, "-75":7, "-72":8, "-69":9, 
    "-66":10, "-63":11, "-60":12, "-57":13, "-54":14, "-51":15, "-48":16}   

amp_env_depths = {
    0:  "-96",
    1:  "-93",
    2:  "-90",
    3:  "-87",
    4:  "-84",
    5:  "-81",
    6:  "-78",
    7:  "-75",
    8:  "-72",
    9:  "-69",
    10: "-66",
    11: "-63",
    12: "-60",
    13: "-57",
    14: "-54",
    15: "-51",
    16: "-48",
}
# --------------------------------------------------
# EnvelopeFrame: Main frame that houses the envelope display and controls.
# --------------------------------------------------
class AmpEnvelopePanel(wx.Panel):
    def __init__(self, parent, envelope_controls, voice_dict, main):
        super().__init__(parent)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        panel = self
        panel.SetSizer(main_sizer)
        self.voice_dict = voice_dict
        self.envelope_display = AmpEnvelopeDisplay(self, min_width=600, min_height=180, on_change=self.on_display_change, main = main)

        main_sizer.Add(self.envelope_display, -1, wx.ALL, 10)


        self.atkrate1 = envelope_controls[0]
        self.atkamt1 = envelope_controls[1]
        self.atkrate2 = envelope_controls[2]
        self.atkamt2 = envelope_controls[3]

        self.dcyrate1 = envelope_controls[4]
        self.dcyamt1 = envelope_controls[5]
        self.dcyrate2 = envelope_controls[6]
        self.dcyamt2 = envelope_controls[7]
                
        self.rlsrate1 = envelope_controls[8]
        self.rlsamt1 = envelope_controls[9]
        self.rlsrate2 = envelope_controls[10]
        self.rlsamt2 = envelope_controls[11]
        
        # self.env_depth = envelope_controls[12]
        # self.amp_env_depth_ctrl = amp_env_depth_ctrl
        
        self.atkrate1.Bind(EVT_DRAGGABLENUMBER, self.on_ctrl_change)
        self.atkamt1.Bind(EVT_DRAGGABLENUMBER, self.on_ctrl_change)
        self.atkrate2.Bind(EVT_DRAGGABLENUMBER, self.on_ctrl_change)
        self.atkamt2.Bind(EVT_DRAGGABLENUMBER, self.on_ctrl_change)
        self.dcyrate1.Bind(EVT_DRAGGABLENUMBER, self.on_ctrl_change)
        self.dcyamt1.Bind(EVT_DRAGGABLENUMBER, self.on_ctrl_change)
        self.dcyrate2.Bind(EVT_DRAGGABLENUMBER, self.on_ctrl_change)
        self.dcyamt2.Bind(EVT_DRAGGABLENUMBER, self.on_ctrl_change)
        self.rlsrate1.Bind(EVT_DRAGGABLENUMBER, self.on_ctrl_change)
        self.rlsamt1.Bind(EVT_DRAGGABLENUMBER, self.on_ctrl_change)
        self.rlsrate2.Bind(EVT_DRAGGABLENUMBER, self.on_ctrl_change)
        self.rlsamt2.Bind(EVT_DRAGGABLENUMBER, self.on_ctrl_change)
        # self.env_depth.Bind(EVT_DRAGGABLENUMBER, self.on_ctrl_change)
        # self.amp_env_depth_ctrl.Bind(wx.EVT_COMBOBOX, self.on_ctrl_change)
    # handler signature
        self.load_up()
        self.Center()
        self.Show()

    def on_ctrl_change(self, event):
        if self.envelope_display.mouse_down == True:
            return
        a_1_rate = self.atkrate1.value
        a_1_level = self.atkamt1.value
        a_2_rate = self.atkrate2.value
        a_2_level = self.atkamt2.value
        d_1_rate = self.dcyrate1.value
        d_1_level = self.dcyamt1.value
        d_2_rate = self.dcyrate2.value
        d_2_level = self.dcyamt2.value
        r_1_rate = self.rlsrate1.value
        r_1_level = self.rlsamt1.value
        r_2_rate = self.rlsrate2.value
        r_2_level = self.rlsamt2.value
        
        # ctrl = event.GetEventObject()
        # if ctrl == self.amp_env_depth_ctrl:
        #     self.env_depth.value = amp_env_depths_conv[ctrl.GetValue()]
        # elif ctrl == self.env_depth:
        #     self.amp_env_depth_ctrl.SetStringSelection(amp_env_depths[ctrl.value])
        depth = 16

        # Update the envelope display.
        self.envelope_display.update_parameters(a_1_rate, a_1_level, a_2_rate, a_2_level, d_1_rate, d_1_level, d_2_rate, d_2_level, r_1_rate, r_1_level, r_2_rate, r_2_level, depth)

    def on_display_change(self, rates = None, levels = None):
        if self.envelope_display.mouse_down == True:
            
            self.atkrate1.set_value(self.envelope_display.attack_1_rate)
            self.atkamt1.set_value(self.envelope_display.attack_1_level)

            self.atkrate2.set_value(self.envelope_display.attack_2_rate)
            self.atkamt2.set_value(self.envelope_display.attack_2_level)

            self.dcyrate1.set_value(self.envelope_display.decay_1_rate)
            self.dcyamt1.set_value(self.envelope_display.decay_1_level)

            self.dcyrate2.set_value(self.envelope_display.decay_2_rate)
            self.dcyamt2.set_value(self.envelope_display.decay_2_level)

            self.rlsrate1.set_value(self.envelope_display.release_1_rate)
            self.rlsamt1.set_value(self.envelope_display.release_1_level)

            self.rlsrate2.set_value(self.envelope_display.release_2_rate)
            self.rlsamt2.set_value(self.envelope_display.release_2_level)
            
            # self.env_depth.set_value(self.envelope_display.depth)
            
    
    def load_up(self):
        a_1_rate = self.atkrate1.value
        a_1_level = self.atkamt1.value
        a_2_rate = self.atkrate2.value
        a_2_level = self.atkamt2.value
        d_1_rate = self.dcyrate1.value
        d_1_level = self.dcyamt1.value
        d_2_rate = self.dcyrate2.value
        d_2_level = self.dcyamt2.value
        r_1_rate = self.rlsrate1.value
        r_1_level = self.rlsamt1.value
        r_2_rate = self.rlsrate2.value
        r_2_level = self.rlsamt2.value
        depth = 16

        # Update the envelope display.
        self.envelope_display.update_parameters(a_1_rate, a_1_level, a_2_rate, a_2_level, d_1_rate, d_1_level, d_2_rate, d_2_level, r_1_rate, r_1_level, r_2_rate, r_2_level, depth)

    























#=====================================================================================================
#=====================================================================================================
#==============================   FILTER  =======================================================================



class FilterEnvelopeDisplay(wx.Panel):
    def __init__(self, parent, min_width=600, min_height=150,
                 on_change=None, main=None):
        super().__init__(parent)
        self.main, self.on_change = main, on_change
        self.SetBackgroundColour("black")
        self.SetDoubleBuffered(True)
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.SetMinSize((min_width, min_height))

        self.mouse_down = False
        self.left_margin = 10; self.right_margin = 10
        self.top_margin  = 10; self.bottom_margin = 10

        # -------- default params (levels 0–200) --------
        self.attack_1_rate, self.attack_1_level = 50, 100
        self.attack_2_rate, self.attack_2_level = 50, 100
        self.decay_1_rate,  self.decay_1_level  = 50, 150
        self.decay_2_rate,  self.decay_2_level  = 50, 150
        self.release_1_rate,self.release_1_level= 50, 100
        self.release_2_rate,self.release_2_level= 50, 100
        self._raw_depth = 16
        self.depth      = (100/16)*self._raw_depth

        self._pts = []; self._drag_i = None; self.point_r = 4
        self.Bind(wx.EVT_PAINT, self._on_paint)
        self.Bind(wx.EVT_LEFT_DOWN, self._on_left_down)
        self.Bind(wx.EVT_LEFT_UP,   self._on_left_up)
        self.Bind(wx.EVT_MOTION,    self._on_mouse_move)
        self.Bind(wx.EVT_SIZE, lambda e: (self.Refresh(), e.Skip()))

    # -------------------------------------------------- helpers
    def _disp(self, lvl):            # 0-200  →  −100…+100
        return (lvl - 100) * (self.depth/100.0)

    def _inv_disp(self, disp):       # −100…+100 → 0-200
        return disp + 100

    def update_parameters(self,
            a1r, a1l, a2r, a2l,
            d1r, d1l, d2r, d2l,
            r1r, r1l, r2r, r2l,
            depth):
        (self.attack_1_rate,  self.attack_1_level,
         self.attack_2_rate,  self.attack_2_level,
         self.decay_1_rate,   self.decay_1_level,
         self.decay_2_rate,   self.decay_2_level,
         self.release_1_rate, self.release_1_level,
         self.release_2_rate, self.release_2_level) = (
            a1r, a1l, a2r, a2l,
            d1r, d1l, d2r, d2l,
            r1r, r1l, r2r, r2l
        )
        self.depth = (100/16)*depth
        self.Refresh()

        if self.on_change:
            rates  = [0, self.attack_1_rate, self.attack_2_rate,
                         self.decay_1_rate,  self.decay_2_rate,
                         self.release_1_rate,self.release_2_rate]
            levels = [0,
                self._disp(self.attack_1_level),
                self._disp(self.attack_2_level),
                self._disp(self.decay_1_level),
                self._disp(self.decay_2_level),
                self._disp(self.release_1_level),
                self._disp(self.release_2_level)]
            self.on_change(rates, levels)

    # -------------------------------------------------- paint
    def _on_paint(self, _):
        dc = wx.PaintDC(self); dc.Clear()
        w,h = self.GetClientSize()
        left = self.left_margin
        avail_w = w - self.left_margin - self.right_margin
        y_top = self.top_margin
        y_bot = h - self.bottom_margin
        span  = y_bot - y_top
        y_mid = (y_top + y_bot) / 2

        # centre-line
        dc.SetPen(wx.Pen(wx.Colour(200,200,200),1,wx.PENSTYLE_DOT))
        dc.DrawLine(left, int(y_mid), left+avail_w, int(y_mid))

        # effective display levels
        ea1, ea2 = self._disp(self.attack_1_level),  self._disp(self.attack_2_level)
        ed1, ed2 = self._disp(self.decay_1_level),   self._disp(self.decay_2_level)
        er1, er2 = self._disp(self.release_1_level), self._disp(self.release_2_level)

        rates = [self.attack_1_rate, self.attack_2_rate,
                 self.decay_1_rate,  self.decay_2_rate,
                 self.release_1_rate,self.release_2_rate]
        total = sum(rates) or 1
        xs = [left]
        for r in rates: xs.append(xs[-1] + (r/total)*avail_w)

        
        def level_to_y(level):
            # level is -100...+100, map to y_bot (bottom) ... y_top (top)
            norm = (level + 200) / 200.0
            return y_bot - norm * (y_bot - y_top)

        ys = [
            level_to_y(-100),           # start at centre
            level_to_y(ea1),
            level_to_y(ea2),
            level_to_y(ed1),
            level_to_y(ed2),
            level_to_y(er1),
            level_to_y(er2)            # last point centre
        ]

        self._pts = list(zip(xs, ys))

        gc = wx.GraphicsContext.Create(dc)
        path = gc.CreatePath(); path.MoveToPoint(xs[0],ys[0])
        for x,y in zip(xs[1:],ys[1:]): path.AddLineToPoint(x,y)
        path.AddLineToPoint(xs[-1], y_bot); path.AddLineToPoint(xs[0], y_bot)
        path.CloseSubpath()
        brush = gc.CreateLinearGradientBrush(left,y_top,left,y_bot,
                    wx.Colour(50,255,150,120), wx.Colour(50,150,255,10))
        
        gc.SetBrush(brush); gc.FillPath(path)
        gc.SetPen(gc.CreatePen(wx.Pen(wx.Colour("green"),2)))
        stroke = gc.CreatePath(); stroke.MoveToPoint(xs[0],ys[0])
        for x,y in zip(xs[1:],ys[1:]): stroke.AddLineToPoint(x,y)
        gc.StrokePath(stroke)
        
        # draw 2 vertical grid lines
        pen_vert = wx.Pen(wx.Colour(200,200,200), 1, wx.PENSTYLE_DOT)
        dc.SetPen(pen_vert)
        # y_full is your top_margin, y_zero is bottom line
        for idx in (2, 4):
            x = xs[idx]
            dc.DrawLine(int(x), int(y_top), int(x), int(y_bot))

        for x,y in zip(xs,ys):
            gc.SetBrush(wx.Brush(wx.Colour("blue")))
            gc.DrawEllipse(x-self.point_r,y-self.point_r,
                           self.point_r*2,self.point_r*2)

    # -------------------------------------------------- dragging
    def _on_left_down(self, evt):
        self.mouse_down = True
        x,y = evt.GetPosition()
        for i,(px,py) in enumerate(self._pts):
            if i>0 and (x-px)**2+(y-py)**2 < (self.point_r*1.5)**2:
                self._drag_i = i; self.CaptureMouse(); return

    def _on_left_up(self, _):
        self.mouse_down = False; self._drag_i = None
        if self.HasCapture(): self.ReleaseMouse()

    def _on_mouse_move(self, evt):
        if self._drag_i is None or not(evt.LeftIsDown() and evt.Dragging()):
            return
        x, y = evt.GetPosition()
        w, h = self.GetClientSize()
        left = self.left_margin
        avail_w = w - self.left_margin - self.right_margin
        y_top = self.top_margin
        y_bot = h - self.bottom_margin

        rates = [self.attack_1_rate, self.attack_2_rate,
                self.decay_1_rate,  self.decay_2_rate,
                self.release_1_rate,self.release_2_rate]
        total = sum(rates) or 1
        xs = [left]
        for r in rates:
            xs.append(xs[-1] + (r / total) * avail_w)

        seg_idx = self._drag_i - 1
        new_r = max(0, min(127, round((x - xs[self._drag_i - 1]) / avail_w * total)))
        if   seg_idx == 0: self.attack_1_rate = new_r; self.main.send_parameter_edit(93, new_r)
        elif seg_idx == 1: self.attack_2_rate = new_r; self.main.send_parameter_edit(95, new_r)
        elif seg_idx == 2: self.decay_1_rate  = new_r; self.main.send_parameter_edit(97, new_r)
        elif seg_idx == 3: self.decay_2_rate  = new_r; self.main.send_parameter_edit(99, new_r)
        elif seg_idx == 4: self.release_1_rate= new_r; self.main.send_parameter_edit(101, new_r)
        elif seg_idx == 5: self.release_2_rate= new_r; self.main.send_parameter_edit(103, new_r)

        # --- FIXED: Convert mouse y to logical level ---
        norm = (y_bot - y) / (y_bot - y_top)
        int_l = int(round(max(-100, min(100, norm * 200.0 - 100))))
        i = self._drag_i
        if   i == 1: self.attack_1_level  = int_l; self.main.send_parameter_edit(94, int(round(int_l)))
        elif i == 2: self.attack_2_level  = int_l; self.main.send_parameter_edit(96, int(round(int_l)))
        elif i == 3: self.decay_1_level   = int_l; self.main.send_parameter_edit(98, int(round(int_l)))
        elif i == 4: self.decay_2_level   = int_l; self.main.send_parameter_edit(100, int(round(int_l)))
        elif i == 5: self.release_1_level = int_l; self.main.send_parameter_edit(102, int(round(int_l)))
        elif i == 6: self.release_2_level = int_l; self.main.send_parameter_edit(104, int(round(int_l)))

        self.update_parameters(
            self.attack_1_rate, self.attack_1_level,
            self.attack_2_rate, self.attack_2_level,
            self.decay_1_rate,  self.decay_1_level,
            self.decay_2_rate,  self.decay_2_level,
            self.release_1_rate,self.release_1_level,
            self.release_2_rate,self.release_2_level,
            self._raw_depth)


#=====================================================================================================
#=====================================================================================================
#=====================================================================================================

# --------------------------------------------------
# EnvelopeFrame: Main frame that houses the envelope display and controls.
# --------------------------------------------------
class FilterEnvelopePanel(wx.Panel):
    def __init__(self, parent, envelope_controls, voice_dict, main):
        super().__init__(parent)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        panel = self
        panel.SetSizer(main_sizer)
        self.voice_dict = voice_dict
        self.envelope_display = FilterEnvelopeDisplay(self, min_width=600, min_height=180, on_change=self.on_display_change, main = main)

        main_sizer.Add(self.envelope_display, -1, wx.ALL, 10)


        self.atkrate1 = envelope_controls[0]
        self.atkamt1 = envelope_controls[1]
        self.atkrate2 = envelope_controls[2]
        self.atkamt2 = envelope_controls[3]

        self.dcyrate1 = envelope_controls[4]
        self.dcyamt1 = envelope_controls[5]
        self.dcyrate2 = envelope_controls[6]
        self.dcyamt2 = envelope_controls[7]
                
        self.rlsrate1 = envelope_controls[8]
        self.rlsamt1 = envelope_controls[9]
        self.rlsrate2 = envelope_controls[10]
        self.rlsamt2 = envelope_controls[11]
        
        # self.env_depth = envelope_controls[12]
        # self.amp_env_depth_ctrl = amp_env_depth_ctrl
        
        self.atkrate1.Bind(EVT_DRAGGABLENUMBER, self.on_ctrl_change)
        self.atkamt1.Bind(EVT_DRAGGABLENUMBER, self.on_ctrl_change)
        self.atkrate2.Bind(EVT_DRAGGABLENUMBER, self.on_ctrl_change)
        self.atkamt2.Bind(EVT_DRAGGABLENUMBER, self.on_ctrl_change)
        self.dcyrate1.Bind(EVT_DRAGGABLENUMBER, self.on_ctrl_change)
        self.dcyamt1.Bind(EVT_DRAGGABLENUMBER, self.on_ctrl_change)
        self.dcyrate2.Bind(EVT_DRAGGABLENUMBER, self.on_ctrl_change)
        self.dcyamt2.Bind(EVT_DRAGGABLENUMBER, self.on_ctrl_change)
        self.rlsrate1.Bind(EVT_DRAGGABLENUMBER, self.on_ctrl_change)
        self.rlsamt1.Bind(EVT_DRAGGABLENUMBER, self.on_ctrl_change)
        self.rlsrate2.Bind(EVT_DRAGGABLENUMBER, self.on_ctrl_change)
        self.rlsamt2.Bind(EVT_DRAGGABLENUMBER, self.on_ctrl_change)
        # self.env_depth.Bind(EVT_DRAGGABLENUMBER, self.on_ctrl_change)
        # self.amp_env_depth_ctrl.Bind(wx.EVT_COMBOBOX, self.on_ctrl_change)
    # handler signature
        self.load_up()
        self.Center()
        self.Show()

    def on_ctrl_change(self, event):
        if self.envelope_display.mouse_down == True:
            return
        a_1_rate = self.atkrate1.value
        a_1_level = self.atkamt1.value
        a_2_rate = self.atkrate2.value
        a_2_level = self.atkamt2.value
        d_1_rate = self.dcyrate1.value
        d_1_level = self.dcyamt1.value
        d_2_rate = self.dcyrate2.value
        d_2_level = self.dcyamt2.value
        r_1_rate = self.rlsrate1.value
        r_1_level = self.rlsamt1.value
        r_2_rate = self.rlsrate2.value
        r_2_level = self.rlsamt2.value
        
        # ctrl = event.GetEventObject()
        # if ctrl == self.amp_env_depth_ctrl:
        #     self.env_depth.value = amp_env_depths_conv[ctrl.GetValue()]
        # elif ctrl == self.env_depth:
        #     self.amp_env_depth_ctrl.SetStringSelection(amp_env_depths[ctrl.value])
        depth = 16

        # Update the envelope display.
        self.envelope_display.update_parameters(a_1_rate, a_1_level, a_2_rate, a_2_level, d_1_rate, d_1_level, d_2_rate, d_2_level, r_1_rate, r_1_level, r_2_rate, r_2_level, depth)

    def on_display_change(self, rates = None, levels = None):
        if self.envelope_display.mouse_down == True:
            
            self.atkrate1.set_value(self.envelope_display.attack_1_rate)
            self.atkamt1.set_value(self.envelope_display.attack_1_level)

            self.atkrate2.set_value(self.envelope_display.attack_2_rate)
            self.atkamt2.set_value(self.envelope_display.attack_2_level)

            self.dcyrate1.set_value(self.envelope_display.decay_1_rate)
            self.dcyamt1.set_value(self.envelope_display.decay_1_level)

            self.dcyrate2.set_value(self.envelope_display.decay_2_rate)
            self.dcyamt2.set_value(self.envelope_display.decay_2_level)

            self.rlsrate1.set_value(self.envelope_display.release_1_rate)
            self.rlsamt1.set_value(self.envelope_display.release_1_level)

            self.rlsrate2.set_value(self.envelope_display.release_2_rate)
            self.rlsamt2.set_value(self.envelope_display.release_2_level)
            
            # self.env_depth.set_value(self.envelope_display.depth)
            
    
    def load_up(self):
        a_1_rate = self.atkrate1.value
        a_1_level = self.atkamt1.value
        a_2_rate = self.atkrate2.value
        a_2_level = self.atkamt2.value
        d_1_rate = self.dcyrate1.value
        d_1_level = self.dcyamt1.value
        d_2_rate = self.dcyrate2.value
        d_2_level = self.dcyamt2.value
        r_1_rate = self.rlsrate1.value
        r_1_level = self.rlsamt1.value
        r_2_rate = self.rlsrate2.value
        r_2_level = self.rlsamt2.value
        depth = 16

        # Update the envelope display.
        self.envelope_display.update_parameters(a_1_rate, a_1_level, a_2_rate, a_2_level, d_1_rate, d_1_level, d_2_rate, d_2_level, r_1_rate, r_1_level, r_2_rate, r_2_level, depth)

    






















































#=====================================================================================================
#=====================================================================================================
#==============================   AUX  =======================================================================


class AuxEnvelopeDisplay(wx.Panel):
    def __init__(self, parent, min_width=600, min_height=150,
                 on_change=None, main=None):
        super().__init__(parent)
        self.main, self.on_change = main, on_change
        self.SetBackgroundColour("black")
        self.SetDoubleBuffered(True)
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.SetMinSize((min_width, min_height))

        self.mouse_down = False
        self.left_margin = 10; self.right_margin = 10
        self.top_margin  = 10; self.bottom_margin = 10

        # -------- default params (levels 0–200) --------
        self.attack_1_rate, self.attack_1_level = 50, 100
        self.attack_2_rate, self.attack_2_level = 50, 100
        self.decay_1_rate,  self.decay_1_level  = 50, 150
        self.decay_2_rate,  self.decay_2_level  = 50, 150
        self.release_1_rate,self.release_1_level= 50, 100
        self.release_2_rate,self.release_2_level= 50, 100
        self._raw_depth = 16
        self.depth      = (100/16)*self._raw_depth

        self._pts = []; self._drag_i = None; self.point_r = 4
        self.Bind(wx.EVT_PAINT, self._on_paint)
        self.Bind(wx.EVT_LEFT_DOWN, self._on_left_down)
        self.Bind(wx.EVT_LEFT_UP,   self._on_left_up)
        self.Bind(wx.EVT_MOTION,    self._on_mouse_move)
        self.Bind(wx.EVT_SIZE, lambda e: (self.Refresh(), e.Skip()))

    # -------------------------------------------------- helpers
    def _disp(self, lvl):            # 0-200  →  −100…+100
        return (lvl - 100) * (self.depth/100.0)

    def _inv_disp(self, disp):       # −100…+100 → 0-200
        return disp + 100

    def update_parameters(self,
            a1r, a1l, a2r, a2l,
            d1r, d1l, d2r, d2l,
            r1r, r1l, r2r, r2l,
            depth):
        (self.attack_1_rate,  self.attack_1_level,
         self.attack_2_rate,  self.attack_2_level,
         self.decay_1_rate,   self.decay_1_level,
         self.decay_2_rate,   self.decay_2_level,
         self.release_1_rate, self.release_1_level,
         self.release_2_rate, self.release_2_level) = (
            a1r, a1l, a2r, a2l,
            d1r, d1l, d2r, d2l,
            r1r, r1l, r2r, r2l
        )
        self.depth = (100/16)*depth
        self.Refresh()

        if self.on_change:
            rates  = [0, self.attack_1_rate, self.attack_2_rate,
                         self.decay_1_rate,  self.decay_2_rate,
                         self.release_1_rate,self.release_2_rate]
            levels = [0,
                self._disp(self.attack_1_level),
                self._disp(self.attack_2_level),
                self._disp(self.decay_1_level),
                self._disp(self.decay_2_level),
                self._disp(self.release_1_level),
                self._disp(self.release_2_level)]
            self.on_change(rates, levels)

    # -------------------------------------------------- paint
    def _on_paint(self, _):
        dc = wx.PaintDC(self); dc.Clear()
        w,h = self.GetClientSize()
        left = self.left_margin
        avail_w = w - self.left_margin - self.right_margin
        y_top = self.top_margin
        y_bot = h - self.bottom_margin
        span  = y_bot - y_top
        y_mid = (y_top + y_bot) / 2

        # centre-line
        dc.SetPen(wx.Pen(wx.Colour(200,200,200),1,wx.PENSTYLE_DOT))
        dc.DrawLine(left, int(y_mid), left+avail_w, int(y_mid))

        # effective display levels
        ea1, ea2 = self._disp(self.attack_1_level),  self._disp(self.attack_2_level)
        ed1, ed2 = self._disp(self.decay_1_level),   self._disp(self.decay_2_level)
        er1, er2 = self._disp(self.release_1_level), self._disp(self.release_2_level)

        rates = [self.attack_1_rate, self.attack_2_rate,
                 self.decay_1_rate,  self.decay_2_rate,
                 self.release_1_rate,self.release_2_rate]
        total = sum(rates) or 1
        xs = [left]
        for r in rates: xs.append(xs[-1] + (r/total)*avail_w)

        
        def level_to_y(level):
            # level is -100...+100, map to y_bot (bottom) ... y_top (top)
            norm = (level + 200) / 200.0
            return y_bot - norm * (y_bot - y_top)

        ys = [
            level_to_y(-100),           # start at centre
            level_to_y(ea1),
            level_to_y(ea2),
            level_to_y(ed1),
            level_to_y(ed2),
            level_to_y(er1),
            level_to_y(er2)            # last point centre
        ]

        self._pts = list(zip(xs, ys))

        gc = wx.GraphicsContext.Create(dc)
        path = gc.CreatePath(); path.MoveToPoint(xs[0],ys[0])
        for x,y in zip(xs[1:],ys[1:]): path.AddLineToPoint(x,y)
        path.AddLineToPoint(xs[-1], y_bot); path.AddLineToPoint(xs[0], y_bot)
        path.CloseSubpath()
        brush = gc.CreateLinearGradientBrush(left,y_top,left,y_bot,
                    wx.Colour(255,50,150,120), wx.Colour(50,150,255,10))
        
        gc.SetBrush(brush); gc.FillPath(path)
        gc.SetPen(gc.CreatePen(wx.Pen(wx.Colour("green"),2)))
        stroke = gc.CreatePath(); stroke.MoveToPoint(xs[0],ys[0])
        for x,y in zip(xs[1:],ys[1:]): stroke.AddLineToPoint(x,y)
        
        # draw 2 vertical grid lines
        pen_vert = wx.Pen(wx.Colour(200,200,200), 1, wx.PENSTYLE_DOT)
        dc.SetPen(pen_vert)
        for idx in (2, 4):
            x = xs[idx]
            dc.DrawLine(int(x), int(y_top), int(x), int(y_bot))
        
        gc.StrokePath(stroke)
        for x,y in zip(xs,ys):
            gc.SetBrush(wx.Brush(wx.Colour("blue")))
            gc.DrawEllipse(x-self.point_r,y-self.point_r,
                           self.point_r*2,self.point_r*2)

    # -------------------------------------------------- dragging
    def _on_left_down(self, evt):
        self.mouse_down = True
        x,y = evt.GetPosition()
        for i,(px,py) in enumerate(self._pts):
            if i>0 and (x-px)**2+(y-py)**2 < (self.point_r*1.5)**2:
                self._drag_i = i; self.CaptureMouse(); return

    def _on_left_up(self, _):
        self.mouse_down = False; self._drag_i = None
        if self.HasCapture(): self.ReleaseMouse()

    def _on_mouse_move(self, evt):
        if self._drag_i is None or not(evt.LeftIsDown() and evt.Dragging()):
            return
        x, y = evt.GetPosition()
        w, h = self.GetClientSize()
        left = self.left_margin
        avail_w = w - self.left_margin - self.right_margin
        y_top = self.top_margin
        y_bot = h - self.bottom_margin

        rates = [self.attack_1_rate, self.attack_2_rate,
                self.decay_1_rate,  self.decay_2_rate,
                self.release_1_rate,self.release_2_rate]
        total = sum(rates) or 1
        xs = [left]
        for r in rates:
            xs.append(xs[-1] + (r / total) * avail_w)

        seg_idx = self._drag_i - 1
        new_r = max(0, min(127, round((x - xs[self._drag_i - 1]) / avail_w * total)))
        if   seg_idx == 0: self.attack_1_rate = new_r; self.main.send_parameter_edit(117, new_r)
        elif seg_idx == 1: self.attack_2_rate = new_r; self.main.send_parameter_edit(119, new_r)
        elif seg_idx == 2: self.decay_1_rate  = new_r; self.main.send_parameter_edit(121, new_r)
        elif seg_idx == 3: self.decay_2_rate  = new_r; self.main.send_parameter_edit(123, new_r)
        elif seg_idx == 4: self.release_1_rate= new_r; self.main.send_parameter_edit(125, new_r)
        elif seg_idx == 5: self.release_2_rate= new_r; self.main.send_parameter_edit(127, new_r)

        # --- FIXED: Convert mouse y to logical level ---
        norm = (y_bot - y) / (y_bot - y_top)
        int_l = int(round(max(-100, min(100, norm * 200.0 - 100))))
        i = self._drag_i
        if   i == 1: self.attack_1_level  = int_l; self.main.send_parameter_edit(118, int(round(int_l)))
        elif i == 2: self.attack_2_level  = int_l; self.main.send_parameter_edit(120, int(round(int_l)))
        elif i == 3: self.decay_1_level   = int_l; self.main.send_parameter_edit(122, int(round(int_l)))
        elif i == 4: self.decay_2_level   = int_l; self.main.send_parameter_edit(124, int(round(int_l)))
        elif i == 5: self.release_1_level = int_l; self.main.send_parameter_edit(126, int(round(int_l)))
        elif i == 6: self.release_2_level = int_l; self.main.send_parameter_edit(128, int(round(int_l)))

        self.update_parameters(
            self.attack_1_rate, self.attack_1_level,
            self.attack_2_rate, self.attack_2_level,
            self.decay_1_rate,  self.decay_1_level,
            self.decay_2_rate,  self.decay_2_level,
            self.release_1_rate,self.release_1_level,
            self.release_2_rate,self.release_2_level,
            self._raw_depth)









#=====================================================================================================
#=====================================================================================================
#========================================     aux   =============================================================


# --------------------------------------------------
# EnvelopeFrame: Main frame that houses the envelope display and controls.
# --------------------------------------------------
class AuxEnvelopePanel(wx.Panel):
    def __init__(self, parent, envelope_controls, voice_dict, main):
        super().__init__(parent)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        panel = self
        panel.SetSizer(main_sizer)
        self.voice_dict = voice_dict
        self.envelope_display = AuxEnvelopeDisplay(self, min_width=600, min_height=180, on_change=self.on_display_change, main = main)

        main_sizer.Add(self.envelope_display, -1, wx.ALL, 10)


        self.atkrate1 = envelope_controls[0]
        self.atkamt1 = envelope_controls[1]
        self.atkrate2 = envelope_controls[2]
        self.atkamt2 = envelope_controls[3]

        self.dcyrate1 = envelope_controls[4]
        self.dcyamt1 = envelope_controls[5]
        self.dcyrate2 = envelope_controls[6]
        self.dcyamt2 = envelope_controls[7]
                
        self.rlsrate1 = envelope_controls[8]
        self.rlsamt1 = envelope_controls[9]
        self.rlsrate2 = envelope_controls[10]
        self.rlsamt2 = envelope_controls[11]
        
        # self.env_depth = envelope_controls[12]
        # self.amp_env_depth_ctrl = amp_env_depth_ctrl
        
        self.atkrate1.Bind(EVT_DRAGGABLENUMBER, self.on_ctrl_change)
        self.atkamt1.Bind(EVT_DRAGGABLENUMBER, self.on_ctrl_change)
        self.atkrate2.Bind(EVT_DRAGGABLENUMBER, self.on_ctrl_change)
        self.atkamt2.Bind(EVT_DRAGGABLENUMBER, self.on_ctrl_change)
        self.dcyrate1.Bind(EVT_DRAGGABLENUMBER, self.on_ctrl_change)
        self.dcyamt1.Bind(EVT_DRAGGABLENUMBER, self.on_ctrl_change)
        self.dcyrate2.Bind(EVT_DRAGGABLENUMBER, self.on_ctrl_change)
        self.dcyamt2.Bind(EVT_DRAGGABLENUMBER, self.on_ctrl_change)
        self.rlsrate1.Bind(EVT_DRAGGABLENUMBER, self.on_ctrl_change)
        self.rlsamt1.Bind(EVT_DRAGGABLENUMBER, self.on_ctrl_change)
        self.rlsrate2.Bind(EVT_DRAGGABLENUMBER, self.on_ctrl_change)
        self.rlsamt2.Bind(EVT_DRAGGABLENUMBER, self.on_ctrl_change)
        # self.env_depth.Bind(EVT_DRAGGABLENUMBER, self.on_ctrl_change)
        # self.amp_env_depth_ctrl.Bind(wx.EVT_COMBOBOX, self.on_ctrl_change)
    # handler signature
        self.load_up()
        self.Center()
        self.Show()

    def on_ctrl_change(self, event):
        if self.envelope_display.mouse_down == True:
            return
        a_1_rate = self.atkrate1.value
        a_1_level = self.atkamt1.value
        a_2_rate = self.atkrate2.value
        a_2_level = self.atkamt2.value
        d_1_rate = self.dcyrate1.value
        d_1_level = self.dcyamt1.value
        d_2_rate = self.dcyrate2.value
        d_2_level = self.dcyamt2.value
        r_1_rate = self.rlsrate1.value
        r_1_level = self.rlsamt1.value
        r_2_rate = self.rlsrate2.value
        r_2_level = self.rlsamt2.value
        
        # ctrl = event.GetEventObject()
        # if ctrl == self.amp_env_depth_ctrl:
        #     self.env_depth.value = amp_env_depths_conv[ctrl.GetValue()]
        # elif ctrl == self.env_depth:
        #     self.amp_env_depth_ctrl.SetStringSelection(amp_env_depths[ctrl.value])
        depth = 16

        # Update the envelope display.
        self.envelope_display.update_parameters(a_1_rate, a_1_level, a_2_rate, a_2_level, d_1_rate, d_1_level, d_2_rate, d_2_level, r_1_rate, r_1_level, r_2_rate, r_2_level, depth)

    def on_display_change(self, rates = None, levels = None):
        if self.envelope_display.mouse_down == True:
            
            self.atkrate1.set_value(self.envelope_display.attack_1_rate)
            self.atkamt1.set_value(self.envelope_display.attack_1_level)

            self.atkrate2.set_value(self.envelope_display.attack_2_rate)
            self.atkamt2.set_value(self.envelope_display.attack_2_level)

            self.dcyrate1.set_value(self.envelope_display.decay_1_rate)
            self.dcyamt1.set_value(self.envelope_display.decay_1_level)

            self.dcyrate2.set_value(self.envelope_display.decay_2_rate)
            self.dcyamt2.set_value(self.envelope_display.decay_2_level)

            self.rlsrate1.set_value(self.envelope_display.release_1_rate)
            self.rlsamt1.set_value(self.envelope_display.release_1_level)

            self.rlsrate2.set_value(self.envelope_display.release_2_rate)
            self.rlsamt2.set_value(self.envelope_display.release_2_level)
            
            # self.env_depth.set_value(self.envelope_display.depth)
            
    
    def load_up(self):
        a_1_rate = self.atkrate1.value
        a_1_level = self.atkamt1.value
        a_2_rate = self.atkrate2.value
        a_2_level = self.atkamt2.value
        d_1_rate = self.dcyrate1.value
        d_1_level = self.dcyamt1.value
        d_2_rate = self.dcyrate2.value
        d_2_level = self.dcyamt2.value
        r_1_rate = self.rlsrate1.value
        r_1_level = self.rlsamt1.value
        r_2_rate = self.rlsrate2.value
        r_2_level = self.rlsamt2.value
        depth = 16

        # Update the envelope display.
        self.envelope_display.update_parameters(a_1_rate, a_1_level, a_2_rate, a_2_level, d_1_rate, d_1_level, d_2_rate, d_2_level, r_1_rate, r_1_level, r_2_rate, r_2_level, depth)

    



