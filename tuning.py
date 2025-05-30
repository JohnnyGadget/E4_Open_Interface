import wx
from custom_widgets import DraggableNumber
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

#====================================================================================================
#====================================================================================================
#====================================================================================================

class Tuning(wx.Panel):
    def __init__(self, parent, main, voice_dict, controls):
        super().__init__(parent)
        # self.SetBackgroundColour()
        self.main = main
        main_sizer = wx.BoxSizer(wx.VERTICAL)


        grid_sizer = wx.GridSizer(rows=4, cols=2, hgap=5, vgap=10)

        label1 = wx.StaticText(self, label="Coarse Tune")
        label2 = DraggableNumber(self, id = 41, value = voice_dict["params"]["E4_GEN_CTUNE"], min_val = -72, max_val = +24, callback = main._onAnyControlChanged)
        controls.dragger_by_id[41] = label2
        
        label3 = wx.StaticText(self, label="Fine Tune")
        label4 = DraggableNumber(self, id = 42, value = voice_dict["params"]["E4_GEN_FTUNE"], min_val = -64, max_val = +64, callback = main._onAnyControlChanged)
        controls.dragger_by_id[42] = label4

        label5 = wx.StaticText(self, label="Key Transpose")
        label6 = DraggableNumber(self, id = 43, value = voice_dict["params"]["E4_GEN_XPOSE"], min_val = -24, max_val = +24, callback = main._onAnyControlChanged)
        controls.dragger_by_id[43] = label6
        
        label7 = wx.StaticText(self, label="Non-Transpose")
        label8 = wx.CheckBox(self, id=57)
        label8.SetValue(voice_dict["params"]["E4_VOICE_NON_TRANSPOSE"])
        label8.Bind(wx.EVT_CHECKBOX, lambda evt: self._on_toggle(evt))
        controls.check_by_id[41] = label8
        
        labels = [
            label7, label8, label5, label6, label1, label2, label3, label4, 
        ]
        

        for label in labels:
            # label.SetBackgroundColour(wx.Colour(176, 186, 160, 127))
            if label == label2 or label == label4 or label == label6 or label == label8:
                label.SetMinSize((60, 20))
                grid_sizer.Add(label,  0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 20)
                label.SetBackgroundColour(wx.Colour(greencontrol)) 
            else:
                label.SetMinSize((120, 20))
                grid_sizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL)
                # label.SetBackgroundColour(wx.Colour(yellow)) 
                
        main_sizer.Add(grid_sizer, flag=wx.ALL, border=10)
        self.SetSizer(main_sizer)
        
    def _on_toggle(self, event):
        checked = bool(event.GetInt())
        self.main.send_parameter_edit(57, checked)
        






def convert_chorus_x_to_ms(val: int) -> str:
    """
    Converts a value in the range -32 to +32 to a delay time in milliseconds
    according to the E4_VOICE_CHORUS_X mapping.
    """
    # Lookup table for absolute values 0 to 32
    delay_lookup = [
        0.000, 0.045, 0.090, 0.136, 0.181, 0.226, 0.272, 0.317,
        0.362, 0.408, 0.453, 0.498, 0.544, 0.589, 0.634, 0.680,
        0.725, 0.770, 0.816, 0.861, 0.907, 0.952, 0.997, 1.043,
        1.088, 1.133, 1.179, 1.224, 1.269, 1.315, 1.360, 1.405, 1.451
    ]
    
    if not (-32 <= val <= 32):
        return "Invalid"

    delay = delay_lookup[abs(val)]
    if val < 0:
        return f"-{delay:.3f}ms"
    elif val > 0:
        return f"+{delay:.3f}ms"
    else:
        return f"+/-{delay:.3f}ms"


def convert_chorus_width_to_percent(val):
    """
    Convert E4_VOICE_CHORUS_WIDTH (range -128 to 0) to a percentage string.

    Example:
        -128 => "0%"
        0    => "100%"
        -64  => "50%"
    """
    pct = ((val + 128) * 100) // 128  # integer division like in C
    return f"{pct}%"






class TuningModifiers(wx.Panel):
    def __init__(self, parent, main, voice_dict, controls):
        super().__init__(parent)
        self.main = main
        # self.SetBackgroundColour()
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        grid_sizer = wx.GridSizer(rows=5, cols=2, hgap=5, vgap=10)

        self.label1 = wx.StaticText(self, label="Chorus Amt %")
        label2 = DraggableNumber(self, id = 58, value = voice_dict["params"]["E4_VOICE_CHORUS_AMOUNT"], min_val = 0, max_val = 100, callback = main._onAnyControlChanged)
        controls.dragger_by_id[58] = label2
        
        self.label3 = wx.StaticText(self, label="Chorus Width")
        self.label4 = DraggableNumber(self, id = 59, value = voice_dict["params"]["E4_VOICE_CHORUS_WIDTH"], min_val = -128, max_val = 0, callback = self.chrwidfunction)
        controls.dragger_by_id[59] = self.label4
        

        self.label5 = wx.StaticText(self, label="Chorus Intial ITD")
        self.label6 = DraggableNumber(self, id = 60, value = voice_dict["params"]["E4_VOICE_CHORUS_X"], min_val = -32, max_val = +32, callback = self.chritdfunction)
        controls.dragger_by_id[60] = self.label6
        
        
        label7 = wx.StaticText(self, label="Delay(0-10000ms)")
        label8 = DraggableNumber(self, id = 61, value = voice_dict["params"]["E4_VOICE_DELAY"], min_val = 0, max_val = 10000, step = 1, callback = main._onAnyControlChanged)
        controls.dragger_by_id[61] = label8
        
        label9 = wx.StaticText(self, label="Start Offset")
        label10 = DraggableNumber(self, id = 62, value = voice_dict["params"]["E4_VOICE_START_OFFSET"], min_val = 0, max_val = 127, callback = main._onAnyControlChanged)
        controls.dragger_by_id[62] = label10


        labels = [
            self.label1, label2, self.label3, self.label4, self.label5, self.label6, label7, label8, label9, label10
        ]
        

        for label in labels:
            if label == label2 or label == self.label4 or label == self.label6 or label == label8 or label == label10:
                label.SetMinSize((80, 20))
                grid_sizer.Add(label,  0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 20)
                label.SetBackgroundColour(wx.Colour(greencontrol)) 
            else:
                label.SetMinSize((120, 20))
                grid_sizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL,20)
                # label.SetBackgroundColour(wx.Colour(yellow)) 

        main_sizer.Add(grid_sizer, flag=wx.ALL, border=10)
        self.SetSizer(main_sizer)
        
    def chrwidfunction(self, evt):
        self.label3.SetLabel(f"Chr Width{convert_chorus_width_to_percent(self.label4.value)}")
        self.main._onAnyControlChanged(evt)
        
    def chritdfunction(self, evt):
        self.label5.SetLabel(f"ITD {convert_chorus_x_to_ms(self.label6.value)}")
        self.main._onAnyControlChanged(evt)    
        








# Lookup tables from EOS manual
envunits1 = [
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 2, 2, 2, 2,
    2, 2, 2, 3, 3, 3, 3, 3,
    4, 4, 4, 4, 5, 5, 5, 5,
    6, 6, 7, 7, 7, 8, 8, 9,
    9, 10, 11, 11, 12, 13, 13, 14,
    15, 16, 17, 18, 19, 20, 22, 23,
    24, 26, 28, 30, 32, 34, 36, 38,
    41, 44, 47, 51, 55, 59, 64, 70,
    76, 83, 91, 100, 112, 125, 142, 163,
]

envunits2 = [
    0, 1, 2, 3, 4, 5, 6, 7,
    8, 9, 10, 11, 12, 13, 14, 15,
    16, 17, 18, 19, 20, 21, 22, 23,
    25, 26, 28, 29, 32, 34, 36, 38,
    41, 43, 46, 49, 52, 55, 58, 62,
    65, 70, 74, 79, 83, 88, 93, 98,
    4, 10, 17, 24, 31, 39, 47, 56,
    65, 74, 84, 95, 6, 18, 31, 44,
    59, 73, 89, 6, 23, 42, 62, 82,
    4, 28, 52, 78, 5, 34, 64, 97,
    32, 67, 6, 46, 90, 35, 83, 34,
    87, 45, 6, 70, 38, 11, 88, 70,
    56, 49, 48, 53, 65, 85, 13, 50,
    97, 54, 24, 6, 2, 15, 44, 93,
    64, 60, 84, 41, 34, 70, 56, 3,
    22, 28, 40, 87, 9, 65, 36, 69,
]


def convert_glide_rate(val: int) -> str:
    """
    Converts E4_VOICE_GLIDE_RATE value (0–127) into seconds per octave for display.
    """
    if not (0 <= val < 128):
        return "Invalid"

    # Formula from EOS manual
    msec = (envunits1[val] * 1000 + envunits2[val] * 10) // 5
    seconds = msec / 1000.0
    return f"{seconds:.3f} sec/oct"


        
solo_modeses = {"Off":0,
                "Multiple Trigger":1,
                "Melody (last)":2,
                "Melody (low)":3,
                "Melody (high)":4,
                "Synth (last)":5,
                "Synth (low)":6,
                "Synth (high)":7,
                "Fingered Glide":8
                }      
 
poly_modes_map = {
    "Poly All":   0,
    "Poly16 A":   1,
    "Poly16 B":   2,
    "Poly 8 A":   3,
    "Poly 8 B":   4,
    "Poly 8 C":   5,
    "Poly 8 D":   6,
    "Poly 4 A":   7,
    "Poly 4 B":   8,
    "Poly 4 C":   9,
    "Poly 4 D":  10,
    "Poly 2 A":  11,
    "Poly 2 B":  12,
    "Poly 2 C":  13,
    "Poly 2 D":  14,
    "Mono A":    15,
    "Mono B":    16,
    "Mono C":    17,
    "Mono D":    18,
    "Mono E":    19,
    "Mono F":    20,
    "Mono G":    21,
    "Mono H":    22,
    "Mono I":    23
} 
        
class TuningSetup(wx.Panel):
    def __init__(self, parent, main, voice_dict, controls):
        super().__init__(parent)
        # self.SetBackgroundColour()
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main = main

        grid_sizer = wx.GridSizer(rows=5, cols=2, hgap=5, vgap=10)

        self.label1 = wx.StaticText(self, label="Glide Rate")
        self.label2 = DraggableNumber(self, id = 63, value = voice_dict["params"]["E4_VOICE_GLIDE_RATE"], min_val = 0, max_val = 127, callback = self.gldrtfunction)
        controls.dragger_by_id[63] = self.label2
        
        label3 = wx.StaticText(self, label="Glide Curve")
        label4 = wx.SpinCtrl(self, id = 64, initial = voice_dict["params"]["E4_VOICE_GLIDE_CURVE"], min = 0, max = 8)
        label4.Bind(wx.EVT_SPINCTRL, lambda evt: self.main._onAnyControlChanged(evt))
        controls.spin_by_id[64] = label4

        label5 = wx.StaticText(self, label="Solo Mode")
        solo_modes = ["Off","Multiple Trigger","Melody (last)","Melody (low)","Melody (high)","Synth (last)","Synth (low)","Synth (high)","Fingered Glide"]
        self.solomode_selector = wx.ComboBox(self, id = 65, choices=solo_modes, style=wx.CB_READONLY,size=(100, -1))
        
        self.solomode_selector.SetSelection(voice_dict["params"]["E4_VOICE_SOLO"])
        self.solomode_selector.Bind(wx.EVT_COMBOBOX, self.solomode_change) 
        controls.combo_by_id[65] = self.solomode_selector
        
        
        poly_modes = [
    "Poly All",
    "Poly16 A",
    "Poly16 B",
    "Poly 8 A",
    "Poly 8 B",
    "Poly 8 C",
    "Poly 8 D",
    "Poly 4 A",
    "Poly 4 B",
    "Poly 4 C",
    "Poly 4 D",
    "Poly 2 A",
    "Poly 2 B",
    "Poly 2 C",
    "Poly 2 D",
    "Mono A",
    "Mono B",
    "Mono C",
    "Mono D",
    "Mono E",
    "Mono F",
    "Mono G",
    "Mono H",
    "Mono I"
]
        label7 = wx.StaticText(self, label="Poly Mode")
        self.polymode_selector = wx.ComboBox(self, id = 66, choices=poly_modes, style=wx.CB_READONLY,size=(100, -1))
        self.polymode_selector.Bind(wx.EVT_COMBOBOX, self.polymode_change) 
        self.polymode_selector.SetSelection(voice_dict["params"]["E4_VOICE_ASSIGN_GROUP"])
        controls.combo_by_id[66] = self.polymode_selector
        
        label9 = wx.StaticText(self, label="Latch Mode")
        label10 = wx.CheckBox(self, id=67)
        label10.SetValue(voice_dict["params"]["E4_VOICE_LATCHMODE"])
        label10.Bind(wx.EVT_CHECKBOX, lambda evt: self._on_toggle(evt))
        controls.check_by_id[67] = label10

        labels = [
            self.label1, self.label2, label3, label4, label5, self.solomode_selector, label7, self.polymode_selector, label9, label10
        ]
        

        for label in labels:
            if label == self.label2 or label == label4 or label == label10:
                label.SetMinSize((80, 20))
                grid_sizer.Add(label,  0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 20)
                label.SetBackgroundColour(wx.Colour(greencontrol)) 
            elif label == self.solomode_selector or label == self.polymode_selector:
                label.SetMinSize((80, 20))
                grid_sizer.Add(label,  0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 20)
                label.SetBackgroundColour(wx.Colour(greencontrol)) 
            else:
                label.SetMinSize((120, 20))
                grid_sizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL)
                # label.SetBackgroundColour(wx.Colour(yellow)) 
            
        main_sizer.Add(grid_sizer, flag=wx.ALL, border=10)
        self.SetSizer(main_sizer)                


    def gldrtfunction(self, evt):
        self.label1.SetLabel(f"Glide Rate {convert_glide_rate(self.label2.value)}")
        self.main._onAnyControlChanged(evt)    

    def solomode_change(self, event):
        selected_value = self.solomode_selector.GetValue()
        # print(selected_value)
        # print(solo_modeses[selected_value])
        self.main.send_parameter_edit(65, solo_modeses[selected_value])
        
    def polymode_change(self, event):
        selected_value = self.polymode_selector.GetValue()
        # print(selected_value)
        # print(poly_modes_map[selected_value])
        self.main.send_parameter_edit(66, poly_modes_map[selected_value])
        
    def _on_toggle(self, event):
        checked = bool(event.GetInt())
        self.main.send_parameter_edit(67, checked)








        
        
        
        
        
        
        
        
        
        
        
# submix_ports = {-1:"voice", 0:"main", 1:"sub1", 2:"sub2", 3:"sub3", 4:"sub4", 5:"sub5", 6:"sub6", 7:"sub7"}
submix_ports = {
    "voice": -1,
    "main":  0,
    "sub1":  1,
    "sub2":  2,
    "sub3":  3,
    "sub4":  4,
    "sub5":  5,
    "sub6":  6,
    "sub7":  7,
}
def convert_submix_to_val(val):
    return submix_ports.get(val, "Invalid")


amp_env_depths_conv= {
    "-96":0, "-93":1, "-90":2, "-87":3, "-84":4, "-81":5, "-78":6, "-75":7, "-72":8, "-69":9, 
    "-66":10, "-63":11, "-60":12, "-57":13, "-54":14, "-51":15, "-48":16}                  
        
        
class Amplifier(wx.Panel):
    def __init__(self, parent, main, voice_dict, controls, v_idx):
        super().__init__(parent)
        
        self.main = main
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        grid_sizer = wx.GridSizer(rows=4, cols=2, hgap=5, vgap=10)


        label1 = wx.StaticText(self, label="Volume")
        label2 = DraggableNumber(self, id = 39, value = voice_dict["params"]["E4_GEN_VOLUME"], min_val = -96, max_val = 10, callback = main._onAnyControlChanged)
        controls.dragger_by_id[39] = label2
        
        self.label3 = wx.StaticText(self, label="Pan (C)")
        self.label4 = DraggableNumber(self, id = 40, value = voice_dict["params"]["E4_GEN_PAN"], min_val = -64, max_val = 63, callback = self.pan_change)
        controls.dragger_by_id[40] = self.label4

        label5 = wx.StaticText(self, label="Amp Env Depth")
        self.amp_env_depths = ["-96", "-93", "-90", "-87", "-84", "-81", "-78", "-75", "-72", "-69", 
        "-66", "-63", "-60", "-57", "-54", "-51", "-48"]
        self.amp_env_depth = wx.ComboBox(self, id = 68, choices=self.amp_env_depths, style=wx.CB_READONLY,size=(100, -1))
        self.amp_env_depth.SetSelection(voice_dict["params"]["E4_VOICE_VOLENV_DEPTH"])
        self.amp_env_depth.Bind(wx.EVT_COMBOBOX, self.ampenvdepth_change)
        controls.combo_by_id[68] = self.amp_env_depth
        
        label7 = wx.StaticText(self, label="Submix")
        submix_ports = ["voice", "main", "sub1", "sub2", "sub3", "sub4", "sub5", "sub6", "sub7"]
        self.submix_selector = wx.ComboBox(self, id = 69, choices=submix_ports, style=wx.CB_READONLY,size=(100, -1))
        self.submix_selector.SetSelection(voice_dict["params"]["E4_VOICE_SUBMIX"])
        # print("self.submix_selector.SetSelection(voice_dict[params][E4_VOICE_SUBMIX])", voice_dict["params"]["E4_VOICE_SUBMIX"])
        self.submix_selector.Bind(wx.EVT_COMBOBOX, self.submix_change)   
        controls.combo_by_id[69] = self.submix_selector
    

        labels = [
            label1, label2, self.label3, self.label4, label5, self.amp_env_depth, label7, self.submix_selector
        ]
        

        for label in labels:
            if label == label2 or label == self.label4 or label == self.amp_env_depth or label == self.submix_selector:
                label.SetMinSize((60, 20))
                grid_sizer.Add(label,  0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 20)
                label.SetBackgroundColour(wx.Colour(greencontrol)) 
            else:
                label.SetMinSize((120, 20))
                grid_sizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL)
                # label.SetBackgroundColour(wx.Colour(yellow)) 
            
        main_sizer.Add(grid_sizer, flag=wx.ALL, border=10)
        self.SetSizer(main_sizer)

    def submix_change(self, event):
        selected_value = self.submix_selector.GetValue()
        # print(selected_value)
        # print(submix_ports[selected_value])
        self.main.send_parameter_edit(69, submix_ports[selected_value])
        
    def ampenvdepth_change(self, event):
        selected_value = self.amp_env_depth.GetValue()
        self.main.send_parameter_edit(68, amp_env_depths_conv[selected_value])
        
    def pan_change(self, event):
        val = self.label4.value
        if val < 0:
            self.label3.Label = f"Pan (L)"
        elif val > 0:

            self.label3.Label = f"Pan (R)"
        else:
            self.label3.Label = f"Pan (C)"
        self.main._onAnyControlChanged(event)



