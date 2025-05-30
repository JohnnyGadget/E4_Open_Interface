import wx
import wx.lib.scrolledpanel as scrolled
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
midimodes = {"Omni":0,"Poly":1,"Multi":2}

class MidigloConfig(wx.Panel):
    def __init__(self, parent, main):
        super().__init__(parent)
        # self.SetBackgroundColour()
        self.main = main
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        

        grid_sizer = wx.GridSizer(rows=2, cols=2, hgap=5, vgap=10)

        label11 = wx.StaticText(self, label="Basic Channel")
        self.label12 = DraggableNumber(self, id = 198, value = 1, min_val = 1, max_val = 32, callback = self.basicchannelconv)
        main.controls.dragger_by_id[198] = self.label12

        label15 = wx.StaticText(self, label="Midi Mode")
        modes = ["Omni","Poly","Multi"]
        self.midimode_selector = wx.ComboBox(self, id = 199, choices=modes, style=wx.CB_READONLY,size=(60, -1))
        self.midimode_selector.SetSelection(0)
        self.midimode_selector.Bind(wx.EVT_COMBOBOX, self.midimode_change) 
        main.controls.combo_by_id[199] = self.midimode_selector
        
        
        labels = [
            label11, self.label12, label15, self.midimode_selector
        ]
        

        for label in labels:
            # label.SetBackgroundColour(wx.Colour(176, 186, 160, 127))
            if label == self.label12 or label == self.midimode_selector:
                label.SetMinSize((60, 20))
                grid_sizer.Add(label,  0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 60)
                label.SetBackgroundColour(wx.Colour(greencontrol)) 
            else:
                label.SetMinSize((180, 20))
                grid_sizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL)
                # label.SetBackgroundColour(wx.Colour(yellow)) 
                
        main_sizer.Add(grid_sizer, flag=wx.ALL, border=10)
        self.SetSizer(main_sizer)
        
    def basicchannelconv(self, event):
        val = self.label12.value
        val =- 1
        self.main.send_parameter_edit(198, val)
        
    def midimode_change(self, event):
        selected_value = self.midimode_selector.GetValue()
        # print(selected_value)
        # print(midimodes[selected_value])
        self.main.send_parameter_edit(199, midimodes[selected_value])
        
        

options_conv = {"Off":-1,"CC 0":0,"CC 1":1,"CC 2":2,"CC 3":3,"CC 4":4,"CC 5":5,"CC 6":6,"CC 7":7,"CC 8":8,"CC 9":9,"CC 10":10,
                   "CC 11":11,"CC 12":12,"CC 13":13,"CC 14":14,"CC 15":15,"CC 16":16,"CC 17":17,"CC 18":18,"CC 19":19,"CC 20":20,
                   "CC 21":21,"CC 22":22,"CC 23":23,"CC 24":24,"CC 25":25,"CC 26":26,"CC 27":27,"CC 28":28,"CC 29":29,
                   "CC 30":30,"CC 31":31, "ptwheel":32, "chnpres":33}

options2_conv = {"Off":-1,"64":0,"65":1,"66":2,"67":3,"68":4,"69":5,"70":6,"71":7,"72":8,"73":9,"74":10,
                   "75":11,"76":12,"77":13,"78":14,"79":15,"80":16,"81":17,"82":18,"83":19,"84":20,
                   "85":21,"86":22,"87":23,"88":24,"89":25,"90":26,"91":27,"92":28,"93":29,
                   "94":30,"95":31, "96":32, "97":33}

class MasterMidiCtrls1(wx.Panel):
    def __init__(self, parent, main):
        super().__init__(parent)
        self.SetBackgroundColour("light grey")
        self.main = main
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        

        grid_sizer = wx.GridSizer(rows=7, cols=2, hgap=5, vgap=10)


        options = ["Off","CC 0","CC 1","CC 2","CC 3","CC 4","CC 5","CC 6","CC 7","CC 8","CC 9","CC 10",
                   "CC 11","CC 12","CC 13","CC 14","CC 15","CC 16","CC 17","CC 18","CC 19","CC 20",
                   "CC 21","CC 22","CC 23","CC 24","CC 25","CC 26","CC 27","CC 28","CC 29",
                   "CC 30","CC 31", "ptwheel", "chnpres"]
        
        label3 = wx.StaticText(self, label="Pitch Ctrl")
        self.MIDIGLO_PITCH_CONTROL = wx.ComboBox(self, id = 201, choices=options, style=wx.CB_READONLY,size=(100, -1))
        self.MIDIGLO_PITCH_CONTROL.SetSelection(0)
        self.MIDIGLO_PITCH_CONTROL.Bind(wx.EVT_COMBOBOX, self.midigloctrl_change) 
        main.controls.combo_by_id[201] = self.MIDIGLO_PITCH_CONTROL
        
        label5 = wx.StaticText(self, label="Mod Ctrl")
        self.MIDIGLO_MOD_CONTROL = wx.ComboBox(self, id = 202, choices=options, style=wx.CB_READONLY,size=(100, -1))
        self.MIDIGLO_MOD_CONTROL.SetSelection(0)
        self.MIDIGLO_MOD_CONTROL.Bind(wx.EVT_COMBOBOX, self.midigloctrl_change) 
        main.controls.combo_by_id[202] = self.MIDIGLO_MOD_CONTROL
        
        label7 = wx.StaticText(self, label="Pressure Ctrl")
        self.MIDIGLO_PRESSURE_CONTROL = wx.ComboBox(self, id = 203, choices=options, style=wx.CB_READONLY,size=(100, -1))
        self.MIDIGLO_PRESSURE_CONTROL.SetSelection(0)
        self.MIDIGLO_PRESSURE_CONTROL.Bind(wx.EVT_COMBOBOX, self.midigloctrl_change)
        main.controls.combo_by_id[203] = self.MIDIGLO_PRESSURE_CONTROL 
        
        label9 = wx.StaticText(self, label="Pedal Ctrl")
        self.MIDIGLO_PEDAL_CONTROL = wx.ComboBox(self, id = 204, choices=options, style=wx.CB_READONLY,size=(100, -1))
        self.MIDIGLO_PEDAL_CONTROL.SetSelection(0)
        self.MIDIGLO_PEDAL_CONTROL.Bind(wx.EVT_COMBOBOX, self.midigloctrl_change) 
        main.controls.combo_by_id[204] = self.MIDIGLO_PEDAL_CONTROL 
        
        options2 = ["Off","64","65","66","67","68","69","70","71","72","73","74",
                   "75","76","77","78","79","80","81","82","83","84",
                   "85","86","87","88","89","90","91","92","93",
                   "94","95", "96", "97"]
        
        label11 = wx.StaticText(self, label="Switch 1 Ctrl")
        self.MIDIGLO_SWITCH_1_CONTROL = wx.ComboBox(self, id = 205, choices=options2, style=wx.CB_READONLY,size=(100, -1))
        self.MIDIGLO_SWITCH_1_CONTROL.SetSelection(0)
        self.MIDIGLO_SWITCH_1_CONTROL.Bind(wx.EVT_COMBOBOX, self.midigloswitch_change) 
        main.controls.combo_by_id[205] = self.MIDIGLO_SWITCH_1_CONTROL 
        
        label13 = wx.StaticText(self, label="Switch 2 Ctrl")
        self.MIDIGLO_SWITCH_2_CONTROL = wx.ComboBox(self, id = 206, choices=options2, style=wx.CB_READONLY,size=(100, -1))
        self.MIDIGLO_SWITCH_2_CONTROL.SetSelection(0)
        self.MIDIGLO_SWITCH_2_CONTROL.Bind(wx.EVT_COMBOBOX, self.midigloswitch_change) 
        main.controls.combo_by_id[206] = self.MIDIGLO_SWITCH_2_CONTROL 
        
        label15 = wx.StaticText(self, label="Switch 3 Ctrl")
        self.MIDIGLO_THUMB_CONTROL = wx.ComboBox(self, id = 207, choices=options2, style=wx.CB_READONLY,size=(100, -1))
        self.MIDIGLO_THUMB_CONTROL.SetSelection(0)
        self.MIDIGLO_THUMB_CONTROL.Bind(wx.EVT_COMBOBOX, self.midigloswitch_change) 
        main.controls.combo_by_id[207] = self.MIDIGLO_THUMB_CONTROL 
        
        labels = [
            label3, self.MIDIGLO_PITCH_CONTROL, 
            label5, self.MIDIGLO_MOD_CONTROL, label7, self.MIDIGLO_PRESSURE_CONTROL,
            label9, self.MIDIGLO_PEDAL_CONTROL, label11, self.MIDIGLO_SWITCH_1_CONTROL,
            label13, self.MIDIGLO_SWITCH_2_CONTROL, label15, self.MIDIGLO_THUMB_CONTROL
        ]
        

        for label in labels:
            # label.SetBackgroundColour(wx.Colour(176, 186, 160, 127))
            if label == label3 or label == label5 or label == label7 or label == label9 or label == label11 or label == label13 or label == label15:
                label.SetMinSize((180, 20))
                grid_sizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL)
               
            else:
                label.SetMinSize((60, 20))
                grid_sizer.Add(label,  0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 60)
                label.SetBackgroundColour(wx.Colour(greencontrol)) 
                # label.SetBackgroundColour(wx.Colour(yellow)) 
                
        main_sizer.Add(grid_sizer, flag=wx.ALL, border=10)
        self.SetSizer(main_sizer)
        

        
    def midigloctrl_change(self, event):
        ctrl = event.GetEventObject()
        selected_value = ctrl.GetValue()
        print(selected_value)
        print(options_conv[selected_value])
        self.main.send_parameter_edit(ctrl.Id, options_conv[selected_value])
        
    def midigloswitch_change(self, event):
        ctrl = event.GetEventObject()
        selected_value = ctrl.GetValue()
        print(selected_value)
        print(options2_conv[selected_value])
        self.main.send_parameter_edit(ctrl.Id, options2_conv[selected_value])










class MasterMidiCtrls2(wx.Panel):
    def __init__(self, parent, main):
        super().__init__(parent)
        # self.SetBackgroundColour()
        self.main = main
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        

        grid_sizer = wx.GridSizer(rows=8, cols=2, hgap=5, vgap=10)



        options = ["Off","CC 0","CC 1","CC 2","CC 3","CC 4","CC 5","CC 6","CC 7","CC 8","CC 9","CC 10",
                   "CC 11","CC 12","CC 13","CC 14","CC 15","CC 16","CC 17","CC 18","CC 19","CC 20",
                   "CC 21","CC 22","CC 23","CC 24","CC 25","CC 26","CC 27","CC 28","CC 29",
                   "CC 30","CC 31", "ptwheel", "chnpres"]
        
        label3 = wx.StaticText(self, label="Midi A Ctrl")
        self.MIDIGLO_MIDI_A_CONTROL = wx.ComboBox(self, id = 208, choices=options, style=wx.CB_READONLY,size=(100, -1))
        self.MIDIGLO_MIDI_A_CONTROL.SetSelection(0)
        self.MIDIGLO_MIDI_A_CONTROL.Bind(wx.EVT_COMBOBOX, self.midigloctrl_change) 
        main.controls.combo_by_id[208] = self.MIDIGLO_MIDI_A_CONTROL 
        
        label5 = wx.StaticText(self, label="Midi B Ctrl")
        self.MIDIGLO_MIDI_B_CONTROL = wx.ComboBox(self, id = 209, choices=options, style=wx.CB_READONLY,size=(100, -1))
        self.MIDIGLO_MIDI_B_CONTROL.SetSelection(0)
        self.MIDIGLO_MIDI_B_CONTROL.Bind(wx.EVT_COMBOBOX, self.midigloctrl_change) 
        main.controls.combo_by_id[209] = self.MIDIGLO_MIDI_B_CONTROL 
        
        label7 = wx.StaticText(self, label="Midi C Ctrl")
        self.MIDIGLO_MIDI_C_CONTROL = wx.ComboBox(self, id = 210, choices=options, style=wx.CB_READONLY,size=(100, -1))
        self.MIDIGLO_MIDI_C_CONTROL.SetSelection(0)
        self.MIDIGLO_MIDI_C_CONTROL.Bind(wx.EVT_COMBOBOX, self.midigloctrl_change) 
        main.controls.combo_by_id[210] = self.MIDIGLO_MIDI_C_CONTROL 
        
        label9 = wx.StaticText(self, label="Midi D Ctrl")
        self.MIDIGLO_MIDI_D_CONTROL = wx.ComboBox(self, id = 211, choices=options, style=wx.CB_READONLY,size=(100, -1))
        self.MIDIGLO_MIDI_D_CONTROL.SetSelection(0)
        self.MIDIGLO_MIDI_D_CONTROL.Bind(wx.EVT_COMBOBOX, self.midigloctrl_change) 
        main.controls.combo_by_id[211] = self.MIDIGLO_MIDI_D_CONTROL 
        
        label11 = wx.StaticText(self, label="Midi E Ctrl")
        self.MIDIGLO_MIDI_E_CONTROL = wx.ComboBox(self, id = 212, choices=options, style=wx.CB_READONLY,size=(100, -1))
        self.MIDIGLO_MIDI_E_CONTROL.SetSelection(0)
        self.MIDIGLO_MIDI_E_CONTROL.Bind(wx.EVT_COMBOBOX, self.midigloctrl_change)
        main.controls.combo_by_id[212] = self.MIDIGLO_MIDI_E_CONTROL 
        
        label13 = wx.StaticText(self, label="Midi F Ctrl")
        self.MIDIGLO_MIDI_F_CONTROL = wx.ComboBox(self, id = 213, choices=options, style=wx.CB_READONLY,size=(100, -1))
        self.MIDIGLO_MIDI_F_CONTROL.SetSelection(0)
        self.MIDIGLO_MIDI_F_CONTROL.Bind(wx.EVT_COMBOBOX, self.midigloctrl_change)
        main.controls.combo_by_id[213] = self.MIDIGLO_MIDI_F_CONTROL 
        
        label15 = wx.StaticText(self, label="Midi G Ctrl")
        self.MIDIGLO_MIDI_G_CONTROL = wx.ComboBox(self, id = 214, choices=options, style=wx.CB_READONLY,size=(100, -1))
        self.MIDIGLO_MIDI_G_CONTROL.SetSelection(0)
        self.MIDIGLO_MIDI_G_CONTROL.Bind(wx.EVT_COMBOBOX, self.midigloctrl_change)
        main.controls.combo_by_id[214] = self.MIDIGLO_MIDI_G_CONTROL 
        
        label17 = wx.StaticText(self, label="Midi H Ctrl")
        self.MIDIGLO_MIDI_H_CONTROL = wx.ComboBox(self, id = 215, choices=options, style=wx.CB_READONLY,size=(100, -1))
        self.MIDIGLO_MIDI_H_CONTROL.SetSelection(0)
        self.MIDIGLO_MIDI_H_CONTROL.Bind(wx.EVT_COMBOBOX, self.midigloctrl_change)
        main.controls.combo_by_id[215] = self.MIDIGLO_MIDI_H_CONTROL 
        
        
        
        
        labels = [
            label3, self.MIDIGLO_MIDI_A_CONTROL, 
            label5, self.MIDIGLO_MIDI_B_CONTROL, 
            label7, self.MIDIGLO_MIDI_C_CONTROL,
            label9, self.MIDIGLO_MIDI_D_CONTROL,
            label11, self.MIDIGLO_MIDI_E_CONTROL, 
            label13, self.MIDIGLO_MIDI_F_CONTROL, 
            label15, self.MIDIGLO_MIDI_G_CONTROL, 
            label17, self.MIDIGLO_MIDI_H_CONTROL 
            
        ]
        

        for label in labels:
            # label.SetBackgroundColour(wx.Colour(176, 186, 160, 127))
            if label == self.MIDIGLO_MIDI_A_CONTROL or label == self.MIDIGLO_MIDI_B_CONTROL or label == self.MIDIGLO_MIDI_C_CONTROL or label == self.MIDIGLO_MIDI_D_CONTROL or label == self.MIDIGLO_MIDI_E_CONTROL or label == self.MIDIGLO_MIDI_F_CONTROL or label == self.MIDIGLO_MIDI_G_CONTROL or label == self.MIDIGLO_MIDI_H_CONTROL:
                label.SetMinSize((60, 20))
                grid_sizer.Add(label,  0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 60)
                label.SetBackgroundColour(wx.Colour(greencontrol)) 
            else:
                label.SetMinSize((180, 20))
                grid_sizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL)
                # label.SetBackgroundColour(wx.Colour(yellow)) 
                
        main_sizer.Add(grid_sizer, flag=wx.ALL, border=10)
        self.SetSizer(main_sizer)
        
        
    def midigloctrl_change(self, event):
        ctrl = event.GetEventObject()
        selected_value = ctrl.GetValue()
        print(selected_value)
        print(options_conv[selected_value])
        self.main.send_parameter_edit(ctrl.Id, options_conv[selected_value])
        
 




ctrl7modes_conv = {"Linear":0,"Squared":1,"Logarithmic":2}

class MasterMidiPrefs1(wx.Panel):
    def __init__(self, parent, main):
        super().__init__(parent)
        # self.SetBackgroundColour()
        self.main = main
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        grid_sizer = wx.GridSizer(rows=4, cols=2, hgap=5, vgap=10)

        label1 = wx.StaticText(self, label="Vel Curve")
        self.MIDIGLO_VEL_CURVE = DraggableNumber(self, id = 216, value = 0, min_val = 0, max_val = 13, callback = main._onAnyControlChanged)
        main.controls.dragger_by_id[216] = self.MIDIGLO_VEL_CURVE 
        
        label3 = wx.StaticText(self, label="Vol Sensitivity")
        self.MIDIGLO_VOLUME_SENSITIVITY = DraggableNumber(self, id = 217, value = 0, min_val = 0, max_val = 31, callback = main._onAnyControlChanged)
        main.controls.dragger_by_id[217] = self.MIDIGLO_VOLUME_SENSITIVITY 

        label5 = wx.StaticText(self, label="Ctrl 7 Curve")
        ctrl7modes = ["Linear","Squared","Logarithmic"]
        self.MIDIGLO_CTRL7_CURVE = wx.ComboBox(self, id = 218, choices=ctrl7modes, style=wx.CB_READONLY,size=(100, -1))
        self.MIDIGLO_CTRL7_CURVE.SetSelection(0)
        self.MIDIGLO_CTRL7_CURVE.Bind(wx.EVT_COMBOBOX, self.ctrl7_change) 
        main.controls.combo_by_id[218] = self.MIDIGLO_CTRL7_CURVE 
        
        label7 = wx.StaticText(self, label="Pedal Override")
        self.MIDIGLO_PEDAL_OVERRIDE = wx.CheckBox(self, id=219)
        self.MIDIGLO_PEDAL_OVERRIDE.Bind(wx.EVT_CHECKBOX, lambda evt: self._on_toggle(evt))
        main.controls.check_by_id[219] = self.MIDIGLO_PEDAL_OVERRIDE 
        

        
        
        
        labels = [
            label1, self.MIDIGLO_VEL_CURVE, label3, self.MIDIGLO_VOLUME_SENSITIVITY,
            label5, self.MIDIGLO_CTRL7_CURVE, label7,self.MIDIGLO_PEDAL_OVERRIDE
        ]
        

        for label in labels:
            # label.SetBackgroundColour(wx.Colour(176, 186, 160, 127))
            if label == label1 or label == label3 or label == label5 or label == label7:
                label.SetMinSize((180, 20))
                grid_sizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL)
            else:
                label.SetMinSize((60, 20))
                grid_sizer.Add(label,  0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 60)
                label.SetBackgroundColour(wx.Colour(greencontrol)) 
                
        main_sizer.Add(grid_sizer, flag=wx.ALL, border=10)
        self.SetSizer(main_sizer)
        
    def ctrl7_change(self, event):
        selected_value = self.MIDIGLO_CTRL7_CURVE.GetValue()
        # print(selected_value)
        # print(ctrl7modes_conv[selected_value])
        self.main.send_parameter_edit(218, ctrl7modes_conv[selected_value])
        
    def _on_toggle(self, event):
        checked = bool(event.GetInt())
        self.main.send_parameter_edit(219, checked)







MAGIC_PRESET_CONV = {
    "Off": 0,
    "1": 1,   "2": 2,   "3": 3,   "4": 4,   "5": 5,   "6": 6,   "7": 7,   "8": 8,   "9": 9,
    "10": 10, "11": 11, "12": 12, "13": 13, "14": 14, "15": 15, "16": 16, "17": 17, "18": 18, "19": 19,
    "20": 20, "21": 21, "22": 22, "23": 23, "24": 24, "25": 25, "26": 26, "27": 27, "28": 28, "29": 29,
    "30": 30, "31": 31, "32": 32, "33": 33, "34": 34, "35": 35, "36": 36, "37": 37, "38": 38, "39": 39,
    "40": 40, "41": 41, "42": 42, "43": 43, "44": 44, "45": 45, "46": 46, "47": 47, "48": 48, "49": 49,
    "50": 50, "51": 51, "52": 52, "53": 53, "54": 54, "55": 55, "56": 56, "57": 57, "58": 58, "59": 59,
    "60": 60, "61": 61, "62": 62, "63": 63, "64": 64, "65": 65, "66": 66, "67": 67, "68": 68, "69": 69,
    "70": 70, "71": 71, "72": 72, "73": 73, "74": 74, "75": 75, "76": 76, "77": 77, "78": 78, "79": 79,
    "80": 80, "81": 81, "82": 82, "83": 83, "84": 84, "85": 85, "86": 86, "87": 87, "88": 88, "89": 89,
    "90": 90, "91": 91, "92": 92, "93": 93, "94": 94, "95": 95, "96": 96, "97": 97, "98": 98, "99": 99,
    "100": 100, "101": 101, "102": 102, "103": 103, "104": 104, "105": 105, "106": 106, "107": 107,
    "108": 108, "109": 109, "110": 110, "111": 111, "112": 112, "113": 113, "114": 114, "115": 115,
    "116": 116, "117": 117, "118": 118, "119": 119, "120": 120, "121": 121, "122": 122, "123": 123,
    "124": 124, "125": 125, "126": 126, "127": 127, "128": 128
}



class MasterMidiPrefs2(wx.Panel):
    def __init__(self, parent, main):
        super().__init__(parent)
        # self.SetBackgroundColour()
        self.main = main
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        grid_sizer = wx.GridSizer(rows=4, cols=2, hgap=5, vgap=10)

        label1 = wx.StaticText(self, label="Receive Program Change")
        self.MIDIGLO_RCV_PROGRAM_CHANGE = wx.CheckBox(self, id=220)
        self.MIDIGLO_RCV_PROGRAM_CHANGE.Bind(wx.EVT_CHECKBOX, lambda evt: self._on_toggle(evt))
        main.controls.check_by_id[220] = self.MIDIGLO_RCV_PROGRAM_CHANGE 
        
        label3 = wx.StaticText(self, label="Send Program Change")
        self.MIDIGLO_SEND_PROGRAM_CHANGE = wx.CheckBox(self, id=221)
        self.MIDIGLO_SEND_PROGRAM_CHANGE.Bind(wx.EVT_CHECKBOX, lambda evt: self._on_toggle(evt))
        main.controls.check_by_id[221] = self.MIDIGLO_SEND_PROGRAM_CHANGE 
        
        label5 = wx.StaticText(self, label="Magic Preset")
        MAGIC_PRESET = [
            "Off", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
            "10", "11", "12", "13", "14", "15", "16", "17", "18", "19",
            "20", "21", "22", "23", "24", "25", "26", "27", "28", "29",
            "30", "31", "32", "33", "34", "35", "36", "37", "38", "39",
            "40", "41", "42", "43", "44", "45", "46", "47", "48", "49",
            "50", "51", "52", "53", "54", "55", "56", "57", "58", "59",
            "60", "61", "62", "63", "64", "65", "66", "67", "68", "69",
            "70", "71", "72", "73", "74", "75", "76", "77", "78", "79",
            "80", "81", "82", "83", "84", "85", "86", "87", "88", "89",
            "90", "91", "92", "93", "94", "95", "96", "97", "98", "99",
            "100", "101", "102", "103", "104", "105", "106", "107", "108", "109",
            "110", "111", "112", "113", "114", "115", "116", "117", "118", "119",
            "120", "121", "122", "123", "124", "125", "126", "127"
        ]
        self.MIDIGLO_MAGIC_PRESET = wx.ComboBox(self, id = 222, choices=MAGIC_PRESET, style=wx.CB_READONLY,size=(100, -1))
        self.MIDIGLO_MAGIC_PRESET.SetSelection(0)
        self.MIDIGLO_MAGIC_PRESET.Bind(wx.EVT_COMBOBOX, self.magicpreset_change) 
        main.controls.combo_by_id[222] = self.MIDIGLO_MAGIC_PRESET 
        

        

        
        
        
        labels = [
            label1, self.MIDIGLO_RCV_PROGRAM_CHANGE, 
            label3, self.MIDIGLO_SEND_PROGRAM_CHANGE,
            label5, self.MIDIGLO_MAGIC_PRESET, 
        
        ]
        

        for label in labels:
            # label.SetBackgroundColour(wx.Colour(176, 186, 160, 127))
            if label == label1 or label == label3 or label == label5:
                label.SetMinSize((180, 20))
                grid_sizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL)
            else:
                label.SetMinSize((60, 20))
                grid_sizer.Add(label,  0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 60)
                label.SetBackgroundColour(wx.Colour(greencontrol)) 
                
        main_sizer.Add(grid_sizer, flag=wx.ALL, border=10)
        self.SetSizer(main_sizer)
        
    def magicpreset_change(self, event):
        selected_value = self.MIDIGLO_MAGIC_PRESET.GetValue()
        # print(selected_value)
        # print(MAGIC_PRESET_CONV[selected_value])
        self.main.send_parameter_edit(222, MAGIC_PRESET_CONV[selected_value])
        
    def _on_toggle(self, event):
        checked = bool(event.GetInt())
        ctrl = event.GetEventObject()
        self.main.send_parameter_edit(ctrl.Id, checked)
        




class MidigloPanel(scrolled.ScrolledPanel):
    def __init__(self, parent, main):
        super().__init__(parent)
       
        self.SetBackgroundColour("dark grey")
        
        pad = 20
        

#====================================================================================================
#====================================================================================================
#====================================================================================================        
        
        self.midigloconfig_panel = wx.Panel(self, size=(300, 120), pos=(pad , pad))
        self.midigloconfig_panel.SetBackgroundColour("light grey")
        
        box1 = wx.StaticBox(self.midigloconfig_panel, label="Midiglo Config")
        midigloconfig_sizer = wx.StaticBoxSizer(box1, wx.VERTICAL)

        # === Inner content ===
        self.midigloconfig = MidigloConfig(self.midigloconfig_panel, main=main)

        # === Sizer setup ===

        midigloconfig_sizer.Add(self.midigloconfig, 1, wx.EXPAND | wx.ALL, 10)
        self.midigloconfig_panel.SetSizer(midigloconfig_sizer)

        # Ensure layout happens
        self.midigloconfig_panel.Layout()
       

#====================================================================================================
#====================================================================================================
#====================================================================================================


        self.mmctrls1_panel = wx.Panel(self, size=(300, 280), pos=(pad, 120 + pad + pad))
        self.mmctrls1_panel.SetBackgroundColour("light grey")
        box2 = wx.StaticBox(self.mmctrls1_panel, label="Master Midi Controls 1")
        mmctrls1_sizer = wx.StaticBoxSizer(box2, wx.VERTICAL)
        # === Inner content ===
        self.mmctrls1 = MasterMidiCtrls1(self.mmctrls1_panel, main=main)

        # === Sizer setup ===
        mmctrls1_sizer.Add(self.mmctrls1, 1, wx.EXPAND | wx.ALL, 10)
        self.mmctrls1_panel.SetSizer(mmctrls1_sizer)

        # Ensure layout happens
        self.mmctrls1_panel.Layout()



#====================================================================================================
#====================================================================================================
#====================================================================================================


        self.mmctrls2_panel = wx.Panel(self, size=(300, 280), pos=(pad + pad + 300, 120 + pad + pad))
        self.mmctrls2_panel.SetBackgroundColour("light grey")
        box2 = wx.StaticBox(self.mmctrls2_panel, label="Master Midi Controls 2")
        mmctrls2_sizer = wx.StaticBoxSizer(box2, wx.VERTICAL)
        # === Inner content ===
        self.mmctrls2 = MasterMidiCtrls2(self.mmctrls2_panel, main=main)

        # === Sizer setup ===
        mmctrls2_sizer.Add(self.mmctrls2, 1, wx.EXPAND | wx.ALL, 10)
        self.mmctrls2_panel.SetSizer(mmctrls2_sizer)

        # Ensure layout happens
        self.mmctrls2_panel.Layout()



#====================================================================================================
#====================================================================================================
#====================================================================================================
 

        self.mmprefs1_panel = wx.Panel(self, size=(300, 180), pos=(pad, 380 + pad + pad + pad + pad))
        self.mmprefs1_panel.SetBackgroundColour("light grey")
        box2 = wx.StaticBox(self.mmprefs1_panel, label="Master Midi Preferences 1")
        mmprefs1_sizer = wx.StaticBoxSizer(box2, wx.VERTICAL)
        # === Inner content ===
        self.mmprefs1 = MasterMidiPrefs1(self.mmprefs1_panel, main=main)

        # === Sizer setup ===
        mmprefs1_sizer.Add(self.mmprefs1, 1, wx.EXPAND | wx.ALL, 10)
        self.mmprefs1_panel.SetSizer(mmprefs1_sizer)

        # Ensure layout happens
        self.mmprefs1_panel.Layout()



#====================================================================================================
#====================================================================================================
#====================================================================================================

        self.mmprefs2_panel = wx.Panel(self, size=(300, 180), pos=(pad + pad + 300, 380 + pad + pad + pad + pad))
        self.mmprefs2_panel.SetBackgroundColour("light grey")
        box2 = wx.StaticBox(self.mmprefs2_panel, label="Master Midi Preferences 2")
        mmprefs2_sizer = wx.StaticBoxSizer(box2, wx.VERTICAL)
        # === Inner content ===
        self.mmprefs2 = MasterMidiPrefs2(self.mmprefs2_panel, main=main)

        # === Sizer setup ===
        mmprefs2_sizer.Add(self.mmprefs2, 1, wx.EXPAND | wx.ALL, 10)
        self.mmprefs2_panel.SetSizer(mmprefs2_sizer)

        # Ensure layout happens
        self.mmprefs2_panel.Layout()



#====================================================================================================
#====================================================================================================
#====================================================================================================  
        dummy = wx.BoxSizer(wx.VERTICAL)
        dummy.AddSpacer(1100)   # height
        self.SetSizer(dummy)
        self.SetVirtualSize((1600, 1100))
        self.SetScrollRate(20, 20)
        self.SetupScrolling(scroll_x=True, scroll_y=True, scrollToTop=False)
