import wx

class InfoPopup(wx.Frame):
    def __init__(self, parent, title, message):
        super().__init__(parent, title=title, size=(400, 200),style = wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP)
        print(message)
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Optional: Info Icon
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(panel, label=message)
        text.Wrap(300) 
        hbox.Add(text, 0, wx.ALIGN_CENTER_VERTICAL)
        vbox.Add(hbox, 0, wx.ALL, 15)

        # OK Button
        btn = wx.Button(panel, label="OK")
        btn.Bind(wx.EVT_BUTTON, self.on_ok)
        vbox.Add(btn, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)

        panel.SetSizer(vbox)
        # self.Fit()
        self.CentreOnParent()
        self.Show()
    
    def on_ok(self, event):
        self.Destroy()

# Usage example:
# Replace this call:
# wx.MessageBox("E4 Open Interface", "Author : JohnnyGadget \nE4 Open Interface v.1111", wx.OK | wx.ICON_INFORMATION)
# def show_info_popup(parent=None):
#     popup = InfoPopup(parent, "E4 Open Interface", "Author: JohnnyGadget\nE4 Open Interface v.1111")
    
#     popup.Show()

# # If running standalone for test:
# if __name__ == "__main__":
#     app = wx.App(False)
#     show_info_popup()
#     app.MainLoop()
