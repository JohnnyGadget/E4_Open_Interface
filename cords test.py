import wx
import mido
from mido import Message


class SpinnerDemo(wx.Frame):
    def __init__(self):
        super().__init__(None, title="SpinCtrl Demo", size=(300, 200))
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.outport = mido.open_output('UMC1820 MIDI Out 1')
        # Create a SpinCtrl (range 0–127, starting at 60)
        self.spin = wx.SpinCtrl(panel, value="0", min=0, max=1000)
        self.spin.SetMinSize((100, 30))
        sizer.Add(self.spin, 0, wx.CENTER | wx.ALL, 20)
        self.device_id = 1
        # Bind the EVT_SPINCTRL event to a handler
        self.spin.Bind(wx.EVT_SPINCTRL, self.on_spin)

        panel.SetSizer(sizer)
        self.Centre()
        self.Show()

    def on_spin(self, event):
        value = event.GetInt()
        param = 130
        self.send_parameter_edit(130, value)
        # print(f"SpinCtrl value: {value}")
        
    def send_parameter_edit(self, param_id: int, value: int):
        # print(param_id, value)

        param_lsb = param_id & 0x7F
        param_msb = (param_id >> 7) & 0x7F
        value_lsb = value & 0x7F
        value_msb = (value >> 7) & 0x7F

        # Data to checksum over
        data_bytes = [param_lsb, param_msb, value_lsb, value_msb]

        # Checksum: 1's complement of the sum, AND 0x7F to keep it 7-bit
        checksum = (~sum(data_bytes)) & 0x7F
        # print(data_bytes)
        sysex = [

            0x18,         # E-MU Manufacturer ID
            0x21,         # Product ID (E4)
            self.device_id,    # Device ID
            0x55,         # Special Editor designator
            0x01,         # Command: Parameter Value Edit
            0x02,         # Byte count: 2 pairs
            param_lsb,
            param_msb,
            value_lsb,
            value_msb,
            checksum

        ]
        msg = Message('sysex', data=sysex)
        # self.outport.send(msg)
        self.outport.send(msg)  

if __name__ == "__main__":
    app = wx.App(False)
    SpinnerDemo()
    app.MainLoop()
