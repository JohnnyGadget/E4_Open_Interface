

import wx
import math
import random
from custom_widgets import DraggableNumber
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




# ---------------------------
# Conversion arrays for LFO Rate Display
# ---------------------------
lfounits1 = [0]*24 + [1]*16 + [2]*16 + [3]*16 + [4]*16 + [5]*8 + [6]*8 + [7]*8 + [8]*8 + [9]*4 + [10]*4 + [11]*4 + [12]*2 + [13]*2 + [14]*2 + [15]*2 + [16]*2 + [17]*2 + [18]
lfounits2 = [8,11,15,18,21,25,28,32,35,39,42,46,50,54,58,63,
             67,71,76,80,85,90,94,99,
             4,10,15,20,25,31,37,42,
             48,54,60,67,73,79,86,93,
             0,7,14,21,29,36,44,52,
             60,68,77,85,94,3,12,21,
             31,40,50,60,70,81,91,2,
             13,25,36,48,60,72,84,97,
             10,23,37,51,65,79,94,8,
             24,39,55,71,88,4,21,39,
             57,75,93,12,32,51,71,92,
             13,34,56,78,0,23,47,71,
             95,20,46,71,98,25,52,80,
             9,38,68,99,30,61,93,26,
             60,94,29,65,1,38,76,14]

def conv_lfo_rate(val):
    return f"{lfounits1[val]:2d}.{lfounits2[val]:02d}" if 0 <= val < len(lfounits1) else "??.??"

class LFODisplay(wx.Panel):
    def __init__(self, parent, size=(150,100)):
        super().__init__(parent, size=size)
        self.SetBackgroundColour(wx.Colour("black")) #wx.Colour(37, 56, 37))
        self.rate = 0; self.shape = 0; self.delay = 0; self.phase_control = 0; self.clock_sync = False
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.dc = None
        self.SetMinSize(size)  # <- Lock minimum size
        self.SetMaxSize(size) 
        self.SetDoubleBuffered(True)
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)



    def update_display(self, rate, shape, delay, phase_control, clock_sync):
        self.rate, self.shape, self.delay, self.phase_control, self.clock_sync = rate, shape, delay, phase_control, clock_sync
        self.Refresh()

    def OnPaint(self, event):
        dc = wx.PaintDC(self); dc.Clear()
        w,h = self.GetSize()
        if w<10 or h<10: return

        baseline = h/2
        delay_ofs = (float(self.delay)/127.0)*(w*0.2)
        draw_w = w - delay_ofs

        # dashed yellow delay line
        dc.SetPen(wx.Pen(wx.Colour("yellow"),1,wx.PENSTYLE_SHORT_DASH))
        dc.DrawLine(0,int(baseline),int(delay_ofs),int(baseline))

        # if clock sync is on, draw a little indicator
        if self.clock_sync:
            dc.SetBrush(wx.Brush(wx.Colour("orange")))
            dc.DrawCircle(w-w+15,15,6)

        phase_ofs = (float(self.phase_control)/100.0)*(2*math.pi)

        # if self.shape in (5,6,7):
        #     self.draw_note_waveform(dc, draw_w, delay_ofs, ["C","E","D","F"], phase_ofs, self.rate)
        if self.shape==16:
            self.draw_sample_and_hold(dc, draw_w, delay_ofs, self.rate, phase_ofs)
        else:
            self.draw_continuous_waveform(dc, draw_w, delay_ofs, self.rate, self.shape, phase_ofs)

    def draw_note_waveform(self, dc, draw_w, delay_ofs, notes, phase_ofs, rate):
        w, h = self.GetSize()
        y0, y1 = 10, h - 10
        note_map = {"C":12,"C#":11,"DB":11,"D":10,"D#":9,"EB":9,
                    "E":8,"F":7,"F#":6,"GB":6,"G":5,"G#":4,"AB":4,
                    "A":3,"A#":2,"BB":2,"B":1}
        vals = []
        for n in notes:
            try: vals.append(float(n))
            except: vals.append(note_map.get(n.upper(),0))
        N = len(vals)
        gap = (draw_w * (rate / 127.0)) / (N-1) if N>1 else draw_w

        pts = []
        for i, v in enumerate(vals):
            x = delay_ofs + gap * i + phase_ofs
            y = y0 + ((12 - v)/12.0)*(y1-y0)
            pts.append((x,y))

        if pts:
            pen = wx.Pen(wx.Colour("red"), 2, wx.PENSTYLE_SHORT_DASH)
            dc.SetPen(pen)
            dc.DrawLine(0, y1, int(pts[0][0]), int(pts[0][1]))

        pen = wx.Pen(wx.Colour("blue"), 2)
        dc.SetPen(pen)
        for (x0,y0),(x1,y1) in zip(pts, pts[1:]):
            dc.DrawLine(int(x0),int(y0),int(x1),int(y0))
            dc.DrawLine(int(x1),int(y0),int(x1),int(y1))

    def draw_continuous_waveform(self, dc, draw_w, delay_ofs, rate, shape, phase_ofs):
        w, h = self.GetSize()
        baseline = h / 2
        cycles = 1 + (rate / 127.0) * 9.5
        patterns = {
            8: [0,12], 9: [0,7,12,7], 10:[0,5,7,5], 11:[0,2,0,2]
        }

        pts = []
        for i in range(500):
            t = i/500.0
            x = delay_ofs + t*draw_w
            phase = t * cycles * 2*math.pi + phase_ofs
            frac = (phase % (2*math.pi)) / (2*math.pi)
            # print(shape)
            if shape == 0:
                yv = math.sin(phase)
            elif shape == 1:
                saw = 2*(phase/(2*math.pi)-math.floor(phase/(2*math.pi)+0.5))
                yv = 2*abs(saw)-1
            elif shape == 2:
                yv = 2*(phase/(2*math.pi)-math.floor(phase/(2*math.pi)+0.5))
            elif shape == 3:
                yv = 1 if math.sin(phase)>=0 else -1
            elif shape in (4,5,6,7):
                duty = {4:0.33,5:0.25,6:0.16,7:0.12}[shape]
                yv = 1 if frac<duty else -1
            elif shape in patterns:
                pat = patterns[shape]
                repeats = 1 + int((rate/127.0) * 8)  # 1 to 9 repeats based on Rate slider  # <-- how many times you want the pattern to repeat per screen
                pat_len = len(pat)
                idx = int(frac * pat_len * repeats)
                yv = (pat[idx % pat_len] / 6.0) - 1

            elif shape == 12:
                yv = (math.sin(phase)+0.5*math.sin(2*phase))/1.5
            elif shape == 13:
                yv = (math.sin(phase)+0.33*math.sin(3*phase)+0.2*math.sin(5*phase))/1.53
            elif shape == 14:
                yv = 0.8*math.sin(phase)+0.2*random.uniform(-1,1)
            elif shape == 15:
                yv = 1 if int(frac*16)%2==0 else -1
            else:
                yv = math.sin(phase)

            y = baseline - yv*(baseline-10)
            pts.append((x,y))

        pen = wx.Pen(wx.Colour("green"), 2)
        dc.SetPen(pen)
        for (x0,y0),(x1,y1) in zip(pts, pts[1:]):
            dc.DrawLine(int(x0),int(y0),int(x1),int(y1))

    def draw_sample_and_hold(self, dc, draw_w, delay_ofs, rate, phase_ofs):
        w, h = self.GetSize()
        baseline = h - 10
        steps = max(1, int((rate/127.0)*20))
        sw = draw_w/steps

        pts = []
        for i in range(steps+1):
            x = delay_ofs + i*sw + (phase_ofs/(2*math.pi))*sw
            v = random.uniform(-1,1)
            y = 10 + ((v+1)/2)*(h-20)
            pts.append((x,y))

        pen = wx.Pen(wx.Colour("orange"), 2)
        dc.SetPen(pen)
        for (x0,y0),(x1,y1) in zip(pts, pts[1:]):
            dc.DrawLine(int(x0),int(y0),int(x1),int(y0))
            dc.DrawLine(int(x1),int(y0),int(x1),int(y1))


class LFO1(wx.Panel):
    def __init__(self, parent, main, voice_dict):
        super().__init__(parent)
        # self.SetBackgroundColour()
        self.main = main
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.display_sizer = wx.BoxSizer(wx.VERTICAL)
        self.display = LFODisplay(self)

        self.display_sizer.Add(self.display, 0, wx.ALL, 10)
 
        main_sizer.Add(self.display_sizer, 0, wx.ALL, 10)
        
        grid_sizer = wx.GridSizer(rows=5, cols=2, hgap=5, vgap=10)
        
        
        self.label0 = wx.StaticText(self, label="LFO1 Shape")

        lfo_shapes = ["Sine","Triangle","Sawtooth","Square",
                "33% Pulse","25% Pulse","16% Pulse","12% Pulse",
                "Octaves","5th+Oct","Sus4","Neener",
                "Sin+2","Sin+3+5","Sin+Noise","16th","S+H"]
        self.lfo_shape_selector = wx.ComboBox(self, id = 106, choices=lfo_shapes, style=wx.CB_READONLY,size=(100, -1))
        self.lfo_shape_selector.SetSelection(voice_dict["params"]["E4_VOICE_LFO_SHAPE"])
        self.lfo_shape_selector.Bind(wx.EVT_COMBOBOX, self.onChange)
        # main.controls.combo_by_id[106] = self.lfo_shape_selector



        self.label1 = wx.StaticText(self, label="Clock Sync")
        self.label2 = wx.CheckBox(self, id = 109)
        self.label2.SetValue(bool(voice_dict["params"]["E4_VOICE_LFO_SYNC"]))
        self.label2.Bind(wx.EVT_CHECKBOX, self.onChange)
        # main.controls.check_by_id[109] = self.label2
        
        self.label3 = wx.StaticText(self, label="Rate")
        self.label4 = DraggableNumber(self, id = 105, value = voice_dict["params"]["E4_VOICE_LFO_RATE"], min_val = 0, max_val = 127, callback=self.onChange)
        # main.controls.dragger_by_id[105] = self.label4

        self.label5 = wx.StaticText(self, label="Delay")
        self.label6 = DraggableNumber(self, id = 107, value = voice_dict["params"]["E4_VOICE_LFO_DELAY"], min_val = 0, max_val = 127, callback=self.onChange)
        # main.controls.dragger_by_id[107] = self.label6
        
        self.label7 = wx.StaticText(self, label="Variation")
        self.label8 = DraggableNumber(self, id = 108, value = voice_dict["params"]["E4_VOICE_LFO_VAR"], min_val = 0, max_val = 100, callback=self.onChange)
        # main.controls.dragger_by_id[108] = self.label8
        
        


        labels = [
           self.label0, self.lfo_shape_selector, self.label1, self.label2, self.label3, self.label4, 
           self.label5, self.label6, self.label7, self.label8
        ]
        

        for label in labels:
            # label.SetBackgroundColour(wx.Colour(176, 186, 160, 127))
            label.SetMinSize((80, 20))
            grid_sizer.Add(label, flag=wx.EXPAND)
            
        
            
        seg1 = [self.label2, self.label4, self.label6, self.label8] 
           
        for label in seg1:
            label.SetBackgroundColour(wx.Colour(greencontrol)) 
            
        main_sizer.Add(grid_sizer, flag=wx.ALL, border=10)
        self.SetSizer(main_sizer)
        

    def onChange(self, event):
       
        rate = self.label4.value
        delay = self.label6.value
        phase = self.label8.value
        shape = self.lfo_shape_selector.GetSelection()  # <-- FIXED HERE
        sync  = self.label2.GetValue()


        self.label3.SetLabel(f"Rate: ({conv_lfo_rate(rate)})")
        self.label5.SetLabel(f"Delay: {delay}")
        self.label7.SetLabel(f"Variation: {phase}%")
        self.display.update_display(rate, shape, delay, phase, sync)
        
        ctrl = event.GetEventObject()   
        if ctrl.Id == 109:
            checked = event.GetInt()
            if checked == 1:
                checked = 0
            else:
                checked = 1
            self.main.send_parameter_edit(109, checked)
        elif ctrl.Id == 106:
            idx = ctrl.GetSelection()
            self.main.send_parameter_edit(106, idx)
        else:
            self.main.send_parameter_edit(ctrl.Id, ctrl.value)
            
    def update(self):
        rate = self.label4.value
        delay = self.label6.value
        phase = self.label8.value
        shape = self.lfo_shape_selector.GetSelection()  # <-- FIXED HERE
        sync  = self.label2.GetValue()


        self.label3.SetLabel(f"Rate: ({conv_lfo_rate(rate)})")
        self.label5.SetLabel(f"Delay: {delay}")
        self.label7.SetLabel(f"Variation: {phase}%")
        self.display.update_display(rate, shape, delay, phase, sync)
        


    
        
class LFO2(wx.Panel):
    def __init__(self, parent, main, voice_dict):
        super().__init__(parent)
        # self.SetBackgroundColour()
        self.main = main
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.display_sizer = wx.BoxSizer(wx.VERTICAL)
        self.display = LFODisplay(self)

        self.display_sizer.Add(self.display, 0, wx.ALL, 10)
 
        main_sizer.Add(self.display_sizer, 0, wx.ALL, 10)
        
        grid_sizer = wx.GridSizer(rows=7, cols=2, hgap=5, vgap=10)
        
        
        self.label0 = wx.StaticText(self, label="LFO2 Shape")

        lfo_shapes = ["Sine","Triangle","Sawtooth","Square",
                "33% Pulse","25% Pulse","16% Pulse","12% Pulse",
                "Octaves","5th+Oct","Sus4","Neener",
                "Sin+2","Sin+3+5","Sin+Noise","16th","S+H"]
        self.lfo_shape_selector = wx.ComboBox(self, id = 111, choices=lfo_shapes,style=wx.CB_READONLY,size=(100, -1))
        self.lfo_shape_selector.SetSelection(voice_dict["params"]["E4_VOICE_LFO2_SHAPE"])
        self.lfo_shape_selector.Bind(wx.EVT_COMBOBOX, self.onChange)
        # main.controls.combo_by_id[111] = self.lfo_shape_selector


        # Create all 76 labels individually and add them
        self.label1 = wx.StaticText(self, label="Clock Sync")
        self.label2 = wx.CheckBox(self, id = 114)
        self.label2.SetValue(bool(voice_dict["params"]["E4_VOICE_LFO2_SYNC"]))
        self.label2.Bind(wx.EVT_CHECKBOX, self.onChange)
        # main.controls.check_by_id[114] = self.label2
        
        self.label3 = wx.StaticText(self, label="Rate")
        self.label4 = DraggableNumber(self, id = 110, value = voice_dict["params"]["E4_VOICE_LFO2_RATE"], min_val = 0, max_val=127, callback = self.onChange)
        # main.controls.dragger_by_id[110] = self.label4
        
        self.label5 = wx.StaticText(self, label="Delay")
        self.label6 = DraggableNumber(self, id = 112, value = voice_dict["params"]["E4_VOICE_LFO2_DELAY"], min_val = 0, max_val=127, callback = self.onChange)
        # main.controls.dragger_by_id[112] = self.label6
        
        self.label7 = wx.StaticText(self, label="Variation %")
        self.label8 = DraggableNumber(self, id = 113, value = voice_dict["params"]["E4_VOICE_LFO2_VAR"], min_val = 0, max_val=100, callback = self.onChange)
        # main.controls.dragger_by_id[113] = self.label8
        
        self.label9 = wx.StaticText(self, label="Lag1")
        self.label10 = DraggableNumber(self, id = 115, value = voice_dict["params"]["E4_VOICE_LFO2_OP0_PARM"], min_val = 0, max_val=10, callback = self.onChange)
        # main.controls.dragger_by_id[115] = self.label10
        
        self.label11 = wx.StaticText(self, label="Lag2")
        self.label12 = DraggableNumber(self, id = 116, value = voice_dict["params"]["E4_VOICE_LFO2_OP1_PARM"], min_val = 0, max_val=10, callback = self.onChange)
        # main.controls.dragger_by_id[116] = self.label12


        labels = [self.label0, self.lfo_shape_selector,
           self.label1, self.label2, self.label3, self.label4, 
           self.label5, self.label6, self.label7, self.label8, 
           self.label9, self.label10, self.label11, self.label12
        ]
        

        for label in labels:
            # label.SetBackgroundColour(wx.Colour(176, 186, 160, 127))
            label.SetMinSize((80, 20))
            grid_sizer.Add(label, flag=wx.EXPAND)
            
        
            
        seg1 = [self.label2, self.label4, self.label6, self.label8, self.label10, self.label12] 
           
        for label in seg1:
            label.SetBackgroundColour(wx.Colour(greencontrol)) 
            
        main_sizer.Add(grid_sizer, flag=wx.ALL, border=10)
        self.SetSizer(main_sizer)
        

    def onChange(self, event):
       
        rate = self.label4.value
        delay = self.label6.value
        phase = self.label8.value
        shape = self.lfo_shape_selector.GetSelection()  # <-- FIXED HERE
        sync  = self.label2.GetValue()


        self.label3.SetLabel(f"Rate: ({conv_lfo_rate(rate)})")
        self.label5.SetLabel(f"Delay: {delay}")
        self.label7.SetLabel(f"Variation: {phase}%")
        self.display.update_display(rate, shape, delay, phase, sync)
        ctrl = event.GetEventObject()
       
            
        if ctrl.Id == 114:
            checked = event.GetInt()
            if checked == 1:
                checked = 0
            else:
                checked = 1
            self.main.send_parameter_edit(114, checked)
        elif ctrl.Id == 111:
            idx = ctrl.GetSelection()
            self.main.send_parameter_edit(111, idx)
        else:
            self.main.send_parameter_edit(ctrl.Id, ctrl.value)

    def update(self):
        rate = self.label4.value
        delay = self.label6.value
        phase = self.label8.value
        shape = self.lfo_shape_selector.GetSelection()  # <-- FIXED HERE
        sync  = self.label2.GetValue()


        self.label3.SetLabel(f"Rate: ({conv_lfo_rate(rate)})")
        self.label5.SetLabel(f"Delay: {delay}")
        self.label7.SetLabel(f"Variation: {phase}%")
        self.display.update_display(rate, shape, delay, phase, sync)


