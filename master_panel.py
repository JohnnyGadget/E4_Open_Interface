import wx
from wx.lib.scrolledpanel import ScrolledPanel
from custom_widgets import DraggableNumber, DraggableNumberEvent
greencontrol = (153, 245, 198, 0)
# Master tuning display values for +0 to +64
MASTER_TUNING_TABLE = [
    0.0, 1.2, 3.5, 4.7, 6.0, 7.2, 9.5, 10.7,
    12.0, 14.2, 15.5, 17.7, 18.0, 20.2, 21.5, 23.7,
    25.0, 26.2, 28.5, 29.7, 31.0, 32.2, 34.5, 35.7,
    37.0, 39.2, 40.5, 42.7, 43.0, 45.2, 46.5, 48.7,
    50.0, 51.2, 53.5, 54.7, 56.0, 57.2, 59.5, 60.7,
    62.0, 64.2, 65.5, 67.7, 68.0, 70.2, 71.5, 73.7,
    75.0, 76.2, 78.5, 79.7, 81.0, 82.2, 84.5, 85.7,
    87.0, 89.2, 90.5, 92.7, 93.0, 95.2, 96.5, 98.7, 100.0
]

MASTER_TRANSPOSE_TABLE = [
    "C -12 (Down Oct)", 
    "C# -11", "D -10", "D# -9", "E -8", "F -7", "F# -6", "G -5", "G# -4", "A -3", "A# -2", "B -1",
    "C +/-0 (Unison)",
    "C# +1", "D +2", "D# +3", "E +4", "F +5", "F# +6", "G +7", "G# +8", "A +9", "A# +10", "B +11",
    "C +12 (Up 1 Oct)"
]


def format_master_transpose(val):
    """Convert -12..+12 transpose value into a readable musical label."""
    index = val + 12  # Shift -12..0..+12 to 0..24
    if 0 <= index < len(MASTER_TRANSPOSE_TABLE):
        return MASTER_TRANSPOSE_TABLE[index]
    else:
        return "ERR"




def format_master_tuning(offset):
    """Convert -64..+64 master tuning offset into formatted display string."""
    if offset < 0:
        return f"{offset}"
    elif offset == 0:
        return "+0.0"
    elif offset > 0 and offset < len(MASTER_TUNING_TABLE):
        value = MASTER_TUNING_TABLE[offset]
        return f"+{value:.1f}"
    else:
        return "ERR"  # outside table range

# Example:
# print(format_master_tuning(-64)) -> "-64"
# print(format_master_tuning(0)) -> "+0.0"
# print(format_master_tuning(5)) -> "+7.2"
# print(format_master_tuning(64)) -> "+100.0"

SYSEX_NAMES = {
    183: "MASTER_TUNING_OFFSET",  # Master tuning fine offset (-64 to +64) => +/- 0.0 to 100.0
    184: "MASTER_TRANSPOSE",      # Master transpose (-12 to +12) => C to C

    185: "MASTER_HEADROOM",       # Output headroom (0-15)
    186: "MASTER_HCHIP_BOOST",    # Output boost 0=+0dB, 1=+12dB
    187: "MASTER_OUTPUT_FORMAT",  # Output format 0=analog, 1=AES Pro, 2=S/PDIF
    188: "MASTER_OUTPUT_CLOCK",   # Output clock rate 0=44.1kHz, 1=48kHz
    189: "MASTER_AES_BOOST",      # AES boost 0=off, 1=on

    190: "MASTER_SCSI_ID",        # SCSI ID (0-7)
    191: "MASTER_SCSI_TERM",      # SCSI termination (0=on, 1=off)
    192: "MASTER_USING_MAC",      # Avoid host on SCSI ID (-1=none, 0–7)

    193: "MASTER_COMBINE_LR",     # Combine L/R stereo import (0=on, 1=off)
    194: "MASTER_AKAI_LOOP_ADJ",  # Adjust Akai fractional loops (0=off, 1=on)
    195: "MASTER_AKAI_SAMPLER_ID" # Akai Sampler SCSI ID (-1=none, 0–7)
}

class MasterGlobalPanel(ScrolledPanel):
    def __init__(self, parent, main):
        super().__init__(parent)
        self.SetBackgroundColour("light grey")
        
        self.send_sysex = main.send_sysex   
        self.device_id = main.device_id   
        
        splitter = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # === Master Output ===
        output_box = wx.StaticBox(self, label="Output Settings")
        # output_box.SetBackgroundColour("light grey")
        output_sizer = wx.StaticBoxSizer(output_box, wx.VERTICAL)
        
        self.headroom = DraggableNumber(self, id = 185, value=0, min_val=0, max_val=15, callback=main._onAnyControlChanged)
        self.headroom.SetMinSize((80,20))
        self.headroom.SetMaxSize((80,20))
        output_sizer.Add(self._labeled("Headroom 0-15", self.headroom), 0, wx.EXPAND | wx.ALL, 5)
        self.headroom.SetBackgroundColour(wx.Colour(greencontrol))
        main.controls.dragger_by_id[185] = self.headroom
        
        self.hchip_boost = wx.RadioBox(self, id = 186, label="Output Boost", choices=["+0dB", "+12dB"], style=wx.RA_HORIZONTAL)
        output_sizer.Add(self.hchip_boost, 0, wx.EXPAND | wx.ALL, 5)
        self.hchip_boost.Bind(wx.EVT_RADIOBOX, self.onRadio)
        main.controls.radio_by_id[186] = self.hchip_boost

        self.output_format = wx.RadioBox(self, id = 187, label="Output Format", choices=["Analog", "AES Pro", "S/PDIF"])
        output_sizer.Add(self.output_format, 0, wx.EXPAND | wx.ALL, 5)
        self.output_format.Bind(wx.EVT_RADIOBOX, self.onRadio)
        main.controls.radio_by_id[187] = self.output_format

        self.output_clock = wx.RadioBox(self, id = 188, label="Output Clock", choices=["44.1kHz", "48kHz"], style=wx.RA_HORIZONTAL)
        output_sizer.Add(self.output_clock, 0, wx.EXPAND | wx.ALL, 5)
        self.output_clock.Bind(wx.EVT_RADIOBOX, self.onRadio)
        main.controls.radio_by_id[188] = self.output_clock

        self.aes_boost = wx.RadioBox(self, id = 189, label="AES Boost", choices=["Off", "On"], style=wx.RA_HORIZONTAL)
        output_sizer.Add(self.aes_boost, 0, wx.EXPAND | wx.ALL, 5)
        self.aes_boost.Bind(wx.EVT_RADIOBOX, self.onRadio)
        main.controls.radio_by_id[189] = self.aes_boost

        main_sizer.Add(output_sizer, 0, wx.EXPAND | wx.ALL, 10)
        
       
        
        
        
        # === Master Tuning ===
        tuning_box = wx.StaticBox(self, label="Master Tuning")
        tuning_sizer = wx.StaticBoxSizer(tuning_box, wx.VERTICAL)
        
 
        self.tuning_offset = wx.SpinCtrl(self, id = 183, min=-64, max=64, initial=0)
        readout_label = wx.StaticText(self, label="Tuning Offset: +0.0")
        main.controls.spin_by_id[183] = self.tuning_offset
        
        def on_tuning_changed(evt):
            val = self.tuning_offset.GetValue()
            readout_label.SetLabel(f"Tuning Offset: +{format_master_tuning(val)}")
            main._onAnyControlChanged(evt)

        self.tuning_offset.Bind(wx.EVT_SPINCTRL, on_tuning_changed)
        tuning_sizer.Add(readout_label, 0, wx.EXPAND | wx.ALL, 5)
        tuning_sizer.Add(self._labeled("Tuning Offset", self.tuning_offset), 0, wx.EXPAND | wx.ALL, 5)
 
        
        self.transpose_spin = wx.SpinCtrl(self, id = 184, min=-12, max=12, initial=0)
        self.transpose_label = wx.StaticText(self, label="(off) C 0 (Unison)")
        main.controls.spin_by_id[184] = self.transpose_spin

        def on_transpose_changed(evt):
            val = self.transpose_spin.GetValue()
            self.transpose_label.SetLabel(f"Master Transpose: {format_master_transpose(val)}")
            main._onAnyControlChanged(evt)

        self.transpose_spin.Bind(wx.EVT_SPINCTRL, on_transpose_changed)
        tuning_sizer.Add(self.transpose_label, 0, wx.EXPAND | wx.ALL, 5)
        tuning_sizer.Add(self._labeled("Master Transpose", self.transpose_spin), 0, wx.EXPAND | wx.ALL, 5)
        

        main_sizer.Add(tuning_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # === SCSI/Host Settings ===
        scsi_box = wx.StaticBox(self, label="SCSI/Host Settings")
        scsi_sizer = wx.StaticBoxSizer(scsi_box, wx.VERTICAL)

        self.scsi_id = wx.SpinCtrl(self, id = 190, min=0, max=7, initial=0)
        scsi_sizer.Add(self._labeled("SCSI ID", self.scsi_id), 0, wx.EXPAND | wx.ALL, 5)
        self.scsi_id.Bind(wx.EVT_SPINCTRL, main._onAnyControlChanged)
        main.controls.spin_by_id[190] = self.scsi_id

        self.scsi_term = wx.RadioBox(self, id = 191, label="SCSI Termination", choices=["On", "Off"], style=wx.RA_HORIZONTAL)
        scsi_sizer.Add(self.scsi_term, 0, wx.EXPAND | wx.ALL, 5)
        self.scsi_term.Bind(wx.EVT_RADIOBOX, self.onRadio)
        main.controls.radio_by_id[191] = self.scsi_term

        self.mac_host = wx.SpinCtrl(self, id = 192, min=-1, max=7, initial=-1)
        scsi_sizer.Add(self._labeled("Avoid Host ID", self.mac_host), 0, wx.EXPAND | wx.ALL, 5)
        self.mac_host.Bind(wx.EVT_SPINCTRL, main._onAnyControlChanged)
        main.controls.spin_by_id[192] = self.mac_host

        main_sizer.Add(scsi_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # === Import Settings ===
        import_box = wx.StaticBox(self, label="Import Settings")
        import_sizer = wx.StaticBoxSizer(import_box, wx.VERTICAL)

        self.combine_lr = wx.RadioBox(self, id = 193, label="Combine L/R", choices=["On", "Off"], style=wx.RA_HORIZONTAL)
        import_sizer.Add(self.combine_lr, 0, wx.EXPAND | wx.ALL, 5)
        self.combine_lr.Bind(wx.EVT_RADIOBOX, self.onRadio)
        main.controls.radio_by_id[193] = self.combine_lr

        self.akai_loop_adj = wx.RadioBox(self, id = 194, label="Akai Loop Adjust", choices=["Off", "On"], style=wx.RA_HORIZONTAL)
        import_sizer.Add(self.akai_loop_adj, 0, wx.EXPAND | wx.ALL, 5)
        self.akai_loop_adj.Bind(wx.EVT_RADIOBOX, self.onRadio)
        main.controls.radio_by_id[194] = self.akai_loop_adj

        self.akai_sampler_id = wx.SpinCtrl(self, id = 195, min=-1, max=7, initial=-1)
        import_sizer.Add(self._labeled("Akai SCSI ID", self.akai_sampler_id), 0, wx.EXPAND | wx.ALL, 5)
        self.akai_sampler_id.Bind(wx.EVT_SPINCTRL, main._onAnyControlChanged)
        main.controls.spin_by_id[195] = self.akai_sampler_id

        main_sizer.Add(import_sizer, 0, wx.EXPAND | wx.ALL, 10)
        sidesizer = wx.BoxSizer(wx.VERTICAL)
        splitter.Add(main_sizer, 0, wx.EXPAND | wx.ALL, 10)
        splitter.Add(sidesizer, 0, wx.EXPAND | wx.ALL, 10)
       
        dummy = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(dummy)
        dummy.Add(splitter, 0, wx.EXPAND | wx.ALL, 10)
        self.SetVirtualSize((1600, 1100))
        self.SetScrollRate(20, 20)
        self.SetupScrolling(scroll_x=True, scroll_y=True, scrollToTop=False)


    def _labeled(self, text, ctrl):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(wx.StaticText(self, label=text), 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 8)
        sizer.Add(ctrl, 1)
        return sizer
    
    def onRadio(self, event):
        idx = event.GetSelection()
        ctrl = event.GetEventObject()
        print(idx)
        # print(MAGIC_PRESET_CONV[selected_value])
        # self.main.send_parameter_edit(222, MAGIC_PRESET_CONV[selected_value])

   
        
    