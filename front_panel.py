# # Enter:	F0 18 7F 00 00 40 5D 00 01 F7; F0 18 7F 00 00 40 5D 00 00 F7,
# # Exit:	F0 18 7F 00 00 40 5E 00 01 F7; F0 18 7F 00 00 40 5E 00 00 F7,
# # F1:	F0 18 7F 00 00 40 62 00 01 F7,
# # F2:	F0 18 7F 00 00 40 64 00 01 F7,
# # F3:	F0 18 7F 00 00 40 66 00 01 F7,
# # F4:	F0 18 7F 00 00 40 68 00 01 F7,
# # F5:	F0 18 7F 00 00 40 6A 00 01 F7,
# # F6:	F0 18 7F 00 00 40 6C 00 01 F7,
# # Master:	F0 18 7F 00 00 40 5C 00 01 F7; F0 18 7F 00 00 40 5C 00 00 F7,
# # Disk:	F0 18 7F 00 00 40 5D 00 01 F7; F0 18 7F 00 00 40 5D 00 00 F7,
# # Pres Man:	F0 18 7F 00 00 40 58 00 01 F7; F0 18 7F 00 00 40 58 00 00 F7,
# # Pres Ed:	F0 18 7F 00 00 40 5A 00 01 F7; F0 18 7F 00 00 40 5A 00 00 F7,
# # Samp Man:	F0 18 7F 00 00 40 59 00 01 F7; F0 18 7F 00 00 40 59 00 00 F7,
# # Samp Ed:	F0 18 7F 00 00 40 5B 00 01 F7; F0 18 7F 00 00 40 5B 00 00 F7,
# # Audit:	F0 18 7F 00 00 40 65 00 01 F7; F0 18 7F 00 00 40 65 00 00 F7,
# # Asgn 1:	F0 18 7F 00 00 40 5F 00 01 F7; F0 18 7F 00 00 40 5F 00 00 F7,
# # Asgn 2:	F0 18 7F 00 00 40 60 00 01 F7; F0 18 7F 00 00 40 60 00 00 F7,
# # Asgn 3:	F0 18 7F 00 00 40 63 00 01 F7; F0 18 7F 00 00 40 63 00 00 F7,
# # Pg >>:	F0 18 7F 00 00 40 6B 00 01 F7; F0 18 7F 00 00 40 6B 00 00 F7,
# # Pg <<:	F0 18 7F 00 00 40 69 00 01 F7; F0 18 7F 00 00 40 69 00 00 F7,
# # Up:	F0 18 7F 00 00 40 6E 00 01 F7; F0 18 7F 00 00 40 6E 00 00 F7,
# # Down:	F0 18 7F 00 00 40 71 00 01 F7; F0 18 7F 00 00 40 71 00 00 F7,
# # Left:	F0 18 7F 00 00 40 6F 00 01 F7; F0 18 7F 00 00 40 6F 00 00 F7,
# # Righ:	F0 18 7F 00 00 40 70 00 01 F7; F0 18 7F 00 00 40 70 00 00 F7,
# # Dec:	F0 18 7F 00 00 40 72 00 01 F7; F0 18 7F 00 00 40 72 00 00 F7,
# # Inc:	F0 18 7F 00 00 40 73 00 01 F7; F0 18 7F 00 00 40 73 00 00 F7,
# # 1:	F0 18 7F 00 00 40 74 00 01 F7; F0 18 7F 00 00 40 74 00 00 F7,
# # 2:	F0 18 7F 00 00 40 75 00 01 F7; F0 18 7F 00 00 40 75 00 00 F7,
# # 3:	F0 18 7F 00 00 40 76 00 01 F7; F0 18 7F 00 00 40 76 00 00 F7,
# # 4:	F0 18 7F 00 00 40 77 00 01 F7; F0 18 7F 00 00 40 77 00 00 F7,
# # 5:	F0 18 7F 00 00 40 78 00 01 F7; F0 18 7F 00 00 40 78 00 00 F7,
# # 6:	F0 18 7F 00 00 40 79 00 01 F7; F0 18 7F 00 00 40 79 00 00 F7,
# # 7:	F0 18 7F 00 00 40 7A 00 01 F7; F0 18 7F 00 00 40 7A 00 00 F7,
# # 8:	F0 18 7F 00 00 40 7B 00 01 F7; F0 18 7F 00 00 40 7B 00 00 F7,
# # 9:	F0 18 7F 00 00 40 7C 00 01 F7; F0 18 7F 00 00 40 7C 00 00 F7,
# # 0:	F0 18 7F 00 00 40 7E 00 01 F7; F0 18 7F 00 00 40 7E 00 00 F7,
# # set:	F0 18 7F 00 00 40 7F 00 01 F7; F0 18 7F 00 00 40 7F 00 00 F7,
# # +/-:	F0 18 7F 00 00 40 7D 00 00 F7; F0 18 7F 00 00 40 7D 00 01 F7,




import wx
import wx.lib.scrolledpanel as scrolled
import mido
# ───── your button → param-ID lookup ───────────────────────────────
button_ids = {
    'Enter':    93,
    'Exit':     94,
    'F1':       98,
    'F2':       100,
    'F3':       102,
    'F4':       104,
    'F5':       106,
    'F6':       108,
    'Master':   92,
    'Disk':     93,
    'Pres Man': 88,
    'Pres Ed':  90,
    'Samp Man': 89,
    'Samp Ed':  91,
    'Audit':    101,
    ' 1 ':   95,
    ' 2 ':   96,
    ' 3 ':   99,
    'Prev':  105,
    'Next':  107,
    'Up':       110,
    'Down':     113,
    'Left':     111,
    'Right':    112,
    'Dec':      114,
    'Inc':      115,
    '1':        116,
    '2':        117,
    '3':        118,
    '4':        119,
    '5':        120,
    '6':        121,
    '7':        122,
    '8':        123,
    '9':        124,
    '0':        126,
    'Set':      127,
    '+/-':      125,
}

# ───── key → name maps for the settings dialog ────────────────────
# (you can adjust/add more wx key constants as needed)


KEY_NAME_MAP = {
    77:           'Master',
    68:           'Disk',
    80:           'Pres Man',
    69:           'Pres Ed',
    83:           'Samp Man',
    71:           'Samp Ed',
    65:           'Audit',
    90:           ' 1 ',
    88:           ' 2 ',
    67:           ' 3 ',
    44:            'Prev',
    46:             'Next',
    315:            "Up",
    317:        "Down",
    314:        "Left",
    316:        "Right",
    13:         "Enter",
    8:          "Exit",
    340:        "F1",
    341:        "F2",
    342:        "F3",
    343:        "F4",
    344:        "F5",
    345:        "F6",
    48:         "0",
    49:         "1",
    50:         "2",
    51:         "3",
    52:         "4",
    53:         "5",
    54:         "6",
    55:         "7",
    56:         "8",
    57:         "9",
    39:         "+/-",
    47:         "Set",
    45:         "Dec",
    61:         "Inc",
}


KEY_CHOICES = sorted(KEY_NAME_MAP.values())

# ───── default key bindings (you can override via settings) ─────────
default_key_bindings = {
    btn: key for key, btn in KEY_NAME_MAP.items()
}



class PresetPanel(wx.Panel):
    def __init__(self, parent, main, buttons):
        super().__init__(parent, size=(60, 50))
        box = wx.StaticBox(self, label="Preset")
        sbs = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        for name, label in (("Pres Man","Manage"),("Pres Ed","Edit")):
            btn = SysExButton(self, label, button_ids[name], main)
            buttons[name] = btn
            btn.SetMinSize((50, 20))
            sbs.Add(btn, 0, wx.ALL, 4)
        self.SetSizerAndFit(sbs)
        box.SetForegroundColour(wx.Colour(153, 245, 198))

class SamplePanel(wx.Panel):
    def __init__(self, parent, main, buttons):
        super().__init__(parent, size=(60, 50))
        box = wx.StaticBox(self, label="Sample")
        sbs = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        for name, label in (("Samp Man","Manage"),("Samp Ed","Edit")):
            btn = SysExButton(self, label, button_ids[name], main)
            btn.SetMinSize((50, 20))
            buttons[name] = btn
            sbs.Add(btn, 0, wx.ALL, 4)
        self.SetSizerAndFit(sbs)
        box.SetForegroundColour(wx.Colour(153, 245, 198))
        
class AssignPanel(wx.Panel):
    def __init__(self, parent, main, buttons):
        super().__init__(parent, size=(180, 30))
        box = wx.StaticBox(self, label="Assign")
        sbs = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        for name in (" 1 ", " 2 ", " 3 "):

            btn = SysExButton(self, name, button_ids[name], main)
            buttons[name] = btn
            btn.SetMinSize((50, 20))
            sbs.Add(btn, 0, wx.ALL, 4)
        self.SetSizerAndFit(sbs)
        box.SetForegroundColour(wx.Colour(153, 245, 198))
        
class NavPanel(wx.Panel):
    def __init__(self, parent, main, buttons):
        super().__init__(parent, size=(220, 30))
        box = wx.StaticBox(self, label="Nav")
        sbs = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        for name in ("Exit","Prev","Next","Enter"):
            btn = SysExButton(self, name, button_ids[name], main)
            btn.SetMinSize((50, 20))
            buttons[name] = btn
            sbs.Add(btn, 0, wx.ALL, 4)
        self.SetSizerAndFit(sbs)
        box.SetForegroundColour(wx.Colour(153, 245, 198))
        
class FKeysPanel(wx.Panel):
    def __init__(self, parent, main):
        super().__init__(parent, size=(350, 30))
        gs = wx.GridSizer(1,6,5,5)
        for i in range(1,7):
            name = f"F{i}"
            btn = SysExButton(self, name, button_ids[name], main)
            btn.SetMinSize((50, 20))
            gs.Add(btn, 0, wx.EXPAND)
        self.SetSizerAndFit(gs)

class ArrowPanel(wx.Panel):
    def __init__(self, parent, main):
        super().__init__(parent, size=(120, 120))
        gs = wx.GridSizer(3,3,5,5)
        pos = {(0,1):"Up",(1,0):"Left",(1,2):"Right",(2,1):"Down"}
        for r in range(3):
            for c in range(3):
                if (r,c) in pos:
                    name = pos[(r,c)]
                    btn  = SysExButton(self, name, button_ids[name], main)
                    btn.SetMinSize((50, 20))
                    gs.Add(btn, 0, wx.EXPAND)
                else:
                    gs.Add((20,20), 0)
        self.SetSizerAndFit(gs)

class NumPadPanel(wx.Panel):
    def __init__(self, parent, main, buttons):
        super().__init__(parent, size=(260, 340))
        grid = wx.GridSizer(5,3,5,5)
        layout = ["Dec","","Inc","1","2","3","4","5","6","7","8","9","+/-","0","Set"]
        for lbl in layout:
            if not lbl:
                grid.Add((35, 20), 0)
            else:
                btn = SysExButton(self, lbl, button_ids[lbl], main)
                btn.SetMinSize((35, 20))
                grid.Add(btn, 0, wx.EXPAND)
                buttons[lbl] = btn
        self.SetSizerAndFit(grid)


# ───── Keyboard-settings dialog (unchanged) ─────────────────────────
class KeyboardSettingsDialog(wx.Dialog):
    def __init__(self, parent, key_bindings):
        super().__init__(parent,
                         title="Keyboard Settings",
                         size=(450, 700),
                         style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        self.key_bindings = key_bindings
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        scroll_pnl = scrolled.ScrolledPanel(self, style=wx.VSCROLL|wx.TAB_TRAVERSAL)
        scroll_pnl.SetupScrolling(scroll_x=False, scroll_y=True)
        rows_sizer = wx.BoxSizer(wx.VERTICAL)
        scroll_pnl.SetSizer(rows_sizer)

        self.choices = {}
        for btn in sorted(button_ids):
            hs = wx.BoxSizer(wx.HORIZONTAL)
            hs.Add(wx.StaticText(scroll_pnl, label=btn), 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)

            choice = wx.Choice(scroll_pnl, choices=KEY_CHOICES)
            curr_name = KEY_NAME_MAP.get(self.key_bindings.get(btn))
            if curr_name in KEY_CHOICES:
                choice.SetStringSelection(curr_name)
            hs.Add(choice, 1, wx.EXPAND)
            rows_sizer.Add(hs, 0, wx.EXPAND|wx.ALL, 2)

            self.choices[btn] = choice

        main_sizer.Add(scroll_pnl, 1, wx.EXPAND|wx.ALL, 10)
        main_sizer.Add(self.CreateButtonSizer(wx.OK|wx.CANCEL),
                       0, wx.ALIGN_CENTER|wx.BOTTOM, 10)

        self.SetSizer(main_sizer)
        self.Layout()

    def apply(self):
        for btn, choice in self.choices.items():
            sel = choice.GetStringSelection()
            for code, nm in KEY_NAME_MAP.items():
                if nm == sel:
                    self.key_bindings[btn] = code
                    break
                
                
# CLICK_SOUND = wx.adv.Sound('click.wav')

# ───── main frame with keyboard integration ─────────────────────────
class FrontPanelFrame(wx.Panel):
    def __init__(self, parent, main):
        super().__init__(parent)
        self.main = main
        panel = self
        # give yourself a default minimum size
        self.SetMinSize((1000, 300))

        self.SetBackgroundColour(wx.Colour("dark grey"))
        # absolute layout
        self.SetSizer(None)

        # keep refs for keyboard dispatch
        self.buttons = {}
        self.key_bindings = default_key_bindings.copy()
        self.do_use_keyboard = False
        self.do_use_scroll = False

        # ─── create all buttons first ───────────────────────────────
        # Master & Disk
        for name,pos in (("Master",(10,30)),("Disk",(10,90))):
            btn = SysExButton(panel, name, button_ids[name], main)
            btn.SetPosition(pos)
            self.buttons[name] = btn

        # grouped panels...
        p = PresetPanel(panel, main, self.buttons);   p.SetPosition((80,10))
        s = SamplePanel(panel, main, self.buttons);   s.SetPosition((80,70))
        a = AssignPanel(panel, main, self.buttons);   a.SetPosition((230,70))
        n = NavPanel(panel, main, self.buttons);      n.SetPosition((440,70))

        aud = SysExButton(panel,"Audition", button_ids["Audit"], main)
        aud.SetPosition((230,30)); self.buttons["Audit"]=aud

        fk = FKeysPanel(panel, main);    fk.SetPosition((320,30))
        # register F-keys if you want shortcuts for them:
        for i in range(1,7):
            lbl = f"F{i}"
            self.buttons[lbl] = fk.FindWindowByLabel(lbl)

        ar = ArrowPanel(panel, main);    ar.SetPosition((700,40))
        # register arrow keys
        for lbl in ("Up","Down","Left","Right"):
            self.buttons[lbl] = ar.FindWindowByLabel(lbl)

        np = NumPadPanel(panel, main, self.buttons);   np.SetPosition((880,10))
        # register numpad keys if desired…
        
    
        self.use_keyboard_btn = wx.ToggleButton(panel, label="Enable Keyboard")
        self.use_keyboard_btn.SetPosition((2,135))
        self.use_keyboard_btn.Bind(wx.EVT_TOGGLEBUTTON , self.on_use_keyboard)
        self.use_keyboard_btn.SetBackgroundColour("medium grey")
        
        self.use_scroll_btn = wx.ToggleButton(panel, label="Enable Scroll")
        self.use_scroll_btn.SetPosition((120,135))
        self.use_scroll_btn.Bind(wx.EVT_TOGGLEBUTTON , self.on_use_mousescroll)
        self.use_scroll_btn.SetBackgroundColour("medium grey")
        

        # ─── now that self.buttons is populated, build accelerators ──
        accel_specs = []
        for name, keycode in self.key_bindings.items():
            btn = self.buttons.get(name)
            if btn:
                accel_specs.append((wx.ACCEL_NORMAL, keycode, btn.GetId()))
        self.SetAcceleratorTable(wx.AcceleratorTable(accel_specs))

        # bind each accelerator to “click” the button
        for btn in self.buttons.values():
            self.Bind(wx.EVT_MENU,
                    lambda evt, b=btn: b.Command(
                        wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED,
                                        b.GetId())),
                    id=btn.GetId())

        # catch all key events for shortcuts (fallback)
        self.Bind(wx.EVT_CHAR_HOOK, self.on_key)
        
        # catch mouse‐wheel
        self.Bind(wx.EVT_MOUSEWHEEL, self.on_wheel)

        # menu → Keyboard Settings…
        # mb = self.Parent.Parent.menu_bar  #wx.MenuBar()
        # m  = wx.Menu()
        # m.Append(wx.ID_PREFERENCES, "Keyboard Settings…")
        # mb.Append(m, "&Settings")
        # self.Parent.Parent.SetMenuBar(mb)
        # self.Parent.Parent.Bind(wx.EVT_MENU, self.open_key_settings, id=wx.ID_PREFERENCES)

        self.Show()
    

    def on_key(self, evt):
        if self.do_use_keyboard == False:
            return
        key = evt.GetKeyCode()
        # print(key)
        # print(self.buttons)
        for name, kc in self.key_bindings.items():
            # print(name, kc)
            if kc == key and name in self.buttons:
                # “press” it
                self.buttons[name].Command(
                    wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED,
                                    self.buttons[name].GetId()))
                return
        evt.Skip()
        
        
    def on_wheel(self, evt):
        if self.do_use_scroll == False:
            return
        delta = evt.GetWheelRotation() // evt.GetWheelDelta()
        val   = delta & 0xFFFF
        lsb, msb = val & 0x7F, (val >> 7) & 0x7F
        # build a SYSEX: [0x18, 0x7F, deviceId=1, hostId=0, ROTARY_EVENT=0x43, page=1, lsb, msb]
        msg_bytes = [0x18, 0x7F, 0x01, 0x00, 0x43, 0x01, lsb, msb]
        # send it straight out
        if self.main.outport:
            self.main.outport.send(mido.Message('sysex', data=msg_bytes))
        # if CLICK_SOUND.IsOk():
        #     CLICK_SOUND.Play(wx.SOUND_ASYNC)
        evt.Skip()

    def open_key_settings(self, _evt):
        # print("open keyboard settings")
        dlg = KeyboardSettingsDialog(self, self.key_bindings)
        if dlg.ShowModal() == wx.ID_OK:
            dlg.apply()
        dlg.Destroy()
        
    def on_use_keyboard(self, evt):
        if self.do_use_keyboard == False:
            self.do_use_keyboard = True
            self.use_keyboard_btn.SetBackgroundColour(wx.Colour(153, 245, 198))
            self.main.ccframe.pc_key_enabled = False
            self.main.ccframe.keyboard_controls.pc_key_toggle.SetBackgroundColour("medium grey")
        else:
            self.do_use_keyboard = False
            self.use_keyboard_btn.SetBackgroundColour("medium grey")
            
    def on_use_mousescroll(self, evt):
        if self.do_use_scroll == False:
            self.do_use_scroll = True
            self.use_scroll_btn.SetBackgroundColour(wx.Colour(153, 245, 198))
        else:
            self.do_use_scroll = False
            self.use_scroll_btn.SetBackgroundColour("medium grey")
        
        
    
class SysExButton(wx.Button):
    def __init__(self, parent, label, button_id, main = None):
        super().__init__(parent, label=label, size=(50, 20))
        self.button_id = button_id
        self.Bind(wx.EVT_BUTTON, self.on_click)
        self.main = main
    def on_click(self, _evt):
        #  18 7F <yourDeviceId> <yourHostId> 51
        press   = [0x18, 0x7F, 0x01, 0x00, 0x40, self.button_id, 0x00, 0x01]
        release = [0x18, 0x7F, 0x01, 0x00, 0x40, self.button_id, 0x00, 0x00]

        self.send(press)
        wx.CallLater(100, lambda: self.send(release))

    def send(self, msg_bytes: bytes):
        # find the top‐level frame/panel that has an `outport`
        
        if self.main.outport:
            print("Pressing Button ", msg_bytes)
            self.main.outport.send(mido.Message('sysex', data=list(msg_bytes)))
        else:
            print("No MIDI out port open – failed to send", msg_bytes)

