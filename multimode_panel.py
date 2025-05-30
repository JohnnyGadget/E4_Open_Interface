import wx
from custom_widgets import DraggableNumber, DraggableNumberEvent

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


 
mmmidich_options_conv = {"None":-1, "1":0, "2":1, "3":2, "4":3, "5":4,
                      "6":5, "7":6, "8":7, "9":8, "10":9,
                      "11":10, "12":11, "13":12, "14":13, "15":14, "16":15}
mmmidich_options_conv2 = {"1":0, "2":1, "3":2, "4":3, "5":4,
                      "6":5, "7":6, "8":7, "9":8, "10":9,
                      "11":10, "12":11, "13":12, "14":13, "15":14, "16":15}
 
class MultiModeControlPanel(wx.Panel):
    def __init__(self, parent, main):
        super().__init__(parent)
        self.SetBackgroundColour("light grey")
        self.main = main
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        effect_a_box = wx.StaticBox(self, label="MultiMode Ctrl Panel")
        bold_font = effect_a_box.GetFont().Bold()
        effect_a_box.SetFont(bold_font)
        effect_a_sizer = wx.StaticBoxSizer(effect_a_box, wx.VERTICAL)
        grid_sizer = wx.GridSizer(rows=7, cols=2, hgap=5, vgap=10)

        label1 = wx.StaticText(self, label="Master Effects Bypass")
        self.MASTER_FX_BYPASS = wx.CheckBox(self, id=244)
        self.MASTER_FX_BYPASS.Bind(wx.EVT_CHECKBOX, lambda evt: self._on_toggle(evt))

        label3 = wx.StaticText(self, label="Master FX MM Midi Ctrl Ch")
        mmmidich_options = ["None", "1", "2", "3", "4", "5",
                      "6", "7", "8", "9", "10",
                      "11", "12", "13", "14", "15", "16"]
        self.MASTER_FX_MM_CTRL_CHANNEL = wx.ComboBox(self, id = 245, choices=mmmidich_options, style=wx.CB_READONLY,size=(100, -1))
        main.controls.combo_by_id[245] = self.MASTER_FX_MM_CTRL_CHANNEL
        self.MASTER_FX_MM_CTRL_CHANNEL.SetSelection(0)
        self.MASTER_FX_MM_CTRL_CHANNEL.Bind(wx.EVT_COMBOBOX, self.mmmidich_change) 


        mmmidich_options2 = ["1", "2", "3", "4", "5",
                      "6", "7", "8", "9", "10",
                      "11", "12", "13", "14", "15", "16"]
        label5 = wx.StaticText(self, label="MultiMode Midi Ch")
        self.MULTIMODE_CHANNEL = wx.ComboBox(self, id = 246, choices=mmmidich_options2, style=wx.CB_READONLY,size=(100, -1))
        main.controls.combo_by_id[246] = self.MULTIMODE_CHANNEL
        self.MULTIMODE_CHANNEL.SetSelection(0)
        self.MULTIMODE_CHANNEL.Bind(wx.EVT_COMBOBOX, self.mmmidich2_change) 
        
        
        label7 = wx.StaticText(self, label="MultiMode Preset")
        self.MULTIMODE_PRESET = DraggableNumber(self, id = 247, value = 0, min_val = 0, max_val = 999, callback = main._onAnyControlChanged)
        
        label9 = wx.StaticText(self, label="MultiMode Volume")
        self.MULTIMODE_VOLUME = DraggableNumber(self, id = 248, value = 127, min_val = 0, max_val = 127, callback = main._onAnyControlChanged)
        
        label11 = wx.StaticText(self, label="MultiMode Pan")
        self.MULTIMODE_PAN = DraggableNumber(self, id = 249, value = 0, min_val = -64, max_val = 63, callback = main._onAnyControlChanged)
        
        label13 = wx.StaticText(self, label="MultiMode Submix")
        self.MULTIMODE_SUBMIX = DraggableNumber(self, id = 249, value = -1, min_val = -1, max_val = 7, callback = main._onAnyControlChanged)
        
        
        labels = [
            label1, self.MASTER_FX_BYPASS, 
            label3, self.MASTER_FX_MM_CTRL_CHANNEL,
            label5, self.MULTIMODE_CHANNEL, 
            label7,self.MULTIMODE_PRESET,
            label9,self.MULTIMODE_VOLUME,
            label11,self.MULTIMODE_PAN,
            label13,self.MULTIMODE_SUBMIX
        ]
        

        for label in labels:
            if isinstance(label, DraggableNumber):
                main.controls.dragger_by_id[label.Id] = label
            # label.SetBackgroundColour(wx.Colour(176, 186, 160, 127))
            if label == label1 or label == label3 or label == label5 or label == label7 or label == label9 or label == label11 or label == label13:
                label.SetMinSize((180, 20))
                grid_sizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL)
            else:
                label.SetMinSize((60, 20))
                grid_sizer.Add(label,  0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 60)
                label.SetBackgroundColour(wx.Colour(greencontrol)) 
                
        effect_a_sizer.Add(grid_sizer, flag=wx.ALL, border=10)       
        main_sizer.Add(effect_a_sizer, flag=wx.ALL, border=10)
        self.SetSizer(main_sizer)
        
    def mmmidich_change(self, event):
        selected_value = self.MASTER_FX_MM_CTRL_CHANNEL.GetValue()
        print(selected_value)
        print(mmmidich_options_conv[selected_value])
        self.main.send_parameter_edit(199, mmmidich_options_conv[selected_value])
        
    def mmmidich2_change(self, event):
        selected_value = self.MULTIMODE_CHANNEL.GetValue()
        print(selected_value)
        print(mmmidich_options_conv2[selected_value])
        self.main.send_parameter_edit(199, mmmidich_options_conv2[selected_value])
        
    def _on_toggle(self, event):
        checked = bool(event.GetInt())
        self.main.send_parameter_edit(219, checked)
