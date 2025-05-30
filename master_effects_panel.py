import wx
import wx.lib.scrolledpanel as scrolled
from multimode_panel import MultiModeControlPanel
from custom_widgets import DraggableNumber, EVT_DRAGGABLENUMBER

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

MASTER_FX_PARAMS = {
    228: {"name": "MASTER_FX_A_ALGORITHM", "min": 0, "max": 44, "default": 14},
    229: {"name": "MASTER_FX_A_PARM_0",     "min": 0, "max": 90,  "default": 54},
    230: {"name": "MASTER_FX_A_PARM_1",     "min": 0, "max": 127, "default": 64},
    231: {"name": "MASTER_FX_A_PARM_2",     "min": 0, "max": 127, "default": 0},
    232: {"name": "MASTER_FX_A_AMT_0",      "min": 0, "max": 100, "default": 10},
    233: {"name": "MASTER_FX_A_AMT_1",      "min": 0, "max": 100, "default": 20},
    234: {"name": "MASTER_FX_A_AMT_2",      "min": 0, "max": 100, "default": 30},
    235: {"name": "MASTER_FX_A_AMT_3",      "min": 0, "max": 100, "default": 40},

    236: {"name": "MASTER_FX_B_ALGORITHM",  "min": 0, "max": 27,  "default": 1},
    237: {"name": "MASTER_FX_B_PARM_0",     "min": 0, "max": 127, "default": 0},
    238: {"name": "MASTER_FX_B_PARM_1",     "min": 0, "max": 127, "default": 3},
    239: {"name": "MASTER_FX_B_PARM_2",     "min": 0, "max": 127, "default": 0},
    240: {"name": "MASTER_FX_B_AMT_0",       "min": 0, "max": 100, "default": 10},
    241: {"name": "MASTER_FX_B_AMT_1",       "min": 0, "max": 100, "default": 15},
    242: {"name": "MASTER_FX_B_AMT_2",       "min": 0, "max": 100, "default": 30},
    243: {"name": "MASTER_FX_B_AMT_3",       "min": 0, "max": 100, "default": 0},

    244: {"name": "MASTER_FX_BYPASS",        "min": 0, "max": 1,   "default": 0},
    245: {"name": "MASTER_FX_MM_CTRL_CHANNEL", "min": -1, "max": 15, "default": -1},
}

# Master Effects Parameter IDs
MASTER_FX_A_ALGORITHM = 228
MASTER_FX_A_PARM_0    = 229
MASTER_FX_A_PARM_1    = 230
MASTER_FX_A_PARM_2    = 231
MASTER_FX_A_AMT_0     = 232
MASTER_FX_A_AMT_1     = 233
MASTER_FX_A_AMT_2     = 234
MASTER_FX_A_AMT_3     = 235
MASTER_FX_B_ALGORITHM = 236
MASTER_FX_B_PARM_0    = 237
MASTER_FX_B_PARM_1    = 238
MASTER_FX_B_PARM_2    = 239
MASTER_FX_B_AMT_0     = 240
MASTER_FX_B_AMT_1     = 241
MASTER_FX_B_AMT_2     = 242
MASTER_FX_B_AMT_3     = 243

MASTER_FX_BYPASS      = 244
MASTER_FX_MM_CTRL_CHANNEL = 245

MULTIMODE_CHANNEL = 246 #(76h,01h) min = 1; max = 16(32); default = 1;
MULTIMODE_PRESET = 247 #(77h,01h) min = -1; max = 999(1255); default = -1;
MULTIMODE_VOLUME = 248 #(78h,01h) min = 0; max = 127; default = 127;
MULTIMODE_PAN = 249 #(79h,01h) min = -64; max = +63; default = 0;
MULTIMODE_SUBMIX = 250 #(7Ah,01h) min = -1; max = 3(7); default = -1;



    
def get_value_from_label(self, selected_label):
    """
    Given a selected label string, look up its associated value
    from the options list.
    Returns the value if found, otherwise None.
    """
    for label, value in self.options:
        if label == selected_label and value is not None:
            return value
    return None



def make_bold(ctrl):
    f = ctrl.GetFont()
    f.SetWeight(wx.FONTWEIGHT_BOLD)
    ctrl.SetFont(f)



# ---------------------------------------------------------------------------==============================
# ---------------------------------------------------------------------------=============================
# ---------------------------------------------------------------------------=================================





class MasterFXAListBox(wx.Panel):
    def __init__(self, parent, main):
        super().__init__(parent)
        self.main = main
        self.parent = parent
        self.options = [
            ("Master Effects A", None),
        ("Room 1", 0),
        ("Room 2", 1),
        ("Room 3", 2),
        ("Hall 1", 3),
        ("Hall 2", 4),
        ("Plate", 5),
        ("Delay", 6),
        ("Panning Delay", 7),
        ("Multitap 1", 8),
        ("Multitap Pan", 9),
        ("3 Tap", 10),
        ("3 Tap Pan", 11),
        ("Soft Room", 12),
        ("Warm Room", 13),
        ("Perfect Room", 14),
        ("Tiled Room", 15),
        ("Hard Plate", 16),
        ("Warm Hall", 17),
        ("Spacious Hall", 18),
        ("Bright Hall", 19),
        ("Brt Hall Pan", 20),
        ("Bright Plate", 21),
        ("BBall Court", 22),
        ("Gymnasium", 23),
        ("Cavern", 24),
        ("Concert 9", 25),
        ("Concert 10 Pan", 26),
        ("Reverse Gate", 27),
        ("Gate 2", 28),
        ("Gate Pan", 29),
        ("Concert 11", 30),
        ("Medium Concert", 31),
        ("Large Concert", 32),
        ("Lg Concert Pan", 33),
        ("Canyon", 34),
        ("DelayVerb 1", 35),
        ("DelayVerb 2", 36),
        ("DelayVerb 3", 37),
        ("DelayVerb 4 Pan", 38),
        ("DelayVerb 5 Pan", 39),
        ("DelayVerb 6", 40),
        ("DelayVerb 7", 41),
        ("DelayVerb 8", 42),
        ("DelayVerb 9", 43),
    ]


        # Build only the *real selectable* labels (no "---" headers)
        self.selectable_items = [(label, value) for label, value in self.options if value is not None]
        labels = [label for label, _ in self.selectable_items]

        # Create the ListBox
        self.listbox = wx.ListBox(self, id = 228, choices=labels, style=wx.LB_SINGLE)
        main.controls.listbox_by_id[228] = self.listbox
        self.listbox.SetSelection(0)
        self.listbox.SetMinSize((150, -1))
        self.listbox.SetMaxSize((150, -1))

        self.listbox.Bind(wx.EVT_LISTBOX, self.on_select)
        # controls.listbox_by_id[228] = self.listbox
        # Layout
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.listbox, 1, wx.EXPAND | wx.ALL, 5)
        
        
        self.SetSizer(sizer)

    def on_select(self, event):
        idx = self.listbox.GetSelection()
        print("effect a  : ", self.options[idx])
        
        # selected_label = self.listbox.GetString(idx)

        # param_value = self.options[selected_label]

        if idx is not None:
            idx = idx + 1
            self.main.send_parameter_edit(228, idx)
            self.parent.update_ctrls()

            
    

class MasterEffectASection(wx.Panel):
    def __init__(self, parent, main):
        super().__init__(parent)
        self.SetBackgroundColour("light grey")
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # === Effect A Static Box ===
        effect_a_box = wx.StaticBox(self, label="Master Effect A")
        bold_font = effect_a_box.GetFont().Bold()
        effect_a_box.SetFont(bold_font)
        effect_a_sizer = wx.StaticBoxSizer(effect_a_box, wx.VERTICAL)

        # --- 1) Effect Type Dropdown ---
        type_row = wx.BoxSizer(wx.HORIZONTAL)
        type_row.Add(wx.StaticText(self, label="Effect Type"), 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 8)
        self.fx_a_algorithm = MasterFXAListBox(self, main)
        type_row.Add(self.fx_a_algorithm, 1, wx.EXPAND)
        effect_a_sizer.Add(type_row, 0, wx.EXPAND | wx.ALL, 5)

        

        # --- 2) Parameters Section ---
        grid_sizer = wx.GridSizer(rows=3, cols=2, hgap=10, vgap=10)

        
        label1 = wx.StaticText(self, label="Decay Time")
        label2 = DraggableNumber(self, id = 229, value = 0, min_val = 0, max_val = 90, callback = main._onAnyControlChanged)

        label3 = wx.StaticText(self, label="HF Damping")
        label4 = DraggableNumber(self, id = 230, value = 0, min_val = 0, max_val = 127, callback = main._onAnyControlChanged)
        
        label5 = wx.StaticText(self, label="FxB → FxA Mix")
        label6 = DraggableNumber(self, id = 231, value = 0, min_val = 0, max_val = 127, callback =  main._onAnyControlChanged)
        
        labels = [
            label1, label2, label3, label4, label5, label6
        ]
        

        for label in labels:
            label.SetMinSize((80, 20))
            grid_sizer.Add(label, flag=wx.Left|wx.TOP|wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL, border=5)
            
        seg1 = [
            label2, label4, label6
        ]
        for label in seg1:
            main.controls.dragger_by_id[label.Id] = label
            label.SetBackgroundColour(wx.Colour(greencontrol)) 
        

        # --- 3) Sends Section ---
        send_sizer = wx.GridSizer(rows=5, cols=2, hgap=10, vgap=10)

        label11 = wx.StaticText(self, label="Main Send")
        label12 = DraggableNumber(self, id = 232, value = 0, min_val = 0, max_val = 100, callback =  main._onAnyControlChanged)

        label13 = wx.StaticText(self, label="Sub1 Send")
        label14 = DraggableNumber(self, id = 233, value = 0, min_val = 0, max_val = 100, callback =  main._onAnyControlChanged)
        
        label15 = wx.StaticText(self, label="Sub2 Send")
        label16 = DraggableNumber(self, id = 234, value = 0, min_val = 0, max_val = 100, callback =  main._onAnyControlChanged)
        
        label17 = wx.StaticText(self, label="Sub3 Send")
        label18 = DraggableNumber(self, id = 235, value = 0, min_val = 0, max_val = 100, callback =  main._onAnyControlChanged)

        spacer1 = wx.StaticText(self, label="")
        spacer2 = wx.StaticText(self, label="")
        labels2 = [
            spacer2, spacer1, label11, label12, label13, label14, label15, label16, label17, label18
        ]
        

        for label in labels2:
            label.SetMinSize((80, 20))
            send_sizer.Add(label, flag=wx.Left|wx.TOP|wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL, border=5)
            
        seg11 = [
            label12, label14, label16, label18
        ]
        for label in seg11:
            main.controls.dragger_by_id[label.Id] = label
            label.SetBackgroundColour(wx.Colour(greencontrol)) 

        effect_a_sizer.Add(grid_sizer, 0, wx.EXPAND | wx.ALL, 5)
        effect_a_sizer.Add(send_sizer, 0, wx.EXPAND | wx.ALL, 5)

        main_sizer.Add(effect_a_sizer, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(main_sizer)
        
    def update_ctrls(self):
        self.main.send_parameter_request(229)
        self.main.send_parameter_request(230)
        self.main.send_parameter_request(231)
        self.main.send_parameter_request(232)
        self.main.send_parameter_request(233)
        self.main.send_parameter_request(234)
        self.main.send_parameter_request(235)
        
   

#==================================================================================================================
#==================================================================================================================
#==================================================================================================================

class MasterFXBListBox(wx.Panel):
    def __init__(self, parent, main):
        super().__init__(parent)
        self.main = main
        self.parent = parent
        self.options = [
        ("Master Effects B", None),
        
        ("Chorus 1", 1),
        ("Chorus 2", 2),
        ("Chorus 3", 3),
        ("Chorus 4", 4),
        ("Chorus 5", 5),
        ("Doubling", 6),
        ("Slapback", 7),
        ("Flange 1", 8),
        ("Flange 2", 9),
        ("Flange 3", 10),
        ("Flange 4", 11),
        ("Flange 5", 12),
        ("Flange 6", 13),
        ("Flange 7", 14),
        ("Big Chorus", 15),
        ("Symphonic", 16),
        ("Ensemble", 17),
        ("Delay", 18),
        ("Delay Stereo", 19),
        ("Delay Stereo 2", 20),
        ("Panning Delay", 21),
        ("Delay Chorus", 22),
        ("Pan Dly Chrs 1", 23),
        ("Pan Dly Chrs 2", 24),
        ("DualTap 1/3", 25),
        ("DualTap 1/4", 26),
        ("Vibrato", 27),
        ("Distortion 1", 28),
        ("Distortion 2", 29),
        ("Distorted Flange", 30),
        ("Distorted Chorus", 31),
        ("Distorted Double", 32),
    ]


        # Build only selectable items (skip section headers)
        self.selectable_items = [(label, value) for label, value in self.options if value is not None]
        labels = [label for label, _ in self.selectable_items]

        # Create ListBox
        self.listbox = wx.ListBox(self, id = 236, choices=labels, style=wx.LB_SINGLE)
        main.controls.listbox_by_id[236] = self.listbox
        self.listbox.SetSelection(0)
        self.listbox.SetMinSize((150, -1))
        self.listbox.SetMaxSize((150, -1))

        self.listbox.Bind(wx.EVT_LISTBOX, self.on_select)
        # self.listbox_by_id[236] = self.listbox
        # Layout
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.listbox, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(sizer)

    def on_select(self, event):
        idx = self.listbox.GetSelection()
        print("effect b  : ", self.options[idx])
        # selected_label = self.listbox.GetString(idx)

        # param_value = self.options[selected_label]

        if idx is not None:
            idx = idx + 1
            self.main.send_parameter_edit(236, idx)
            self.parent.update_ctrls()

   



class MasterEffectBSection(wx.Panel):
    def __init__(self, parent, main):
        super().__init__(parent)
        self.SetBackgroundColour("light grey")
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # === Effect B Static Box ===
        effect_b_box = wx.StaticBox(self, label="Master Effect B")
        bold_font = effect_b_box.GetFont().Bold()
        effect_b_box.SetFont(bold_font)
        effect_b_sizer = wx.StaticBoxSizer(effect_b_box, wx.VERTICAL)

        # --- 1) Effect Type ListBox ---
        type_row = wx.BoxSizer(wx.HORIZONTAL)
        type_row.Add(wx.StaticText(self, label="Effect Type"), 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 8)

        self.fx_b_algorithm = MasterFXBListBox(self, main)
        type_row.Add(self.fx_b_algorithm, 1, wx.EXPAND)
        effect_b_sizer.Add(type_row, 0, wx.EXPAND | wx.ALL, 5)
        grid_sizer = wx.GridSizer(rows=3, cols=2, hgap=10, vgap=10)

        
        label1 = wx.StaticText(self, label="Feedback")
        label2 = DraggableNumber(self, id = 237, value = 0, min_val = 0, max_val = 127, callback = main._onAnyControlChanged)

        label3 = wx.StaticText(self, label="LFO Rate")
        label4 = DraggableNumber(self, id = 238, value = 0, min_val = 0, max_val = 127, callback = main._onAnyControlChanged)
        
        label5 = wx.StaticText(self, label="Delay Time")
        label6 = DraggableNumber(self, id = 239, value = 0, min_val = 0, max_val = 127, callback = main._onAnyControlChanged)
        
        labels = [
            label1, label2, label3, label4, label5, label6
        ]
        

        for label in labels:
            label.SetMinSize((80, 20))
            grid_sizer.Add(label, flag=wx.Left|wx.TOP|wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL, border=5)
            
        seg1 = [
            label2, label4, label6
        ]
        for label in seg1:
            main.controls.dragger_by_id[label.Id] = label
            label.SetBackgroundColour(wx.Colour(greencontrol)) 
        

        # --- 3) Sends Section ---
        # send_box = wx.StaticBox(self, label="Sends")
        # send_box.SetFont(bold_font)
        send_sizer = wx.GridSizer(rows=5, cols=2, hgap=10, vgap=10)

        label11 = wx.StaticText(self, label="Main Send")
        label12 = DraggableNumber(self, id = 240, value = 0, min_val = 0, max_val = 100, callback = main._onAnyControlChanged)

        label13 = wx.StaticText(self, label="Sub1 Send")
        label14 = DraggableNumber(self, id = 241, value = 0, min_val = 0, max_val = 100, callback = main._onAnyControlChanged)
        
        label15 = wx.StaticText(self, label="Sub2 Send")
        label16 = DraggableNumber(self, id = 242, value = 0, min_val = 0, max_val = 100, callback = main._onAnyControlChanged)
        
        label17 = wx.StaticText(self, label="Sub3 Send")
        label18 = DraggableNumber(self, id = 243, value = 0, min_val = 0, max_val = 100, callback = main._onAnyControlChanged)

        spacer1 = wx.StaticText(self, label="")
        spacer2 = wx.StaticText(self, label="")

        labels2 = [
                spacer1, spacer2, label11, label12, label13, label14, label15, label16, label17, label18
        ]
        
        
        for label in labels2:
            label.SetMinSize((80, 20))
            send_sizer.Add(label, flag=wx.Left|wx.TOP|wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL, border=5)
            
        seg11 = [
            label12, label14, label16, label18
        ]
        for label in seg11:
            main.controls.dragger_by_id[label.Id] = label
            label.SetBackgroundColour(wx.Colour(greencontrol)) 

        effect_b_sizer.Add(grid_sizer, 0, wx.EXPAND | wx.ALL, 5)
        effect_b_sizer.Add(send_sizer, 0, wx.EXPAND | wx.ALL, 5)

        main_sizer.Add(effect_b_sizer, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(main_sizer)
        
    def update_ctrls(self):
        self.main.send_parameter_request(237)
        self.main.send_parameter_request(238)
        self.main.send_parameter_request(239)
        self.main.send_parameter_request(240)
        self.main.send_parameter_request(241)
        self.main.send_parameter_request(242)
        self.main.send_parameter_request(243)





#================================================================================================================
#================================================================================================================
#================================================================================================================
#================================================================================================================
#================================================================================================================




class MasterEffectsPanel(scrolled.ScrolledPanel):
    def __init__(self, parent, main):
        super().__init__(parent)
        self.main = main
        self.SetBackgroundColour("dark grey")
        
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        

        hbox2 = wx.StaticBox(self)
        hbox2.SetMinSize((300, 500))
        hbox2.SetMaxSize((300, 500))
        hbox2_sizer = wx.StaticBoxSizer(hbox2, wx.HORIZONTAL)
        
        lfo1 = MasterEffectASection(hbox2, main)
        hbox2_sizer.Add(lfo1, 0, 10)

        hbox2_sizer.Add((20,0), 0) 
        
        lfo2 = MasterEffectBSection(hbox2, main)
        hbox2_sizer.Add(lfo2, 0, 10)

        hbox.Add(hbox2_sizer, 0,  10)
        hbox.Add((20,0), 0) 
        hbox3 = wx.StaticBox(self)
        hbox3.SetMinSize((300, 500))
        hbox3.SetMaxSize((300, 500))
        hbox3_sizer = wx.StaticBoxSizer(hbox3, wx.HORIZONTAL)
        mmcp = MultiModeControlPanel(self, main)
        hbox3_sizer.Add(mmcp, 0,  10)
        hbox.Add(hbox3_sizer, 0,  10)
        
        self.SetSizer(hbox)
        
        self.SetBackgroundColour("dark grey")
        self.SetupScrolling(scroll_x=True, scroll_y=True)

       
