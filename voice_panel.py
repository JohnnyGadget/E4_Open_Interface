import wx
import wx.lib.scrolledpanel as scrolled

from lfo_display import LFO1, LFO2
from cords_panel import CordsPanel
from filter_panel import FilterPanel
from envelopes import AmpEnvelopePanel, FilterEnvelopePanel, AuxEnvelopePanel
from envelope_ctrls import Amp_Env_Ctrls, Filter_Env_Ctrls, Aux_Env_Ctrls



from tuning import Tuning, TuningModifiers, TuningSetup, Amplifier
class Controls:
    """Container for all the by-id lookup dictionaries."""
    def __init__(self):
        self.spin_by_id       = {}
        self.combo_by_id      = {}
        self.entry_by_id      = {}
        self.listbox_by_id    = {}
        self.check_by_id      = {}
        self.radio_by_id      = {}
        self.dragger_by_id    = {}
        self.last_param = {1111:"params complete"}
        
class EditVoicePanels(wx.Panel):
    def __init__(self, parent, main):
        super().__init__(parent)
        self.main = main
        
        # … build your notebook …
        self.voices_nb = wx.Notebook(self)
        # bind page‐change
        self.voices_nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.on_voice_tab_changed)
         # 2) lay it out to fill this panel
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.voices_nb, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
        
        
    def add_voice_panel(self, voice_dict, v_idx, voice_button):
        # 1) create your new EditVoicePanel and add it to the notebook
        page = EditVoicePanel(self.voices_nb,
                                main=self.main,
                                voice_dict=voice_dict,
                                v_idx=v_idx)
        self.voices_nb.AddPage(page, f"Voice {v_idx}")
        page_index = self.voices_nb.GetPageCount() - 1

        # 2) bind your button so that on click you see the index and then select it
        def _on_voice_button(evt, idx=page_index):
                self.voices_nb.SetSelection(idx)
                self.main.nb.SetSelection(2)

        voice_button.Bind(wx.EVT_BUTTON, _on_voice_button)

    def on_voice_tab_changed(self, evt):
        # zero‐based notebook index → zero‐based voice number
        voice_num = evt.GetSelection()
  
        # self.main.send_parameter_edit(223, 0) #PRESET_SELECT
        # self.main.send_parameter_edit(224, 0) #LINK_SELECT
        self.main.send_parameter_edit(225, voice_num) #VOICE_SELECT
        # self.main.send_parameter_edit(227, 0) #GROUP_SELECT
        # self.main.send_parameter_edit(226, idx) #SAMPLE_ZONE_SELECT
        evt.Skip()



class EditVoicePanel(scrolled.ScrolledPanel):
    def __init__(self, parent, main, voice_dict, v_idx):
        super().__init__(parent)
        self.controls = Controls()
        main.voices_by_page[v_idx] = self
        self.SetBackgroundColour("dark grey")
        self.amp_env_update_display = None
        self.filter_env_update_display = None
        self.aux_env_update_display = None
        
        
        pad = 20
        half_pad = 10

#====================================================================================================
#====================================================================================================
#====================================================================================================        
        
        self.amplifier_panel = wx.Panel(self, size=(240, 180), pos=(pad , pad))
        self.amplifier_panel.SetBackgroundColour("light grey")
        
        box1 = wx.StaticBox(self.amplifier_panel, label="Amplifier")
        amplifier_sizer = wx.StaticBoxSizer(box1, wx.VERTICAL)

        # === Inner content ===
        self.amplifier = Amplifier(self.amplifier_panel, main=main, voice_dict = voice_dict, controls = self.controls, v_idx = v_idx)
        self.amp_env_depth_ctrl = self.amplifier.amp_env_depth
        # === Sizer setup ===

        amplifier_sizer.Add(self.amplifier, 1, wx.EXPAND | wx.ALL, 10)
        self.amplifier_panel.SetSizer(amplifier_sizer)

        # Ensure layout happens
        self.amplifier_panel.Layout()
       

#====================================================================================================
#====================================================================================================
#====================================================================================================


        self.tuning_panel = wx.Panel(self, size=(240, 180), pos=(pad, 180 + pad + pad))
        self.tuning_panel.SetBackgroundColour("light grey")
        box2 = wx.StaticBox(self.tuning_panel, label="Tuning")
        tuning_sizer = wx.StaticBoxSizer(box2, wx.VERTICAL)
        # === Inner content ===
        self.tuning = Tuning(self.tuning_panel, main=main, voice_dict = voice_dict, controls = self.controls)

        # === Sizer setup ===
        tuning_sizer.Add(self.tuning, 1, wx.EXPAND | wx.ALL, 10)
        self.tuning_panel.SetSizer(tuning_sizer)

        # Ensure layout happens
        self.tuning_panel.Layout()



#====================================================================================================
#====================================================================================================
#====================================================================================================

        
        
        self.tuning_mod_panel = wx.Panel(self, size=(240, 180), pos=(pad, 360 + pad + pad + pad))
        self.tuning_mod_panel.SetBackgroundColour("light grey")
        box3 = wx.StaticBox(self.tuning_mod_panel, label="Tuning Modifiers")
        tuning_mod_sizer = wx.StaticBoxSizer(box3, wx.VERTICAL)
        # === Inner content ===
        self.tuning_mod = TuningModifiers(self.tuning_mod_panel, main=main, voice_dict = voice_dict, controls = self.controls)

        # === Sizer setup ===
        tuning_mod_sizer.Add(self.tuning_mod, 1, wx.EXPAND | wx.ALL, 10)
        self.tuning_mod_panel.SetSizer(tuning_mod_sizer)

        # Ensure layout happens
        self.tuning_mod_panel.Layout()      
       
        
#====================================================================================================
#====================================================================================================
#====================================================================================================        


        
        self.tuning_setup_panel = wx.Panel(self, size=(240, 220), pos=(pad , 600 + pad))
        self.tuning_setup_panel.SetBackgroundColour("light grey")
        box4 = wx.StaticBox(self.tuning_setup_panel, label="Tuning Setup")
        tuning_setup_sizer = wx.StaticBoxSizer(box4, wx.VERTICAL)
        # === Inner content ===
        self.tuning_setup = TuningSetup(self.tuning_setup_panel, main=main, voice_dict = voice_dict, controls = self.controls)

        # === Sizer setup ===
        tuning_setup_sizer.Add(self.tuning_setup, 1, wx.EXPAND | wx.ALL, 10)
        self.tuning_setup_panel.SetSizer(tuning_setup_sizer)

        # Ensure layout happens
        self.tuning_setup_panel.Layout()              
 

        
        
#====================================================================================================
#====================================================================================================
#=====================================AMP ENVELOPE=============================================================== 

        new_pad = 40

        self.amp_env_ctrls_panel = wx.Panel(self, size=(280, 180), pos=(new_pad + 220 + pad + half_pad, pad))
        self.amp_env_ctrls_panel.SetBackgroundColour("light grey")

        # Create the StaticBox with a label
        ampenvctrls_box = wx.StaticBox(self.amp_env_ctrls_panel, label="Amp Envelope")
        ampenvctrls_sizer = wx.StaticBoxSizer(ampenvctrls_box, wx.VERTICAL)

        # Add the custom envelope display inside the StaticBoxSizer
        self.amp_env_ctrls = Amp_Env_Ctrls(self.amp_env_ctrls_panel, self.amp_env_ctrls_panel, "Amp Envelope", main, self.amp_env_depth_ctrl, voice_dict)
        ampenvctrls_sizer.Add(self.amp_env_ctrls, 1, wx.EXPAND | wx.ALL, 10)

        # Set the sizer and layout
        self.amp_env_ctrls_panel.SetSizer(ampenvctrls_sizer)
        self.amp_env_ctrls_panel.Layout()
        
 
 
 
        self.envActrls = self.amp_env_ctrls.envelope_ctrls




        self.amp_env_panel = wx.Panel(self, size=(400, 180), pos=(new_pad + 500 + pad + half_pad, pad))
        self.amp_env_panel.SetBackgroundColour("light grey")

        # Create the StaticBox with a label
        ampenv_box = wx.StaticBox(self.amp_env_panel, label="Amp Envelope")
        ampenv_sizer = wx.StaticBoxSizer(ampenv_box, wx.VERTICAL)

        # Add the custom envelope display inside the StaticBoxSizer
        
        self.amp_env = AmpEnvelopePanel(self.amp_env_panel, self.envActrls, self.amp_env_depth_ctrl, voice_dict)
        ampenv_sizer.Add(self.amp_env, 1, wx.EXPAND | wx.ALL, 10)

        # Set the sizer and layout
        self.amp_env_panel.SetSizer(ampenv_sizer)
        self.amp_env_panel.Layout()
        
        
#====================================================================================================
#====================================================================================================
#====================================================================================================
#====================================================================================================
#====================================================================================================
#=====================================FILTER ENVELOPE=============================================================== 

        


        self.filter_env_ctrls_panel = wx.Panel(self, size=(280, 180), pos=(new_pad + 220 + pad + half_pad, 180 + pad + pad))
        self.filter_env_ctrls_panel.SetBackgroundColour("light grey")

        # Create the StaticBox with a label
        filterenvctrls_box = wx.StaticBox(self.filter_env_ctrls_panel, label="Filter Envelope")
        filterenvctrls_sizer = wx.StaticBoxSizer(filterenvctrls_box, wx.VERTICAL)

        # Add the custom envelope display inside the StaticBoxSizer
        self.filter_env_ctrls = Filter_Env_Ctrls(self.filter_env_ctrls_panel, self.filter_env_ctrls_panel, "Filter Envelope", main, voice_dict)
        filterenvctrls_sizer.Add(self.filter_env_ctrls, 1, wx.EXPAND | wx.ALL, 10)

        # Set the sizer and layout
        self.filter_env_ctrls_panel.SetSizer(filterenvctrls_sizer)
        self.filter_env_ctrls_panel.Layout()
        
 
 
 
        self.envFctrls = self.filter_env_ctrls.envelope_ctrls




        self.filter_env_panel = wx.Panel(self, size=(400, 180), pos=(new_pad + 500 + pad + half_pad, 180 + pad + pad))
        self.filter_env_panel.SetBackgroundColour("light grey")

        # Create the StaticBox with a label
        filterenv_box = wx.StaticBox(self.filter_env_panel, label="Filter Envelope")
        filterenv_sizer = wx.StaticBoxSizer(filterenv_box, wx.VERTICAL)

        # Add the custom envelope display inside the StaticBoxSizer
        
        self.filter_env = FilterEnvelopePanel(self.filter_env_panel, self.envFctrls, voice_dict)
        filterenv_sizer.Add(self.filter_env, 1, wx.EXPAND | wx.ALL, 10)

        # Set the sizer and layout
        self.filter_env_panel.SetSizer(filterenv_sizer)
        self.filter_env_panel.Layout()


        
#====================================================================================================
#====================================================================================================
#====================================================================================================
#====================================================================================================
#====================================================================================================
#=====================================AUX ENVELOPE=============================================================== 

        mid_x = pad + 2 * (450 + pad + 20)
        right_x = mid_x + 400 + pad + pad



        self.aux_env_ctrls_panel = wx.Panel(self, size=(280, 180), pos=(mid_x + 400 + pad + pad, pad))
        self.aux_env_ctrls_panel.SetBackgroundColour("light grey")

        # Create the StaticBox with a label
        auxenvctrls_box = wx.StaticBox(self.aux_env_ctrls_panel, label="Aux Envelope")
        auxenvctrls_sizer = wx.StaticBoxSizer(auxenvctrls_box, wx.VERTICAL)

        # Add the custom envelope display inside the StaticBoxSizer
        self.aux_env_ctrls = Aux_Env_Ctrls(self.aux_env_ctrls_panel, self.aux_env_ctrls_panel, "Aux Envelope", main, voice_dict)
        auxenvctrls_sizer.Add(self.aux_env_ctrls, 1, wx.EXPAND | wx.ALL, 10)

        # Set the sizer and layout
        self.aux_env_ctrls_panel.SetSizer(auxenvctrls_sizer)
        self.aux_env_ctrls_panel.Layout()
        
 
 
 
        self.envAuxctrls = self.aux_env_ctrls.envelope_ctrls




        self.aux_env_panel = wx.Panel(self, size=(400, 180), pos=(mid_x + 680 + pad + pad, pad))
        self.aux_env_panel.SetBackgroundColour("light grey")

        # Create the StaticBox with a label
        auxenv_box = wx.StaticBox(self.aux_env_panel, label="Aux Envelope")
        auxenv_sizer = wx.StaticBoxSizer(auxenv_box, wx.VERTICAL)

        # Add the custom envelope display inside the StaticBoxSizer
        
        self.aux_env = AuxEnvelopePanel(self.aux_env_panel, self.envAuxctrls, voice_dict)
        auxenv_sizer.Add(self.aux_env, 1, wx.EXPAND | wx.ALL, 10)

        # Set the sizer and layout
        self.aux_env_panel.SetSizer(auxenv_sizer)
        self.aux_env_panel.Layout()

        
        
#====================================================================================================
#====================================================================================================
#====================================================================================================       
#====================================================================================================
#====================================================================================================
#==================================================================================================== 



        # === MIDDLE 4 VERTICAL PANELS ===
        mid_x = pad + 2 * (450 + pad + 20)
        self.lfo1_panel = wx.Panel(self, size=(200, 420), pos=(mid_x, pad))
        self.lfo1_panel.SetBackgroundColour("light grey")
        self.lfo1_box = wx.StaticBox(self.lfo1_panel, label="LFO 1")
        self.lfo1_sizer = wx.StaticBoxSizer(self.lfo1_box, wx.VERTICAL)
        self.lfo1_panel.SetSizer(self.lfo1_sizer)
        
        self.lfo1 = LFO1(self.lfo1_panel, main, voice_dict)
        self.lfo1_sizer.Add(self.lfo1, 1, wx.EXPAND | wx.ALL, 10)
        
        self.lfo1_panel.Layout()
        

        self.lfo2_panel = wx.Panel(self, size=(200, 420), pos=(mid_x + 200 + pad, pad))
        self.lfo2_panel.SetBackgroundColour("light grey")
        self.lfo2_box = wx.StaticBox(self.lfo2_panel, label="LFO 2")
        self.lfo2_sizer = wx.StaticBoxSizer(self.lfo2_box, wx.VERTICAL)
        self.lfo2_panel.SetSizer(self.lfo2_sizer)
        
        self.lfo2 = LFO2(self.lfo2_panel, main, voice_dict)
        self.lfo2_sizer.Add(self.lfo2, 1, wx.EXPAND | wx.ALL, 10)
        self.lfo2_panel.Layout()
        

#====================================================================================================
#====================================================================================================
#====================================================================================================       
#====================================================================================================
#====================================================================================================
#==================================================================================================== 


        self.filter_panel = wx.Panel(self, size=(680, 400), pos=(new_pad + 220 + pad + half_pad, 360 + pad + pad))
        self.filter_panel.SetBackgroundColour("light grey")
        
        self.filter_box = wx.StaticBox(self.filter_panel, label="FILTER")
        self.filter_sizer = wx.StaticBoxSizer(self.filter_box, wx.VERTICAL)
        self.filter_panel.SetSizer(self.filter_sizer)
        
        self.filter = FilterPanel(self.filter_panel, main, voice_dict)   #FilterPanel(self.filter_panel)
        self.filter_sizer.Add(self.filter, 1, wx.EXPAND | wx.ALL, 10)
        self.filter_panel.Layout()
        
        
        
                                                        
        

        self.panel_m4 = wx.Panel(self, size=(400, 300), pos=(mid_x, 1020))
        self.panel_m4.SetBackgroundColour("green")



        # === RIGHT TALL PANEL ===
        right_x = mid_x + 400 + pad + pad


        self.cords_panel = wx.Panel(self, size=(600, 800), pos=(right_x, pad + 180 + pad))
        self.cords_panel.SetBackgroundColour("light grey")

        # === Inner content ===
        self.cords = CordsPanel(self.cords_panel, main=main, voice_dict = voice_dict)
        # self.aux_env_ctrls.aux_env_update_display = self.aux_env.on_ctrl_change
        # === Sizer setup ===
        cords_sizer = wx.BoxSizer(wx.VERTICAL)
        cords_sizer.Add(self.cords, 1, wx.EXPAND | wx.ALL, 10)
        self.cords_panel.SetSizer(cords_sizer)

        # Ensure layout happens
        self.cords_panel.Layout()


        dummy = wx.BoxSizer(wx.VERTICAL)
        dummy.AddSpacer(1100)   # height
        self.SetSizer(dummy)
        self.SetVirtualSize((2200, 1600))
        dummy.Add((2200,1), 0)    # phantom wide item
        dummy.Add((1,1100), 0)    # plus tall item
        self.SetScrollRate(20, 20)
        self.SetupScrolling(scroll_x=True, scroll_y=True, scrollToTop=False)
        
        self.Show()

    def amp_env_update_display(self, event):
        self.amp_env.on_ctrl_change(event)

   