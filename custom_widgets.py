import wx
import wx.lib.newevent
import math

DraggableNumberEvent, EVT_DRAGGABLENUMBER = wx.lib.newevent.NewCommandEvent()

class DraggableNumber(wx.StaticText):
    def __init__(self, parent,
                 id=0,
                 value=0,
                 min_val=0,
                 max_val=127,
                 step=1,
                 callback=None,
                 callback_click=None,   # <-- new parameter
                 preset=None,
                 link=None,
                 voice=None,
                 zone=None,
                 group=None,
                 sample=None):
        super().__init__(parent, id, label=str(value), style=wx.ALIGN_CENTER)
        self.parent = parent

        # context
        self.preset = preset
        self.link   = link
        self.voice  = voice
        self.zone   = zone
        self.group  = group
        self.sample = sample

        # state
        self.value          = value
        self.min_val        = min_val
        self.max_val        = max_val
        self.step           = step
        self.callback       = callback
        self.callback_click = callback_click

        self.start_y = None

        # mouse events
        self.Bind(wx.EVT_LEFT_DOWN, self.on_mouse_down)
        self.Bind(wx.EVT_MOTION,    self.on_mouse_drag)
        self.Bind(wx.EVT_LEFT_UP,   self.on_mouse_up)

        self.SetCursor(wx.Cursor(wx.CURSOR_SIZENS))

    def on_mouse_down(self, event):
        # 1) record starting position
        self.start_y = event.GetY()
        self.CaptureMouse()

        # 2) call your click callback if provided
        if self.callback_click:
            # pass the same wx.Event (or wrap as you like)
            self.callback_click(event)

        event.Skip()

    def on_mouse_drag(self, event):
        if not (self.HasCapture() and event.Dragging() and event.LeftIsDown()):
            event.Skip()
            return

        dy = self.start_y - event.GetY()
        ctrl_held = event.ControlDown()
        sensitivity = 16 if ctrl_held else 2
        if event.AltDown():
            sensitivity = 0.2

        delta = round(dy / sensitivity)
        if delta:
            new_value = max(self.min_val,
                            min(self.max_val,
                                self.value + delta*self.step))
            if new_value != self.value:
                self.value = new_value
                self.SetLabel(str(self.value))

                # fire your drag event
                ev = DraggableNumberEvent(self.GetId())
                ev.SetEventObject(self)
                ev.SetInt(self.value)
                self.GetEventHandler().ProcessEvent(ev)

            self.start_y = event.GetY()

            # call the continuous callback (if any)
            if self.callback and (not hasattr(self, "_last_sent_value")
                                  or self.value != self._last_sent_value):
                cmd = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED,
                                      self.GetId())
                cmd.SetEventObject(self)
                cmd.SetInt(self.value)
                self.callback(cmd)
                self._last_sent_value = self.value

        event.Skip()

    def on_mouse_up(self, event):
        if self.HasCapture():
            self.ReleaseMouse()
        event.Skip()

    def set_value(self, new_value):
        new_value = max(self.min_val, min(self.max_val, new_value))
        if new_value == self.value:
            return

        self.value = new_value
        self.SetLabel(str(self.value))

        ev = DraggableNumberEvent(self.GetId())
        ev.SetEventObject(self)
        ev.SetInt(self.value)
        self.GetEventHandler().ProcessEvent(ev)





import wx

class SpinNumber(wx.SpinCtrl):
    def __init__(self, parent,
                 id=wx.ID_ANY,
                 value=0,
                 min_val=0,
                 max_val=127,
                 step=1,
                 callback=None,
                 callback_click=None,   # called on initial mouse‐down
                 preset=None,
                 link=None,
                 voice=None,
                 zone=None,
                 group=None,
                 sample=None):
        super().__init__(parent,
                         id=id,
                         initial=value,
                         min=min_val,
                         max=max_val,
                         style=wx.SP_ARROW_KEYS)
        # store everything
        self.step           = step
        self.callback       = callback
        self.callback_click = callback_click
        self.preset = preset
        self.link   = link
        self.voice  = voice
        self.zone   = zone
        self.group  = group
        self.sample = sample

        # catch the click on the control itself
        self.Bind(wx.EVT_LEFT_DOWN,   self._on_mouse_down)
        # catch all spin events (arrows, wheel, typing <Enter>)
        self.Bind(wx.EVT_SPINCTRL,    self._on_spin)
        self.Bind(wx.EVT_TEXT_ENTER,  self._on_spin)  # if you allow typing

    def _on_mouse_down(self, evt):
        if self.callback_click:
            # pass through the same event (or wrap if you like)
            self.callback_click(evt)
        evt.Skip()

    def _on_spin(self, evt):
        # fetch new value
        new_value = self.GetValue()
        # if step >1 we could quantize here, but spinctrl already steps by 1
        # so for custom step you could do:
        # new_value = (new_value // self.step) * self.step

        if self.callback:
            # wrap it in a CommandEvent with .GetInt() carrying the value
            cmd = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, self.GetId())
            cmd.SetEventObject(self)
            cmd.SetInt(new_value)
            self.callback(cmd)

        evt.Skip()




import wx

class DropDown(wx.Choice):
    def __init__(self, parent,
                 id=wx.ID_ANY,
                 choices=None,
                 selection=None,       # either an index or the string to select
                 callback=None,        # called on each selection change
                 callback_click=None,  # called once on the first mouse-down
                 preset=None,
                 link=None,
                 voice=None,
                 zone=None,
                 group=None,
                 sample=None):
        super().__init__(parent, id, choices=choices or [])
        # store your callbacks & context
        self.callback       = callback
        self.callback_click = callback_click
        self.preset = preset
        self.link   = link
        self.voice  = voice
        self.zone   = zone
        self.group  = group
        self.sample = sample

        # set the initial selection if provided
        if selection is not None:
            if isinstance(selection, int):
                self.SetSelection(selection)
            else:
                # assume string
                self.SetStringSelection(str(selection))

        # bind the mouse-down so we can get a first-click callback
        self.Bind(wx.EVT_LEFT_DOWN, self._on_mouse_down)
        # bind the choice event
        self.Bind(wx.EVT_CHOICE,    self._on_choice)

    def _on_mouse_down(self, evt):
        if self.callback_click:
            # fire your “first click” callback
            self.callback_click(evt)
        evt.Skip()

    def _on_choice(self, evt):
        sel_index = self.GetSelection()
        sel_str   = self.GetString(sel_index)
        if self.callback:
            # wrap it in a CommandEvent so you can do `.GetInt()` in your handler
            cmd = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, self.GetId())
            cmd.SetEventObject(self)
            cmd.SetInt(sel_index)
            cmd.SetString(sel_str)
            self.callback(cmd)
        evt.Skip()




# create a new command event for knob changes
KnobEvent, EVT_KNOB = wx.lib.newevent.NewCommandEvent()

class KnobCtrl(wx.Control):
    def __init__(self, parent, id=wx.ID_ANY,
                 min_val=0, max_val=100, initial=0,
                 left_stop=135, right_stop=45,
                 size=(60, 80), style=wx.BORDER_NONE):
        super().__init__(parent, id, size=size, style=style)
        self.min_val    = min_val
        self.max_val    = max_val
        self.value      = max(min(initial, max_val), min_val)
        self.left_stop  = left_stop    # degrees (math coords)
        self.right_stop = right_stop
        self._dragging  = False
        self._start_y   = 0
        self._start_val = self.value

        # for crisp drawing
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        # bind events
        self.Bind(wx.EVT_PAINT,       self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN,   self.OnLeftDown)
        self.Bind(wx.EVT_MOTION,      self.OnMotion)
        self.Bind(wx.EVT_LEFT_UP,     self.OnLeftUp)

    def OnPaint(self, evt):
        dc = wx.AutoBufferedPaintDC(self)
        w, h = self.GetClientSize()
        # clear
        dc.SetBrush(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()

        # knob circle
        radius = min(w, h-20)//2 - 4
        cx, cy = w//2, radius + 4
        dc.SetPen(wx.Pen(wx.BLACK, 1))
        dc.SetBrush(wx.Brush(wx.Colour(220,220,220)))
        dc.DrawCircle(cx, cy, radius)

        # compute angle for current value
        start = self.left_stop % 360
        end   = self.right_stop % 360
        if end <= start:
            end += 360
        frac = (self.value - self.min_val) / (self.max_val - self.min_val)
        angle = math.radians(start + frac*(end-start))

        # marker line
        mx = cx + math.cos(angle)*radius*0.8
        my = cy - math.sin(angle)*radius*0.8
        dc.SetPen(wx.Pen(wx.BLACK, 2))
        dc.DrawLine(cx, cy, mx, my)

        # value readout below
        txt = str(self.value)
        dc.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        tw, th = dc.GetTextExtent(txt)
        dc.DrawText(txt, (w-tw)//2, h- th - 4)

    def OnLeftDown(self, evt):
        self._dragging  = True
        self._start_y   = evt.GetY()
        self._start_val = self.value
        self.CaptureMouse()

    def OnMotion(self, evt):
        if not self._dragging or not evt.Dragging(): 
            return
        dy = self._start_y - evt.GetY()
        # 1 pixel = 1 unit (you can scale this)
        new_val = self._start_val + dy
        new_val = max(self.min_val, min(self.max_val, new_val))
        if new_val != self.value:
            self.value = new_val
            self.Refresh()

            # fire custom event
            e = KnobEvent(self.GetId())
            e.SetEventObject(self)
            e.SetInt(self.value)
            self.GetEventHandler().ProcessEvent(e)

    def OnLeftUp(self, evt):
        if self.HasCapture():
            self.ReleaseMouse()
        self._dragging = False

    def GetValue(self):
        return self.value

    def SetValue(self, v):
        v = max(self.min_val, min(self.max_val, v))
        if v != self.value:
            self.value = v
            self.Refresh()
            e = KnobEvent(self.GetId())
            e.SetEventObject(self)
            e.SetInt(self.value)
            self.GetEventHandler().ProcessEvent(e)





class Demo(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Knob Demo")
        knob = KnobCtrl(self, min_val=0, max_val=127, initial=64,
                        left_stop=135, right_stop=45)
        knob.Bind(EVT_KNOB, lambda e: print("Knob:", e.GetInt()))
        s = wx.BoxSizer(wx.VERTICAL)
        s.Add(knob, 0, wx.ALL|wx.CENTER, 20)
        self.SetSizer(s)
        self.Fit()
        self.Show()




# import wx
# import wx.lib.newevent

# DraggableNumberEvent, EVT_DRAGGABLENUMBER = wx.lib.newevent.NewCommandEvent()

# class DraggableNumber(wx.StaticText):
#     def __init__(self, parent, id=0, value=0, min_val=0, max_val=127, step=1, callback=None):
#         super().__init__(parent, id=id, label=str(value), style=wx.ALIGN_CENTER|wx.BORDER_SIMPLE)
#         self.parent    = parent
#         self.value     = value
#         self.min_val   = min_val
#         self.max_val   = max_val
#         self.step      = step
#         self.callback  = callback
#         self._editing  = False
#         self.start_y   = None

#         # normal dragging
#         self.Bind(wx.EVT_LEFT_DOWN,  self.on_mouse_down)
#         self.Bind(wx.EVT_MOTION,     self.on_mouse_drag)
#         self.Bind(wx.EVT_LEFT_UP,    self.on_mouse_up)
#         # double-click to edit
#         self.Bind(wx.EVT_LEFT_DCLICK, self.on_double_click)

#         self.SetCursor(wx.Cursor(wx.CURSOR_SIZENS))

#     # ─────────────────────────────────────────────────────────
#     # Mouse‐drag behavior (unchanged, except disabled while editing)
#     def on_mouse_down(self, event):
#         if self._editing:
#             return
#         self.start_y = event.GetY()
#         self.CaptureMouse()
#         event.Skip()

#     def on_mouse_drag(self, event):
#         if self._editing:
#             return
#         if self.HasCapture() and event.Dragging() and event.LeftIsDown():
#             dy = self.start_y - event.GetY()
#             ctrl_held = event.ControlDown()
#             sensitivity = 16 if ctrl_held else 2
#             delta = dy // sensitivity
#             if delta:
#                 new_value = max(self.min_val,
#                                 min(self.max_val,
#                                     self.value + delta * self.step))
#                 if new_value != self.value:
#                     self.set_value(new_value)
#                 self.start_y = event.GetY()
#         event.Skip()

#     def on_mouse_up(self, event):
#         if self._editing:
#             return
#         if self.HasCapture():
#             self.ReleaseMouse()
#         event.Skip()

#     # ─────────────────────────────────────────────────────────
#     # Double‐click → switch to text‐entry mode
#     def on_double_click(self, event):
#         if self._editing:
#             return
#         self._editing = True

#         # hide the label
#         self.Hide()

#         # compute absolute position for the editor
#         screen_pos = self.ClientToScreen((0, 0))
#         client_pos = self.parent.ScreenToClient(screen_pos)

#         # create a TextCtrl right on top of where the StaticText was
#         self._editor = wx.TextCtrl(
#             self.parent,
#             value=str(self.value),
#             pos=client_pos,
#             size=self.GetSize(),
#             style=wx.TE_PROCESS_ENTER
#         )
#         # bind Enter and focus‐lost to finish editing
#         self._editor.Bind(wx.EVT_TEXT_ENTER, self.on_text_enter)
#         self._editor.Bind(wx.EVT_KILL_FOCUS, self.on_text_enter)
#         self._editor.SetFocus()

#     def on_text_enter(self, event):
#         # read & clamp
#         try:
#             new_val = int(self._editor.GetValue())
#         except ValueError:
#             new_val = self.value
#         self.set_value(new_val)

#         # destroy editor and show label again
#         self._editor.Destroy()
#         self._editing = False
#         self.Show()

#     # ─────────────────────────────────────────────────────────
#     # Programmatic setter (fires your normal drag event)
#     def set_value(self, new_value):
#         new_value = max(self.min_val, min(self.max_val, new_value))
#         if new_value == self.value:
#             return

#         self.value = new_value
#         self.SetLabel(str(self.value))

#         # fire custom drag event
#         ev = DraggableNumberEvent(self.GetId())
#         ev.SetEventObject(self)
#         ev.SetInt(self.value)
#         self.GetEventHandler().ProcessEvent(ev)

#         # also call the callback (as your old code did on a “click”)
#         if self.callback:
#             click_ev = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, self.GetId())
#             click_ev.SetEventObject(self)
#             click_ev.SetInt(self.value)
#             self.callback(click_ev)
