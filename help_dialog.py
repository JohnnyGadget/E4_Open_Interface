import wx
import wx.html
import os
class HelpDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="Help", size=(600, 800))
        
        # create an HTML control — it scrolls automatically
        html = wx.html.HtmlWindow(self)
        # base_path = os.path.abspath(os.path.dirname(__file__))
        # build your HTML with paragraphs, bullet lists, and images
        # NOTE: make sure help1.png, help2.png, help3.png are in your cwd
        content = """
        <html>
        <body style="font-family: sans-serif;">

        <h2>1. Getting Started</h2>
        <p>On first launch a popup will appear where you can slect your midi ports and Device Id.\n
            Select your midi ports and device ID then press the "Connect" button</p>
        
        <br/><br/>
        
        <img src="images/open_ports.png" width="386" height = "193"/>
        
        <br/><br/><br/><br/>
        
        <p>The E4 should connect immediately and a popup will confirm your E4 Model and EOS version.</p>
        <p>Note : E4 Open Interface will save your chosen midi port names so the next time you run the\n
            software it will automatically connect to the E4. If you ever need to select different midi ports\n
            click the "Connect E4 (Midi)" button and the midi port selection popup will appear. </p>
        
        <br/><br/>
        
        <img src="images/id_response.png" width="352" height = "162"/>
        <br/><br/><br/><br/>
        <h2>2. "Get Preset" Button.</h2>
        <p>
            Enter the Preset Number you want to edit and click the "Get Preset" button.
            \nThe UI parameter control tabs will populate in about +-5 seconds.
        </p>
        <br/><br/>
        <img src="images/get_preset.png" width="273" height = "170" />
        <br/><br/><br/><br/>
        <h2>3. Editing Preset Parameters</h2>
        <p>
            The E4 is live updated as you edit the parameters in the E4 Open Interface. To save your edits to the preset, save the preset on the E4. No preset data is saved in the software.
        </p>
        <br/><br/>
        <img src="images/voice_edit.png" width="560" height = "195"/>
        <img src="images/voices.png" width="560" height = "192"/>
        <img src="images/filter.png" width="560" height = "478"/>
        <img src="images/lfos.png" width="560" height = "554"/>
        <img src="images/cords.png" width="560" height = "487"/>
        <img src="images/master_effects.png" width="560" height = "321"/>
        <br/><br/><br/><br/>
        
        <h2>5. The Pc keyboard and mouse can control the front panel of the E4.</h2>
        <p>
            Press the 'Enable Keyboard" button or the 'Enable Scroll" on the 'front panel'.\n
            Scrolling the mouse wheel while the mouse pointer hovers over the front panel\n
            box will scroll the highlighted value on the E4.
        </p>
        <br/><br/>
        <img src="images/use_keyboard.png" width="560" height = "273"/>
        <img src="images/front_panel.png" width="560" height = "90"/>
        <br/><br/><br/><br/>
        <h2>3. KEY MAP .</h2>
        <ul>
        <li>M = 'Master'</li>
        <li>D = 'Disk'</li>
        <li>P = 'Preset Manage'</li>
        <li>E = 'Preset Edit'</li>
        <li>S = 'Sample Manage'</li>
        <li>G = 'Sample Edit'</li>
        <li>A = 'Audition'</li>
        <li>Z = 'Assign 1'</li>
        <li>X = 'Assign 2'</li>
        <li>C = 'Assign 3'</li>
        <li>&lt; = 'Previous'</li>
        <li>&gt; = 'Next'</li>
        <li>up = "Up"</li>
        <li>down = "Down"</li>
        <li>left = "Left"</li>
        <li>right = "Right"</li>
        <li>enter = "Enter"</li>
        <li>backspace = "Exit"</li>
        <li>F1 = "F1"</li>
        <li>F2 = "F2"</li>
        <li>F3 = "F3"</li>
        <li>F4 = "F4"</li>
        <li>F5 = "F5"</li>
        <li>F6 = "F6"</li>
        <li>0 = "0"</li>
        <li>1 = "1"</li>
        <li>2 = "2"</li>
        <li>3 = "3"</li>
        <li>4 = "4"</li>
        <li>5 = "5"</li>
        <li>6 = "6"</li>
        <li>7 = "7"</li>
        <li>8 = "8"</li>
        <li>9 = "9"</li>
        <li>' = "+/-"</li>
        <li>/ = "Set"</li>
        <li>- = "Dec"</li>
        <li>+ = "Inc"</li>
        </ul>
        <br/><br/><br/><br/>
        <h2>4. Bonus Features... A Metronome! A CC controller panel with 128 CCs! A midi keyboard that can even play chords!</h2>
        <p>
            Just because it's awesome to have this stuff on hand. Keep your CC controllers in order by giving them custom names. The names are saved on exit and automatically restored the next time E4 Open Interface is opened.
        </p>
        <br/><br/>
        
        <img src="images/midictrls.png" width="560" height = "315"/>
        <img src="images/midictrls_panel.png" width="560" height = "397"/>
        <br/><br/><br/><br/>
        </body>
        </html>
        """
        html.SetPage(content)

        # layout
        s = wx.BoxSizer(wx.VERTICAL)
        s.Add(html, 1, wx.EXPAND|wx.ALL, 10)
        self.SetSizer(s)
        self.Layout()