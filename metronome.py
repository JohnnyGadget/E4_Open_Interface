import wx
import threading
import time
from mido import Message


NOTE_NAMES = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
BLACK_KEYS = {1, 3, 6, 8, 10}

def midi_to_note(n: int) -> str:
    """Convert 0–127 to 'C 3' style with C3 at 60."""
    octave = (n // 12) - 2
    name   = NOTE_NAMES[n % 12]
    return f"{name} {octave}"


class MetronomePanel(wx.Panel):
    def __init__(self, parent, main):
        super().__init__(parent, size=(520, 30))
        
        box = wx.StaticBox(self, label="Metronome")
        box.SetBackgroundColour("medium grey")
        box.SetForegroundColour(wx.Colour(153, 245, 198))
        sbs = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        self.main = main



        # Start/Stop button
        self.btn = wx.Button(self, label="Start")
        self.btn.SetMinSize((60, 20))
        sbs.Add(self.btn, 0, wx.ALL, 4)

        # BPM spinner
        sbs.Add(wx.StaticText(self, label="BPM:"), 
                0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)
        self.bpm = wx.SpinCtrl(self, value="120", min=20, max=300)
        self.bpm.SetMinSize((60, 20))
        sbs.Add(self.bpm, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 10)
        
        # Note1 button
        self.spin = wx.SpinCtrl(self, initial = 60, min = 0, max = 127, value ="Note 1", name="Note 1")
        self.spin.SetMinSize((60, 20))
        sbs.Add(self.spin, 0, wx.ALL, 4)
        self.spin.Bind(wx.EVT_SPINCTRL, self._on_note)
        self.note = 60
        
        
        # Note2 button
        self.spin2 = wx.SpinCtrl(self, initial = 60, min = 0, max = 127, value ="Note 2", name="Note 2")
        self.spin2.SetMinSize((60, 20))
        sbs.Add(self.spin2, 0, wx.ALL, 4)
        self.spin2.Bind(wx.EVT_SPINCTRL, self._on_note2)
        self.note2 = 60
        
        # Velocity button
        self.Velocity = wx.SpinCtrl(self, initial = 64, min = 0, max = 127, value ="Vel", name="Vel")
        self.Velocity.SetMinSize((60, 20))
        sbs.Add(self.Velocity, 0, wx.ALL, 4)
        self.Velocity.Bind(wx.EVT_SPINCTRL, self._on_Vel)
        self.vel = 64

        self.SetSizerAndFit(sbs)

        # threading control
        self._running = False
        self._thread  = None
        self._lock    = threading.Lock()
        self._beat    = 0

        # event binding
        self.btn.Bind(wx.EVT_BUTTON, self._on_toggle)

    def _on_toggle(self, _evt):
        with self._lock:
            if self._running:
                # stop
                self._running = False
                self.btn.SetLabel("Start")
            else:
                # start
                self._running = True
                self.btn.SetLabel("Stop")
                self._beat = 0
                self._thread = threading.Thread(target=self._run_loop, daemon=True)
                self._thread.start()
                
    def _on_note(self, _evt):
        self.note = self.spin.GetValue()
        
    def _on_note2(self, _evt):
        self.note2 = self.spin2.GetValue()
        
    def _on_Vel(self, _evt):
        self.vel = self.Velocity.GetValue()

    def _run_loop(self):
        """
        Runs in background thread: sleeps for the interval derived from BPM,
        then posts a wx.CallAfter to the main thread to print the beat.
        """
        self._running = True
        while self._running:
            with self._lock:
                bpm = self.bpm.GetValue()
            interval = 60.0 / bpm   # seconds per beat
            time.sleep(interval)
            with self._lock:
                # advance beat count
                self._beat = (self._beat % 4) + 1
                beat = self._beat
            # now marshal back to GUI thread to print
            wx.CallAfter(self.play_beat, beat)
        self.main.outport.panic()

    def play_beat(self, beat):
        if beat < 4:
            # print(f"Tick {beat}")
            msg = Message('note_off', note=self.note)
            self.main.outport.send(msg)
            msg = Message('note_on', note=self.note, velocity=self.vel)
            self.main.outport.send(msg)
        else:
            # print("Tick 4 (+1 octave)")
            msg = Message('note_off', note=self.note2)
            self.main.outport.send(msg)
            msg = Message('note_on', note=self.note2, velocity=self.vel)
            self.main.outport.send(msg)
            
