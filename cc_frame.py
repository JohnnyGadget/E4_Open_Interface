import wx
import wx.lib.scrolledpanel as scrolled
from mido import Message
from custom_widgets import DraggableNumber, EVT_DRAGGABLENUMBER

# CC → label mapping (0–31,64–97)
# CC_LABELS = {
#     0:  "Bank Select",      1:  "Mod Wheel",       2:  "Breath",
#     4:  "Foot Ctrl",        5:  "Portamento Time", 6:  "Data Entry MSB",
#     7:  "Channel Volume",   8:  "Balance",        10: "Pan",
#     11: "Expression",       12: "Effect Ctrl 1",  13: "Effect Ctrl 2",
#     16: "GP Ctrl 1",        17: "GP Ctrl 2",      18: "GP Ctrl 3",
#     19: "GP Ctrl 4",        64: "Sustain",        65: "Portamento",
#     66: "Sostenuto",        67: "Soft Pedal",     68: "Legato",
#     69: "Hold 2",           70: "Sound Ctrl 1",   71: "Sound Ctrl 2",
#     72: "Sound Ctrl 3",     73: "Sound Ctrl 4",   74: "Sound Ctrl 5",
#     75: "Sound Ctrl 6",     76: "Sound Ctrl 7",   77: "Sound Ctrl 8",
#     78: "Sound Ctrl 9",     79: "Sound Ctrl 10",  80: "GP Ctrl 5",
#     81: "GP Ctrl 6",        82: "GP Ctrl 7",      83: "GP Ctrl 8",
#     84: "Portamento Ctrl",  91: "FX1 Depth",      92: "FX2 Depth",
#     93: "FX3 Depth",        94: "FX4 Depth",      95: "FX5 Depth",
#     96: "Data +",           97: "Data -"
# }
CC_LABELS = {
            0:"CC 0"
}
# fill in defaults for everything 0–127
for cc in range(128):
    CC_LABELS.setdefault(cc, f"CC {cc}")


class CCDraggablePanel(scrolled.ScrolledPanel):
    """Scrolled 2-column strip of all 128 CC controllers."""
    def __init__(self, parent, main):
        super().__init__(parent, style=wx.VSCROLL|wx.TAB_TRAVERSAL)
        self.main = main
        self.SetupScrolling(scroll_x=False, scroll_y=True)
        
        self.notes_fields = {} 
        self.cc_ids = list(range(128))
        half   = (len(self.cc_ids) + 1) // 2  # 64 rows each column

        grid = wx.FlexGridSizer(rows=half, cols=2, vgap=8, hgap=20)
        grid.AddGrowableCol(0)
        grid.AddGrowableCol(1)

        left  = self.cc_ids[:half]
        right = self.cc_ids[half:]

        for i in range(half):
            # left cell
            grid.Add(self._make_row(left[i]), 0, wx.EXPAND)

            # right cell (or empty spacer)
            if i < len(right):
                grid.Add(self._make_row(right[i]), 0, wx.EXPAND)
            else:
                grid.Add((0, 0), 0)

        self.SetSizer(grid)
        
        

    def _make_row(self, cc):
        row = wx.BoxSizer(wx.HORIZONTAL)
        lbl = wx.StaticText(self, label=f"{CC_LABELS[cc]}", size=(40, -1))
        dn  = DraggableNumber(self,
                                id      = cc,
                                value   = 0,
                                min_val = 0,
                                max_val = 127,
                                step    = 1,
                                callback= self.on_cc_change)
        dn.SetMinSize((100, -1))
        dn.SetMaxSize((40, -1))
        dn.SetBackgroundColour(wx.Colour(153, 245, 198))
        notes = wx.TextCtrl(self, size=(150, -1))
        self.notes_fields[cc] = notes
        row.Add(lbl, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 8)
        row.Add(dn,  1, wx.EXPAND)
        row.Add((10,0))
        row.Add(notes, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 8)
        return row
    
    

    def on_cc_change(self, evt):
        cc  = evt.GetId()
        val = evt.GetInt()
        msg = Message('control_change', control=cc, value=val)
        self.main.send_midi(msg)
        
    def save_notes(self):
        for cc, notes_ctrl in self.notes_fields.items():
            value = notes_ctrl.GetValue()
            self.main.cfg.Write(f"CCNotes/{cc}", value)
            self.main.cfg.Flush()  # Ensure data is written to file
    
    def restore_cc_notes(self):
        for cc in self.cc_ids:
            val = self.main.cfg.Read(f"CCNotes/{cc}", "")
            if val:
                self.notes_fields[cc].SetValue(val)


class CCframe(wx.Frame):
    def __init__(self, main):
        super().__init__(None, title="CC Controllers", size=(1000,700))
        # open default MIDI out
        self.Bind(wx.EVT_CLOSE, self.on_close)
        panel = wx.Panel(self)
        vs = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(vs)

        
        sc = scrolled.ScrolledPanel(panel, style=wx.TAB_TRAVERSAL|wx.BORDER_SUNKEN)
        sc.SetupScrolling(scroll_x=False, scroll_y=True)
        self.cc = CCDraggablePanel(sc, main)
        sc.SetSizer(wx.BoxSizer(wx.VERTICAL))
        sc.GetSizer().Add(self.cc,1,wx.EXPAND|wx.ALL,5)
        sc.SetMinSize((-1,600))
        vs.Add(sc,0,wx.EXPAND|wx.ALL,5)
        
    def on_close(self, event):
        self.Hide()
