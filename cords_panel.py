import wx
from custom_widgets import DraggableNumber
from functools import partial



yellow = (245, 243, 187, 0)
green1 = (147, 245, 161, 0)
greencontrol = (153, 245, 198, 0)
greenlight = (219, 245, 214, 0)
blue1 = (152, 245, 228, 0)
bluepowder = (152, 231, 245, 0)   



SOURCE_OPTIONS = {
    0:   "Off",
    4:   "XfdRnd (Crossfade Random)",
    8:   "Key+ (Key 0…127)",
    9:   "Key~ (Key –64…+63)",
    10:  "Vel+ (Velocity 0…127)",
    11:  "Vel~ (Velocity –64…+63)",
    12:  "Vel< (Velocity –127…0)",
    13:  "RlsVel (Release Velocity)",
    14:  "Gate",
    16:  "PitWl (Pitch Wheel)",
    17:  "ModWl (Mod Wheel)",
    18:  "Press (Pressure)",
    19:  "Pedal",
    20:  "MidiA",
    21:  "MidiB",
    22:  "FtSw1 (Foot Switch 1)",
    23:  "FtSw2 (Foot Switch 2)",
    24:  "Ft1FF (Flip‑Flop Foot Switch 1)",
    25:  "Ft2FF (Flip‑Flop Foot Switch 2)",
    26:  "MidiVl (Midi Volume Ctr 7)",
    27:  "MidPn (Midi Pan Ctr 10)",
    32:  "Midi C",
    33:  "Midi D",
    34:  "Midi E",
    35:  "Midi F",
    36:  "Midi G",
    37:  "Midi H",
    38:  "Thumb",
    39:  "ThmFF",
    40:  "Midi I",
    41:  "Midi J",
    42:  "Midi K",
    43:  "Midi L",
    48:  "KeyGld (Key Glide)",
    72:  "VEnv+ (Volume Env 0…127)",
    73:  "VEnv~ (Volume Env –64…+63)",
    74:  "VEnv< (Volume Env –127…0)",
    80:  "FEnv+ (Filter Env 0…127)",
    81:  "FEnv~ (Filter Env –64…+63)",
    82:  "FEnv< (Filter Env –127…0)",
    88:  "AEnv+ (Aux Env 0…127)",
    89:  "AEnv~ (Aux Env –64…+63)",
    90:  "AEnv< (Aux Env –127…0)",
    96:  "Lfo1~",
    97:  "Lfo1+",
    98:  "White (White Noise)",
    99:  "Pink (Pink Noise)",
    100: "kRand1 (kRandom 1)",
    101: "kRand2 (kRandom 2)",
    104: "Lfo2~",
    105: "Lfo2+",
    106: "Lag0in (Summing Amp Out)",
    107: "Lag0",
    108: "Lag1in (Summing Amp Out)",
    109: "Lag1",
    144: "CkDwhl (Clock Double Whole Note)",
    145: "CkWhle (Clock Whole Note)",
    146: "CkHalf (Clock Half Note)",
    147: "CkQtr (Clock Quarter Note)",
    148: "Ck8th (Clock Eighth Note)",
    149: "Ck16th (Clock Sixteenth Note)",
    160: "DC (DC Offset)",
    161: "Sum (Summing Amp)",
    162: "Switch",
    163: "Abs (Absolute Value)",
    164: "Diode",
    165: "FlipFlop",
    166: "Quantiz (Quantizer)",
    167: "Gain4X"
}


SOURCE_OPTIONS_INDEX_REV = {
    0:0,
    4:1,
    8:2,
    9:3,
    10:4,
    11:5,
    12:6,
    13:7,
    14:8,
    16:9,
    17:10,
    18:11,
    19:12,
    20:13,
    21:14,
    22:15,
    23:16,
    24:17,
    25:18,
    26:19,
    27:20,
    32:21,
    33:22,
    34:23,
    35:24,
    36:25,
    37:26,
    38:27,
    39:28,
    40:29,
    41:30,
    42:31,
    43:32,
    48:33,
    72:34,
    73:35,
    74:36,
    80:37,
    81:38,
    82:39,
    88:40,
    89:41,
    90:42,
    96:43,
    97:44,
    98:45,
    99:46,
    100:47,
    101:48,
    104:49,
    105:50,
    106:51,
    107:52,
    108:53,
    109:54,
    144:55,
    145:56,
    146:57,
    147:58,
    148:59,
    149:60,
    160:61,
    161:62,
    162:63,
    163:64,
    164:65,
    165:66,
    166:67,
    167:68
}
SOURCE_OPTIONS_INDEX = {
    0: 0,
    1: 4,
    2: 8,
    3: 9,
    4: 10,
    5: 11,
    6: 12,
    7: 13,
    8: 14,
    9: 16,
    10: 17,
    11: 18,
    12: 19,
    13: 20,
    14: 21,
    15: 22,
    16: 23,
    17: 24,
    18: 25,
    19: 26,
    20: 27,
    21: 32,
    22: 33,
    23: 34,
    24: 35,
    25: 36,
    26: 37,
    27: 38,
    28: 39,
    29: 40,
    30: 41,
    31: 42,
    32: 43,
    33: 48,
    34: 72,
    35: 73,
    36: 74,
    37: 80,
    38: 81,
    39: 82,
    40: 88,
    41: 89,
    42: 90,
    43: 96,
    44: 97,
    45: 98,
    46: 99,
    47: 100,
    48: 101,
    49: 104,
    50: 105,
    51: 106,
    52: 107,
    53: 108,
    54: 109,
    55: 144,
    56: 145,
    57: 146,
    58: 147,
    59: 148,
    60: 149,
    61: 160,
    62: 161,
    63: 162,
    64: 163,
    65: 164,
    66: 165,
    67: 166,
    68: 167,
}


DEST_OPTIONS = {
    0:   "Off",
    8:   "KeySust",
    47:  "FinePtch",
    48:  "Pitch",
    49:  "Glide",
    50:  "ChrsAmt (Chorus Amount)",
    51:  "ChrsITD (Chorus Position ITD)",
    52:  "SStart (Sample Start)",
    53:  "SLoop (Sample Loop)",
    54:  "SRetrig (Sample Retrigger)",
    56:  "FilFreq (Filter Frequency)",
    57:  "FilRes (Filter Resonance)",
    64:  "AmpVol (Amplifier Volume)",
    65:  "AmpPan (Amplifier Pan)",
    66:  "AmpXfd (Amplifier Crossfade)",
    68:  "SndMain",
    69:  "SndAux1",
    70:  "SndAux2",
    71:  "SndAux3",
    72:  "VEnvRts (Volume Env Rates)",
    73:  "VEnvAtk (Volume Env Attack)",
    74:  "VEnvDcy (Volume Env Decay)",
    75:  "VEnvRls (Volume Env Release)",
    80:  "FEnvRts (Filter Env Rates)",
    81:  "FEnvAtk (Filter Env Attack)",
    82:  "FEnvDcy (Filter Env Decay)",
    83:  "FEnvRls (Filter Env Release)",
    86:  "FEnvTrig (Filter Env Trigger)",
    88:  "AEnvRts (Aux Env Rates)",
    89:  "AEnvAtk (Aux Env Attack)",
    90:  "AEnvDcy (Aux Env Decay)",
    91:  "AEnvRls (Aux Env Release)",
    94:  "AEnvTrig (Aux Env Trigger)",
    96:  "Lfo1Rt (LFO 1 Rate)",
    97:  "Lfo1Trig (LFO 1 Trigger)",
    104: "Lfo2Rt (LFO 2 Rate)",
    105: "Lfo2Trig (LFO 2 Trigger)",
    106: "Lag0in",
    108: "Lag1in",
    161: "Sum (Summing Amp)",
    162: "Switch",
    163: "Abs (Absolute Value)",
    164: "Diode",
    165: "FlipFlop",
    166: "Quantize",
    167: "Gain4X",
    168: "C00Amt (Cord 0 Amount)",
    169: "C01Amt (Cord 1 Amount)",
    170: "C02Amt (Cord 2 Amount)",
    171: "C03Amt (Cord 3 Amount)",
    172: "C04Amt (Cord 4 Amount)",
    173: "C05Amt (Cord 5 Amount)",
    174: "C06Amt (Cord 6 Amount)",
    175: "C07Amt (Cord 7 Amount)",
    176: "C08Amt (Cord 8 Amount)",
    177: "C09Amt (Cord 9 Amount)",
    178: "C10Amt (Cord 10 Amount)",
    179: "C11Amt (Cord 11 Amount)",
    180: "C12Amt (Cord 12 Amount)",
    181: "C13Amt (Cord 13 Amount)",
    182: "C14Amt (Cord 14 Amount)",
    183: "C15Amt (Cord 15 Amount)",
    184: "C16Amt (Cord 16 Amount)",
    185: "C17Amt (Cord 17 Amount)",
    186: "C18Amt (Cord 18 Amount)",
    187: "C19Amt (Cord 19 Amount)",
    188: "C20Amt (Cord 20 Amount)",
    189: "C21Amt (Cord 21 Amount)",
    190: "C22Amt (Cord 22 Amount)",
    191: "C23Amt (Cord 23 Amount)",
}

DEST_OPTIONS_INDEX_REV = {
    0:0,
    8:1,
    47:2,
    48:3,
    49:4,
    50:5,
    51:6,
    52:7,
    53:8,
    54:9,
    56:10,
    57:11,
    63:191,
    64:12,
    65:13,
    66:14,
    68:15,
    69:16,
    70:17,
    71:18,
    72:19,
    73:20,
    74:21,
    75:22,
    80:23,
    81:24,
    82:25,
    83:26,
    86:27,
    88:28,
    89:29,
    90:30,
    91:31,
    94:32,
    96:33,
    97:34,
    104:35,
    105:36,
    106:37,
    108:38,
    161:39,
    162:40,
    163:41,
    164:42,
    165:43,
    166:44,
    167:45,
    168:46,
    169:47,
    170:48,
    171:49,
    172:50,
    173:51,
    174:52,
    175:53,
    176:54,
    177:55,
    178:56,
    179:57,
    180:58,
    181:59,
    182:60,
    183:61,
    184:62,
    185:63,
    186:64,
    187:65,
    188:66,
    189:67,
    190:68,
    191:69,
}



DEST_OPTIONS_INDEX = {
    0: 0,
    1: 8,
    2: 47,
    3: 48,
    4: 49,
    5: 50,
    6: 51,
    7: 52,
    8: 53,
    9: 54,
    10: 56,
    11: 57,
    12: 64,
    13: 65,
    14: 66,
    15: 68,
    16: 69,
    17: 70,
    18: 71,
    19: 72,
    20: 73,
    21: 74,
    22: 75,
    23: 80,
    24: 81,
    25: 82,
    26: 83,
    27: 86,
    28: 88,
    29: 89,
    30: 90,
    31: 91,
    32: 94,
    33: 96,
    34: 97,
    35: 104,
    36: 105,
    37: 106,
    38: 108,
    39: 161,
    40: 162,
    41: 163,
    42: 164,
    43: 165,
    44: 166,
    45: 167,
    46: 168,
    47: 169,
    48: 170,
    49: 171,
    50: 172,
    51: 173,
    52: 174,
    53: 175,
    54: 176,
    55: 177,
    56: 178,
    57: 179,
    58: 180,
    59: 181,
    60: 182,
    61: 183,
    62: 184,
    63: 185,
    64: 186,
    65: 187,
    66: 188,
    67: 189,
    68: 190,
    69: 191,
}



source_table = {
    0: 0, 4: 1, 8: 2, 9: 3, 10: 4, 11: 5, 12: 6, 13: 7, 14: 8, 16: 9,
    17: 10, 18: 11, 19: 12, 20: 13, 21: 14, 22: 15, 23: 16, 24: 17, 25: 18, 26: 19,
    27: 20, 32: 21, 33: 22, 34: 23, 35: 24, 36: 25, 37: 26, 38: 27, 39: 28, 48: 29,
    72: 30, 73: 31, 74: 32, 80: 33, 81: 34, 82: 35, 88: 36, 89: 37, 90: 38, 96: 39,
    97: 40, 98: 41, 99: 42, 100: 43, 101: 44, 104: 45, 105: 46, 106: 47, 107: 48, 108: 49,
    109: 50, 144: 51, 145: 52, 146: 53, 147: 54, 148: 55, 149: 56, 160: 57, 161: 58, 162: 59,
    163: 60, 164: 61, 165: 62, 166: 63, 167: 64
}

dest_table = {
    0: 0, 8: 1, 47: 2, 48: 3, 49: 4, 50: 5, 51: 6, 52: 7, 53: 8, 54: 9,
    56: 10, 57: 11, 64: 12, 65: 13, 66: 14, 72: 15, 73: 16, 74: 17, 75: 18, 80: 19,
    81: 20, 82: 21, 83: 22, 86: 23, 88: 24, 89: 25, 90: 26, 91: 27, 94: 28, 96: 29,
    97: 30, 104: 31, 105: 32, 106: 33, 108: 34, 116: 35, 161: 36, 162: 37, 163: 38, 164: 39,
    165: 40, 166: 41, 167: 42, 168: 43, 169: 44, 170: 45, 171: 46, 172: 47, 173: 48, 174: 49,
    175: 50, 176: 51, 177: 52, 178: 53, 179: 54, 180: 55, 181: 56, 182: 57, 183: 58, 184: 59,
    185: 60
}
source_index_to_value = {
    0: 0, 1: 4, 2: 8, 3: 9, 4: 10, 5: 11, 6: 12, 7: 13, 8: 14, 9: 16,
    10: 17, 11: 18, 12: 19, 13: 20, 14: 21, 15: 22, 16: 23, 17: 24, 18: 25, 19: 26,
    20: 27, 21: 32, 22: 33, 23: 34, 24: 35, 25: 36, 26: 37, 27: 38, 28: 39, 29: 48,
    30: 72, 31: 73, 32: 74, 33: 80, 34: 81, 35: 82, 36: 88, 37: 89, 38: 90, 39: 96,
    40: 97, 41: 98, 42: 99, 43: 100, 44: 101, 45: 104, 46: 105, 47: 106, 48: 107, 49: 108,
    50: 109, 51: 144, 52: 145, 53: 146, 54: 147, 55: 148, 56: 149, 57: 160, 58: 161, 59: 162,
    60: 163, 61: 164, 62: 165, 63: 166, 64: 167
}

dest_index_to_value = {
    0: 0, 1: 8, 2: 47, 3: 48, 4: 49, 5: 50, 6: 51, 7: 52, 8: 53, 9: 54,
    10: 56, 11: 57, 12: 64, 13: 65, 14: 66, 15: 72, 16: 73, 17: 74, 18: 75, 19: 80,
    20: 81, 21: 82, 22: 83, 23: 86, 24: 88, 25: 89, 26: 90, 27: 91, 28: 94, 29: 96,
    30: 97, 31: 104, 32: 105, 33: 106, 34: 108, 35: 116, 36: 161, 37: 162, 38: 163, 39: 164,
    40: 165, 41: 166, 42: 167, 43: 168, 44: 169, 45: 170, 46: 171, 47: 172, 48: 173, 49: 174,
    50: 175, 51: 176, 52: 177, 53: 178, 54: 179, 55: 180, 56: 181, 57: 182, 58: 183, 59: 184,
    60: 185
}



SYSEX_NAMES = {
                129: "E4_VOICE_CORD0_SRC",
                130: "E4_VOICE_CORD0_DST",
                131: "E4_VOICE_CORD0_AMT",
                132: "E4_VOICE_CORD1_SRC",
                133: "E4_VOICE_CORD1_DST",
                134: "E4_VOICE_CORD1_AMT",
                135: "E4_VOICE_CORD2_SRC",
                136: "E4_VOICE_CORD2_DST",
                137: "E4_VOICE_CORD2_AMT",
                138: "E4_VOICE_CORD3_SRC",
                139: "E4_VOICE_CORD3_DST",
                140: "E4_VOICE_CORD3_AMT",
                141: "E4_VOICE_CORD4_SRC",
                142: "E4_VOICE_CORD4_DST",
                143: "E4_VOICE_CORD4_AMT",
                144: "E4_VOICE_CORD5_SRC",
                145: "E4_VOICE_CORD5_DST",
                146: "E4_VOICE_CORD5_AMT",
                147: "E4_VOICE_CORD6_SRC",
                148: "E4_VOICE_CORD6_DST",
                149: "E4_VOICE_CORD6_AMT",
                150: "E4_VOICE_CORD7_SRC",
                151: "E4_VOICE_CORD7_DST",
                152: "E4_VOICE_CORD7_AMT",
                153: "E4_VOICE_CORD8_SRC",
                154: "E4_VOICE_CORD8_DST",
                155: "E4_VOICE_CORD8_AMT",
                156: "E4_VOICE_CORD9_SRC",
                157: "E4_VOICE_CORD9_DST",
                158: "E4_VOICE_CORD9_AMT",
                159: "E4_VOICE_CORD10_SRC",
                160: "E4_VOICE_CORD10_DST",
                161: "E4_VOICE_CORD10_AMT",
                162: "E4_VOICE_CORD11_SRC",
                163: "E4_VOICE_CORD11_DST",
                164: "E4_VOICE_CORD11_AMT",
                165: "E4_VOICE_CORD12_SRC",
                166: "E4_VOICE_CORD12_DST",
                167: "E4_VOICE_CORD12_AMT",
                168: "E4_VOICE_CORD13_SRC",
                169: "E4_VOICE_CORD13_DST",
                170: "E4_VOICE_CORD13_AMT",
                171: "E4_VOICE_CORD14_SRC",
                172: "E4_VOICE_CORD14_DST",
                173: "E4_VOICE_CORD14_AMT",
                174: "E4_VOICE_CORD15_SRC",
                175: "E4_VOICE_CORD15_DST",
                176: "E4_VOICE_CORD15_AMT",
                177: "E4_VOICE_CORD16_SRC",
                178: "E4_VOICE_CORD16_DST",
                179: "E4_VOICE_CORD16_AMT",
                180: "E4_VOICE_CORD17_SRC",
                181: "E4_VOICE_CORD17_DST",
                182: "E4_VOICE_CORD17_AMT",
            }


E4_VOICE_CORD0_SRC  = 129
E4_VOICE_CORD0_DST  = 130
E4_VOICE_CORD0_AMT  = 131
E4_VOICE_CORD1_SRC  = 132
E4_VOICE_CORD1_DST  = 133
E4_VOICE_CORD1_AMT  = 134
E4_VOICE_CORD2_SRC  = 135
E4_VOICE_CORD2_DST  = 136
E4_VOICE_CORD2_AMT  = 137
E4_VOICE_CORD3_SRC  = 138
E4_VOICE_CORD3_DST  = 139
E4_VOICE_CORD3_AMT  = 140
E4_VOICE_CORD4_SRC  = 141
E4_VOICE_CORD4_DST  = 142
E4_VOICE_CORD4_AMT  = 143
E4_VOICE_CORD5_SRC  = 144
E4_VOICE_CORD5_DST  = 145
E4_VOICE_CORD5_AMT  = 146
E4_VOICE_CORD6_SRC  = 147
E4_VOICE_CORD6_DST  = 148
E4_VOICE_CORD6_AMT  = 149
E4_VOICE_CORD7_SRC  = 150
E4_VOICE_CORD7_DST  = 151
E4_VOICE_CORD7_AMT  = 152
E4_VOICE_CORD8_SRC  = 153
E4_VOICE_CORD8_DST  = 154
E4_VOICE_CORD8_AMT  = 155
E4_VOICE_CORD9_SRC  = 156
E4_VOICE_CORD9_DST  = 157
E4_VOICE_CORD9_AMT  = 158
E4_VOICE_CORD10_SRC = 159
E4_VOICE_CORD10_DST = 160
E4_VOICE_CORD10_AMT = 161
E4_VOICE_CORD11_SRC = 162
E4_VOICE_CORD11_DST = 163
E4_VOICE_CORD11_AMT = 164
E4_VOICE_CORD12_SRC = 165
E4_VOICE_CORD12_DST = 166
E4_VOICE_CORD12_AMT = 167
E4_VOICE_CORD13_SRC = 168
E4_VOICE_CORD13_DST = 169
E4_VOICE_CORD13_AMT = 170
E4_VOICE_CORD14_SRC = 171
E4_VOICE_CORD14_DST = 172
E4_VOICE_CORD14_AMT = 173
E4_VOICE_CORD15_SRC = 174
E4_VOICE_CORD15_DST = 175
E4_VOICE_CORD15_AMT = 176
E4_VOICE_CORD16_SRC = 177
E4_VOICE_CORD16_DST = 178
E4_VOICE_CORD16_AMT = 179
E4_VOICE_CORD17_SRC = 180
E4_VOICE_CORD17_DST = 181
E4_VOICE_CORD17_AMT = 182




            
#=========================================================================================================== 
#=========================================================================================================== 
#=========================================================================================================== 

def make_bold(ctrl):
    f = ctrl.GetFont()
    f.SetWeight(wx.FONTWEIGHT_BOLD)
    ctrl.SetFont(f)



    
    
#===========================================================================================================    
#=========================================================================================================== 
#=========================================================================================================== 


src_items = [f"{v}" for k, v in sorted(SOURCE_OPTIONS.items())]
class source_selector(wx.ComboBox):
    def __init__(self, parent, id = 0, choices=src_items, style=wx.CB_READONLY, callback = None):
        super().__init__(parent, id=id, choices=choices, style=style)
        self.SetSelection(0)
        self.SetMinSize((160, -1))
        self.SetMaxSize((160, -1))
        self.Bind(wx.EVT_COMBOBOX, callback)
        # main.controls.combo_by_id[id] = self
        
dst_items = [f"{v}" for k, v in sorted(DEST_OPTIONS.items())]
class destination_selector(wx.ComboBox):
    def __init__(self, parent, id = 0, choices=dst_items, style=wx.CB_READONLY, callback = None):
        super().__init__(parent, id=id, choices=choices, style=style)
        self.SetSelection(0)
        self.SetMinSize((160, -1))
        self.SetMaxSize((160, -1))
        self.Bind(wx.EVT_COMBOBOX, callback)  
        # main.controls.combo_by_id[id] = self



class CordsPanel(wx.Panel):
    def __init__(self, parent, main, voice_dict):
        super().__init__(parent)
        self.device_id = main.device_id
        self.controls = main.controls
        self.main = main
        

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Create FlexGridSizer with 4 columns
        grid_sizer = wx.FlexGridSizer(rows=19, cols=4, hgap=10, vgap=15)
        grid_sizer.AddGrowableCol(1, proportion=1)  # Make 2nd column growable
        grid_sizer.AddGrowableCol(2, proportion=1)  # Make 3rd column growable

        # Column 1 wrapper (fixed width)
        wrapper1 = wx.Panel(self, size=(50, 22))
        wrapper1.SetMinSize((50, 22))
        label1 = wx.StaticText(wrapper1, label="")
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(label1, 0, wx.ALIGN_CENTER)
        wrapper1.SetSizer(sizer1)

        # Column 2 
        label2 = wx.StaticText(self, label="Src", size = (70,22))
        label2.SetMinSize((70, 22))
        # Column 3 
        label3 = wx.StaticText(self, label="Dst", size = (70,22))
        label3.SetMinSize((70, 22))
        # Column 4 
        wrapper4 = wx.Panel(self, size=(50, 22))
        wrapper4.SetMinSize((50, 22))
        label4 = wx.StaticText(wrapper4, label="Amt", size = (70,22))
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(label4, 0, wx.ALIGN_CENTER)
        wrapper4.SetSizer(sizer4)

        
        label5 = wx.StaticText(self, label="Cord 0")
        label6 = source_selector(self, id = 129, callback = self.source_select)
        label6.SetSelection(SOURCE_OPTIONS_INDEX_REV.get(voice_dict["params"]["E4_VOICE_CORD0_SRC"], 0))
        label7 = destination_selector(self, id = 130, callback = self.destination_select)
        label7.SetSelection(DEST_OPTIONS_INDEX_REV.get(voice_dict["params"]["E4_VOICE_CORD0_DST"], 0))
        label8 = DraggableNumber(self, id = 131, value = voice_dict["params"]["E4_VOICE_CORD0_AMT"], min_val=-100, max_val=100, callback = main._onAnyControlChanged)
        
        label9 = wx.StaticText(self, label="Cord 1")
        label10 = source_selector(self, id = 132, callback = self.source_select)
        label10.SetSelection(SOURCE_OPTIONS_INDEX_REV.get(voice_dict["params"]["E4_VOICE_CORD1_SRC"], 0))
        label11 = destination_selector(self, id = 133, callback = self.destination_select)
        label11.SetSelection(DEST_OPTIONS_INDEX_REV.get(voice_dict["params"]["E4_VOICE_CORD1_DST"], 0))
        label12 = DraggableNumber(self, id = 134, value = voice_dict["params"]["E4_VOICE_CORD1_AMT"], min_val=-100, max_val=100, callback = main._onAnyControlChanged)
        
        label13 = wx.StaticText(self, label="Cord 2")
        label14 = source_selector(self, id = 135, callback = self.source_select)
        label14.SetSelection(SOURCE_OPTIONS_INDEX_REV.get(voice_dict["params"]["E4_VOICE_CORD2_SRC"], 0))
        label15 = destination_selector(self, id = 136, callback = self.destination_select)
        label15.SetSelection(DEST_OPTIONS_INDEX_REV.get(voice_dict["params"]["E4_VOICE_CORD2_DST"], 0))
        label16 = DraggableNumber(self, id = 137, value = voice_dict["params"]["E4_VOICE_CORD2_AMT"], min_val=-100, max_val=100, callback = main._onAnyControlChanged)
        
        label17 = wx.StaticText(self, label="Cord 3")
        label18 = source_selector(self, id = 138, callback = self.source_select)
        label18.SetSelection(SOURCE_OPTIONS_INDEX_REV.get(voice_dict["params"]["E4_VOICE_CORD3_SRC"], 0))
        label19 = destination_selector(self, id = 139, callback = self.destination_select)
        label19.SetSelection(DEST_OPTIONS_INDEX_REV.get(voice_dict["params"]["E4_VOICE_CORD3_DST"], 0))
        label20 = DraggableNumber(self, id = 140, value = voice_dict["params"]["E4_VOICE_CORD3_AMT"], min_val=-100, max_val=100, callback = main._onAnyControlChanged)
        
        label21 = wx.StaticText(self, label="Cord 4")
        label22 = source_selector(self, id = 141, callback = self.source_select)
        label22.SetSelection(SOURCE_OPTIONS_INDEX_REV.get(voice_dict["params"]["E4_VOICE_CORD4_SRC"], 0))
        label23 = destination_selector(self, id = 142, callback = self.destination_select)
        label23.SetSelection(DEST_OPTIONS_INDEX_REV.get(voice_dict["params"]["E4_VOICE_CORD4_DST"], 0))
        label24 = DraggableNumber(self, id = 143, value = voice_dict["params"]["E4_VOICE_CORD4_AMT"], min_val=-100, max_val=100, callback = main._onAnyControlChanged)
        
        label25 = wx.StaticText(self, label="Cord 5")
        label26 = source_selector(self, id = 144, callback = self.source_select)
        label26.SetSelection(SOURCE_OPTIONS_INDEX_REV.get(voice_dict["params"]["E4_VOICE_CORD5_SRC"], 0))
        label27 = destination_selector(self, id = 145, callback = self.destination_select)
        label27.SetSelection(DEST_OPTIONS_INDEX_REV.get(voice_dict["params"]["E4_VOICE_CORD5_DST"], 0))
        label28 = DraggableNumber(self, id = 146, value = voice_dict["params"]["E4_VOICE_CORD5_AMT"], min_val=-100, max_val=100, callback = main._onAnyControlChanged)
        
        label29 = wx.StaticText(self, label="Cord 6")
        label30 = source_selector(self, id = 147, callback = self.source_select)
        label30.SetSelection(SOURCE_OPTIONS_INDEX_REV.get(voice_dict["params"]["E4_VOICE_CORD6_SRC"], 0))
        label31 = destination_selector(self, id = 148, callback = self.destination_select)
        label31.SetSelection(DEST_OPTIONS_INDEX_REV.get(voice_dict["params"]["E4_VOICE_CORD6_DST"], 0))
        label32 = DraggableNumber(self, id = 149, value = voice_dict["params"]["E4_VOICE_CORD6_AMT"], min_val=-100, max_val=100, callback = main._onAnyControlChanged)
        
        label33 = wx.StaticText(self, label="Cord 7")
        label34 = source_selector(self, id = 150, callback = self.source_select)
        label34.SetSelection(SOURCE_OPTIONS_INDEX_REV.get(voice_dict["params"]["E4_VOICE_CORD7_SRC"], 0))
        label35 = destination_selector(self, id = 151, callback = self.destination_select)
        label35.SetSelection(DEST_OPTIONS_INDEX_REV.get(voice_dict["params"]["E4_VOICE_CORD7_DST"], 0))
        label36 = DraggableNumber(self, id = 152, value = voice_dict["params"]["E4_VOICE_CORD7_AMT"], min_val=-100, max_val=100, callback = main._onAnyControlChanged)
        
        label37 = wx.StaticText(self, label="Cord 8")
        label38 = source_selector(self, id = 153, callback = self.source_select)
        label38.SetSelection(SOURCE_OPTIONS_INDEX_REV.get(voice_dict["params"]["E4_VOICE_CORD8_SRC"], 0))
        label39 = destination_selector(self, id = 154, callback = self.destination_select)
        label39.SetSelection(DEST_OPTIONS_INDEX_REV.get(voice_dict["params"]["E4_VOICE_CORD8_DST"], 0))
        label40 = DraggableNumber(self, id = 155, value = voice_dict["params"]["E4_VOICE_CORD8_AMT"], min_val=-100, max_val=100, callback = main._onAnyControlChanged)
        
        label41 = wx.StaticText(self, label="Cord 9")
        label42 = source_selector(self, id = 156, callback = self.source_select)
        label42.SetSelection(SOURCE_OPTIONS_INDEX_REV.get(voice_dict["params"]["E4_VOICE_CORD9_SRC"], 0))
        label43 = destination_selector(self, id = 157, callback = self.destination_select)
        label43.SetSelection(DEST_OPTIONS_INDEX_REV.get(voice_dict["params"]["E4_VOICE_CORD9_DST"], 0))
        label44 = DraggableNumber(self, id = 158, value = voice_dict["params"]["E4_VOICE_CORD9_AMT"], min_val=-100, max_val=100, callback = main._onAnyControlChanged)
        
        label45 = wx.StaticText(self, label="Cord 10")
        label46 = source_selector(self, id = 159, callback = self.source_select)
        label46.SetSelection(SOURCE_OPTIONS_INDEX_REV.get(voice_dict["params"]["E4_VOICE_CORD10_SRC"], 0))
        label47 = destination_selector(self, id = 160, callback = self.destination_select)
        label47.SetSelection(DEST_OPTIONS_INDEX_REV.get(voice_dict["params"]["E4_VOICE_CORD10_DST"], 0))
        label48 = DraggableNumber(self, id = 161, value = voice_dict["params"]["E4_VOICE_CORD10_AMT"], min_val=-100, max_val=100, callback = main._onAnyControlChanged)
        
        label49 = wx.StaticText(self, label="Cord 11")
        label50 = source_selector(self, id = 162, callback = self.source_select)
        label50.SetSelection(SOURCE_OPTIONS_INDEX_REV.get(voice_dict["params"]["E4_VOICE_CORD11_SRC"], 0))
        label51 = destination_selector(self, id = 163, callback = self.destination_select)
        label51.SetSelection(DEST_OPTIONS_INDEX_REV.get(voice_dict["params"]["E4_VOICE_CORD11_DST"], 0))
        label52 = DraggableNumber(self, id = 164, value = voice_dict["params"]["E4_VOICE_CORD11_AMT"], min_val=-100, max_val=100, callback = main._onAnyControlChanged)
        
        label53 = wx.StaticText(self, label="Cord 12")
        label54 = source_selector(self, id = 165, callback = self.source_select)
        label54.SetSelection(SOURCE_OPTIONS_INDEX_REV.get(voice_dict["params"]["E4_VOICE_CORD12_SRC"], 0))
        label55 = destination_selector(self, id = 166, callback = self.destination_select)
        label55.SetSelection(DEST_OPTIONS_INDEX_REV.get(voice_dict["params"]["E4_VOICE_CORD12_DST"], 0))
        label56 = DraggableNumber(self, id = 167, value = voice_dict["params"]["E4_VOICE_CORD12_AMT"], min_val=-100, max_val=100, callback = main._onAnyControlChanged)
        
        label57 = wx.StaticText(self, label="Cord 13")
        label58 = source_selector(self, id = 168, callback = self.source_select)
        label58.SetSelection(SOURCE_OPTIONS_INDEX_REV.get(voice_dict["params"]["E4_VOICE_CORD13_SRC"], 0))
        label59 = destination_selector(self, id = 169, callback = self.destination_select)
        label59.SetSelection(DEST_OPTIONS_INDEX_REV.get(voice_dict["params"]["E4_VOICE_CORD13_DST"], 0))
        label60 = DraggableNumber(self, id = 170, value = voice_dict["params"]["E4_VOICE_CORD13_AMT"], min_val=-100, max_val=100, callback = main._onAnyControlChanged)
        
        label61 = wx.StaticText(self, label="Cord 14")
        label62 = source_selector(self, id = 171, callback = self.source_select)
        label62.SetSelection(SOURCE_OPTIONS_INDEX_REV.get(voice_dict["params"]["E4_VOICE_CORD14_SRC"], 0))
        label63 = destination_selector(self, id = 172, callback = self.destination_select)
        label63.SetSelection(DEST_OPTIONS_INDEX_REV.get(voice_dict["params"]["E4_VOICE_CORD14_DST"], 0))
        label64 = DraggableNumber(self, id = 173, value = voice_dict["params"]["E4_VOICE_CORD14_AMT"], min_val=-100, max_val=100, callback = main._onAnyControlChanged)
        
        label65 = wx.StaticText(self, label="Cord 15")
        label66 = source_selector(self, id = 174, callback = self.source_select)
        label66.SetSelection(SOURCE_OPTIONS_INDEX_REV.get(voice_dict["params"]["E4_VOICE_CORD15_SRC"], 0))
        label67 = destination_selector(self, id = 175, callback = self.destination_select)
        label67.SetSelection(DEST_OPTIONS_INDEX_REV.get(voice_dict["params"]["E4_VOICE_CORD15_DST"], 0))
        label68 = DraggableNumber(self, id = 176, value = voice_dict["params"]["E4_VOICE_CORD15_AMT"], min_val=-100, max_val=100, callback = main._onAnyControlChanged)
        
        label69 = wx.StaticText(self, label="Cord 16")
        label70 = source_selector(self, id = 177, callback = self.source_select)
        label70.SetSelection(SOURCE_OPTIONS_INDEX_REV.get(voice_dict["params"]["E4_VOICE_CORD16_SRC"], 0))
        label71 = destination_selector(self, id = 178, callback = self.destination_select)
        label71.SetSelection(DEST_OPTIONS_INDEX_REV.get(voice_dict["params"]["E4_VOICE_CORD16_DST"], 0))
        label72 = DraggableNumber(self, id = 179, value = voice_dict["params"]["E4_VOICE_CORD16_AMT"], min_val=-100, max_val=100, callback = main._onAnyControlChanged)
        
        label73 = wx.StaticText(self, label="Cord 17")
        label74 = source_selector(self, id = 180, callback = self.source_select)
        label74.SetSelection(SOURCE_OPTIONS_INDEX_REV.get(voice_dict["params"]["E4_VOICE_CORD17_SRC"], 0))
        label75 = destination_selector(self, id = 181, callback = self.destination_select)
        label75.SetSelection(DEST_OPTIONS_INDEX_REV.get(voice_dict["params"]["E4_VOICE_CORD17_DST"], 0))
        label76 = DraggableNumber(self, id = 182, value = voice_dict["params"]["E4_VOICE_CORD17_AMT"], min_val=-100, max_val=100, callback = main._onAnyControlChanged)
        
        

        labels = [
            wrapper1, label2, label3, wrapper4, label5, label6, label7, label8, label9, label10,
            label11, label12, label13, label14, label15, label16, label17, label18, label19, label20,
            label21, label22, label23, label24, label25, label26, label27, label28, label29, label30,
            label31, label32, label33, label34, label35, label36, label37, label38, label39, label40,
            label41, label42, label43, label44, label45, label46, label47, label48, label49, label50,
            label51, label52, label53, label54, label55, label56, label57, label58, label59, label60,
            label61, label62, label63, label64, label65, label66, label67, label68, label69, label70,
            label71, label72, label73, label74, label75, label76
        ]

        for label in labels:
            if isinstance(label, wx.ComboBox):
                # main.controls.combo_by_id[label.Id] = label
                label.SetMinSize((180, 22))
            elif isinstance(label, DraggableNumber):
                # main.controls.dragger_by_id[label.Id] = label
                label.SetMinSize((40, 22))
            elif isinstance(label, wx.StaticText):
                if label != wrapper1 or label != label2 or label != label3 or label != wrapper4:
                    label.SetMinSize((50, 22))
                    label.SetMaxSize((50, 22))
                else:
                    label.SetMinSize((70, 22))
                    label.SetMaxSize((70, 22))
            grid_sizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 20)
            
        param_values = [label8, label12, label16, label20, label24, label28, label32, label36,
                    label40, label44, label48, label52, label56, label60, label64, label68, label72, label76]  
        for label in param_values:
            label.SetBackgroundColour(greencontrol)

            
        param_labels = [label2, label3, wrapper4]  
        for label in param_labels:
            label.SetBackgroundColour(yellow)      

        main_sizer.Add(grid_sizer, flag=wx.ALL, border=10)
        self.SetSizer(main_sizer)
        
    def source_select(self, evt):
        ctrl = evt.GetEventObject()
        wId = ctrl.GetId()
        value = ctrl.GetSelection()
        print(ctrl, wId, value)
        value = SOURCE_OPTIONS_INDEX[value]
        print(ctrl, wId, value)
        self.main.send_parameter_edit(wId, value)
        
    def destination_select(self, evt):
        ctrl = evt.GetEventObject()
        wId = ctrl.GetId()
        value = ctrl.GetSelection()
        value = DEST_OPTIONS_INDEX[value]
        self.main.send_parameter_edit(wId, value)
#======================================================================================================================
#======================================================================================================================
#======================================================================================================================

