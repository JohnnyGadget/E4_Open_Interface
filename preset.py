import wx
import wx.lib.scrolledpanel as scrolled
from custom_widgets import DraggableNumber, EVT_DRAGGABLENUMBER
# ---------------------------------------------------------------------------
# logical parameter IDs (not used as actual wx IDs)
# ---------------------------------------------------------------------------

greencontrol = (153, 245, 198, 0)

E4_PRESET_NUMBER    = 0
E4_PRESET_NAME      = 1
E4_PRESET_TRANSPOSE = 0
E4_PRESET_VOLUME    = 1
E4_PRESET_CTRL_A    = 2
E4_PRESET_CTRL_B    = 3
E4_PRESET_CTRL_C    = 4
E4_PRESET_CTRL_D    = 5

E4_PRESET_FX_A_ALGORITHM = 6
E4_PRESET_FX_A_PARM_0 = 7
E4_PRESET_FX_A_PARM_1 = 8
E4_PRESET_FX_A_PARM_2 = 9
E4_PRESET_FX_A_AMT_0 = 10
E4_PRESET_FX_A_AMT_1 = 11
E4_PRESET_FX_A_AMT_2 = 12
E4_PRESET_FX_A_AMT_3 = 13

E4_PRESET_FX_B_ALGORITHM = 14
E4_PRESET_FX_B_PARM_0 = 15
E4_PRESET_FX_B_PARM_1 = 16
E4_PRESET_FX_B_PARM_2 = 17
E4_PRESET_FX_B_AMT_0 = 18
E4_PRESET_FX_B_AMT_1 = 19
E4_PRESET_FX_B_AMT_2 = 20
E4_PRESET_FX_B_AMT_3 = 21


PRESET_TRANSPOSE_TABLE = {
    -24: "C -24 (-2 Oct)",
    -23: "C# -23",
    -22: "D -22",
    -21: "D# -21",
    -20: "E -20",
    -19: "F -19",
    -18: "F# -18",
    -17: "G -17",
    -16: "G# -16",
    -15: "A -15",
    -14: "A# -14",
    -13: "B -13",
    -12: "C -12 (-1 Oct)",
    -11: "C# -11",
    -10: "D -10",
     -9: "D# -9",
     -8: "E -8",
     -7: "F -7",
     -6: "F# -6",
     -5: "G -5",
     -4: "G# -4",
     -3: "A -3",
     -2: "A# -2",
     -1: "B -1",
      0: "C +/-0 (Unison)",
      1: "C# +1",
      2: "D +2",
      3: "D# +3",
      4: "E +4",
      5: "F +5",
      6: "F# +6",
      7: "G +7",
      8: "G# +8",
      9: "A +9",
     10: "A# +10",
     11: "B +11",
     12: "C +12 (+1 Oct)",
     13: "C# +13",
     14: "D +14",
     15: "D# +15",
     16: "E +16",
     17: "F +17",
     18: "F# +18",
     19: "G +19",
     20: "G# +20",
     21: "A +21",
     22: "A# +22",
     23: "B +23",
     24: "C +24 (+2 Oct)",
}






def make_bold(ctrl):
    f = ctrl.GetFont()
    f.SetWeight(wx.FONTWEIGHT_BOLD)
    ctrl.SetFont(f)


# PresetPanel

class InitCtrlrs(wx.Panel):
    def __init__(self, parent, main):
        super().__init__(parent)
        # self.SetBackgroundColour()
        self.main = main
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        grid_sizer = wx.GridSizer(rows=8, cols=2, hgap=5, vgap=10)

        label1 = wx.StaticText(self, label="Initial Controller A")
        self.E4_PRESET_CTRL_A = DraggableNumber(self, id = 2, value = -1, min_val = -1, max_val = 100, callback = main._onAnyControlChanged)
        lblfill1 = wx.StaticText(self)
        
        label3 = wx.StaticText(self, label="Initial Controller B")
        self.E4_PRESET_CTRL_B = DraggableNumber(self, id = 3, value = -1, min_val = -1, max_val = 100, callback = main._onAnyControlChanged)
        lblfill2 = wx.StaticText(self)

        label5 = wx.StaticText(self, label="Initial Controller C")
        self.E4_PRESET_CTRL_C = DraggableNumber(self, id = 4, value = -1, min_val = -1, max_val = 100, callback = main._onAnyControlChanged)
        lblfill3 = wx.StaticText(self)
        
        label7 = wx.StaticText(self, label="Initial Controller D")
        self.E4_PRESET_CTRL_D = DraggableNumber(self, id = 5, value = -1, min_val = -1, max_val = 100, callback = main._onAnyControlChanged)
        lblfill4 = wx.StaticText(self)
        
        lblfill5 = wx.StaticText(self)
        lblfill6 = wx.StaticText(self)
        lblfill7 = wx.StaticText(self)
        lblfill8 = wx.StaticText(self)


        labels = [
            label1, self.E4_PRESET_CTRL_A, lblfill1, lblfill5, label3, self.E4_PRESET_CTRL_B, lblfill2, lblfill6, label5, self.E4_PRESET_CTRL_C, lblfill3, lblfill7, label7, self.E4_PRESET_CTRL_D, lblfill4, lblfill8
            
        ]
        


        for label in labels:
            # label.SetBackgroundColour(wx.Colour(176, 186, 160, 127))
            label.SetBackgroundColour("light grey")
            grid_sizer.Add(label, flag=wx.Left|wx.TOP|wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL, border=5)
            if isinstance(label, DraggableNumber):
                main.controls.dragger_by_id[label.Id] = label
            
        seg0 = [
            label1,  label3, label5, label7
        ]
        for label in seg0:
            
            label.SetMinSize((120, 20))
        

        seg1 = [self.E4_PRESET_CTRL_A, self.E4_PRESET_CTRL_B, self.E4_PRESET_CTRL_C, self.E4_PRESET_CTRL_D] 
        
        for label in seg1:
            label.SetBackgroundColour(wx.Colour(greencontrol)) 
            label.SetMinSize((80, 20))
                
        main_sizer.Add(grid_sizer, flag=wx.ALL, border=10)
        self.SetSizer(main_sizer)

        
            
        
        
        













class Preset_Basic(wx.Panel):
    def __init__(self, parent, main):
        super().__init__(parent)
        # self.SetBackgroundColour()
        self.main = main
        main_sizer = wx.BoxSizer(wx.VERTICAL)


        grid_sizer = wx.GridSizer(rows=8, cols=2, hgap=10, vgap=10)

        label1 = wx.StaticText(self, label="Current Preset")
        self.E4_PRESET_NUMBER =  wx.StaticText(self, label = str(0), style=wx.TE_PROCESS_ENTER | wx.TE_CENTRE)
        char_width = wx.ScreenDC().GetTextExtent('W')[0]
        self.E4_PRESET_NUMBER.SetMinSize((char_width * 3, -1))
        self.E4_PRESET_NUMBER.SetMaxSize((char_width * 3, -1))
        self.E4_PRESET_NUMBER.Bind(wx.EVT_TEXT_ENTER, self._onPresetNumberCommit)
        
        label3 = wx.StaticText(self, label="Preset Name")
        self.E4_PRESET_NAME = wx.TextCtrl(self, id = 5, style=wx.TE_PROCESS_ENTER)
        self.E4_PRESET_NAME.SetMaxLength(16)
        self.E4_PRESET_NAME.SetMinSize((char_width * 16, -1))
        self.E4_PRESET_NAME.SetMaxSize((char_width * 16, -1))
        self.E4_PRESET_NAME.Bind(wx.EVT_TEXT_ENTER, self.change_preset_name)
        main.controls.entry_by_id[E4_PRESET_NAME] = self.E4_PRESET_NAME
        
        label5 = wx.StaticText(self, label="Volume dB")
        self.E4_PRESET_VOLUME = DraggableNumber(self, id=1, value=0, min_val=-96, max_val=+10, callback = main._onAnyControlChanged)
        self.E4_PRESET_VOLUME.SetMinSize((80, -1))
        self.E4_PRESET_VOLUME.SetMaxSize((80, -1))
        self.E4_PRESET_VOLUME.SetBackgroundColour(greencontrol)
        main.controls.dragger_by_id[E4_PRESET_VOLUME] = self.E4_PRESET_VOLUME
        
        transposelabel = wx.StaticText(self, label="Transpose C +/-0 (Unison)")
        transpose_spin = wx.SpinCtrl(self, id=0, min=-24, max=24, initial=0)

        def on_transpose_changed(evt):
            val = transpose_spin.GetValue()
            transposelabel.SetLabel(f"Transpose {PRESET_TRANSPOSE_TABLE[val]}")
            main.send_parameter_edit(transpose_spin.Id, val)

        transpose_spin.Bind(wx.EVT_SPINCTRL, on_transpose_changed)
        main.controls.spin_by_id[E4_PRESET_TRANSPOSE] = transpose_spin
        lblfill5 = wx.StaticText(self)
        lblfill6 = wx.StaticText(self)
        lblfill7 = wx.StaticText(self)
        lblfill8 = wx.StaticText(self)
        lblfill9 = wx.StaticText(self)
        lblfill10 = wx.StaticText(self)

        labels2 = [
                label1, self.E4_PRESET_NUMBER, lblfill5, lblfill6, label3, self.E4_PRESET_NAME, lblfill7, lblfill8, label5, self.E4_PRESET_VOLUME, lblfill9, lblfill10, transposelabel,
                transpose_spin,
        ]
        for label in labels2:
            grid_sizer.Add(label, wx.ALIGN_CENTER_VERTICAL, border=5)
            label.SetBackgroundColour("light grey")
            if not self.E4_PRESET_NUMBER or not self.E4_PRESET_NAME:
                if label == label1 or label == label3 or label == label5 or label == transposelabel:
                    label.SetMinSize((120, 20))
                else:
                    label.SetMinSize((80, 60))
                    
            
            
        seg11 = [
                    self.E4_PRESET_NAME, self.E4_PRESET_VOLUME, transpose_spin
        ]
        for label in seg11:
            label.SetBackgroundColour(wx.Colour(greencontrol)) 
                
        main_sizer.Add(grid_sizer, flag=wx.ALL, border=10)
        self.SetSizer(main_sizer)
        
        
    def change_preset_name(self, name: str):
        """
        Command 05h: overwrite the 16‑byte preset name on the E4.
        """
        # 1) pad or truncate to exactly 16 chars
        
        raw_name = self.E4_PRESET_NAME.GetValue()
        name = raw_name.ljust(16)[:16]

        # 2) turn into 7‑bit ASCII bytes
        name_bytes = [ord(c) & 0x7F for c in name]

        # 3) split the preset number (an int!) into two 7‑bit bytes
        num = int(self.E4_PRESET_NUMBER.GetValue()) or 0
        lsb = num & 0x7F
        msb = (num >> 7) & 0x7F

        # 4) build the payload: manufacturer, device, family, cmd, preset#, name…
        data = [
            0x18,         # Emu SysEx manuf. ID byte 1
            0x21,         #                    ID byte 2
            self.main.device_id,
            0x55,         # E4 family ID
            0x05,         # “Preset Name” command
            lsb, msb,     # which preset to rename
        ] + name_bytes

        # Send it off!
        self.main.send_sysex(data)
        
#======================================================================================================================
#======================================================================================================================
#======================================================================================================================  
    def _onPresetNameCommit(self, evt):
        txt = self.E4_PRESET_NAME.GetValue()
        self.E4_PRESET_NAME.SetValue(txt)
        self.change_preset_name()
        evt.Skip()
#======================================================================================================================
#======================================================================================================================
#======================================================================================================================  
    def _onPresetNumberCommit(self, evt):
        txt = self.E4_PRESET_NUMBER.GetValue()
        try:
            n = int(txt)
        except ValueError:
            n = 0
        # clamp
        n = max(0, min(999, n))
        
        self.main.seen_params = set()
        
        self.main.send_parameter_edit(223, n)
        
        self.main.get_preset()
        evt.Skip()













        
        
        
        
# ---------------------------------------------------------------------------
class PresetPanel(scrolled.ScrolledPanel):
    def __init__(self, parent, main):
        super().__init__(parent)
        self.SetBackgroundColour("dark grey")
        pad = 20
        self.preset_data = []
        self.device_id = main.device_id
        self.main = main
        self.send_sysex = main.send_sysex


        
        self.preset_panel = wx.Panel(self, size=(400, 180), pos=(pad, pad))
        self.preset_panel.SetBackgroundColour("light grey")
        box2 = wx.StaticBox(self.preset_panel, label="Preset Settings")
        preset_sizer = wx.StaticBoxSizer(box2, wx.VERTICAL)
        # === Inner content ===
        self.preset = Preset_Basic(self.preset_panel, main=main)

        # === Sizer setup ===
        preset_sizer.Add(self.preset, 1, wx.EXPAND | wx.ALL, 10)
        self.preset_panel.SetSizer(preset_sizer)

        # Ensure layout happens
        self.preset_panel.Layout()    
        
        
        
        

        self.initctrlrs_panel = wx.Panel(self, size=(400, 180), pos=(pad , 180 + pad + pad))
        self.initctrlrs_panel.SetBackgroundColour("light grey")
        box2 = wx.StaticBox(self.initctrlrs_panel, label="Initial Controllers")
        initctrlrs_sizer = wx.StaticBoxSizer(box2, wx.VERTICAL)
        # === Inner content ===
        self.init_ctrlrs = InitCtrlrs(self.initctrlrs_panel, main=main)

        # === Sizer setup ===
        initctrlrs_sizer.Add(self.init_ctrlrs, 1, wx.EXPAND | wx.ALL, 10)
        self.initctrlrs_panel.SetSizer(initctrlrs_sizer)

        # Ensure layout happens
        self.initctrlrs_panel.Layout()

        
        dummy = wx.BoxSizer(wx.VERTICAL)
        dummy.AddSpacer(1100)   # height
        self.SetSizer(dummy)
        self.SetVirtualSize((1600, 1100))
        self.SetScrollRate(20, 20)
        self.SetupScrolling(scroll_x=True, scroll_y=True, scrollToTop=False)



#======================================================================================================================
#======================================================================================================================
#======================================================================================================================  
