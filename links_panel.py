import wx
import wx.lib.scrolledpanel as scrolled
from custom_widgets import DraggableNumber
from keywindow import LinkKeyWindowStrip, KeyTopStrip
from velocitywindow import LinkVelocityWindowStrip, VelocityTopStrip
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
link_params = {
                251: "E4_LINK_INTERNAL_EXTERNAL",
                252: "E4_LINK_FILTER_PITCH",
                253: "E4_LINK_FILTER_MOD",
                254: "E4_LINK_FILTER_PRESSURE",
                255: "E4_LINK_FILTER_PEDAL",
                256: "E4_LINK_FILTER_CTRL_A",
                257: "E4_LINK_FILTER_CTRL_B",
                258: "E4_LINK_FILTER_CTRL_C",
                259: "E4_LINK_FILTER_CTRL_D",
                260: "E4_LINK_FILTER_CTRL_E",
                261: "E4_LINK_FILTER_CTRL_F",
                262: "E4_LINK_FILTER_CTRL_G",
                263: "E4_LINK_FILTER_CTRL_H",
                264: "E4_LINK_FILTER_SWITCH_1",
                265: "E4_LINK_FILTER_SWITCH_2",
                266: "E4_LINK_FILTER_THUMB"
}



#  E4_LINK_PRESET, id = 23 (17h,00h) min = 0; max = 999(1255)
#  E4_LINK_VOLUME, id = 24 (18h,00h) min = -96; max = +10
#  E4_LINK_PAN, id = 25 (19h,00h) min = -64; max = +63
#  E4_LINK_TRANSPOSE, id = 26 (1Ah,00h) min = -24; max = +24
#  E4_LINK_FINE_TUNE, id = 27 (1Bh,00h) min = -64; max = +64
#  E4_LINK_KEY_LOW, id = 28 (1Ch,00h) min = 0; max = 127 (C-2 -> G8)
#  E4_LINK_KEY_LOWFADE, id = 29 (1Dh,00h) min = 0; max = 127
#  E4_LINK_KEY_HIGH, id = 30 (1Eh,00h) min = 0; max = 127 (C-2 -> G8)
#  E4_LINK_KEY_HIGHFADE, id = 31 (1Fh,00h) min = 0; max = 127
#  E4_LINK_VEL_LOW, id = 32 (20h,00h) min = 0; max = 127
#  E4_LINK_VEL_LOWFADE, id = 33 (21h,00h) min = 0; max = 127
#  E4_LINK_VEL_HIGH, id = 34 (22h,00h) min = 0; max = 127
#  E4_LINK_VEL_HIGHFADE, id = 35 (23h,00h) min = 0; max = 127 






class linkctrlrow(wx.Panel):
    CTRL_ORDER = [
        ("link",     None,   None),
        ("Link Preset",     23,   (0,999)),
        ("Volume",     24,   (-96, 10)),
        ("Pan",        25,   (-64, 63)),
        ("Transpose", 26,     (-24,  24)),
        ("F-Tune",    27,     (-64,   64)),
        
    ]

    def __init__(self, parent, link_index, main, controls):
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
            if name == "link":
                lbl = wx.StaticText(self, label=f"Link {link_index}", style=wx.ALIGN_CENTER)
                lbl.SetMinSize((80, row_h))
                grid.Add(lbl, 0, wx.EXPAND)
            else:
                lbl = wx.StaticText(self, label=name, style=wx.ALIGN_CENTER)
                lbl.SetMinSize((80, row_h))
                grid.Add(lbl, 0, wx.EXPAND)

        # Row 2: controls
        for idx, (name, pid, rng) in enumerate(self.CTRL_ORDER):
            
            if name == "Link Preset":
                val = 0
                w = DraggableNumber(
                    self,
                    id      = pid,
                    value = 0,
                    min_val = 0,
                    max_val = 999,
                    link = link_index,
                    callback = main._onAnyControlChanged,
                    callback_click= main._on_ctrl_clicked
                )
                controls["E4_LINK_PRESET"] = w
            elif name == "link":
                w = wx.StaticText(self, label="", style=wx.ALIGN_CENTER)
            elif name == "Volume":
                val = 0
                minv, maxv = rng
                w = DraggableNumber(
                    self,
                    id      = pid,
                    value = val,
                    min_val = minv,
                    max_val = maxv,
                    link = link_index,
                    callback = main._onAnyControlChanged,
                    callback_click= main._on_ctrl_clicked
                )
                controls["E4_LINK_VOLUME"] = w
                
            elif name == "Pan":
                val = 0
                minv, maxv = rng
                w = DraggableNumber(
                    self,
                    id      = pid,
                    value = val,
                    min_val = minv,
                    max_val = maxv,
                    link = link_index,
                    callback = main._onAnyControlChanged,
                    callback_click= main._on_ctrl_clicked
                )
                controls["E4_LINK_PAN"] = w
                
            elif name == "F-Tune":
                val = 0
                minv, maxv = rng
                w = DraggableNumber(
                    self,
                    id      = pid,
                    value = val,
                    min_val = minv,
                    max_val = maxv,
                    link = link_index,
                    callback = main._onAnyControlChanged,
                    callback_click= main._on_ctrl_clicked
                )
                controls["E4_LINK_FINE_TUNE"] = w
                
            elif name == "Transpose":
                val = 0
                minv, maxv = rng
                w = DraggableNumber(
                    self,
                    id      = pid,
                    value = val,
                    min_val = minv,
                    max_val = maxv,
                    link = link_index,
                    callback = main._onAnyControlChanged,
                    callback_click= main._on_ctrl_clicked
                )
                controls["E4_LINK_TRANSPOSE"] = w
                
            w.SetMinSize((80, row_h))
            w.SetMaxSize((80, row_h))
            if not isinstance(w, wx.StaticText):
                w.SetBackgroundColour(greencontrol)
            if isinstance(w, DraggableNumber):
                w.SetBackgroundColour(greencontrol)
                w.SetMinSize((40, row_h))
                w.SetMaxSize((40, row_h))
            
            grid.Add(w, 0, wx.EXPAND)


            

        top_sizer.Add(grid, 1, wx.EXPAND|wx.ALL, gap)

        # ─── Finalize ────────────────────────────────────
        self.SetSizerAndFit(top_sizer)


class Link_Row(wx.Panel):
    """One row representing a voice’s own parameters (no key/vel/rt), 
       with placeholders for alignment."""
    ctrl_width  = 500
    row_height  = 60

    def __init__(self, parent, linkparams, l_idx, main_frame):
        super().__init__(parent, style=wx.BORDER_SIMPLE)
        self.main        = main_frame
        self.linkparams = linkparams
        # print(linkparams)
        self.l_idx = l_idx
        self.controls = {"E4_LINK_PRESET":None,
            "E4_LINK_VOLUME":None,
            "E4_LINK_PAN":None,
            "E4_LINK_TRANSPOSE":None,
            "E4_LINK_FINE_TUNE":None,
            "E4_LINK_KEY_LOW":None,
            "E4_LINK_KEY_LOWFADE":None,
            "E4_LINK_KEY_HIGH":None,
            "E4_LINK_KEY_HIGHFADE":None,
            "E4_LINK_VEL_LOW":None,
            "E4_LINK_VEL_LOWFADE":None,
            "E4_LINK_VEL_HIGH":None,
            "E4_LINK_VEL_HIGHFADE":None}
        # light grey bg
        self.SetBackgroundColour(wx.Colour(240,240,240))

        # 1×4 grid
        gs = wx.GridSizer(1, 4, 2, 2)

        # 1) ctrlrow_voice
        ctrl = linkctrlrow(self,
                            link_index = l_idx,
                            main        = main_frame,
                            controls = self.controls)
        ctrl .SetMinSize((700, self.row_height))
        ctrl .SetMaxSize((700, self.row_height))
        gs.Add(ctrl, 0, wx.EXPAND)
        # print(voice_dict)
        # ─── 2) key‐window strip ───────────────────────────────────
        key = LinkKeyWindowStrip(self,
                                link_index = l_idx,
                                main       =main_frame,
                                controls = self.controls)
        key .SetMinSize((self.ctrl_width, self.row_height))
        key .SetMaxSize((self.ctrl_width, self.row_height))
        gs.Add(key, 0, wx.EXPAND)

        # ─── 3) velocity‐window strip ──────────────────────────────
        vel = LinkVelocityWindowStrip(self,
                                        link_index = l_idx,
                                        main       =main_frame,
                                        controls = self.controls)
        vel .SetMinSize((self.ctrl_width, self.row_height))
        vel .SetMaxSize((self.ctrl_width, self.row_height))
        gs.Add(vel, 0, wx.EXPAND)


        self.update_link()
        self.SetSizer(gs)
        self.Layout()
        
    def update_link(self):
        data = self.linkparams
        self.controls["E4_LINK_PRESET"].Value = data["E4_LINK_PRESET"]
        self.controls["E4_LINK_VOLUME"].Value = data["E4_LINK_VOLUME"]
        self.controls["E4_LINK_PAN"].Value = data["E4_LINK_PAN"]
        self.controls["E4_LINK_TRANSPOSE"].Value = data["E4_LINK_TRANSPOSE"]
        self.controls["E4_LINK_FINE_TUNE"].Value = data["E4_LINK_FINE_TUNE"]
        
        self.controls["E4_LINK_KEY_LOW"] = data["E4_LINK_KEY_LOW"]
        self.controls["E4_LINK_KEY_LOWFADE"] = data["E4_LINK_KEY_LOWFADE"]
        self.controls["E4_LINK_KEY_HIGH"] = data["E4_LINK_KEY_HIGH"]
        self.controls["E4_LINK_KEY_HIGHFADE"] = data["E4_LINK_KEY_HIGHFADE"]
        
        self.controls["E4_LINK_VEL_LOW"] = data["E4_LINK_VEL_LOW"]
        self.controls["E4_LINK_VEL_LOWFADE"] = data["E4_LINK_VEL_LOWFADE"]
        self.controls["E4_LINK_VEL_HIGH"] = data["E4_LINK_VEL_HIGH"]
        self.controls["E4_LINK_VEL_HIGHFADE"] = data["E4_LINK_VEL_HIGHFADE"]



class linkctrltopstrip(wx.Panel):
    CTRL_ORDER = [
        ("Link",      None,   None),
        ("Volume",    None,   None),
        ("Pan",       None,   None),
        ("Transpose", None,   None),
        ("F-Tune",    None,   None),
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


        
class top_strip_header(wx.Panel):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)

        header_height = 30
        col_width     = 500

        # 2 rows × 4 columns, with a little padding between cells
        grid = wx.GridSizer(rows=2, cols=4, vgap=2, hgap=2)

        # ─── Row 1: labels ───────────────────────────────────────────────
        # 1a) empty top-left
        lbl_ctrl = wx.StaticText(self, label="Link Parameters", style=wx.ALIGN_CENTER)
        lbl_ctrl.SetMinSize((col_width, header_height))
        grid.Add(lbl_ctrl, 0, wx.EXPAND)

        # 1b) "Key"
        lbl_key = wx.StaticText(self, label="Key", style=wx.ALIGN_CENTER)
        lbl_key.SetMinSize((col_width, header_height))
        grid.Add(lbl_key, 0, wx.EXPAND)

        # 1c) "Velocity"
        lbl_vel = wx.StaticText(self, label="Velocity", style=wx.ALIGN_CENTER)
        lbl_vel.SetMinSize((col_width, header_height))
        grid.Add(lbl_vel, 0, wx.EXPAND)
        
        spacer = wx.StaticText(self, label="", style=wx.ALIGN_CENTER)
        spacer.SetMinSize((col_width, header_height))
        grid.Add(spacer, 0, wx.EXPAND)

        # # 1d) "Realtime (voice only)"
        # lbl_rt = wx.StaticText(self, label="Realtime (voice only)",
        #                        style=wx.ALIGN_CENTER)
        # lbl_rt.SetMinSize((col_width, header_height))
        # grid.Add(lbl_rt, 0, wx.EXPAND)


        # ─── Row 2: the actual strips ─────────────────────────────────────
        # 2a) your ctrl-strip (whatever panel/class you made for the left)

        ctrl = linkctrltopstrip(self)
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
        
        spacer = wx.StaticText(self, label="", style=wx.ALIGN_CENTER)
        spacer.SetMinSize((col_width, header_height))
        grid.Add(spacer, 0, wx.EXPAND)



        # plug the grid into your panel
        self.SetSizer(grid)
        self.Layout()
        

        
class Links_Panel(wx.Panel):
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

    def display_all_links(self, parsed_preset):
        if not wx.IsMainThread():
            wx.CallAfter(self.display_all_links, parsed_preset)
            return

        # clear out just the scrollable content
        self.content_sizer.Clear(True)

        # re‐add the header
        top = top_strip_header(self.scroll_pnl)
        top.SetMinSize((self.ctrl_width*4, 120))
        top.SetBackgroundColour("light grey")
        self.content_sizer.Add(top, 0, wx.EXPAND | wx.ALL, 5)
        if parsed_preset['num_links'] > 0:
            for l_idx, link in enumerate(parsed_preset['links']):
                self.content_sizer.Add((1, 20), 0)
                vrow = Link_Row(self.scroll_pnl, linkparams = parsed_preset['links'][l_idx], l_idx = l_idx, main_frame=self.main)
                self.content_sizer.Add(vrow, 0, wx.EXPAND|wx.ALL, 2)

                # spacer
                self.content_sizer.Add((1, 20), 0)
            

        
        # re‐layout and reset scrolling
        self.scroll_pnl.Layout()
        self.scroll_pnl.SetupScrolling(scroll_x=True, scroll_y=True)


