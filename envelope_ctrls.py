import wx
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

#====================================================================================================
#====================================================================================================
#====================================================================================================

class Amp_Env_Ctrls(wx.Panel):
    def __init__(self, parent, parent_panel, label, main, amp_env_depth_ctrl, voice_dict):
        super().__init__(parent_panel)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        grid_sizer = wx.GridSizer(rows=6, cols=5, hgap=10, vgap=5)

    
        label1 = wx.StaticText(self, label="")
        label2 = wx.StaticText(self, label="SEG 1")
        label3 = wx.StaticText(self, label="SEG 1")
        label4 = wx.StaticText(self, label="SEG 2")
        label5 = wx.StaticText(self, label="SEG 2")
        
        label6 = wx.StaticText(self, label="")
        label7 = wx.StaticText(self, label="Rate")
        label8 = wx.StaticText(self, label="Amt")
        label9 = wx.StaticText(self, label="Rate")
        label10 = wx.StaticText(self, label="Amt")
        
        label11 = wx.StaticText(self, label="Attack")
        self.atkrate1 = DraggableNumber(self, id = 70, value= voice_dict["params"]["E4_VOICE_VENV_SEG0_RATE"], min_val=0, max_val=127, callback = main._onAnyControlChanged)
        self.atkamt1 = DraggableNumber(self, id = 71, value=voice_dict["params"]["E4_VOICE_VENV_SEG0_TGTLVL"], min_val=0, max_val=100, callback = main._onAnyControlChanged)
        self.atkrate2 = DraggableNumber(self, id = 72, value=voice_dict["params"]["E4_VOICE_VENV_SEG1_RATE"], min_val=0, max_val=127, callback = main._onAnyControlChanged)
        self.atkamt2 = DraggableNumber(self, id = 73, value=voice_dict["params"]["E4_VOICE_VENV_SEG1_TGTLVL"], min_val=0, max_val=100, callback = main._onAnyControlChanged)
        
        label16 = wx.StaticText(self, label="Decay")       
        self.dcyrate1 = DraggableNumber(self, id = 74, value=voice_dict["params"]["E4_VOICE_VENV_SEG2_RATE"], min_val=0, max_val=127, callback = main._onAnyControlChanged)
        self.dcyamt1 = DraggableNumber(self, id = 75, value=voice_dict["params"]["E4_VOICE_VENV_SEG2_TGTLVL"], min_val=0, max_val=100, callback = main._onAnyControlChanged)
        self.dcyrate2  = DraggableNumber(self, id = 76, value=voice_dict["params"]["E4_VOICE_VENV_SEG3_RATE"], min_val=0, max_val=127, callback = main._onAnyControlChanged)
        self.dcyamt2 = DraggableNumber(self, id = 77, value=voice_dict["params"]["E4_VOICE_VENV_SEG3_TGTLVL"], min_val=0, max_val=100, callback = main._onAnyControlChanged)

        label21 = wx.StaticText(self, label="Release")
        self.rlsrate1 = DraggableNumber(self, id = 78, value=voice_dict["params"]["E4_VOICE_VENV_SEG4_RATE"], min_val=0, max_val=127, callback = main._onAnyControlChanged)
        self.rlsamt1 = DraggableNumber(self, id = 79, value=voice_dict["params"]["E4_VOICE_VENV_SEG4_TGTLVL"], min_val=0, max_val=100, callback = main._onAnyControlChanged)
        self.rlsrate2 = DraggableNumber(self, id = 80, value=voice_dict["params"]["E4_VOICE_VENV_SEG5_RATE"], min_val=0, max_val=127, callback = main._onAnyControlChanged)
        self.rlsamt2 = DraggableNumber(self, id = 81, value=voice_dict["params"]["E4_VOICE_VENV_SEG5_TGTLVL"], min_val=0, max_val=100, callback = main._onAnyControlChanged)
        
        label26 = wx.StaticText(self, label="Depth")
        self.env_depth = DraggableNumber(self, id = 68, value=voice_dict["params"]["E4_VOICE_VOLENV_DEPTH"], min_val=0, max_val=16, callback = main._onAnyControlChanged)
        
        self.envelope_ctrls = [ self.atkrate1,
                self.atkamt1,
                self.atkrate2, 
                self.atkamt2,
        
                self.dcyrate1,
                self.dcyamt1,
                self.dcyrate2, 
                self.dcyamt2,
                        
                self.rlsrate1,
                self.rlsamt1,
                self.rlsrate2, 
                self.rlsamt2,
                self.env_depth]
        

        labels = [
            label1, label2, label3, label4, label5, label6, label7, label8, label9, label10,
            label11, self.atkrate1, self.atkamt1, self.atkrate2, self.atkamt2, label16, 
            self.dcyrate1, self.dcyamt1, self.dcyrate2, self.dcyamt2,
            label21, self.rlsrate1, self.rlsamt1, self.rlsrate2, self.rlsamt2,# label26, self.env_depth
        ]
        

        for label in labels:
            if isinstance(label, DraggableNumber):
                main.controls.dragger_by_id[label.Id] = label
            label.SetMinSize((40, 13.5))
            grid_sizer.Add(label, flag=wx.EXPAND)
            
        
            
        seg1 = [label2, label3, label7, label8, self.atkrate1, self.atkamt1,  
                self.dcyrate1, self.dcyamt1, self.rlsrate1, self.rlsamt1,self.env_depth ] 

        for label in seg1:
            label.SetBackgroundColour(wx.Colour(greencontrol)) 
            
        seg2 = [label4, label5,  label9, label10, self.atkrate2, self.atkamt2,
                self.dcyrate2, self.dcyamt2, self.rlsrate2, self.rlsamt2,]   
        for label in seg2:
            label.SetBackgroundColour(wx.Colour(blue1))  
            
        seg3 = [label11, label16,  label21, label7, label8,  label9, label10, label26]   
        for label in seg3:
            label.SetBackgroundColour(wx.Colour(yellow))  
            
        
        main_sizer.Add(grid_sizer, flag=wx.ALL, border=10)
        self.SetSizer(main_sizer)
        
    def _forward_callback(self, event):
        ctrl = event.GetEventObject()
        self.main._onAnyControlChanged(event)
        # print(ctrl.value)


#====================================================================================================
#====================================================================================================
#==================================    FILTER  ==================================================================
        
class Filter_Env_Ctrls(wx.Panel):
    def __init__(self, parent, parent_panel, label, main, voice_dict):
        super().__init__(parent_panel)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        grid_sizer = wx.GridSizer(rows=5, cols=5, hgap=10, vgap=5)


        label1 = wx.StaticText(self, label="")
        label2 = wx.StaticText(self, label="SEG 1")
        label3 = wx.StaticText(self, label="SEG 1")
        label4 = wx.StaticText(self, label="SEG 2")
        label5 = wx.StaticText(self, label="SEG 2")
        
        label6 = wx.StaticText(self, label="")
        label7 = wx.StaticText(self, label="Rate")
        label8 = wx.StaticText(self, label="Amt")
        label9 = wx.StaticText(self, label="Rate")
        label10 = wx.StaticText(self, label="Amt")
        
        label11 = wx.StaticText(self, label="Attack")
        self.atkrate1 = DraggableNumber(self, id = 93, value=50, min_val=voice_dict["params"]["E4_VOICE_FENV_SEG0_RATE"], max_val=127, callback = main._onAnyControlChanged)
        self.atkamt1 = DraggableNumber(self, id = 94, value=100, min_val=voice_dict["params"]["E4_VOICE_FENV_SEG0_TGTLVL"], max_val=100, callback = main._onAnyControlChanged)
        self.atkrate2 = DraggableNumber(self, id = 95, value=50, min_val=voice_dict["params"]["E4_VOICE_FENV_SEG1_RATE"], max_val=127, callback = main._onAnyControlChanged)
        self.atkamt2 = DraggableNumber(self, id = 96, value=100, min_val=voice_dict["params"]["E4_VOICE_FENV_SEG1_TGTLVL"], max_val=100, callback = main._onAnyControlChanged)
        
        label16 = wx.StaticText(self, label="Decay")       
        self.dcyrate1 = DraggableNumber(self, id = 97, value=50, min_val=voice_dict["params"]["E4_VOICE_FENV_SEG2_RATE"], max_val=127, callback = main._onAnyControlChanged)
        self.dcyamt1 = DraggableNumber(self, id = 98, value=50, min_val=voice_dict["params"]["E4_VOICE_FENV_SEG2_TGTLVL"], max_val=100, callback = main._onAnyControlChanged)
        self.dcyrate2  = DraggableNumber(self, id = 99, value=50, min_val=voice_dict["params"]["E4_VOICE_FENV_SEG3_RATE"], max_val=127, callback = main._onAnyControlChanged)
        self.dcyamt2 = DraggableNumber(self, id = 100, value=50, min_val=voice_dict["params"]["E4_VOICE_FENV_SEG3_TGTLVL"], max_val=100, callback = main._onAnyControlChanged)

        label21 = wx.StaticText(self, label="Release")
        self.rlsrate1 = DraggableNumber(self, id = 101, value=50, min_val=voice_dict["params"]["E4_VOICE_FENV_SEG4_RATE"], max_val=127, callback = main._onAnyControlChanged)
        self.rlsamt1 = DraggableNumber(self, id = 102, value=0, min_val=voice_dict["params"]["E4_VOICE_FENV_SEG4_TGTLVL"], max_val=100, callback = main._onAnyControlChanged)
        self.rlsrate2 = DraggableNumber(self, id = 103, value=50, min_val=voice_dict["params"]["E4_VOICE_FENV_SEG5_RATE"], max_val=127, callback = main._onAnyControlChanged)
        self.rlsamt2 = DraggableNumber(self, id = 104, value=0, min_val=voice_dict["params"]["E4_VOICE_FENV_SEG5_TGTLVL"], max_val=100, callback = main._onAnyControlChanged)
        
        self.envelope_ctrls = [ self.atkrate1,
                self.atkamt1,
                self.atkrate2, 
                self.atkamt2,
        
                self.dcyrate1,
                self.dcyamt1,
                self.dcyrate2, 
                self.dcyamt2,
                        
                self.rlsrate1,
                self.rlsamt1,
                self.rlsrate2, 
                self.rlsamt2,]

        labels = [
            label1, label2, label3, label4, label5, label6, label7, label8, label9, label10,
            label11, self.atkrate1, self.atkamt1, self.atkrate2, self.atkamt2, label16, 
            self.dcyrate1, self.dcyamt1, self.dcyrate2, self.dcyamt2,
            label21, self.rlsrate1, self.rlsamt1, self.rlsrate2, self.rlsamt2,
        ]
        

        for label in labels:
            if isinstance(label, DraggableNumber):
                main.controls.dragger_by_id[label.Id] = label
            label.SetMinSize((40, 13.5))
            grid_sizer.Add(label, flag=wx.EXPAND)
            
        
            
        seg1 = [label2, label3, label7, label8, self.atkrate1, self.atkamt1,  
                self.dcyrate1, self.dcyamt1, self.rlsrate1, self.rlsamt1, ] 

        for label in seg1:
            label.SetBackgroundColour(wx.Colour(greencontrol)) 
            
        seg2 = [label4, label5,  label9, label10, self.atkrate2, self.atkamt2,
                self.dcyrate2, self.dcyamt2, self.rlsrate2, self.rlsamt2,]   
        for label in seg2:
            label.SetBackgroundColour(wx.Colour(blue1))  
            
        seg3 = [label11, label16,  label21, label7, label8,  label9, label10]   
        for label in seg3:
            label.SetBackgroundColour(wx.Colour(yellow))  
            

        main_sizer.Add(grid_sizer, flag=wx.ALL, border=10)
        self.SetSizer(main_sizer)

        
#====================================================================================================
#====================================================================================================
#==================================    FILTER  ==================================================================
        
class Aux_Env_Ctrls(wx.Panel):
    def __init__(self, parent, parent_panel, label, main, voice_dict):
        super().__init__(parent_panel)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        grid_sizer = wx.GridSizer(rows=5, cols=5, hgap=10, vgap=5)

        label1 = wx.StaticText(self, label="")
        label2 = wx.StaticText(self, label="SEG 1")
        label3 = wx.StaticText(self, label="SEG 1")
        label4 = wx.StaticText(self, label="SEG 2")
        label5 = wx.StaticText(self, label="SEG 2")
        
        label6 = wx.StaticText(self, label="")
        label7 = wx.StaticText(self, label="Rate")
        label8 = wx.StaticText(self, label="Amt")
        label9 = wx.StaticText(self, label="Rate")
        label10 = wx.StaticText(self, label="Amt")
        
        label11 = wx.StaticText(self, label="Attack")
        self.atkrate1 = DraggableNumber(self, id = 117, value=voice_dict["params"]["E4_VOICE_AENV_SEG0_RATE"], min_val = 0, max_val=127, callback = main._onAnyControlChanged)
        self.atkamt1 = DraggableNumber(self, id = 118, value=voice_dict["params"]["E4_VOICE_AENV_SEG0_TGTLVL"], min_val= -100, max_val=100, callback = main._onAnyControlChanged)
        self.atkrate2 = DraggableNumber(self, id = 119, value=voice_dict["params"]["E4_VOICE_AENV_SEG1_RATE"], min_val = 0, max_val=127, callback = main._onAnyControlChanged)
        self.atkamt2 = DraggableNumber(self, id = 120, value=voice_dict["params"]["E4_VOICE_AENV_SEG1_TGTLVL"], min_val= -100, max_val=100, callback = main._onAnyControlChanged)
        
        label16 = wx.StaticText(self, label="Decay")       
        self.dcyrate1 = DraggableNumber(self, id = 121, value=voice_dict["params"]["E4_VOICE_AENV_SEG2_RATE"], min_val = 0, max_val=127, callback = main._onAnyControlChanged)
        self.dcyamt1 = DraggableNumber(self, id = 122, value=voice_dict["params"]["E4_VOICE_AENV_SEG2_TGTLVL"], min_val= -100, max_val=100, callback = main._onAnyControlChanged)
        self.dcyrate2  = DraggableNumber(self, id = 123, value=voice_dict["params"]["E4_VOICE_AENV_SEG3_RATE"], min_val = 0, max_val=127, callback = main._onAnyControlChanged)
        self.dcyamt2 = DraggableNumber(self, id = 124, value=voice_dict["params"]["E4_VOICE_AENV_SEG3_TGTLVL"], min_val= -100, max_val=100, callback = main._onAnyControlChanged)

        label21 = wx.StaticText(self, label="Release")
        self.rlsrate1 = DraggableNumber(self, id = 125, value=voice_dict["params"]["E4_VOICE_AENV_SEG4_RATE"], min_val = 0, max_val=127, callback = main._onAnyControlChanged)
        self.rlsamt1 = DraggableNumber(self, id = 126, value=voice_dict["params"]["E4_VOICE_AENV_SEG4_TGTLVL"], min_val= -100, max_val=100, callback = main._onAnyControlChanged)
        self.rlsrate2 = DraggableNumber(self, id = 127, value=voice_dict["params"]["E4_VOICE_AENV_SEG5_RATE"], min_val = 0, max_val=127, callback = main._onAnyControlChanged)
        self.rlsamt2 = DraggableNumber(self, id = 128, value=voice_dict["params"]["E4_VOICE_AENV_SEG5_TGTLVL"], min_val= -100, max_val=100, callback = main._onAnyControlChanged)
        
        self.envelope_ctrls = [ self.atkrate1,
                self.atkamt1,
                self.atkrate2, 
                self.atkamt2,
        
                self.dcyrate1,
                self.dcyamt1,
                self.dcyrate2, 
                self.dcyamt2,
                        
                self.rlsrate1,
                self.rlsamt1,
                self.rlsrate2, 
                self.rlsamt2,]
        

        labels = [
            label1, label2, label3, label4, label5, label6, label7, label8, label9, label10,
            label11, self.atkrate1, self.atkamt1, self.atkrate2, self.atkamt2, label16, 
            self.dcyrate1, self.dcyamt1, self.dcyrate2, self.dcyamt2,
            label21, self.rlsrate1, self.rlsamt1, self.rlsrate2, self.rlsamt2,
        ]
        

        for label in labels:
            if isinstance(label, DraggableNumber):
                main.controls.dragger_by_id[label.Id] = label
            label.SetMinSize((40, 13.5))
            grid_sizer.Add(label, flag=wx.EXPAND)
            
        
            
        seg1 = [label2, label3, label7, label8, self.atkrate1, self.atkamt1,  
                self.dcyrate1, self.dcyamt1, self.rlsrate1, self.rlsamt1, ] 
    
        for label in seg1:
            label.SetBackgroundColour(wx.Colour(greencontrol)) 
            
        seg2 = [label4, label5,  label9, label10, self.atkrate2, self.atkamt2,
                self.dcyrate2, self.dcyamt2, self.rlsrate2, self.rlsamt2,]   
        for label in seg2:
            label.SetBackgroundColour(wx.Colour(blue1))  
            
        seg3 = [label11, label16,  label21, label7, label8,  label9, label10]   
        for label in seg3:
            label.SetBackgroundColour(wx.Colour(yellow))  
            

        main_sizer.Add(grid_sizer, flag=wx.ALL, border=10)
        self.SetSizer(main_sizer)
        
        
#====================================================================================================
#====================================================================================================
#====================================================================================================
