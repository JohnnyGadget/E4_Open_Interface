
import wx
import mido
class MidiConnectPopup(wx.Frame):
    def __init__(self, parent=None, callback=None):
        
        super().__init__(parent, title="Open Midi Ports", size=(400, 200),style = wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP)
        self.parent = parent
        self.callback = callback
        self.input_port_name = None
        self.output_port_name = None

        input_names = mido.get_input_names()
        output_names = mido.get_output_names()
        
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        instruct_box = wx.BoxSizer(wx.HORIZONTAL)
        instruct_box.Add(wx.StaticText(panel, label="On the E4 set the Device ID to 1 and Midi Channel to 1"), 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 8)
        sizer.Add(instruct_box, 0, wx.EXPAND|wx.ALL, 10)
        hbox_in = wx.BoxSizer(wx.HORIZONTAL)
        hbox_in.Add(wx.StaticText(panel, label="MIDI Input Port:   "), 0, wx.RIGHT, 8)
        self.input_dd = wx.ComboBox(panel, choices=input_names, style=wx.CB_READONLY)
        self.input_dd.Bind(wx.EVT_COMBOBOX, self.on_select_input)
        self.input_dd.SetMinSize((200, -1))
        self.input_dd.SetMaxSize((200, -1))
        hbox_in.Add(self.input_dd, 1, wx.EXPAND)
        sizer.Add(hbox_in, 0, wx.EXPAND|wx.ALL, 10)

        hbox_out = wx.BoxSizer(wx.HORIZONTAL)
        hbox_out.Add(wx.StaticText(panel, label="MIDI Output Port:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 8)
        self.output_dd = wx.ComboBox(panel, choices=output_names, style=wx.CB_READONLY)
        self.output_dd.Bind(wx.EVT_COMBOBOX, self.on_select_output)
        self.output_dd.SetMinSize((200, -1))
        self.output_dd.SetMaxSize((200, -1))
        hbox_out.Add(self.output_dd, 1, wx.EXPAND)
        sizer.Add(hbox_out, 0, wx.EXPAND|wx.ALL, 10)

        hbox_send = wx.BoxSizer(wx.HORIZONTAL)
        hbox_send.Add(wx.StaticText(panel, label="Device ID (0–127):"), 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 8)
        self.device_entry = wx.TextCtrl(panel, value="1", style=wx.TE_PROCESS_ENTER)
        self.device_entry.SetMaxLength(3)
        self.device_entry.SetMinSize((40, -1))
        self.device_entry.SetMaxSize((40, -1))
        hbox_send.Add(self.device_entry, 0, wx.RIGHT, 8)
        hbox_send.Add((60,0))
        self.send_button = wx.Button(panel, label="Connect to E4")
        self.send_button.Bind(wx.EVT_BUTTON, self.on_connect_midi)
        hbox_send.Add(self.send_button, 0)
        sizer.Add(hbox_send, 0, wx.EXPAND|wx.ALL, 10)

        panel.SetSizer(sizer)
        self.CentreOnParent()
        self.Show()

    def on_select_input(self, event):
        self.input_port_name = event.GetString()
        self.parent.in_name = self.input_port_name
        


    def on_select_output(self, event):
        self.output_port_name = event.GetString()
        self.parent.out_name = self.output_port_name


    def on_connect_midi(self, event):
        device_id = int(self.device_entry.GetValue())
        device_id = int(self.device_entry.GetValue())
        print(self.input_port_name, self.output_port_name, device_id)
        self.callback(self.input_port_name, self.output_port_name, device_id)
        self.Close()









