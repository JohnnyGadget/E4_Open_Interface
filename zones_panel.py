

import wx
import wx.lib.scrolledpanel as scrolled
from custom_widgets import DraggableNumber, DropDown, SpinNumber
from keywindow import KeyWindowStrip, KeyTopStrip, MultisampleKeyWindowStrip
from velocitywindow import VelocityWindowStrip, VelocityTopStrip
from realtime_window import RealtimeWindowStrip, RealtimeTopStrip



import wx.lib.newevent
DraggableNumberEvent, EVT_DRAGGABLENUMBER = wx.lib.newevent.NewCommandEvent()



greencontrol = (153, 245, 198, 0)
sample_zone_color = wx.Colour(235, 243, 190)
multi_voice_color = wx.Colour(245, 175, 81)
single_voice_color = wx.Colour(152, 231, 245)


yellow = (235, 243, 190, 0)
green1 = (147, 245, 161, 0)
greencontrol = (153, 245, 198, 0)
greenlight = (219, 245, 214, 0)
blue1 = (152, 245, 228, 0)
bluepowder = (152, 231, 245, 0)  
bluefresh = (86, 245, 216)  
bluesky = (167, 233, 245)
orange = (245, 175, 81, 0)









class voice_creation_ctrls(wx.Panel):
    CTRL_ORDER = [
        # label                  , MIDI-PID,       (min, max) or None
        ("New Voice",              32,             None),  # 0x20
        ("Delete Voice",           33,             None),  # 0x21
        ("Copy Voice",             34,             None),  # 0x22
        ("New Sample Zone",        48,             None),  # 0x30
        ("Get Multisample",        49,             None),  # 0x31
        ("Delete Sample Zone",     50,             None),  # 0x32
        ("Combine",                51,             None),  # 0x33
        ("Expand",                 52,             None),  # 0x34
    ]

    def __init__(self, parent):
        super().__init__(parent)

        # total size
        ctrl_width  = 500
        ctrl_height = 60
        self.SetMinSize((ctrl_width, ctrl_height))
        self.SetMaxSize((ctrl_width, ctrl_height))

        cols   = len(self.CTRL_ORDER)
        cell_w = ctrl_width // cols
        cell_h = ctrl_height // 2

        gs = wx.GridSizer(rows=2, cols=cols, vgap=4, hgap=4)

        # ─── top row: labels ─────────────────────────
        for name, _, _ in self.CTRL_ORDER:
            lbl = wx.StaticText(self, label=name, style=wx.ALIGN_CENTER)
            lbl.SetMinSize((cell_w, cell_h))
            lbl.SetMaxSize((cell_w, cell_h))
            gs.Add(lbl, 0, wx.EXPAND)

        self.SetSizer(gs)
        self.Layout()





class sample_ctrlrow(wx.Panel):
    CTRL_ORDER = [
        ("S-Zone", None, None),
        ("",       None, None),
        ("Sample", 38,   (0,999)),
        ("Volume", 39,   (-96,10)),
        ("Pan",    40,   (-64,63)),
        ("",       None, None),
        ("F-Tune", 42,   (-64,64)),
        ("",       None, None),
    ]

    CTRL_ORDER2 = [
        ("Delete", 50),
        ("",       None),
        ("",       None),
        ("",       None),
    ]

    def __init__(self, parent, zone_dict, voice_index, group_num,
                 zone_index, sample, main):
        super().__init__(parent)
        self.main = main
        self.v_idx = voice_index
        self.sample = sample
        self.sample_name_lbl = None
        zone = zone_index - 1
        cols     = len(self.CTRL_ORDER)
        row_h    = 30
        gap      = 2

        # ── make a top‐level HBox to hold everything
        top_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # ── make a child panel to host your 2×8 grid
        ctrl_panel = wx.Panel(self)
        grid = wx.FlexGridSizer(2, cols, gap, gap)
        grid.AddGrowableCol(0)
        for c in range(1, cols):
            grid.AddGrowableCol(c)

        # Row 1: labels
        for name, pid, rng in self.CTRL_ORDER:
            lbl = wx.StaticText(ctrl_panel, label=name, style=wx.ALIGN_CENTER)
            lbl.SetMinSize((80, row_h))
            grid.Add(lbl, 0, wx.EXPAND)
            if name == "Sample":
                self.sample_name_lbl = lbl
            elif name =="S-Zone":
                lbl.SetBackgroundColour(sample_zone_color)

        # Row 2: controls
        for name, pid, rng in self.CTRL_ORDER:
            if name == ("S-Zone") or name == "":
                w = wx.StaticText(ctrl_panel, label="", style=wx.ALIGN_CENTER)
                # w = wx.Button(ctrl_panel, label="delete")
                # def on_delete(evt):
                #     # first do your local cleanup
                #     delete_szone(self)               # if your delete_szone wants the event
                #     # then send to the main frame
                #     main.delete_sample_zone(self.v_idx, zone)

                # w.Bind(wx.EVT_BUTTON, on_delete)
                                
            elif name == "Sample":
                minv, maxv = rng
                val = zone_dict.get(f"E4_GEN_SAMPLE", 0)
                w = SpinNumber( 
                            ctrl_panel,
                            id      = pid,
                            value = sample,
                            min_val = minv,
                            max_val = maxv,
                            voice = voice_index,
                            zone = zone_index,
                            callback = main._onAnyControlChanged,
                            callback_click = main._on_ctrl_clicked)
                # main.request_sample_name(voice_index, sample, self.sample_name_lbl)
                    
                    
                    
            elif name == "Volume":
                val = zone_dict.get(f"E4_GEN_VOLUME", 0)
                minv, maxv = rng
                w = DraggableNumber(
                    ctrl_panel,
                    id      = pid,
                    value = val,
                    min_val = minv,
                    max_val = maxv,
                    voice = voice_index,
                    zone = zone_index,
                    callback = main._onAnyControlChanged,
                    callback_click = main._on_ctrl_clicked
                )
                
                
            elif name == "Pan":
                val = zone_dict.get(f"E4_GEN_PAN", 0)
                minv, maxv = rng
                w = DraggableNumber(
                    ctrl_panel,
                    id      = pid,
                    value = val,
                    min_val = minv,
                    max_val = maxv,
                    voice = voice_index,
                    zone = zone_index,
                    callback = main._onAnyControlChanged,
                    callback_click = main._on_ctrl_clicked
                )
                
                
            elif name == "F-Tune":
                val = zone_dict.get(f"E4_GEN_FTUNE", 0)
                minv, maxv = rng
                w = DraggableNumber(
                    ctrl_panel,
                    id      = pid,
                    value = val,
                    min_val = minv,
                    max_val = maxv,
                    voice = voice_index,
                    zone = zone_index,
                    callback = main._onAnyControlChanged,
                    callback_click = main._on_ctrl_clicked
                )
            else:
                w = wx.StaticText(ctrl_panel, label="", style=wx.ALIGN_CENTER)
            if not isinstance(w, wx.StaticText):
                w.SetBackgroundColour(greencontrol)
            if isinstance(w, DraggableNumber):
                w.SetBackgroundColour(greencontrol)
            
            w.SetMinSize((80, row_h))
            grid.Add(w, 0, wx.EXPAND)

        # finally attach grid to ctrl_panel
        ctrl_panel.SetSizer(grid)

        # add that entire ctrl_panel into the top‐level sizer
        top_sizer.Add(ctrl_panel, 1, wx.EXPAND|wx.ALL, gap)

        # ── NOW TELL WX ABOUT top_sizer ───────────────────
        self.SetSizer(top_sizer)
        self.Layout()

        
def get_name(main, voice_index, sample, lbl):
    main.request_sample_name(voice_index, sample, lbl)

def delete_szone(szone_panel):
    mzone = szone_panel.Parent
    sizer = mzone.GetSizer()
    sizer.Detach(szone_panel)
    szone_panel.Destroy()
    
    mzone.Layout()
    mzone.Parent.SetupScrolling(scroll_x=True, scroll_y=True)
    






























class multivoice_ctrlrow(wx.Panel):
    CTRL_ORDER = [
        ("Voice\n(multi)",     None,   None),
        ("Group",     37,   (0,32)),
        ("",          None,   None),
        ("Volume",    39,     (-96,  10)),
        ("Pan",       40,     (-64,   63)),
        ("C-Tune",    41,     (-72,   24)),
        ("F-Tune",    42,     (-64,   64)),
        ("Transpose", 43,     (-24,  24)),
    ]

    CTRL_ORDER2 = [
        ("Delete",    33),
        ("Copy",      34),
        ("New SZone", 48),
        ("Expand",    52),
    ]

    def __init__(self, parent, voice_dict, voice_index, group_num,
                 zone_index, sample, main):
        super().__init__(parent)
        self.main = main

        cols = len(self.CTRL_ORDER)
        btn_width = 60
        row_h = 30
        gap = 0

        # ─── Top‐level horizontal sizer ─────────────────
        top_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # ─── Left: 2×8 FlexGrid for labels + controls ───
        grid = wx.FlexGridSizer(2, cols, gap, gap)
        grid.AddGrowableCol(0)
        for c in range(1, cols):
            grid.AddGrowableCol(c)

        # Row 1: labels
        for name, _, _ in self.CTRL_ORDER:
            lbl = wx.StaticText(self, label=name, style=wx.ALIGN_CENTER)
            lbl.SetMinSize((80, row_h))
            grid.Add(lbl, 0, wx.EXPAND)
            lbl.SetBackgroundColour(multi_voice_color)

        # Row 2: controls
        for idx, (name, pid, rng) in enumerate(self.CTRL_ORDER):
            if name == "":
                w = wx.StaticText(self, label="", style=wx.ALIGN_CENTER)
            
            elif name == "Voice\n(multi)":
                w = wx.Button(self, label=str(voice_index + 1))
                main.edit_voice_panel.add_voice_panel(voice_dict = voice_dict, v_idx = voice_index + 1, voice_button = w)
                
            elif name == "Group":
            
                w = DraggableNumber(
                    self,
                    id      = 37,
                    value = group_num,
                    min_val = 1,
                    max_val = 32,
                    voice = voice_index,
                    callback = main._onAnyControlChanged,
                    callback_click = main._on_ctrl_clicked
                )
            elif name == "Sample":
                
                w = SpinNumber( 
                            self,
                            id      = pid,
                            value = sample,
                            min_val = 0,
                            max_val = maxv,
                            voice = voice_index,
                            callback = main._onAnyControlChanged,
                            callback_click = main._on_ctrl_clicked)
            elif name == "Volume":
                val = voice_dict.get(f"E4_GEN_VOLUME", 0)
                minv, maxv = rng
                w = DraggableNumber(
                    self,
                    id      = pid,
                    value = val,
                    min_val = minv,
                    max_val = maxv,
                    voice = voice_index,
                    callback = main._onAnyControlChanged,
                    callback_click = main._on_ctrl_clicked
                )
            elif name == "Pan":
                val = voice_dict.get(f"E4_GEN_PAN", 0)
                minv, maxv = rng
                w = DraggableNumber(
                    self,
                    id      = pid,
                    value = val,
                    min_val = minv,
                    max_val = maxv,
                    voice = voice_index,
                    callback = main._onAnyControlChanged,
                    callback_click = main._on_ctrl_clicked
                )
            elif name == "C-Tune":
                val = voice_dict.get(f"E4_GEN_CTUNE", 0)
                minv, maxv = rng
                w = DraggableNumber(
                    self,
                    id      = pid,
                    value = val,
                    min_val = minv,
                    max_val = maxv,
                    voice = voice_index,
                    callback = main._onAnyControlChanged,
                    callback_click = main._on_ctrl_clicked
                )
            elif name == "F-Tune":
                val = voice_dict.get(f"E4_GEN_FTUNE", 0)
                minv, maxv = rng
                w = DraggableNumber(
                    self,
                    id      = pid,
                    value = val,
                    min_val = minv,
                    max_val = maxv,
                    voice = voice_index,
                    callback = main._onAnyControlChanged,
                    callback_click = main._on_ctrl_clicked
                )
            elif name == "Transpose":
                val = voice_dict.get(f"E4_GEN_XPOSE", 0)
                minv, maxv = rng
                w = DraggableNumber(
                    self,
                    id      = pid,
                    value = val,
                    min_val = minv,
                    max_val = maxv,
                    voice = voice_index,
                    callback = main._onAnyControlChanged,
                    callback_click = main._on_ctrl_clicked
                )
            if not isinstance(w, wx.StaticText):
                w.SetBackgroundColour(greencontrol)
            if isinstance(w, DraggableNumber):
                w.SetBackgroundColour(greencontrol)
            w.SetMinSize((80, row_h))
            w.SetMaxSize((80, row_h))
            grid.Add(w, 0, wx.EXPAND)


            

        top_sizer.Add(grid, 1, wx.EXPAND|wx.ALL, gap)

        # ─── Right: vertical stack of 4 buttons ──────────
        # btn_sizer = wx.BoxSizer(wx.VERTICAL)
        # for label, pid in self.CTRL_ORDER2:
        #     btn = wx.Button(self, label=label)
        #     btn.SetMinSize((btn_width, 15))
        #     btn.Bind(wx.EVT_BUTTON,
        #             lambda ev, c=pid: self.main.send_parameter_edit(c, 0))
        #     btn_sizer.Add(btn, 0, wx.EXPAND|wx.BOTTOM, 0)
        # top_sizer.Add(btn_sizer, 0, wx.EXPAND|wx.ALL, 0)

        # ─── Finalize ────────────────────────────────────
        self.SetSizerAndFit(top_sizer)


























class singlevoice_ctrlrow(wx.Panel):
    CTRL_ORDER = [
        ("Voice\n(single)",     None,   None),
        ("Group",     37,   (0,32)),
        ("Sample",          32,   (0, 255)),
        ("Volume",    39,     (-96,  10)),
        ("Pan",       40,     (-64,   63)),
        ("C-Tune",    41,     (-72,   24)),
        ("F-Tune",    42,     (-64,   64)),
        ("Transpose", 43,     (-24,  24)),
    ]

    CTRL_ORDER2 = [
        ("Delete",    33),
        ("Copy",      34),
        ("New SZone", 48),
        ("",    52),
    ]

    def __init__(self, parent, voice_dict, voice_index, group_num,
                 zone_index, sample, main):
        super().__init__(parent)
        self.main = main

        cols = len(self.CTRL_ORDER)
        btn_width = 60
        row_h = 30
        gap = 0

        # ─── Top‐level horizontal sizer ─────────────────
        top_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # ─── Left: 2×8 FlexGrid for labels + controls ───
        grid = wx.FlexGridSizer(2, cols, gap, gap)
        grid.AddGrowableCol(0)
        for c in range(1, cols):
            grid.AddGrowableCol(c)

        # Row 1: labels
        for name, _, _ in self.CTRL_ORDER:
            lbl = wx.StaticText(self, label=name, style=wx.ALIGN_CENTER)
            lbl.SetMinSize((80, row_h))
            grid.Add(lbl, 0, wx.EXPAND)
            if name == "Voice\n(single)":
                lbl.SetBackgroundColour(single_voice_color)

        # Row 2: controls
        for idx, (name, pid, rng) in enumerate(self.CTRL_ORDER):
            if name == "":
                w = wx.StaticText(self, label="", style=wx.ALIGN_CENTER)
            
            elif name == "Voice\n(single)":
                w = wx.Button(self, label=str(voice_index + 1))
                main.edit_voice_panel.add_voice_panel(voice_dict = voice_dict, v_idx = voice_index + 1, voice_button = w)
                
            elif name == "Group":
            
                w = DraggableNumber(
                    self,
                    id      = pid,
                    value = group_num,
                    min_val = 1,
                    max_val = 32,
                    voice = voice_index,
                    callback = main._onAnyControlChanged,
                    callback_click = main._on_ctrl_clicked
                )
            elif name == "Sample":
                minv, maxv = rng
                w = SpinNumber( 
                            self,
                            id      = pid,
                            value = sample,
                            min_val = 0,
                            max_val = maxv,
                            voice = voice_index,
                            callback = main._onAnyControlChanged,
                            callback_click = main._on_ctrl_clicked)
            elif name == "Volume":
                val = voice_dict.get(f"E4_GEN_VOLUME", 0)
                minv, maxv = rng
                w = DraggableNumber(
                    self,
                    id      = pid,
                    value = val,
                    min_val = minv,
                    max_val = maxv,
                    voice = voice_index,
                    callback = main._onAnyControlChanged,
                    callback_click = main._on_ctrl_clicked
                )
            elif name == "Pan":
                val = voice_dict.get(f"E4_GEN_PAN", 0)
                minv, maxv = rng
                w = DraggableNumber(
                    self,
                    id      = pid,
                    value = val,
                    min_val = minv,
                    max_val = maxv,
                    voice = voice_index,
                    callback = main._onAnyControlChanged,
                    callback_click = main._on_ctrl_clicked
                )
            elif name == "C-Tune":
                val = voice_dict.get(f"E4_GEN_CTUNE", 0)
                minv, maxv = rng
                w = DraggableNumber(
                    self,
                    id      = pid,
                    value = val,
                    min_val = minv,
                    max_val = maxv,
                    voice = voice_index,
                    callback = main._onAnyControlChanged,
                    callback_click = main._on_ctrl_clicked
                )
            elif name == "F-Tune":
                val = voice_dict.get(f"E4_GEN_FTUNE", 0)
                minv, maxv = rng
                w = DraggableNumber(
                    self,
                    id      = pid,
                    value = val,
                    min_val = minv,
                    max_val = maxv,
                    voice = voice_index,
                    callback = main._onAnyControlChanged,
                    callback_click = main._on_ctrl_clicked
                )
            elif name == "Transpose":
                val = voice_dict.get(f"E4_GEN_XPOSE", 0)
                minv, maxv = rng
                w = DraggableNumber(
                    self,
                    id      = pid,
                    value = val,
                    min_val = minv,
                    max_val = maxv,
                    voice = voice_index,
                    callback = main._onAnyControlChanged,
                    callback_click = main._on_ctrl_clicked
                )
            if not isinstance(w, wx.StaticText):
                w.SetBackgroundColour(greencontrol)
            if isinstance(w, DraggableNumber):
                w.SetBackgroundColour(greencontrol)
            w.SetMinSize((80, row_h))
            w.SetMaxSize((80, row_h))
            grid.Add(w, 0, wx.EXPAND)


            

        top_sizer.Add(grid, 1, wx.EXPAND|wx.ALL, gap)

        # ─── Right: vertical stack of 4 buttons ──────────
        # btn_sizer = wx.BoxSizer(wx.VERTICAL)
        # for label, pid in self.CTRL_ORDER2:
        #     btn = wx.Button(self, label=label)
        #     btn.SetMinSize((btn_width, 15))
        #     btn.Bind(wx.EVT_BUTTON,
        #             lambda ev, c=pid: self.main.send_parameter_edit(c, 0))
        #     btn_sizer.Add(btn, 0, wx.EXPAND|wx.BOTTOM, 0)
        # top_sizer.Add(btn_sizer, 0, wx.EXPAND|wx.ALL, 0)

        # ─── Finalize ────────────────────────────────────
        self.SetSizerAndFit(top_sizer)



        
        
        












        
        
        
        
        
        

class ctrltopstrip(wx.Panel):
    CTRL_ORDER = [
        ("Voice",        None,   None),
        ("Group",        None,   None),
        ("Sample",    None,   None),
        ("Volume",    39,    (-96,  10)),
        ("Transpose", 43,    (-24,  24)),
        ("Pan",       40,    (-64,   63)),
        ("C-Tune",    41,    (-72,   24)),
        ("F-Tune",    42,    (-64,   64)),
    ]

    def __init__(self, parent):
        super().__init__(parent)

        # total size
        ctrl_width  = 500
        ctrl_height = 60
        self.SetMinSize((ctrl_width, ctrl_height))
        self.SetMaxSize((ctrl_width, ctrl_height))

        cols   = len(self.CTRL_ORDER)
        cell_w = ctrl_width // cols
        cell_h = ctrl_height // 2

        gs = wx.GridSizer(rows=2, cols=cols, vgap=4, hgap=4)

        # ─── top row: labels ─────────────────────────
        for name, _, _ in self.CTRL_ORDER:
            lbl = wx.StaticText(self, label=name, style=wx.ALIGN_BOTTOM)
            lbl.SetMinSize((cell_w, cell_h))
            lbl.SetMaxSize((cell_w, cell_h))
            gs.Add(lbl, 0, wx.EXPAND)

        self.SetSizer(gs)
        self.Layout()





class SingleVoice_Row(wx.Panel):
    ctrl_width  = 500
    row_height  = 60

    def __init__(self, parent, voice_dict, voice_index, main_frame):
        super().__init__(parent, style=wx.BORDER_SIMPLE)
        self.main        = main_frame
        self.voice_index = voice_index
        grp              = voice_dict['group']
        # print("SingleVoice_Row, ", voice_dict)
        # light gray background
        self.SetBackgroundColour(wx.Colour(240,240,240))

        # single 1×4 grid
        gs = wx.GridSizer(rows=1, cols=4, vgap=2, hgap=2)
        self.SetSizer(gs)

        # ─── 1) ctrl‐row strip ─────────────────────────────────────
        ctrl = singlevoice_ctrlrow(self,
                            voice_dict   = voice_dict,
                            voice_index = voice_index,
                            group_num   = grp,
                            zone_index  = None,
                            sample      = voice_dict['params']['E4_GEN_SAMPLE'],
                            main        = main_frame)
        ctrl .SetMinSize((self.ctrl_width, self.row_height))
        ctrl .SetMaxSize((self.ctrl_width, self.row_height))
        gs.Add(ctrl, 0, wx.EXPAND)

        # ─── 2) key‐window strip ───────────────────────────────────
        key = KeyWindowStrip(self,
                            voice_dict['params']['E4_GEN_ORIG_KEY'],
                            voice_dict['params']['E4_GEN_KEY_LOW'],
                            voice_dict['params']['E4_GEN_KEY_HIGH'],
                            voice_dict['params']['E4_GEN_KEY_LOWFADE'],
                            voice_dict['params']['E4_GEN_KEY_HIGHFADE'],
                            voice_index=voice_index,
                            zone_index =1,
                            group_num  =grp,
                            main       =main_frame)
        key .SetMinSize((self.ctrl_width, self.row_height))
        key .SetMaxSize((self.ctrl_width, self.row_height))
        gs.Add(key, 0, wx.EXPAND)

        # ─── 3) velocity‐window strip ──────────────────────────────
        vel = VelocityWindowStrip(self,
                                voice_dict['params']['E4_GEN_VEL_LOW'],
                                voice_dict['params']['E4_GEN_VEL_HIGH'],
                                voice_dict['params']['E4_GEN_VEL_LOWFADE'],
                                voice_dict['params']['E4_GEN_VEL_HIGHFADE'],
                                voice_index=voice_index,
                                zone_index =1,
                                group_num  =grp,
                                main       =main_frame)
        vel .SetMinSize((self.ctrl_width, self.row_height))
        vel .SetMaxSize((self.ctrl_width, self.row_height))
        gs.Add(vel, 0, wx.EXPAND)

        # ─── 4) realtime‐window strip ------ not applicable to samples, so a blank panel instead───────────────────────────────
        rt = RealtimeWindowStrip(self,
                                voice_dict['params']['E4_GEN_RT_LOW'],
                                voice_dict['params']['E4_GEN_RT_HIGH'],
                                voice_dict['params']['E4_GEN_RT_LOWFADE'],
                                voice_dict['params']['E4_GEN_RT_HIGHFADE'],
                                voice_index=voice_index,
                                zone_index =1,
                                group_num = grp,                                  
                                main       =main_frame)
        rt .SetMinSize((self.ctrl_width, self.row_height))
        rt .SetMaxSize((self.ctrl_width, self.row_height))
        gs.Add(rt, 0, wx.EXPAND)
























        
class MultiVoice_Row(wx.Panel):
    """One row representing a voice’s own parameters (no key/vel/rt), 
       with placeholders for alignment."""
    ctrl_width  = 500
    row_height  = 60

    def __init__(self, parent, voice_dict, voice_index, main_frame):
        super().__init__(parent, style=wx.BORDER_SIMPLE)
        self.main        = main_frame
        self.voice_index = voice_index
        grp              = voice_dict['group']

        # light grey bg
        self.SetBackgroundColour(wx.Colour(240,240,240))

        # 1×4 grid
        gs = wx.GridSizer(1, 4, 2, 2)

        # 1) ctrlrow_voice
        ctrl = multivoice_ctrlrow(self,
                            voice_dict   = voice_dict,
                            voice_index = voice_index,
                            group_num   = grp,
                            zone_index  = None,
                            sample      = None,
                            main        = main_frame)
        ctrl .SetMinSize((700, self.row_height))
        ctrl .SetMaxSize((700, self.row_height))
        gs.Add(ctrl, 0, wx.EXPAND)
        # print(voice_dict)
        # ─── 2) key‐window strip ───────────────────────────────────
        key = MultisampleKeyWindowStrip(self,
                            60,
                            voice_dict['params']['E4_GEN_KEY_LOW'],
                            voice_dict['params']['E4_GEN_KEY_HIGH'],
                            voice_dict['params']['E4_GEN_KEY_LOWFADE'],
                            voice_dict['params']['E4_GEN_KEY_HIGHFADE'],
                            voice_index=voice_index,
                            zone_index = 0,
                            group_num  =grp,
                            main       =main_frame)
        key .SetMinSize((self.ctrl_width, self.row_height))
        key .SetMaxSize((self.ctrl_width, self.row_height))
        gs.Add(key, 0, wx.EXPAND)

        # ─── 3) velocity‐window strip ──────────────────────────────
        vel = VelocityWindowStrip(self,
                                voice_dict['params']['E4_GEN_VEL_LOW'],
                                voice_dict['params']['E4_GEN_VEL_HIGH'],
                                voice_dict['params']['E4_GEN_VEL_LOWFADE'],
                                voice_dict['params']['E4_GEN_VEL_HIGHFADE'],
                                voice_index=voice_index,
                                zone_index = -1,
                                group_num  =grp,
                                main       =main_frame)
        vel .SetMinSize((self.ctrl_width, self.row_height))
        vel .SetMaxSize((self.ctrl_width, self.row_height))
        gs.Add(vel, 0, wx.EXPAND)

        # ─── 4) realtime‐window strip ------ not applicable to samples, so a blank panel instead───────────────────────────────
        rt = RealtimeWindowStrip(self,
                                voice_dict['params']['E4_GEN_RT_LOW'],
                                voice_dict['params']['E4_GEN_RT_HIGH'],
                                voice_dict['params']['E4_GEN_RT_LOWFADE'],
                                voice_dict['params']['E4_GEN_RT_HIGHFADE'],
                                voice_index=voice_index,
                                zone_index = -1,
                                group_num = grp,                                  
                                main       =main_frame)
        rt .SetMinSize((self.ctrl_width, self.row_height))
        rt .SetMaxSize((self.ctrl_width, self.row_height))
        gs.Add(rt, 0, wx.EXPAND)

        self.SetSizer(gs)
        self.Layout()





















class Sample_Row(wx.Panel):
    ctrl_width  = 500
    row_height  = 60

    def __init__(self, parent, zone, voice_index, group_num,
                 zone_index, sample_num, main_frame):
        super().__init__(parent, style=wx.BORDER_SIMPLE)
        self.main        = main_frame
        self.voice_index = voice_index
        self.group_num   = group_num
        self.zone_index  = zone_index
        self.sample_num  = sample_num
        self.zone        = zone

        # light gray background
        self.SetBackgroundColour(wx.Colour(240,240,240))

        # single 1×4 grid
        gs = wx.GridSizer(rows=1, cols=4, vgap=2, hgap=2)
        self.SetSizer(gs)

        # ─── 1) ctrl‐row strip ─────────────────────────────────────
        ctrl = sample_ctrlrow(self,
                            zone_dict  = zone,
                            voice_index= voice_index,
                            group_num  = group_num,
                            zone_index = zone_index,
                            sample     = sample_num,
                            main       = main_frame)
        ctrl .SetMinSize((self.ctrl_width, self.row_height))
        ctrl .SetMaxSize((self.ctrl_width, self.row_height))
        gs.Add(ctrl, 0, wx.EXPAND)

        # ─── 2) key‐window strip ───────────────────────────────────
        key = KeyWindowStrip(self,
                            zone['E4_GEN_ORIG_KEY'],
                            zone['E4_GEN_KEY_LOW'],
                            zone['E4_GEN_KEY_HIGH'],
                            zone['E4_GEN_KEY_LOWFADE'],
                            zone['E4_GEN_KEY_HIGHFADE'],
                            voice_index=voice_index,
                            zone_index =zone_index,
                            group_num  =group_num,
                            main       =main_frame)
        key .SetMinSize((self.ctrl_width, self.row_height))
        key .SetMaxSize((self.ctrl_width, self.row_height))
        gs.Add(key, 0, wx.EXPAND)

        # ─── 3) velocity‐window strip ──────────────────────────────
        vel = VelocityWindowStrip(self,
                                    zone['E4_GEN_VEL_LOW'],
                                    zone['E4_GEN_VEL_HIGH'],
                                    zone['E4_GEN_VEL_LOWFADE'],
                                    zone['E4_GEN_VEL_HIGHFADE'],
                                    voice_index=voice_index,
                                    zone_index =zone_index,
                                    group_num  =group_num,
                                    main       =main_frame)
        vel .SetMinSize((self.ctrl_width, self.row_height))
        vel .SetMaxSize((self.ctrl_width, self.row_height))
        gs.Add(vel, 0, wx.EXPAND)

        # ─── 4) realtime‐window strip ------ not applicable to samples, so a blank panel instead───────────────────────────────
        
        rt  = wx.Panel()
        rt.SetBackgroundColour(wx.Colour("dim grey"))
        rt  .SetMinSize((self.ctrl_width, self.row_height))
        rt  .SetMaxSize((self.ctrl_width, self.row_height))
        gs.Add(rt, 0, wx.EXPAND)



















class top_strip_header(wx.Panel):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)

        header_height = 30
        col_width     = 500

        # 2 rows × 4 columns, with a little padding between cells
        grid = wx.GridSizer(rows=2, cols=4, vgap=2, hgap=2)

        # ─── Row 1: labels ───────────────────────────────────────────────
        # 1a) empty top-left
        grid.Add((col_width, header_height), 0)

        # 1b) "Key"
        lbl_key = wx.StaticText(self, label="Key", style=wx.ALIGN_CENTER)
        lbl_key.SetMinSize((col_width, header_height))
        grid.Add(lbl_key, 0, wx.EXPAND)

        # 1c) "Velocity"
        lbl_vel = wx.StaticText(self, label="Velocity", style=wx.ALIGN_CENTER)
        lbl_vel.SetMinSize((col_width, header_height))
        grid.Add(lbl_vel, 0, wx.EXPAND)

        # 1d) "Realtime (voice only)"
        lbl_rt = wx.StaticText(self, label="Realtime (voice only)",
                               style=wx.ALIGN_CENTER)
        lbl_rt.SetMinSize((col_width, header_height))
        grid.Add(lbl_rt, 0, wx.EXPAND)


        # ─── Row 2: the actual strips ─────────────────────────────────────
        # 2a) your ctrl-strip (whatever panel/class you made for the left)
        ctrl = ctrltopstrip(self)
        ctrl.SetMinSize((col_width, header_height))
        grid.Add(ctrl, 0, wx.EXPAND)

        # 2b) TopKeyStrip
        top = KeyTopStrip(self, height=header_height)
        top.SetMinSize((col_width, header_height))
        grid.Add(top, 0, wx.EXPAND)

        # 2c) VelocityTopStrip
        vel = VelocityTopStrip(self, height=header_height)
        vel.SetMinSize((col_width, header_height))
        grid.Add(vel, 0, wx.EXPAND)

        # 2d) RealtimeTopStrip (you’ll need to implement this similarly)
        rt = RealtimeTopStrip(self, height=header_height)
        rt.SetMinSize((col_width, header_height))
        grid.Add(rt, 0, wx.EXPAND)


        # plug the grid into your panel
        self.SetSizer(grid)
        self.Layout()












class Voice_Zones_Panel(wx.Panel):
    def __init__(self, parent, main):
        super().__init__(parent)
        self.main = main
        self.ctrl_width = 500
        self.SetBackgroundColour("dark grey")
        # ─── top‐level sizer ──────────────────────────────────────────
        outer = wx.BoxSizer(wx.VERTICAL)

        # 2) The scrollable area
        self.scroll_pnl = scrolled.ScrolledPanel(self,
                                                style=wx.VSCROLL|wx.HSCROLL)
        self.scroll_pnl.SetupScrolling(scroll_x=True, scroll_y=True)
        
        # must tell it what sizer to use
        self.content_sizer = wx.BoxSizer(wx.VERTICAL)
        self.scroll_pnl.SetSizer(self.content_sizer)


        # finally, put the scroll panel into the outer sizer
        outer.Add(self.scroll_pnl, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(outer)
        self.Layout()

    def display_all_zones(self, parsed_preset):
        if not wx.IsMainThread():
            wx.CallAfter(self.display_all_zones, parsed_preset)
            return

        # clear out just the scrollable content
        self.content_sizer.Clear(True)

        # re‐add the header
        top = top_strip_header(self.scroll_pnl)
        top.SetMinSize((self.ctrl_width*4, 120))
        top.SetBackgroundColour("light grey")
        self.content_sizer.Add(top, 0, wx.EXPAND | wx.ALL, 5)

        for v_idx, voice in enumerate(parsed_preset['voices']):
            if voice['is_multisample']:
                block = wx.Panel(self.scroll_pnl)
                block.SetBackgroundColour("dim grey")
                block_sizer = wx.BoxSizer(wx.VERTICAL)
                block.SetSizer(block_sizer)
                block_sizer.Add((1, 20), 0)
                # 1) MultiVoice row
                vrow = MultiVoice_Row(block, voice, v_idx, main_frame=self.main)
                block_sizer.Add(vrow, 0, wx.EXPAND|wx.ALL, 2)
                block_sizer.Add((1, 20), 0)
                # 2) Sample rows
                for z_idx, zone in enumerate(voice['zones']):
                    sample = zone.get('E4_GEN_SAMPLE', 0)
                    srow = Sample_Row(
                        block, zone,
                        voice_index=v_idx,
                        group_num=voice['group'],
                        zone_index=z_idx,
                        sample_num=sample,
                        main_frame=self.main
                    )
                    block_sizer.Add(srow, 0, wx.EXPAND|wx.LEFT|wx.BOTTOM, 20)

                # ←– **Here**: add the block **panel**, not the block_sizer
                self.content_sizer.Add(block, 0, wx.EXPAND|wx.ALL, 2)

            else:
                # non‐multisample voice
                self.content_sizer.Add((1, 20), 0)
                vrow = SingleVoice_Row(self.scroll_pnl, voice, v_idx, main_frame=self.main)
                self.content_sizer.Add(vrow, 0, wx.EXPAND|wx.ALL, 2)

            # spacer
            self.content_sizer.Add((1, 20), 0)
            

        
        # re‐layout and reset scrolling
        self.scroll_pnl.Layout()
        self.scroll_pnl.SetupScrolling(scroll_x=True, scroll_y=True)
        
        
        
        
        # self.main.request_all_individual_params()










