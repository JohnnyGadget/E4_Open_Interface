import wx
from mido import Message

NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

def note_number_to_name(n):
    if not (0 <= n <= 127):
        return "?"
    note = NOTE_NAMES[n % 12]
    octave = (n // 12) - 2
    return f"{note}{octave}"

def is_white_key(n):
    return NOTE_NAMES[n % 12] not in ['C#', 'D#', 'F#', 'G#', 'A#']

CHORDS = [
    ("Single Note", [0]),
    ("Major", [0, 4, 7]),
    ("Minor", [0, 3, 7]),
    ("Diminished", [0, 3, 6]),
    ("Augmented", [0, 4, 8]),
    ("Maj7", [0, 4, 7, 11]),
    ("Min7", [0, 3, 7, 10]),
    ("7 (Dom7)", [0, 4, 7, 10]),
    ("Sus2", [0, 2, 7]),
    ("Sus4", [0, 5, 7]),
]

class DraggableNumber(wx.StaticText):
    def __init__(self, parent, value=100, min_val=1, max_val=127, callback=None):
        wx.StaticText.__init__(self, parent, label=str(value), style=wx.ALIGN_CENTER)
        self.value = value
        self.min_val = min_val
        self.max_val = max_val
        self.callback = callback
        self.start_y = None
        self.SetCursor(wx.Cursor(wx.CURSOR_SIZENS))
        self.Bind(wx.EVT_LEFT_DOWN, self.on_mouse_down)
        self.Bind(wx.EVT_MOTION, self.on_mouse_drag)
        self.Bind(wx.EVT_LEFT_UP, self.on_mouse_up)
        self.SetMinSize((38, 18))

    def on_mouse_down(self, event):
        self.start_y = event.GetY()
        self.CaptureMouse()
        event.Skip()

    def on_mouse_drag(self, event):
        if not (self.HasCapture() and event.Dragging() and event.LeftIsDown()):
            event.Skip()
            return
        dy = self.start_y - event.GetY()
        sensitivity = 5
        delta = int(dy / sensitivity)
        if delta:
            new_value = max(self.min_val, min(self.max_val, self.value + delta))
            if new_value != self.value:
                self.value = new_value
                self.SetLabel(str(self.value))
                if self.callback:
                    self.callback(self.value)
            self.start_y = event.GetY()
        event.Skip()

    def on_mouse_up(self, event):
        if self.HasCapture():
            self.ReleaseMouse()
        event.Skip()

    def set_value(self, v):
        v = max(self.min_val, min(self.max_val, v))
        self.value = v
        self.SetLabel(str(self.value))
        if self.callback:
            self.callback(self.value)

    def GetValue(self):
        return self.value

class ControlsPanel(wx.Panel):
    """Contains chord selector, velocity, octave, and PC keyboard toggle. Forwards changes via callback."""
    def __init__(self, parent, on_chord=None, on_velocity=None, on_pc_key_toggle=None, on_octave=None):
        wx.Panel.__init__(self, parent)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)

        # Chord selector
        self.chord_choice = wx.Choice(self, choices=[name for name, _ in CHORDS])
        self.chord_choice.SetSelection(0)
        hsizer.Add(self.chord_choice, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)

        # PC keyboard toggle
        self.pc_key_toggle = wx.ToggleButton(self, label="Enable PC Keyboard")
        self.pc_key_toggle.SetValue(False)
        hsizer.Add(self.pc_key_toggle, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)

        # Octave spinner (NEW!)
        hsizer.Add(wx.StaticText(self, label="Octave:"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        self.octave_spinner = wx.SpinCtrl(self, min=-2, max=8, initial=4, style=wx.SP_ARROW_KEYS)
        hsizer.Add(self.octave_spinner, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)

        # Velocity
        hsizer.Add(wx.StaticText(self, label="Velocity:"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        self.vel_ctrl = DraggableNumber(self, value=100, min_val=1, max_val=127)
        hsizer.Add(self.vel_ctrl, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)

        self.SetSizer(hsizer)

        # Bind events
        if on_chord:
            self.chord_choice.Bind(wx.EVT_CHOICE, lambda evt: on_chord(self.chord_choice.GetSelection()))
        if on_velocity:
            self.vel_ctrl.callback = on_velocity
        if on_pc_key_toggle:
            self.pc_key_toggle.Bind(wx.EVT_TOGGLEBUTTON, lambda evt: on_pc_key_toggle(self.pc_key_toggle.GetValue()))
        if on_octave:
            self.octave_spinner.Bind(wx.EVT_SPINCTRL, lambda evt: on_octave(self.octave_spinner.GetValue()))

    def set_velocity(self, v):
        self.vel_ctrl.set_value(v)

    def set_chord(self, idx):
        self.chord_choice.SetSelection(idx)

    def set_pc_key_enabled(self, enabled):
        self.pc_key_toggle.SetValue(enabled)

    def set_octave(self, octave):
        self.octave_spinner.SetValue(octave)

    def get_octave(self):
        return self.octave_spinner.GetValue()

class KeyboardPanel(wx.Panel):
    def __init__(self, parent, get_chord, get_velocity, get_pc_keys_enabled, get_octave, main=None, callback=None):
        wx.Panel.__init__(self, parent, size=(127*14, 120), style=wx.WANTS_CHARS)
        self.main = main
        self.callback = callback
        self.key_width = 14
        self.white_height = 70
        self.black_height = 40
        self.pressed_note = None
        self.pressed_by_mouse = None
        self.pressed_chord_notes = []
        self.get_chord = get_chord
        self.get_velocity = get_velocity
        self.get_pc_keys_enabled = get_pc_keys_enabled
        self.get_octave = get_octave  # NEW: fetch octave
        self.base_note = 60  # C4 (default; updated dynamically)

        self.pc_keymap = {
            90: 0, 88: 2, 67: 4, 86: 5, 66: 7, 78: 9, 77: 11, 188: 12, 190: 14, 191: 16,
            83: 1, 68: 3, 71: 6, 72: 8, 74: 10, 76: 13, 59: 15,
        }

        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.Bind(wx.EVT_LEFT_UP, self.on_left_up)
        self.Bind(wx.EVT_KEY_DOWN, self.on_key_down)
        self.Bind(wx.EVT_KEY_UP, self.on_key_up)
        self.Bind(wx.EVT_ENTER_WINDOW, lambda evt: self.SetFocus())

    def get_chord_intervals(self):
        idx = self.get_chord()
        return CHORDS[idx][1]

    def get_velocity_value(self):
        return self.get_velocity()

    def get_base_note(self):
        """Returns the midi note number for 'z' key (C of selected octave)"""
        octave = self.get_octave()
        return max(0, min(127, 12 * (octave + 2)))  # octave=-2 -> 0; octave=4 -> 72

    def on_left_down(self, event):
        self.SetFocus()
        n = self.get_key_at_pos(event.GetPosition())
        if n is not None:
            self.pressed_note = n
            self.pressed_by_mouse = n
            notes = [n + interval for interval in self.get_chord_intervals() if 0 <= n+interval <= 127]
            self.pressed_chord_notes = notes
            for note in notes:
                if self.main:
                    self.main.outport.send(Message('note_on', note=note, velocity=self.get_velocity_value()))
                if self.callback:
                    self.callback('note_on', note)
            self.Refresh()

    def on_left_up(self, event):
        self.SetFocus()
        if self.pressed_by_mouse is not None:
            for note in self.pressed_chord_notes:
                if self.main:
                    self.main.outport.send(Message('note_off', note=note))
                if self.callback:
                    self.callback('note_off', note)
            self.pressed_note = None
            self.pressed_by_mouse = None
            self.pressed_chord_notes = []
            self.Refresh()

    def on_key_down(self, event):
        if not self.get_pc_keys_enabled():
            event.Skip()
            return
        keycode = event.GetKeyCode()
        rel = self.pc_keymap.get(keycode)
        if rel is not None:
            base = self.get_base_note()
            n = base + rel
            if 0 <= n <= 127:
                if self.pressed_note != n:
                    self.pressed_note = n
                    notes = [n + interval for interval in self.get_chord_intervals() if 0 <= n+interval <= 127]
                    self.pressed_chord_notes = notes
                    for note in notes:
                        if self.main:
                            self.main.outport.send(Message('note_on', note=note, velocity=self.get_velocity_value()))
                        if self.callback:
                            self.callback('note_on', note)
                    self.Refresh()
        event.Skip()

    def on_key_up(self, event):
        if not self.get_pc_keys_enabled():
            event.Skip()
            return
        keycode = event.GetKeyCode()
        rel = self.pc_keymap.get(keycode)
        if rel is not None:
            base = self.get_base_note()
            n = base + rel
            if 0 <= n <= 127 and self.pressed_note == n:
                for note in self.pressed_chord_notes:
                    if self.main:
                        self.main.outport.send(Message('note_off', note=note))
                    if self.callback:
                        self.callback('note_off', note)
                self.pressed_note = None
                self.pressed_chord_notes = []
                self.Refresh()
        event.Skip()

    def get_key_at_pos(self, pos):
        x, y = pos
        key_for_pos = None
        x_white = 0
        for n in range(128):
            if is_white_key(n):
                rect = wx.Rect(x_white, 30, self.key_width, self.white_height)
                if rect.Contains(pos):
                    key_for_pos = n
                x_white += self.key_width

        x_white = 0
        for n in range(128):
            if is_white_key(n):
                if NOTE_NAMES[(n % 12)] not in ['E', 'B'] and n+1 < 128:
                    bx = x_white + self.key_width * 0.65
                    rect = wx.Rect(int(bx-5), 30, int(self.key_width-4), int(self.black_height))
                    if rect.Contains(pos):
                        return n+1
                x_white += self.key_width
        return key_for_pos

    def on_paint(self, event):
        dc = wx.PaintDC(self)
        w, h = self.GetSize()
        dc.SetPen(wx.Pen(wx.Colour(40, 40, 45)))
        x_white = 0
        for n in range(128):
            if is_white_key(n):
                rect = wx.Rect(x_white, 30, self.key_width, self.white_height)
                highlight = False
                if self.pressed_note is not None:
                    chord_notes = [self.pressed_note + i for i in self.get_chord_intervals() if 0 <= self.pressed_note + i <= 127]
                    if n in chord_notes:
                        highlight = True
                if highlight:
                    dc.SetBrush(wx.Brush(wx.Colour(90, 190, 255)))
                else:
                    dc.SetBrush(wx.Brush(wx.Colour(240, 240, 240)))
                dc.DrawRectangle(rect)
                note_label = note_number_to_name(n)
                if NOTE_NAMES[n % 12] in ['C', 'F'] or highlight:
                    dc.SetTextForeground(wx.Colour(50, 50, 80))
                    font = wx.Font(7, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
                    dc.SetFont(font)
                    tw, th = dc.GetTextExtent(note_label)
                    dc.DrawText(note_label, rect.x + (rect.width-tw)//2, rect.y + self.white_height - th - 2)
                x_white += self.key_width

        x_white = 0
        for n in range(128):
            if is_white_key(n):
                if NOTE_NAMES[(n % 12)] not in ['E', 'B'] and n+1 < 128:
                    bx = x_white + self.key_width * 0.65
                    rect = wx.Rect(int(bx-5), 30, int(self.key_width-4), int(self.black_height))
                    black_note = n+1
                    highlight = False
                    if self.pressed_note is not None:
                        chord_notes = [self.pressed_note + i for i in self.get_chord_intervals() if 0 <= self.pressed_note + i <= 127]
                        if black_note in chord_notes:
                            highlight = True
                    if highlight:
                        dc.SetBrush(wx.Brush(wx.Colour(90, 190, 255)))
                    else:
                        dc.SetBrush(wx.Brush(wx.Colour(30, 30, 35)))
                    dc.SetPen(wx.Pen(wx.Colour(40, 40, 45)))
                    dc.DrawRectangle(rect)
                    if highlight:
                        dc.SetTextForeground(wx.Colour(200, 200, 220))
                        font = wx.Font(7, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
                        dc.SetFont(font)
                        note_label = note_number_to_name(black_note)
                        tw, th = dc.GetTextExtent(note_label)
                        dc.DrawText(note_label, rect.x + (rect.width-tw)//2, rect.y + self.black_height - th - 2)
                x_white += self.key_width

    def set_base_note(self, midi_note):
        pass  # not used, handled by get_base_note()

# ------------- Example Usage -------------

if __name__ == "__main__":
    class DummyMain:
        def __init__(self):
            self.outport = self
        def send(self, msg):
            print(msg)

    class MyFrame(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None, title="MIDI Keyboard: Octave, Chord, Velocity")
            panel = wx.Panel(self)
            vsizer = wx.BoxSizer(wx.VERTICAL)

            # State for control panel
            self.chord_index = 0
            self.velocity = 100
            self.pc_key_enabled = False
            self.octave = 4

            # Controls panel (top)
            self.controls = ControlsPanel(
                panel,
                on_chord=self.on_chord_change,
                on_velocity=self.on_velocity_change,
                on_pc_key_toggle=self.on_pc_key_toggle,
                on_octave=self.on_octave_change
            )
            vsizer.Add(self.controls, 0, wx.ALL | wx.EXPAND, 0)

            # Keyboard panel (bottom, always focusable)
            self.kb = KeyboardPanel(
                panel,
                get_chord=lambda: self.chord_index,
                get_velocity=lambda: self.velocity,
                get_pc_keys_enabled=lambda: self.pc_key_enabled,
                get_octave=lambda: self.octave,
                main=DummyMain(),
                callback=self.on_note_event
            )
            vsizer.Add(self.kb, 1, wx.ALL | wx.EXPAND, 4)
            panel.SetSizer(vsizer)
            self.SetMinSize((1200, 220))
            self.Centre()

        def on_chord_change(self, idx):
            self.chord_index = idx
            wx.CallAfter(self.kb.SetFocus)

        def on_velocity_change(self, value):
            self.velocity = value
            wx.CallAfter(self.kb.SetFocus)

        def on_pc_key_toggle(self, enabled):
            self.pc_key_enabled = enabled
            wx.CallAfter(self.kb.SetFocus)

        def on_octave_change(self, val):
            self.octave = val
            wx.CallAfter(self.kb.SetFocus)

        def on_note_event(self, evt_type, note):
            print(f"{evt_type}: {note} ({note_number_to_name(note)})")

    app = wx.App(False)
    frame = MyFrame()
    frame.Show()
    app.MainLoop()
