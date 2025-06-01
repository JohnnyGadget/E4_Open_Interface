import wx
import math

# NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# def note_number_to_name(n):
#     if not (0 <= n <= 127):
#         return "?"
#     note = NOTE_NAMES[n % 12]
#     octave = (n // 12) - 2
#     return f"{note} {octave}"

# class CircularNoteSelector(wx.Panel):
#     def __init__(self, parent, value=60, min_val=0, max_val=127, callback=None):
#         wx.Panel.__init__(self, parent, size=(120, 120))
#         self.value = value
#         self.min_val = min_val
#         self.max_val = max_val
#         self.callback = callback
#         self.radius = 50
#         self.dragging = False
#         self._last_mouse_x = None
#         self.SetMinSize((120, 120))

#         self.Bind(wx.EVT_PAINT, self.on_paint)
#         self.Bind(wx.EVT_LEFT_DOWN, self.on_mouse_down)
#         self.Bind(wx.EVT_LEFT_UP, self.on_mouse_up)
#         self.Bind(wx.EVT_MOTION, self.on_mouse_move)
#         self.Bind(wx.EVT_MOUSEWHEEL, self.on_mouse_wheel)
#         self.SetCursor(wx.Cursor(wx.CURSOR_HAND))

#     def on_paint(self, event):
#         dc = wx.PaintDC(self)
#         dc.SetBackground(wx.Brush(wx.Colour(20, 20, 30)))
#         dc.Clear()

#         w, h = self.GetClientSize()
#         cx, cy = w // 2, h // 2

#         # Draw wheel
#         dc.SetPen(wx.Pen(wx.Colour(80, 200, 255), 2))
#         dc.SetBrush(wx.Brush(wx.Colour(40, 60, 110)))
#         dc.DrawCircle(cx, cy, self.radius)

#         # Draw notes around wheel (show 11 notes: current + 5 up/down)
#         note_count = 11
#         for i in range(-5, 6):
#             n = self.value + i
#             if self.min_val <= n <= self.max_val:
#                 angle = (math.pi / 2) - (i * (math.pi / (note_count - 1)))  # top is current
#                 nx = cx + int(math.cos(angle) * (self.radius - 12))
#                 ny = cy - int(math.sin(angle) * (self.radius - 12))
#                 label = note_number_to_name(n)
#                 font = wx.Font(8 if i else 11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL,
#                                wx.FONTWEIGHT_BOLD if i == 0 else wx.FONTWEIGHT_NORMAL)
#                 dc.SetFont(font)
#                 if i == 0:
#                     dc.SetTextForeground(wx.Colour(250, 255, 160))
#                 else:
#                     dc.SetTextForeground(wx.Colour(120, 220, 255) if abs(i) < 3 else wx.Colour(90, 120, 170))
#                 tw, th = dc.GetTextExtent(label)
#                 dc.DrawText(label, nx - tw // 2, ny - th // 2)

#         # Draw current value at center
#         dc.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
#         dc.SetTextForeground(wx.Colour(240, 255, 255))
#         big_label = note_number_to_name(self.value)
#         tw, th = dc.GetTextExtent(big_label)
#         dc.DrawText(big_label, cx - tw // 2, cy - th // 2)

#         # Draw up/down triangles
#         dc.SetPen(wx.Pen(wx.Colour(255,255,255,180), 1))
#         dc.SetBrush(wx.Brush(wx.Colour(90,200,250,180)))
#         dc.DrawPolygon([ (cx-10,cy-self.radius+6), (cx+10,cy-self.radius+6), (cx,cy-self.radius-10) ])
#         dc.DrawPolygon([ (cx-10,cy+self.radius-6), (cx+10,cy+self.radius-6), (cx,cy+self.radius+10) ])

#     def on_mouse_down(self, event):
#         self.dragging = True
#         self._last_mouse_x = event.GetX()
#         self._last_mouse_y = event.GetY()
#         # Click on up triangle = increment, down triangle = decrement
#         w, h = self.GetClientSize()
#         cx, cy = w // 2, h // 2
#         mx, my = event.GetX(), event.GetY()
#         if cy - self.radius - 14 < my < cy - self.radius + 16 and abs(mx - cx) < 14:
#             self.set_value(self.value + 1)
#             return
#         if cy + self.radius - 16 < my < cy + self.radius + 14 and abs(mx - cx) < 14:
#             self.set_value(self.value - 1)
#             return

#     def on_mouse_up(self, event):
#         self.dragging = False
#         self._last_mouse_x = None
#         self._last_mouse_y = None

#     def on_mouse_move(self, event):
#         if not self.dragging:
#             return
#         # Horizontal mouse movement to change notes
#         delta_x = event.GetX() - self._last_mouse_x
#         if abs(delta_x) > 7:
#             new_value = self.value + (1 if delta_x > 0 else -1)
#             self.set_value(new_value)
#             self._last_mouse_x = event.GetX()

#     def on_mouse_wheel(self, event):
#         rot = event.GetWheelRotation()
#         if rot > 0:
#             self.set_value(self.value + 1)
#         else:
#             self.set_value(self.value - 1)

#     def set_value(self, new_value):
#         new_value = max(self.min_val, min(self.max_val, new_value))
#         if new_value == self.value:
#             return
#         self.value = new_value
#         self.Refresh()
#         if self.callback:
#             evt = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, self.GetId())
#             evt.SetEventObject(self)
#             evt.SetInt(self.value)
#             self.callback(evt)

# # -------------------------------------------
# # Example Usage
# if __name__ == "__main__":
#     class MyFrame(wx.Frame):
#         def __init__(self):
#             wx.Frame.__init__(self, None, title="Circular Note Selector Demo")
#             panel = wx.Panel(self)
#             sizer = wx.BoxSizer(wx.VERTICAL)
#             self.note_selector = CircularNoteSelector(panel, value=60, callback=self.on_note_change)
#             sizer.Add(self.note_selector, 0, wx.ALL | wx.CENTER, 20)
#             panel.SetSizer(sizer)
#             self.SetSize((200, 220))

#         def on_note_change(self, evt):
#             print("Note changed:", evt.GetInt(), note_number_to_name(evt.GetInt()))

#     app = wx.App(False)
#     frame = MyFrame()
#     frame.Show()
#     app.MainLoop()



NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

def note_number_to_name(n):
    if not (0 <= n <= 127):
        return "?"
    note = NOTE_NAMES[n % 12]
    octave = (n // 12) - 2
    return f"{note}{octave}"

def is_white_key(n):
    return NOTE_NAMES[n % 12] not in ['C#', 'D#', 'F#', 'G#', 'A#']

class MidiKeyboardSelector(wx.Panel):
    def __init__(self, parent, note1=60, note2=64, callback=None):
        # This will be a long horizontal keyboard (may want to use a scrolled panel for UI, but here is direct)
        wx.Panel.__init__(self, parent, size=(127*14, 80))
        self.SetMinSize((127*14, 80))
        self.note1 = note1
        self.note2 = note2
        self.callback = callback
        self.key_width = 14
        self.white_height = 70
        self.black_height = 40
        self.selected_brush1 = wx.Brush(wx.Colour(60, 180, 255))    # Blue
        self.selected_brush2 = wx.Brush(wx.Colour(255, 140, 30))    # Orange
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_click)
        self.Bind(wx.EVT_RIGHT_DOWN, self.on_right_click)
        self.SetBackgroundColour(wx.Colour(30, 30, 35))
        self.key_rects = self._build_key_rects()

    def _build_key_rects(self):
        rects = []
        x = 0
        for n in range(128):
            if is_white_key(n):
                rects.append((n, wx.Rect(x, 0, self.key_width, self.white_height)))
                x += self.key_width
        return rects

    def get_key_at_pos(self, pos):
        # Prefer black keys if click overlaps both
        x, y = pos
        key_for_pos = None
        x_white = 0
        for n in range(128):
            if is_white_key(n):
                # Check white key
                rect = wx.Rect(x_white, 0, self.key_width, self.white_height)
                if rect.Contains(pos):
                    key_for_pos = n
                x_white += self.key_width

        # Now black keys (drawn on top), smaller and offset
        x_white = 0
        for n in range(128):
            if is_white_key(n):
                # Is there a black key after this?
                if NOTE_NAMES[(n % 12)] not in ['E', 'B'] and n+1 < 128:
                    # Black keys are offset a bit to the right
                    bx = x_white + self.key_width * 0.65
                    rect = wx.Rect(int(bx-5), 0, int(self.key_width-4), int(self.black_height))
                    if rect.Contains(pos):
                        return n+1

                x_white += self.key_width
        return key_for_pos

    def on_left_click(self, event):
        n = self.get_key_at_pos(event.GetPosition())
        if n is not None:
            if n != self.note1:
                self.note1 = n
                self.Refresh()
                if self.callback:
                    self.callback(self.note1, self.note2)

    def on_right_click(self, event):
        n = self.get_key_at_pos(event.GetPosition())
        if n is not None:
            if n != self.note2:
                self.note2 = n
                self.Refresh()
                if self.callback:
                    self.callback(self.note1, self.note2)

    def on_paint(self, event):
        dc = wx.PaintDC(self)
        w, h = self.GetSize()
        dc.SetPen(wx.Pen(wx.Colour(40, 40, 45)))
        x_white = 0
        white_key_indices = []
        # Draw white keys
        for n in range(128):
            if is_white_key(n):
                rect = wx.Rect(x_white, 0, self.key_width, self.white_height)
                if n == self.note1:
                    dc.SetBrush(self.selected_brush1)
                elif n == self.note2:
                    dc.SetBrush(self.selected_brush2)
                else:
                    dc.SetBrush(wx.Brush(wx.Colour(240, 240, 240)))
                dc.DrawRectangle(rect)
                # Draw label for every C, F, or selected
                note_label = note_number_to_name(n)
                if NOTE_NAMES[n % 12] in ['C', 'F'] or n in (self.note1, self.note2):
                    dc.SetTextForeground(wx.Colour(50, 50, 80))
                    font = wx.Font(7, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
                    dc.SetFont(font)
                    tw, th = dc.GetTextExtent(note_label)
                    dc.DrawText(note_label, rect.x + (rect.width-tw)//2, rect.y + self.white_height - th - 2)
                white_key_indices.append(x_white)
                x_white += self.key_width

        # Draw black keys (overlap)
        x_white = 0
        for n in range(128):
            if is_white_key(n):
                if NOTE_NAMES[(n % 12)] not in ['E', 'B'] and n+1 < 128:
                    bx = x_white + self.key_width * 0.65
                    rect = wx.Rect(int(bx-5), 0, int(self.key_width-4), int(self.black_height))
                    black_note = n+1
                    if black_note == self.note1:
                        dc.SetBrush(self.selected_brush1)
                    elif black_note == self.note2:
                        dc.SetBrush(self.selected_brush2)
                    else:
                        dc.SetBrush(wx.Brush(wx.Colour(30, 30, 35)))
                    dc.SetPen(wx.Pen(wx.Colour(40, 40, 45)))
                    dc.DrawRectangle(rect)
                    # Draw label for selected only
                    if black_note in (self.note1, self.note2):
                        dc.SetTextForeground(wx.Colour(200, 200, 220))
                        font = wx.Font(7, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
                        dc.SetFont(font)
                        note_label = note_number_to_name(black_note)
                        tw, th = dc.GetTextExtent(note_label)
                        dc.DrawText(note_label, rect.x + (rect.width-tw)//2, rect.y + self.black_height - th - 2)
                x_white += self.key_width

    def set_notes(self, note1, note2):
        self.note1 = note1
        self.note2 = note2
        self.Refresh()

# --------------------------------------
# Example Usage
if __name__ == "__main__":
    class MyFrame(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None, title="MIDI Keyboard Selector Demo")
            panel = wx.Panel(self)
            sizer = wx.BoxSizer(wx.VERTICAL)
            kb = MidiKeyboardSelector(panel, note1=60, note2=64, callback=self.on_notes)
            sizer.Add(kb, 0, wx.ALL|wx.EXPAND, 8)
            panel.SetSizer(sizer)
            self.SetMinSize((1300, 120))
            self.Centre()

        def on_notes(self, note1, note2):
            print(f"Note 1: {note1} ({note_number_to_name(note1)}), Note 2: {note2} ({note_number_to_name(note2)})")

    app = wx.App(False)
    frame = MyFrame()
    frame.Show()
    app.MainLoop()
