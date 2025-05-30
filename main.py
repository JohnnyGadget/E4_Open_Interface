
import os
import threading
import wx
import mido
from mido import Message
import time
import queue


from preset import PresetPanel
from master_panel import MasterGlobalPanel
from connect_midi import MidiConnectPopup
from master_panel import MasterGlobalPanel
from preset_effects_panel import PresetEffectsPanel
from master_effects_panel import MasterEffectsPanel
# from keyboard_panel import MidiKeyboard
from voice_panel import EditVoicePanels
from custom_widgets import DraggableNumber
from midiglo import MidigloPanel
from zones_panel import Voice_Zones_Panel
from front_panel import FrontPanelFrame
from metronome import MetronomePanel
from links_panel import Links_Panel
from cc_frame import CCframe
from help_dialog import HelpDialog
# from popup import InfoPopup

CORD_SRC_PARAMS = [
    129, 132, 135, 138, 141, 144, 147, 150, 153, 156,
    159, 162, 165, 168, 171, 174, 177, 180
]
CORD_SRC_PARAMS_SET = set(CORD_SRC_PARAMS)
CORD_DST_PARAMS = [
    130, 133, 136, 139, 142, 145, 148, 151, 154, 157,
    160, 163, 166, 169, 172, 175, 178, 181
]
CORD_DST_PARAMS_SET = set(CORD_DST_PARAMS)
CORD_AMT_PARAMS = [
    131, 134, 137, 140, 143, 146, 149, 152, 155, 158,
    161, 164, 167, 170, 173, 176, 179, 182
]
CORD_AMT_PARAMS_SET = set(CORD_AMT_PARAMS)


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
    32:  "MidiC",
    33:  "MidiD",
    34:  "MidiE",
    35:  "MidiF",
    36:  "MidiG",
    37:  "MidiH",
    38:  "Thumb",
    39:  "ThmFF",
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

SOURCE_VALUE_TO_INDEX = {key: i for i, key in enumerate(SOURCE_OPTIONS)}

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
    116: "???",
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
    185: "C17Amt (Cord 17 Amount)"
}
DST_VALUE_TO_INDEX = {key: i for i, key in enumerate(DEST_OPTIONS)}


poly_modes_map_rev = {
    0:  "Poly All",
    1:  "Poly16 A",
    2:  "Poly16 B",
    3:  "Poly 8 A",
    4:  "Poly 8 B",
    5:  "Poly 8 C",
    6:  "Poly 8 D",
    7:  "Poly 4 A",
    8:  "Poly 4 B",
    9:  "Poly 4 C",
    10: "Poly 4 D",
    11: "Poly 2 A",
    12: "Poly 2 B",
    13: "Poly 2 C",
    14: "Poly 2 D",
    15: "Mono A",
    16: "Mono B",
    17: "Mono C",
    18: "Mono D",
    19: "Mono E",
    20: "Mono F",
    21: "Mono G",
    22: "Mono H",
    23: "Mono I",
}

submix_ports_rev = {
    -1: "voice",
     0: "main",
     1: "sub1",
     2: "sub2",
     3: "sub3",
     4: "sub4",
     5: "sub5",
     6: "sub6",
     7: "sub7",
}

solo_modes_rev = {
    0: "Off",
    1: "Multiple Trigger",
    2: "Melody (last)",
    3: "Melody (low)",
    4: "Melody (high)",
    5: "Synth (last)",
    6: "Synth (low)",
    7: "Synth (high)",
    8: "Fingered Glide",
}


amp_env_depths = {
    0:  "-96",
    1:  "-93",
    2:  "-90",
    3:  "-87",
    4:  "-84",
    5:  "-81",
    6:  "-78",
    7:  "-75",
    8:  "-72",
    9:  "-69",
    10: "-66",
    11: "-63",
    12: "-60",
    13: "-57",
    14: "-54",
    15: "-51",
    16: "-48",
}



param_names = { 0: "E4_PRESET_TRANSPOSE",
                1: "E4_PRESET_VOLUME",
                2: "E4_PRESET_CTRL_A",
                3: "E4_PRESET_CTRL_B",
                4: "E4_PRESET_CTRL_C",
                5: "E4_PRESET_CTRL_D",

                6: "E4_PRESET_FX_A_ALGORITHM",
                7: "E4_PRESET_FX_A_PARM_0",
                8: "E4_PRESET_FX_A_PARM_1",
                9: "E4_PRESET_FX_A_PARM_2",
                10: "E4_PRESET_FX_A_AMT_0",
                11: "E4_PRESET_FX_A_AMT_1",
                12: "E4_PRESET_FX_A_AMT_2",
                13: "E4_PRESET_FX_A_AMT_3",

                14: "E4_PRESET_FX_B_ALGORITHM",
                15: "E4_PRESET_FX_B_PARM_0",
                16: "E4_PRESET_FX_B_PARM_1",
                17: "E4_PRESET_FX_B_PARM_2",
                18: "E4_PRESET_FX_B_AMT_0",
                19: "E4_PRESET_FX_B_AMT_1",
                20: "E4_PRESET_FX_B_AMT_2",
                21: "E4_PRESET_FX_B_AMT_3",

                # ID 22 is unused

                23: "E4_LINK_PRESET",
                24: "E4_LINK_VOLUME",
                25: "E4_LINK_PAN",
                26: "E4_LINK_TRANSPOSE",
                27: "E4_LINK_FINE_TUNE",
                28: "E4_LINK_KEY_LOW",
                29: "E4_LINK_KEY_LOWFADE",
                30: "E4_LINK_KEY_HIGH",
                31: "E4_LINK_KEY_HIGHFADE",
                32: "E4_LINK_VEL_LOW",
                33: "E4_LINK_VEL_LOWFADE",
                34: "E4_LINK_VEL_HIGH",
                35: "E4_LINK_VEL_HIGHFADE",


                37: "E4_GEN_GROUP_NUM",
                38: "E4_GEN_SAMPLE",
                39: "E4_GEN_VOLUME",
                40: "E4_GEN_PAN",
                41: "E4_GEN_CTUNE",
                42: "E4_GEN_FTUNE",
                43: "E4_GEN_XPOSE",
                44: "E4_GEN_ORIG_KEY",
                45: "E4_GEN_KEY_LOW",
                46: "E4_GEN_KEY_LOWFADE",
                47: "E4_GEN_KEY_HIGH",
                48: "E4_GEN_KEY_HIGHFADE",
                49: "E4_GEN_VEL_LOW",
                50: "E4_GEN_VEL_LOWFADE",
                51: "E4_GEN_VEL_HIGH",
                52: "E4_GEN_VEL_HIGHFADE",
                53: "E4_GEN_RT_LOW",
                54: "E4_GEN_RT_LOWFADE",
                55: "E4_GEN_RT_HIGH",
                56: "E4_GEN_RT_HIGHFADE",
                
                
                57: "E4_VOICE_NON_TRANSPOSE",
                58: "E4_VOICE_CHORUS_AMOUNT",
                59: "E4_VOICE_CHORUS_WIDTH",
                60: "E4_VOICE_CHORUS_X",
                61: "E4_VOICE_DELAY",
                62: "E4_VOICE_START_OFFSET",
                63: "E4_VOICE_GLIDE_RATE",
                64: "E4_VOICE_GLIDE_CURVE",
                65: "E4_VOICE_SOLO",
                66: "E4_VOICE_ASSIGN_GROUP",
                67: "E4_VOICE_LATCHMODE",
                68: "E4_VOICE_VOLENV_DEPTH",
                69: "E4_VOICE_SUBMIX",
                
                
                70: "E4_VOICE_VENV_SEG0_RATE",
                71: "E4_VOICE_VENV_SEG0_TGTLVL",
                72: "E4_VOICE_VENV_SEG1_RATE",
                73: "E4_VOICE_VENV_SEG1_TGTLVL",
                74: "E4_VOICE_VENV_SEG2_RATE",
                75: "E4_VOICE_VENV_SEG2_TGTLVL",
                76: "E4_VOICE_VENV_SEG3_RATE",
                77: "E4_VOICE_VENV_SEG3_TGTLVL",
                78: "E4_VOICE_VENV_SEG4_RATE",
                79: "E4_VOICE_VENV_SEG4_TGTLVL",
                80: "E4_VOICE_VENV_SEG5_RATE",
                81: "E4_VOICE_VENV_SEG5_TGTLVL",
                
                
                82: "E4_VOICE_FTYPE",
                83: "E4_VOICE_FMORPH",
                84: "E4_VOICE_FKEY_XFORM",
                85: "E4_VOICE_FILT_GEN_PARM1",
                86: "E4_VOICE_FILT_GEN_PARM2",
                87: "E4_VOICE_FILT_GEN_PARM3",
                88: "E4_VOICE_FILT_GEN_PARM4",
                89: "E4_VOICE_FILT_GEN_PARM5",
                90: "E4_VOICE_FILT_GEN_PARM6",
                91: "E4_VOICE_FILT_GEN_PARM7",
                92: "E4_VOICE_FILT_GEN_PARM8",
                
                
                93: "E4_VOICE_FENV_SEG0_RATE",
                94: "E4_VOICE_FENV_SEG0_TGTLVL",
                95: "E4_VOICE_FENV_SEG1_RATE",
                96: "E4_VOICE_FENV_SEG1_TGTLVL",
                97: "E4_VOICE_FENV_SEG2_RATE",
                98: "E4_VOICE_FENV_SEG2_TGTLVL",
                99: "E4_VOICE_FENV_SEG3_RATE",
                100: "E4_VOICE_FENV_SEG3_TGTLVL",
                101: "E4_VOICE_FENV_SEG4_RATE",
                102: "E4_VOICE_FENV_SEG4_TGTLVL",
                103: "E4_VOICE_FENV_SEG5_RATE",
                104: "E4_VOICE_FENV_SEG5_TGTLVL",
                
                
                105: "E4_VOICE_LFO_RATE",
                106: "E4_VOICE_LFO_SHAPE",
                107: "E4_VOICE_LFO_DELAY",
                108: "E4_VOICE_LFO_VAR",
                109: "E4_VOICE_LFO_SYNC",
                
                
                110: "E4_VOICE_LFO2_RATE",
                111: "E4_VOICE_LFO2_SHAPE",
                112: "E4_VOICE_LFO2_DELAY",
                113: "E4_VOICE_LFO2_VAR",
                114: "E4_VOICE_LFO2_SYNC",
                115: "E4_VOICE_LFO2_OP0_PARM",
                116: "E4_VOICE_LFO2_OP1_PARM",
                
                
                117: "E4_VOICE_AENV_SEG0_RATE",
                118: "E4_VOICE_AENV_SEG0_TGTLVL",
                119: "E4_VOICE_AENV_SEG1_RATE",
                120: "E4_VOICE_AENV_SEG1_TGTLVL",
                121: "E4_VOICE_AENV_SEG2_RATE",
                122: "E4_VOICE_AENV_SEG2_TGTLVL",
                123: "E4_VOICE_AENV_SEG3_RATE",
                124: "E4_VOICE_AENV_SEG3_TGTLVL",
                125: "E4_VOICE_AENV_SEG4_RATE",
                126: "E4_VOICE_AENV_SEG4_TGTLVL",
                127: "E4_VOICE_AENV_SEG5_RATE",
                128: "E4_VOICE_AENV_SEG5_TGTLVL",
                
                
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
                
                
                183: "MASTER_TUNING_OFFSET",
                184: "MASTER_TRANSPOSE",
                185: "MASTER_HEADROOM",
                186: "MASTER_HCHIP_BOOST",
                187: "MASTER_OUTPUT_FORMAT",
                188: "MASTER_OUTPUT_CLOCK",
                189: "MASTER_AES_BOOST",
                190: "MASTER_SCSI_ID",
                191: "MASTER_SCSI_TERM",
                192: "MASTER_USING_MAC",
                193: "MASTER_COMBINE_LR",
                194: "MASTER_AKAI_LOOP_ADJ",
                195: "MASTER_AKAI_SAMPLER_ID",
                
                
                198: "MIDIGLO_BASIC_CHANNEL",
                199: "MIDIGLO_MIDI_MODE",
                201: "MIDIGLO_PITCH_CONTROL",
                202: "MIDIGLO_MOD_CONTROL",
                203: "MIDIGLO_PRESSURE_CONTROL",
                204: "MIDIGLO_PEDAL_CONTROL",
                205: "MIDIGLO_SWITCH_1_CONTROL",
                206: "MIDIGLO_SWITCH_2_CONTROL",
                207: "MIDIGLO_THUMB_CONTROL",
                208: "MIDIGLO_MIDI_A_CONTROL",
                209: "MIDIGLO_MIDI_B_CONTROL",
                210: "MIDIGLO_MIDI_C_CONTROL",
                211: "MIDIGLO_MIDI_D_CONTROL",
                212: "MIDIGLO_MIDI_E_CONTROL",
                213: "MIDIGLO_MIDI_F_CONTROL",
                214: "MIDIGLO_MIDI_G_CONTROL",
                215: "MIDIGLO_MIDI_H_CONTROL",
                216: "MIDIGLO_VEL_CURVE",
                217: "MIDIGLO_VOLUME_SENSITIVITY",
                218: "MIDIGLO_CTRL7_CURVE",
                219: "MIDIGLO_PEDAL_OVERRIDE",
                220: "MIDIGLO_RCV_PROGRAM_CHANGE",
                221: "MIDIGLO_SEND_PROGRAM_CHANGE",
                222: "MIDIGLO_MAGIC_PRESET",
                
                
                223: "PRESET_SELECT",
                224: "LINK_SELECT",
                225: "VOICE_SELECT",
                226: "SAMPLE_ZONE_SELECT",
                227: "GROUP_SELECT",
                
                
                228: "MASTER_FX_A_ALGORITHM",
                229: "MASTER_FX_A_PARM_0",
                230: "MASTER_FX_A_PARM_1",
                231: "MASTER_FX_A_PARM_2",
                232: "MASTER_FX_A_AMT_0",
                233: "MASTER_FX_A_AMT_1",
                234: "MASTER_FX_A_AMT_2",
                235: "MASTER_FX_A_AMT_3",
                
                
                236: "MASTER_FX_B_ALGORITHM",
                237: "MASTER_FX_B_PARM_0",
                238: "MASTER_FX_B_PARM_1",
                239: "MASTER_FX_B_PARM_2",
                240: "MASTER_FX_B_AMT_0",
                241: "MASTER_FX_B_AMT_1",
                242: "MASTER_FX_B_AMT_2",
                243: "MASTER_FX_B_AMT_3",
                244: "MASTER_FX_BYPASS",
                
                
                245: "MASTER_FX_MM_CTRL_CHANNEL",
                246: "MULTIMODE_CHANNEL",
                247: "MULTIMODE_PRESET",
                248: "MULTIMODE_VOLUME",
                249: "MULTIMODE_PAN",
                250: "MULTIMODE_SUBMIX",
                
                
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
                266: "E4_LINK_FILTER_THUMB",
                
                
                267: "MASTER_WORD_CLOCK_IN",
                268: "MASTER_WORD_CLOCK_PHASE_IN",
                269: "MASTER_WORD_CLOCK_PHASE_OUT",
                270: "MASTER_OUTPUT_DITHER",
                
                
                32:  "NEW_VOICE",
                33:  "DELETE_VOICE",
                34:  "COPY_VOICE",
                48:  "NEW_SAMPLE_ZONE",
                49:  "GET_MULTISAMPLE",
                50:  "DELETE_SAMPLE_ZONE",
                51:  "COMBINE (Voices)",
                52:  "EXPAND (Sample Zones)",
                64:  "NEW_LINK",
                65:  "DELETE_LINK",
                66:  "COPY_LINK",
                80:  "SAMPLE_ERASE",
                82:  "SAMPLE_DEFRAGMENT_MEMORY",
                112: "PRESET_COPY",
                113: "PRESET_DELETE",
                114: "MULTIMODE_MAP_DUMP",
                115: "MULTIMODE_MAP_DUMP_REQUEST",
                116: "ERASE_CURRENT_RAM_BANK",
                117: "ERASE_ALL_RAM_PRESETS",
                118: "ERASE_ALL_RAM_SAMPLES",
}




global_param_names = {
            0:"E4_PRESET_TRANSPOSE",    # id 0
            1:"E4_PRESET_VOLUME",       # id 1
            2:"E4_PRESET_CTRL_A",       # id 2
            3:"E4_PRESET_CTRL_B",       # id 3
            4:"E4_PRESET_CTRL_C",       # id 4
            5:"E4_PRESET_CTRL_D",       # id 5

            6:"E4_PRESET_FX_A_ALGORITHM",  # id 6
            7:"E4_PRESET_FX_A_PARM_0",     # id 7
            8:"E4_PRESET_FX_A_PARM_1",     # id 8
            9:"E4_PRESET_FX_A_PARM_2",     # id 9
            10:"E4_PRESET_FX_A_AMT_0",      # id 10
            11:"E4_PRESET_FX_A_AMT_1",      # id 11
            12:"E4_PRESET_FX_A_AMT_2",      # id 12
            13:"E4_PRESET_FX_A_AMT_3",      # id 13

            14:"E4_PRESET_FX_B_ALGORITHM",  # id 14
            15:"E4_PRESET_FX_B_PARM_0",     # id 15
            16:"E4_PRESET_FX_B_PARM_1",     # id 16
            17:"E4_PRESET_FX_B_PARM_2",     # id 17
            18:"E4_PRESET_FX_B_AMT_0",      # id 18
            19:"E4_PRESET_FX_B_AMT_1",      # id 19
            20:"E4_PRESET_FX_B_AMT_2",      # id 20
            21:"E4_PRESET_FX_B_AMT_3",      # id 21
}

dump_param_names = {
                37: "E4_GEN_GROUP_NUM",
                38: "E4_GEN_SAMPLE",
                39: "E4_GEN_VOLUME",
                40: "E4_GEN_PAN",
                41: "E4_GEN_CTUNE",
                42: "E4_GEN_FTUNE",
                43: "E4_GEN_XPOSE",
                44: "E4_GEN_ORIG_KEY",
                45: "E4_GEN_KEY_LOW",
                46: "E4_GEN_KEY_LOWFADE",
                47: "E4_GEN_KEY_HIGH",
                48: "E4_GEN_KEY_HIGHFADE",
                49: "E4_GEN_VEL_LOW",
                50: "E4_GEN_VEL_LOWFADE",
                51: "E4_GEN_VEL_HIGH",
                52: "E4_GEN_VEL_HIGHFADE",
                53: "E4_GEN_RT_LOW",
                54: "E4_GEN_RT_LOWFADE",
                55: "E4_GEN_RT_HIGH",
                56: "E4_GEN_RT_HIGHFADE",
                57: "E4_VOICE_NON_TRANSPOSE",
                58: "E4_VOICE_CHORUS_AMOUNT",
                59: "E4_VOICE_CHORUS_WIDTH",
                60: "E4_VOICE_CHORUS_X",
                61: "E4_VOICE_DELAY",
                62: "E4_VOICE_START_OFFSET",
                63: "E4_VOICE_GLIDE_RATE",
                64: "E4_VOICE_GLIDE_CURVE",
                65: "E4_VOICE_SOLO",
                66: "E4_VOICE_ASSIGN_GROUP",
                67: "E4_VOICE_LATCHMODE",
                68: "E4_VOICE_VOLENV_DEPTH",
                69: "E4_VOICE_SUBMIX",
                70: "E4_VOICE_VENV_SEG0_RATE",
                71: "E4_VOICE_VENV_SEG0_TGTLVL",
                72: "E4_VOICE_VENV_SEG1_RATE",
                73: "E4_VOICE_VENV_SEG1_TGTLVL",
                74: "E4_VOICE_VENV_SEG2_RATE",
                75: "E4_VOICE_VENV_SEG2_TGTLVL",
                76: "E4_VOICE_VENV_SEG3_RATE",
                77: "E4_VOICE_VENV_SEG3_TGTLVL",
                78: "E4_VOICE_VENV_SEG4_RATE",
                79: "E4_VOICE_VENV_SEG4_TGTLVL",
                80: "E4_VOICE_VENV_SEG5_RATE",
                81: "E4_VOICE_VENV_SEG5_TGTLVL",
                82: "E4_VOICE_FTYPE",
                83: "E4_VOICE_FMORPH",
                84: "E4_VOICE_FKEY_XFORM",
                85: "E4_VOICE_FILT_GEN_PARM1",
                86: "E4_VOICE_FILT_GEN_PARM2",
                87: "E4_VOICE_FILT_GEN_PARM3",
                88: "E4_VOICE_FILT_GEN_PARM4",
                89: "E4_VOICE_FILT_GEN_PARM5",
                90: "E4_VOICE_FILT_GEN_PARM6",
                91: "E4_VOICE_FILT_GEN_PARM7",
                92: "E4_VOICE_FILT_GEN_PARM8",
                93: "E4_VOICE_FENV_SEG0_RATE",
                94: "E4_VOICE_FENV_SEG0_TGTLVL",
                95: "E4_VOICE_FENV_SEG1_RATE",
                96: "E4_VOICE_FENV_SEG1_TGTLVL",
                97: "E4_VOICE_FENV_SEG2_RATE",
                98: "E4_VOICE_FENV_SEG2_TGTLVL",
                99: "E4_VOICE_FENV_SEG3_RATE",
                100: "E4_VOICE_FENV_SEG3_TGTLVL",
                101: "E4_VOICE_FENV_SEG4_RATE",
                102: "E4_VOICE_FENV_SEG4_TGTLVL",
                103: "E4_VOICE_FENV_SEG5_RATE",
                104: "E4_VOICE_FENV_SEG5_TGTLVL",
                105: "E4_VOICE_LFO_RATE",
                106: "E4_VOICE_LFO_SHAPE",
                107: "E4_VOICE_LFO_DELAY",
                108: "E4_VOICE_LFO_VAR",
                109: "E4_VOICE_LFO_SYNC",
                110: "E4_VOICE_LFO2_RATE",
                111: "E4_VOICE_LFO2_SHAPE",
                112: "E4_VOICE_LFO2_DELAY",
                113: "E4_VOICE_LFO2_VAR",
                114: "E4_VOICE_LFO2_SYNC",
                115: "E4_VOICE_LFO2_OP0_PARM",
                116: "E4_VOICE_LFO2_OP1_PARM",
                117: "E4_VOICE_AENV_SEG0_RATE",
                118: "E4_VOICE_AENV_SEG0_TGTLVL",
                119: "E4_VOICE_AENV_SEG1_RATE",
                120: "E4_VOICE_AENV_SEG1_TGTLVL",
                121: "E4_VOICE_AENV_SEG2_RATE",
                122: "E4_VOICE_AENV_SEG2_TGTLVL",
                123: "E4_VOICE_AENV_SEG3_RATE",
                124: "E4_VOICE_AENV_SEG3_TGTLVL",
                125: "E4_VOICE_AENV_SEG4_RATE",
                126: "E4_VOICE_AENV_SEG4_TGTLVL",
                127: "E4_VOICE_AENV_SEG5_RATE",
                128: "E4_VOICE_AENV_SEG5_TGTLVL",
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
                # 183: "NUMBER OF ZONES",
            }

link_params = {
                23:"E4_LINK_PRESET",
                24:"E4_LINK_VOLUME",
                25:"E4_LINK_PAN",
                26:"E4_LINK_TRANSPOSE",
                27:"E4_LINK_FINE_TUNE",
                28:"E4_LINK_KEY_LOW",
                29:"E4_LINK_KEY_LOWFADE",
                30:"E4_LINK_KEY_HIGH",
                31:"E4_LINK_KEY_HIGHFADE",
                32:"E4_LINK_VEL_LOW",
                33:"E4_LINK_VEL_LOWFADE",
                34:"E4_LINK_VEL_HIGH",
                35:"E4_LINK_VEL_HIGHFADE",
}

zone_fields = [
                    "sample","volume","pan","fine_tune","orig_key",
                    "key_low","key_lowfade","key_high","key_highfade",
                    "vel_low","vel_lowfade","vel_high","vel_highfade"
                ]

def decode_ctrl_param(raw_word: int) -> int:
        """
        Given the 14‑bit word raw = lsb + (msb<<7),
        return the EOS “Ctrl A” value in the range -1…126.
        127 means “off” (–1).
        """
        seven_bit = raw_word >> 7      # drop the low 7 bits (always zero)
        return 127 if seven_bit == 127 else seven_bit


MODEL_MAP = {
        (0x00, 0x05): "E4",
        (0x01, 0x05): "E64",
        (0x02, 0x05): "E4k",
        (0x03, 0x05): "E64FX",
        (0x04, 0x05): "E4XT",
        (0x05, 0x05): "E4X",
        (0x06, 0x05): "E6400",
        (0x07, 0x05): "E4XT ULTRA",
        (0x08, 0x05): "E6400 ULTRA",
    }









class DeviceInfoFrame(wx.Frame):
    def __init__(self,message, timeout_ms=2000):
        super().__init__(self,
                        title="E4 Info",
                        size=(400, 150),
                        style=wx.DEFAULT_FRAME_STYLE & ~wx.RESIZE_BORDER)

        # ─── layout ───────────────────────────────────────────
        panel = wx.Panel(self)
        st    = wx.StaticText(panel, label=message)
        btn   = wx.Button(panel, id=wx.ID_OK, label="OK")
        btn.Bind(wx.EVT_BUTTON, lambda e: self.Close())

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(st,  1, wx.ALL|wx.EXPAND, 10)
        sizer.Add(btn, 0, wx.ALL|wx.ALIGN_CENTER, 10)
        panel.SetSizerAndFit(sizer)

        # ─── one‐shot timer to close the frame ────────────────
        self._timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, lambda e: self.Close(), self._timer)
        # start in single‐shot mode
        self._timer.Start(timeout_ms, oneShot=True)

        self.Show()





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

greencontrol = (153, 245, 198, 0)

in_name = 'UMC1820 MIDI In 0'
out_name = 'UMC1820 MIDI Out 1'
class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="E4 Open Interface", size=(1040,600))
        self.SetBackgroundColour("medium grey")
        self.SetForegroundColour(wx.Colour(153, 245, 198))

        self.menu_bar = wx.MenuBar()
        self.create_menu_bar()
        
        self.Bind(wx.EVT_CLOSE, self.on_close)
        
        # self.midi_popup = MidiConnectPopup(self, self.open_midi_ports)
        self.should_run_sysex_thread = True
        self.device_id = 1
        # local_appdata = os.environ.get("LOCALAPPDATA",
        #                                 os.path.expanduser("~"))
        # cfg_dir = os.path.join(local_appdata, "E4OpenInterface")
        # os.makedirs(cfg_dir, exist_ok=True)

        # self.CFG_FILE = os.path.join(cfg_dir, "settings.ini")
        # print("Config file will live at:", self.CFG_FILE)

        # # 2) create FileConfig pointing at that full path
        # self.cfg = wx.FileConfig(
        #     localFilename=self.CFG_FILE,
        #     style=wx.CONFIG_USE_LOCAL_FILE,
        #     appName="E4 Open Interface"
        # )

        # # 3) read any existing settings
        # self.out_name = self.cfg.Read("MIDI/OutPort", "")
        # self.in_name  = self.cfg.Read("MIDI/InPort",  "")
        
        # print("Restored ports:", self.in_name, "→", self.out_name)
        
        # self.outport = None
        # self.inport = None
        # if not self.out_name or not self.in_name:
        #     print("not self.out_name or not self.in_name", self.out_name, self.in_name)
        #     self.connect_midi()
        # else:
        #     self.open_midi_ports(self.in_name, self.out_name, self.device_id)

        self.should_run_sysex_thread = True
        self.sysex_queue = None
        self.sysex_send_delay = 0.02  # delay in seconds between messages (e.g. 50 ms)
        

        
        
        

        self.num_params = 0
        self.current_preset = 0
        self._pending_sample_name = {}
        self.dump_expected_length = 0
        
        self.packets   = {}
        self.payload   = []
        self.seen_widgets = set()
        self.seen_params = set()
        
        self.parsed_data = []
        
        self._last_update_time = {}
        
        self.in_name = None
        self.out_name = None
        
        self.midi_connected = False
        
        # self.send_midi = send_midi_message
        self.SOURCE_VALUE_TO_INDEX = {key: i for i, key in enumerate(SOURCE_OPTIONS)}
        self.DST_VALUE_TO_INDEX = {key: i for i, key in enumerate(DEST_OPTIONS)}

        self.getting_voices = False
        
        
        
        
        self.controls = Controls()
        self.voices_by_page = {}
        self.current_page_update = 1
        
        

        
        
        pnl = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        pnl.SetSizer(main_sizer)
        self.SetDefaultItem(None)
        
        # --- Preset # strip at top
        strip = wx.BoxSizer(wx.HORIZONTAL)
        
        # kb = create_open_frame_button(pnl, send_midi=send_midi_message, send_sysex=send_sysex)
        # strip.Add(kb, 0,wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5)
        
        # self.test_button = wx.Button(pnl, label="test")
        # strip.Add(self.test_button, 0,wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5)
        # self.test_button.Bind(wx.EVT_BUTTON, self.on_test)
        
        
        self.cc_button = wx.Button(pnl, label="CC Ctrlrs")
        strip.Add(self.cc_button, 0,wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5)
        self.cc_button.Bind(wx.EVT_BUTTON, self.on_cc)
        
        
        self.get_button = wx.Button(pnl, label="Get Preset")
        strip.Add(self.get_button, 0,wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5)
        self.get_button.Bind(wx.EVT_BUTTON, self.get_preset)
        strip.Add((10,0))
        self.preset_number_label = wx.StaticText(pnl, label="Preset Number: ")
        self.preset_number_label.SetForegroundColour(wx.Colour(153, 245, 198))
        strip.Add(self.preset_number_label, 0,wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 10)
        self.preset_number = wx.TextCtrl(pnl, value="0", style=wx.TE_PROCESS_ENTER|wx.TE_RIGHT,size=(60,-1))
        strip.Add(self.preset_number, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 10)
        self.preset_number.Bind(wx.EVT_TEXT_ENTER, self.get_preset)
        
        
        
        self.preset_name_label = wx.StaticText(pnl, label="Preset Name: ")
        self.preset_name_label.SetForegroundColour(wx.Colour(153, 245, 198))
        strip.Add(self.preset_name_label, 0,wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 10)
        self.preset_name = wx.StaticText(pnl, label="—")
        self.preset_name.SetForegroundColour(wx.Colour(153, 245, 198))
        strip.Add(self.preset_name, 1, wx.ALIGN_CENTER_VERTICAL)


        strip.AddStretchSpacer()  


        # Connect midi button
        self.connect_midi_button = wx.Button(pnl, label="Connect E4 (Midi)")
        strip.Add(self.connect_midi_button, 0,wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        self.connect_midi_button.Bind(wx.EVT_BUTTON, self.connect_midi)
        self.status_label = wx.StaticText(pnl, label="Not Connected")
        # self.status_label.SetForegroundColour(wx.Colour(200, 50, 75))
        strip.Add(self.status_label, 1, wx.ALIGN_CENTER_VERTICAL)
        
        
        # device button
        self.device_button = wx.Button(pnl, label="E4 Device info")
        strip.Add(self.device_button, 0,
                wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        self.device_button.Bind(wx.EVT_BUTTON, self.get_device_info)
        main_sizer.Add(strip, 0, wx.EXPAND|wx.ALL, 10)
        
        
        
        
        #==============================================================================================================================
        #==============================================================================================================================
        #==============================================================================================================================        

        
        
        self.metronome = MetronomePanel(pnl, self)
        main_sizer.Add(self.metronome, 0, wx.EXPAND | wx.ALL, 10)
        
        
        
        self.front_panel = FrontPanelFrame(pnl, self)
        self.front_panel.SetMinSize((1000, 160))
        main_sizer.Add(self.front_panel, 0, wx.EXPAND | wx.ALL, 10)
        
        
        #==============================================================================================================================
        #==============================================================================================================================
        #==============================================================================================================================
        
        # --- Notebook + Tabs ---
        self.nb = wx.Notebook(pnl)
        self.nb.SetBackgroundColour("light grey")
        self.master_global_panel = MasterGlobalPanel(self.nb, self)
        self.preset_panel  = PresetPanel(self.nb, self)
        self.voice_zones_panel  = Voice_Zones_Panel(self.nb, self)
        self.preset_effects_panel = PresetEffectsPanel(self.nb, self)
        self.master_effects_panel = MasterEffectsPanel(self.nb, self)
        self.edit_voice_panel = EditVoicePanels(self.nb, self)
        self.midiglo_panel = MidigloPanel(self.nb, self)
        self.links_panel = Links_Panel(self.nb, self)
        
        self.ccframe = CCframe(self)

        self.nb.AddPage(self.preset_panel,  "Selected Preset")
        self.nb.AddPage(self.voice_zones_panel,  "Preset Voices")
        self.nb.AddPage(self.edit_voice_panel,  "Voice Edit")
        self.nb.AddPage(self.preset_effects_panel,  "Preset Effects")
        self.nb.AddPage(self.master_effects_panel,  "Master Effects")
        self.nb.AddPage(self.midiglo_panel,  "Midiglo / Midi Prefs")
        self.nb.AddPage(self.links_panel,  "Links")
        self.nb.AddPage(self.master_global_panel,  "Master Global")
    
        main_sizer.Add(self.nb, 1, wx.EXPAND|wx.ALL, 10)
        
        #==============================================================================================================================
        #==============================================================================================================================
        #==============================================================================================================================
        

        
        #==============================================================================================================================
        #==============================================================================================================================
        #==============================================================================================================================
        
        self.Centre(wx.BOTH)
        self.Show()
        

        #==============================================================================================================================
        #==============================================================================================================================
        #==============================================================================================================================
        
        local_appdata = os.environ.get("LOCALAPPDATA",
                                        os.path.expanduser("~"))
        cfg_dir = os.path.join(local_appdata, "E4OpenInterface")
        os.makedirs(cfg_dir, exist_ok=True)

        self.CFG_FILE = os.path.join(cfg_dir, "settings.ini")
        print("Config file will live at:", self.CFG_FILE)

        # 2) create FileConfig pointing at that full path
        self.cfg = wx.FileConfig(
            localFilename=self.CFG_FILE,
            style=wx.CONFIG_USE_LOCAL_FILE,
            appName="E4 Open Interface"
        )

        # 3) read any existing settings
        self.out_name = self.cfg.Read("MIDI/OutPort", "")
        self.in_name  = self.cfg.Read("MIDI/InPort",  "")
        
        print("Restored ports:", self.in_name, "→", self.out_name)
        self.midi_popup = None
        self.outport = None
        self.inport = None
        if not self.out_name or not self.in_name:
            self.connect_midi()
        else:
            self.open_midi_ports(self.in_name, self.out_name, self.device_id)

        self.ccframe.cc.restore_cc_notes()
        #==============================================================================================================================
        #==============================================================================================================================
        #==============================================================================================================================
        

    def print_all(self):
        """Print every id→widget (or id→value) mapping in self.controls."""
        for name, d in vars(self.controls).items():
            if isinstance(d, dict):
                print(f"\n{name} ({len(d)} items):")
                if d:
                    for key, val in d.items():
                        if key == 218:
                            print(val.Parent)
                        print(f"  {key!r} → {val!r}")
                else:
                    print("  <empty>")

  
    def on_test(self, evt):
        # self.ccframe.Show()
        self.print_all()

    def on_cc(self, evt):
        self.ccframe.Show()





        #==============================================================================================================================
        #==============================================================================================================================
        #==============================================================================================================================




        
    def send_sysex(self, msg):
        if self.outport is None:
            raise RuntimeError("MIDI out not initialized")
        # print(msg)
        self.sysex_queue.put(msg)  



    def process_sysex_queue(self):
        while self.should_run_sysex_thread:
            # this will block until there's something in the queue
            msg = self.sysex_queue.get()
            try:
                self.outport.send(msg)
                # print("Sent:", msg)
            except Exception as e:
                print("Failed to send:", e)
            time.sleep(self.sysex_send_delay) 



    def send_midi(self, msg):
        if self.outport is None:
            raise RuntimeError("MIDI out not initialized")
        # print(msg)
        self.outport.send(msg)        
            


        
    def connect_midi(self, event = None):
        print("connect_midi(self, event = None):")
        self.midi_popup = MidiConnectPopup(self, self.open_midi_ports)
        
        
        
        
        
        
        
    def open_midi_ports(self, inport_name, outport_name, device_id):
        self.in_name = inport_name
        self.out_name = outport_name
        self.device_id = device_id
        self.outport = mido.open_output(self.out_name)
        self.inport = mido.open_input(self.in_name, callback=self.handle_midi)
        self.sysex_queue = queue.Queue()
        threading.Thread(target=self.process_sysex_queue, daemon=True).start()
        self.get_device_info(None)
        
        
        
        
        
        
        
    def get_device_info(self, event = None):
        print("Attempting to contact the E4. Sending Emu ID request")
        sysex=[0x7E,0x7F,0x06,0x01]
        msg = Message('sysex', data=sysex)
        self.outport.send(msg)
        
        
        
        
    def handle_midi(self, message: Message):
        print("midi callback", message.bytes())
        raw = message.bytes()
        # print(raw)
        if raw[0] == 240:
            self.parse_sysex_response(raw)    
        
        
        
        
        
        
        
        
        
    def parse_sysex_response(self, raw):
        # print('parse_sysex_response')
        
        data = raw[1:-1]
        # print(data)
        if data[2] == 6:
            if data[3] == 2:
                print("*E4 Response* Device Id =", self.device_id)
                if self.midi_connected == False:
                    self.midi_connected = True
                    self.status_label.SetLabelText("Connected")
                    self.status_label.SetForegroundColour(wx.Colour(0, 192, 0))  # a nice green
                    self.status_label.Refresh()
                    if hasattr(self, "out_name") and self.out_name:
                        self.cfg.Write("MIDI/OutPort", self.out_name)
                    if hasattr(self, "in_name") and self.in_name:
                        self.cfg.Write("MIDI/InPort",  self.in_name)
                    # make sure it really writes out to settings.ini
                    self.cfg.Flush()
                self.parse_identity_reply_sysex(raw)
                
            return
            
        if data[4] == 1:
            self.decode_parameter_value_response(raw)
            return
        elif data[4] == 5:
            self.preset_grid_panel.parse_preset_name_response(data)
            
            
        elif data[4] == 13:  # Command for preset dump
            # self.sample_detail_panel.parse_sample_memory_response(data)
            
            if data[5] == 1:  # Dump Header subcommand
                self.dump_expected_length = (
                    data[7] |
                    (data[8] << 7) |
                    (data[9] << 14) |
                    (data[10] << 21)
                )
                # print("Preset Dump Expected Length ", self.dump_expected_length)
                self.send_preset_dump_ack(data[6])  # Send ACK for dump header packet
                
                
                
            elif data[5] == 2:  # Dump Data Message subcommand
                print("[Preset Dump Message cmd 2]")

                self.add_packet(raw)
                # Send ACK for data message
            
        elif data[4] == 64:  # End of SysEx message
                if data[7] == 1:
                    print("Front Panel Button Pressed :", data[5])
                elif data[7] == 0:
                    print("Front Panel Button Released :", data[5])


        elif data[4] == 123:  # End of SysEx message
            print("[EOX] Preset Dump COMPLETED")
            self.parse_preset_dump(self.payload)
            
        elif data[4] == 125:  # Cancel SysEx message
            print("[Cancel] End of SysEx message received parse_sysex_response")
            
        elif data[4] == 126:  # NAK message
            print("[NAK] NAK received.")
            # Handle NAK: resend or take corrective action
            # self.resend_last_packet()  # Example, implement this method for resending the packet
            
        elif data[4] == 127:  # ACK message
            print("[ACK] received. cmd:", data[5])
            if data[5] == 17:
                print("Session Status : Open")
            # self.send_ack(data[6])
            
    
        
        #====================================================================================================================
        #====================================================================================================================
        #=========================================SAMPLES===========================================================================
        
        
        elif data[4] == 9:
            # self.parse_sample_name_response(data)
            print("Sample Name Response")
            
        elif data[4] == 6:
            # self.preset_grid_panel.parse_preset_name_response(data)  
            print("Preset Name Response")
        #============================================SAMPLES========================================================================
        #====================================================================================================================
        #====================================================================================================================

        else:
            print("[Error] Unrecognized SYSEX message type : in function : parse_sysex_response")    
        
        
        
        
        
        
        
        
        
        
#====================================================================================================================
#====================================================================================================================
#====================================================================================================================
#====================================================================================================================
#====================================================================================================================
#====================================================================================================================        

        
        
        
        
        
        
        
    def parse_identity_reply_sysex(self, sysex_data):
        try:
            device_id = sysex_data[2]
            manufacturer_id = sysex_data[5]
            family_code = sysex_data[6] | (sysex_data[7] << 7)
            model_code = sysex_data[8]
            # print(sysex_data[5], family_code,sysex_data[6],sysex_data[7] )
            

            swrev = ''.join(chr(b) for b in sysex_data[10:14])

            manufacturer_lookup = {
                0x18: "Emu",
            }

            model_lookup = {
                0: "E4",
                1: "E64",
                2: "E4K",
                3: "E64FX",
                4: "E4XT",
                5: "E4X",
                6: "E6400",
                7: "E4XT ULTRA",
                8: "E6400 ULTRA",
            }

            mfr_str = manufacturer_lookup.get(manufacturer_id, f"Unknown (0x{manufacturer_id:02X})")
            model_str = model_lookup.get(model_code, f"Unknown model (code 0x{model_code:04X})")

            
            self.device_id = device_id
            
            id_msg = (
                f"Device ID: ({device_id})\n"
                f"Manufacturer ID: ({mfr_str})\n"
                f"Model: {model_str}\n"
                f"Eos Version: {swrev}"
            )

            # usage:
            wx.MessageBox(id_msg, "MIDI Identity Response", wx.OK | wx.ICON_INFORMATION)
            data = [24,127,1,0,16]
            msg  = mido.Message('sysex', data=data)
            self.outport.send(msg)
        except Exception as e:
            wx.MessageBox(f"Error parsing SysEx Identity Reply:\n{e}", "Error", wx.OK | wx.ICON_ERROR)
        
        


    def send_preset_dump_ack(self, packet_number):
        """Send an ACK message to acknowledge receipt of the dump packet"""
        sysex=[0x18, 0x21, 0x01, 0x55, 0x7F, packet_number]
        # print("Sending Ack, Packet Number ", packet_number)
        msg = Message('sysex', data=sysex)
        self.outport.send(msg)
        



    def add_packet(self, raw: list[int]):
        """
        Store each packet by its packet number (raw[6]).
        Strip off the first 7 bytes (header) and final byte (EOX).
        """
        # print("packet ", raw)
        pkt = raw[7]
        raw = raw[7:-1]
        self.payload.extend(raw)
        # print("payload", self.payload)
        self.send_preset_dump_ack(pkt)
        
        
        
        
#====================================================================================================================
#====================================================================================================================
#====================================================================================================================
#====================================================================================================================
#====================================================================================================================
#====================================================================================================================        

        
        
        
    def get_preset(self, event = None): #request_preset
        
        now = time.time()
        last = self._last_update_time.get(1111, 0)
        # if we updated this param less than 1.5 seconds ago, skip it
        if now - last < 5:
            return
        # otherwise remember this update time and actually update
        self._last_update_time[1111] = now
        # print("Send the “new‐preset‐dump” request SysEx.")
        
        if self.midi_connected == False:
            self.connect_midi()
            return
        self.seen_params = set()
        self.dump_expected_length = 0
        self.packets   = {}
        self.payload   = []
        number = 0
        lsb =  number        & 0x7F
        msb = (number >> 7)  & 0x7F
        
        sysex = [0x18, 
                0x21, 
                self.device_id,
                0x55,       # Model sub‑ID
                0x0E, 
                lsb, msb]
        
        self.current_preset = self.preset_number.GetValue()
        self.preset_panel.preset.E4_PRESET_NUMBER.SetLabel(str(self.current_preset))
        # self.send_parameter_edit(223, int(self.current_preset))
        msg = Message('sysex', data=sysex)
        self.send_sysex(msg)
            
            
            
            
            
            
            
    
    def update_parameter_value(self, param_id, value):
        
        if param_id in self.controls.dragger_by_id:
            # print("dragger", param_id, value)
            dragger = self.controls.dragger_by_id[param_id]
            dragger.set_value(value)
            dragger.value = value


        elif param_id in self.controls.entry_by_id:
            # print("entry", param_id, value)
            self.controls.entry_by_id[param_id].SetValue(str(value))

        elif param_id in self.controls.combo_by_id:
            # print("combo", param_id, value)
            
            if param_id == 66: 
                # value = poly_modes_map_rev[value]
                self.controls.combo_by_id[param_id].SetSelection(value)
                
            elif param_id == 69:
                # value = submix_ports_rev[value]
                self.controls.combo_by_id[param_id].SetSelection(value)
                
            elif param_id == 65:   
                # value = solo_modes_rev[value]
                self.controls.combo_by_id[param_id].SetSelection(value)

            elif param_id == 68:
                # value = amp_env_depths[value]
                self.controls.combo_by_id[param_id].SetSelection(value)
                
            elif param_id in CORD_SRC_PARAMS_SET:
                self.controls.combo_by_id[param_id].SetSelection(self.SOURCE_VALUE_TO_INDEX[value])
            elif param_id in CORD_DST_PARAMS_SET:
                self.controls.combo_by_id[param_id].SetSelection(self.DST_VALUE_TO_INDEX[value])
            else:
                self.controls.combo_by_id[param_id].SetSelection(value)

        elif param_id in self.controls.listbox_by_id:
            # print("listbox", param_id, value)
            self.controls.listbox_by_id[param_id].SetSelection(max(0, value - 1))  # listbox is often 1-based in EOS

        elif param_id in self.controls.spin_by_id:
            # print("spin", param_id, value)
            self.controls.spin_by_id[param_id].SetValue(value)

        elif param_id in self.controls.check_by_id:
            # print("checkbox", param_id, value)
            self.controls.check_by_id[param_id].SetValue(bool(value))


        elif param_id in self.controls.radio_by_id:
            # print("radio", param_id, value)
            self.controls.radio_by_id[param_id].SetSelection(value)
        
        else:
            print("Unknown Parameter", param_id)


    
    
    
    
    
    
    
    
    def decode_parameter_value_response(self, data):
        if data[0] != 0xF0 or data[-1] != 0xF7:
            raise ValueError("Not a valid SysEx message.")

        if data[5] != 0x01:
            raise ValueError("Not a Parameter Value Response (expected command 0x01).")


        # Extract ID and Data
        param_id = data[7] | (data[8] << 7)
        value = data[9] | (data[10] << 7)
        


        if value > 1000:
            value = int(round(value / 16383 * 127))
        # value = self.normalize_midi7bit(value)
        self.update_parameter_value(param_id,value)







    def normalize_midi7bit(val: int) -> int:

        if val < 0:
            return 0
        if val <= 127:
            return val
        if val <= 0x3FFF:  # 16383
            return val >> 7
        return 127









    

    
    
    
    
    
    
    def request_all_individual_params(self):
        self.seen_widgets = set()
        self.seen_params = set()
        self.name_to_param = {v: k for k, v in param_names.items()}
        

        widget_maps = [
            ("dragger_by_id", self.controls.dragger_by_id),
            ("entry_by_id", self.controls.entry_by_id),
            ("combo_by_id", self.controls.combo_by_id),
            ("spin_by_id", self.controls.spin_by_id),
            ("check_by_id", self.controls.check_by_id),
            ("listbox_by_id", self.controls.listbox_by_id),
            ("radio_by_id", self.controls.radio_by_id),
            ("last_param", self.controls.last_param)
        ]

        for map_name, widget_map in widget_maps:
            for k, v in widget_map.items():
                # print(k,v)
                param = None
                if k == 1111:
                    print("* All parameters scanned *")
                    # self.request_voice_page_params(self.current_page_update)
                    
                else:
                    try:
                        if isinstance(k, int):
                            param = k
                        else:
                            param = self.name_to_param[k]
                    except Exception as e:
                        print(f"{k}, {v}, {type(k)}, Got exception: {e!r}")
                        continue

                    # Skip if already seen
                    if param in self.seen_params:
                        # print(f"Skipping duplicate param {param} from map '{map_name}'")
                        continue
                
                    self.seen_params.add(param)
                    self.seen_widgets.add(v)
                    self.send_parameter_request(param)



    def send_parameter_request(self, param_id):
            # print("send_parameter_request", param_id)


            LSB = param_id & 0x7F
            MSB = (param_id >> 7) & 0x7F
            checksum = (~((LSB + MSB) & 0x7F)) & 0x7F

            sysex = [

                0x18,         # E-MU Manufacturer ID
                0x21,         # E4 product ID
                self.device_id,    # Target device ID
                0x55,         # Special Editor byte
                0x02,         # Parameter Value Request command
                0x01,         # Byte count (1 word/pair)
                LSB, MSB,     # Parameter ID (LSB first)
                checksum,     # XOR 1's complement of LSB + MSB
    
            ]
            msg = Message('sysex', data=sysex)
            self.send_sysex(msg)
            return






        
#====================================================================================================================
#====================================================================================================================
#====================================================================================================================
#====================================================================================================================
#====================================================================================================================
#====================================================================================================================        

        





    def _on_ctrl_clicked(self, event):
        ctrl = event.GetEventObject()
        wId = ctrl.GetId()
        preset = getattr(ctrl, 'preset', None)
        link   = getattr(ctrl, 'link',   None)
        voice  = getattr(ctrl, 'voice',  None)
        group  = getattr(ctrl, 'group',  None)
        zone   = getattr(ctrl, 'zone',   None)
        
        _mapping = {
            'preset': (223, preset),
            'link':   (224, link),
            'voice':  (225, voice),
            'zone':   (226, zone),
            'group':  (227, group),
        }

        for name, (pid, val) in _mapping.items():
            if val is not None:
                self.send_parameter_edit(pid, val)




    def _onAnyControlChanged(self, event):
        """Fires whenever any of the preset controls change."""
        ctrl = event.GetEventObject()
        wId = ctrl.GetId()


        # Now figure out the value depending on control type
        if isinstance(ctrl, DraggableNumber):
            
            val = ctrl.value
        elif isinstance(ctrl, wx.TextCtrl):
            wId = wId - 1000
            val = ctrl.GetValue()
            try:
                val = int(val)
            except ValueError:
                pass  # keep as string if not int
        elif isinstance(ctrl, wx.RadioBox):
            val = ctrl.GetSelection()
        elif isinstance(ctrl, wx.ComboBox):
            val = ctrl.GetSelection()  # or GetStringSelection()
        elif isinstance(ctrl, wx.ListBox):
            val = ctrl.GetSelection()
        elif isinstance(ctrl, wx.SpinCtrl):
            val = ctrl.GetValue()
        elif isinstance(ctrl, wx.CheckBox):
            val = int(ctrl.GetValue())  # 0 = unchecked, 1 = checked
        elif isinstance(ctrl, wx.Slider):
            val = ctrl.GetValue()
        else:
            print(f"Unhandled control type: {type(ctrl)}")
            val = None

        print(f"Parameter {wId} changed to {val!r}")

        if val is not None:
            self.send_parameter_edit(wId, val)

        event.Skip()  # let other handlers still process the event if needed

        
        
        
        
        
        
        
    
        
        
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
        self.send_sysex(msg)    
        
        
        
        
        
        
#====================================================================================================================
#====================================================================================================================
#====================================================================================================================
#====================================================================================================================
#====================================================================================================================
#====================================================================================================================        










            
            
    def parse_preset_dump(self, data: list[int]):
        
        """
        data: the concatenated SysEx dump payload (all 7-bit words, no F0/F7)
        """
        try:
            payload = data[:]   # work on a copy
            cursor = 0
            parsed_data = {}  # short‐hand for self.parsed_data
            voices = []
            
            # --- Preset Number (2 bytes → 14-bit word) ---
            raw14 = payload[cursor] | (payload[cursor+1] << 7)
            preset_number = raw14 - 1
            parsed_data['E4_PRESET_NUMBER'] = preset_number
            print(f"E4_PRESET_NUMBER: {preset_number}")
            cursor += 2

            # --- Preset Name (16 ASCII bytes) ---
            name_bytes = payload[cursor:cursor+16]
            preset_name = ''.join(chr(b) for b in name_bytes if 32 <= b < 127).strip()
            parsed_data['E4_PRESET_NAME'] = preset_name
            print(f"E4_PRESET_NAME: '{preset_name}'")
            cursor += 16




            
            # --- Global Parameters (22 words) ---
            global_params = {}
            
            global_pids = [0, 1, 2, 3, 4,
                        5, 6, 7, 8, 9,
                        10, 11, 12, 13, 14, 
                        15, 16, 17, 18, 19, 
                        20, 21]
            
            for pid in global_pids:
                raw14 = payload[cursor] | (payload[cursor+1] << 7)
                raw7  = raw14 >> 7

                if pid == 0 or pid == 1 or pid == 2 or pid == 3 or pid == 4 or pid == 5:
                    # raw7 is 0…127 but fine-tune is –64…+63
                    val7 = raw7 - 128 if raw7 >= 64 else raw7
                else:
                    val7 = decode_ctrl_param(raw14)
                
                name = global_param_names[pid]
                global_params[name] = val7
                print(f"  {name}: {val7}")
                cursor += 2



            # --- Links Section ---
            # read the 14-bit word that holds “number of links”
            raw14_links = payload[cursor] | (payload[cursor+1] << 7)
            num_links   = raw14_links >> 7
            parsed_data['num_links'] = num_links
            print(f"\nNumber of Links: {num_links}")
            cursor += 2

            # # now actually parse each Link’s 13 parameters (2 bytes each → one 14-bit word)

            links = []
            link_pids = [23, 24, 25, 26, 27,
                        28, 29, 30, 31, 32,
                        33, 34, 35]
            if num_links != 0:
                for link_idx in range(num_links):
                    link_data = {}
                    print(f"\n-- Link {link_idx+1} --")
                    for pid in link_pids:
                        raw14 = payload[cursor] | (payload[cursor+1] << 7)
                        raw7  = raw14 >> 7
                        if pid == 24 or pid == 25 or pid == 26 or pid == 27:
                            # raw7 is 0…127 but fine-tune is –64…+63
                            val7 = raw7 - 128 if raw7 >= 64 else raw7
                        else:
                            val7 = decode_ctrl_param(raw14)
                            
                        name = link_params[pid]
                        link_data[name] = val7
                        print(f"  {name}: {val7}")
                        cursor += 2

                    links.append(link_data)

            parsed_data['links'] = links




            # --- Voices Section ---
            raw14_voices = payload[cursor] | (payload[cursor+1] << 7)
            num_voices = raw14_voices >> 7
            parsed_data['num_voices'] = num_voices
            print(f"\nNumber of Voices: {num_voices}")
            cursor += 2

            parsed_data['voices'] = []
            # Voice Parms: (292 Bytes * Number of Voices)
            for v in range(num_voices):
                voice = {}
                print(f"\n--- Voice {v+1} ---")

                # group number
                group = payload[cursor] | (payload[cursor+1] << 7)
                group = decode_ctrl_param(group)
                while group == 0: 
                    cursor += 2
                    group = payload[cursor] | (payload[cursor+1] << 7)
                    group = raw14_zone >> 7
                    print("skip byte") #========================================= skipping extra bytes. I don't know why they're there, but sometimes they are
                                                                                # the logic is, there is no group 0, so if group == 0 then that's not the right value,
                                                                                # skipping the bytes until group is a value not 0 works.

                voice['group'] = group
                print(f" Group Number: {group}")
                cursor += 2

                



                # Sample
                raw14_sample = payload[cursor] | (payload[cursor+1] << 7)
                raw14_sample = (raw14_sample >> 7) & 0x7F
                
                # sometimes there are extra bytes right here, so check the next value just to see if it's 127, 
                # which would mean it's a multisample, because volume max value is 10, so that wouldn't be 127, so if 127 
                # is here then it's probably a multisample ========================================================
                
                if raw14_sample != 127: 
                    cursor += 2
                    raw14_sample2 = payload[cursor] | (payload[cursor+1] << 7)
                    raw14_sample2 = (raw14_sample2 >> 7) & 0x7F
                    if raw14_sample2 == 127:
                        raw14_sample = raw14_sample2
                    else: #==============================================================================================================================================
                        cursor -= 2

                is_multisample = (raw14_sample == 127)
                voice['is_multisample'] = is_multisample
                print(f"\nVoice is Multisample? {is_multisample}")

                # parse params 38..181
                param_pids = list(range(38, 184))
                voice_params = {}
                
                voice_neg_val_params = [59, 60, 69,]  #=================================== these parameters can return negative values, so adjust
                                        # 129, 130, 132, 133, 135, 136, 138, 139,
                                        # 141, 142, 144, 145, 147, 148, 150, 151,
                                        # 153, 154, 156, 157, 159, 160, 162, 163,
                                        # 165, 166, 168, 169, 171, 172, 174, 175,
                                        # 177, 178, 180, 181]
                
                src_ids = [
                    129, 132, 135, 138, 141, 144, 147, 150, 153, 156, 159, 162, 165, 168, 171, 174, 177, 180
                ]

                dst_ids = [
                    130, 133, 136, 139, 142, 145, 148, 151, 154, 157, 160, 163, 166, 169, 172, 175, 178, 181
                ]

                amt_ids = [ #========================================================these values are 0-255 so they have to be decoded differently than a value with max 127
                    131, 134, 137, 140, 143, 146, 149, 152, 155, 158, 161, 164, 167, 170, 173, 176, 179, 182
                ]
                
                src_options = [
                0, 4, 8, 9, 10, 11, 12, 13, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
                32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 48, 72, 73, 74, 80, 81, 82, 88,
                89, 90, 96, 97, 98, 99, 100, 101, 104, 105, 106, 107, 108, 109, 144, 145, 146,
                147, 148, 149, 160, 161, 162, 163, 164, 165, 166, 167
                ]

                dst_options = [
                    0, 8, 47, 48, 49, 50, 51, 52, 53, 54, 56, 57, 64, 65, 66, 68, 69, 70, 71, 72, 73,
                    74, 75, 80, 81, 82, 83, 86, 88, 89, 90, 91, 94, 96, 97, 104, 105, 106, 108, 161,
                    162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177,
                    178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191
                ]

                for pid in param_pids:
                    if pid == 44 and is_multisample:
                        cursor += 2
                    else:
                        raw14 = payload[cursor] | (payload[cursor+1] << 7)
                        raw7  = raw14 >> 7
                        # print(pid, raw14, raw7)
                        if pid in voice_neg_val_params:
                            val7 = raw7 - 128 if raw7 >= 64 else raw7
                            
                        elif pid in amt_ids:
                            val7 = raw7
                            # print("val7 ", val7, raw7)
                        
                        elif pid in src_ids:
                            # print("src_ids raw7", raw7)
                            if raw7 in src_options:
                                val7 = raw7
                            else:
                                if raw7 + 128 in src_options:
                                    val7 = raw7 + 128
                                else:
                                    cursor += 2
                                    raw14 = payload[cursor] | (payload[cursor+1] << 7)
                                    val7  = raw14 >> 7
                                    # print("raw7 not in src_options")
                                
                        elif pid in dst_ids:
                            # print("dst_ids raw7", raw7, raw7+128)
                            
                            
                            if raw7 in dst_options:
                                val7 = raw7
                            else:
                                if raw7 + 128 in dst_options:
                                    val7 = raw7 + 128
                                else:
                                    cursor += 2
                                    raw14 = payload[cursor] | (payload[cursor+1] << 7)
                                    val7  = raw14 >> 7
                                    # print("raw7 not in dst_options")
                        else:
                            val7  = decode_ctrl_param(raw14)
                            
                        name  = dump_param_names.get(pid, f"ID_{pid}")
                        voice_params[name] = val7
                        print(f"   {name}: {val7}")
                        cursor += 2

                voice['params'] = voice_params




                # read zone count
                raw14_zone = payload[cursor] | (payload[cursor+1] << 7)
                zone_count = raw14_zone >> 7
                if is_multisample and zone_count <= 1:
                    cursor -= 2
                    raw14_zone = payload[cursor] | (payload[cursor+1] << 7)
                    zone_count = raw14_zone >> 7

                    # Try up to 5 times moving forward to find zone_count > 0
                    for _ in range(5):
                        if zone_count == 0:
                            # print("skip byte")
                            cursor += 2
                            raw14_zone = payload[cursor] | (payload[cursor+1] << 7)
                            zone_count = raw14_zone >> 7
                        else:
                            break

                    # If still zero, search backwards (with a safety limit to avoid infinite loop)
                reverse_limit = 20
                reverse_attempts = 0
                while zone_count == 0 and reverse_attempts < reverse_limit:
                    cursor -= 2
                    # print("reverse byte")
                    raw14_zone = payload[cursor] | (payload[cursor+1] << 7)
                    zone_count = raw14_zone >> 7
                    reverse_attempts += 1

                    # zone_count is now > 0, or you hit your backwards search limit

                                
                    
                print(f"\nVoice {v+1} : {zone_count} zones")
                cursor += 2
                if is_multisample:
                    
                
                # --- parse each zone’s 13 words (26 bytes) ---
                    zones = []
                    # these are the sample-zone PIDs in order:
                    zone_pids = [38, 39, 40, 42, 44,
                                    45, 46, 47, 48, 49,
                                    50, 51, 52]
                    
                    for z in range(zone_count):
                        zone = {}
                        print(f"  Zone {z+1}:")
            
                        for pid in zone_pids:
                            raw14 = payload[cursor] | (payload[cursor+1] << 7)
                            raw7  = raw14 >> 7
                            if pid == 38 and raw7 == 0: 
                                cursor += 2
                                raw14 = payload[cursor] | (payload[cursor+1] << 7)
                                raw7  = raw14 >> 7

                            # special-case signed pan and fine-tune
                            if pid == 39 or pid == 40 or pid == 41 or pid == 42 or pid == 43:
                                # raw7 is 0…127 but pan and fine-tune is –64…+63
                                val7 = raw7 - 128 if raw7 >= 64 else raw7
                            else:
                                val7 = decode_ctrl_param(raw14)
                                
                            name  = dump_param_names.get(pid, f"ID_{pid}")
                            zone[name] = val7
                            print(f"    {name}: {val7}")
                            cursor += 2
                        
                        zones.append(zone)

                    voice['zones'] = zones
                    parsed_data['voices'].append(voice)
                    voices.append(voice)
                    

            if is_multisample:
                self.parsed_data = parsed_data
                self.update_panels(parsed_data)
                
            else:
                
                voice['zones'] = zones
                
                parsed_data['voices'].append(voice)
                voices.append(voice)
                self.parsed_data = parsed_data
                self.update_panels(parsed_data)
        except Exception as e:
            print(f"[Error] while parsing preset dump: {e}")
            self.parsed_data = parsed_data
            self.update_panels(parsed_data)        
            
            
            
            
#====================================================================================================================
#====================================================================================================================
#====================================================================================================================
#====================================================================================================================
#====================================================================================================================
#====================================================================================================================        

            
            
            
    def update_panels(self, data):
        self.preset_name.SetLabel(data["E4_PRESET_NAME"])
        self.preset_panel.preset.E4_PRESET_NAME.SetLabel(data["E4_PRESET_NAME"])
        self.preset_panel.preset.E4_PRESET_NUMBER.SetLabel(str(data["E4_PRESET_NUMBER"]))
        self.current_preset = data["E4_PRESET_NUMBER"]
        if data['num_voices'] > 0:
            self.voice_zones_panel.display_all_zones(data)
        if data['num_links'] > 0:
            self.links_panel.display_all_links(data)
        self.request_all_individual_params()
            
            
            
# #===============================================================================================================
# #===============================================================================================================
# #===============================================================================================================    





    def on_donate_click(self, event):
        import webbrowser
        webbrowser.open("https://www.paypal.com/donate/?business=XQVKTPXF82CZ2&no_recurring=0&item_name=Thank+you%21+Your+appreciation+is+gratefully+received+and+it+encourages+development+on+the+E4+Open+Interface+and+beyond%21%F0%9F%99%8F%F0%9F%98%8C&currency_code=USD")

    def create_menu_bar(self):
        # Create the menu bar
        menu_bar = self.menu_bar
        # File menu
        file_menu = wx.Menu()
        item_quit = file_menu.Append(wx.ID_EXIT, "E&xit\tCtrl+Q", "Quit the application")
        self.Bind(wx.EVT_MENU, self.on_close, item_quit)
        menu_bar.Append(file_menu, "&File")

        # Help menu
        help_menu = wx.Menu()
        help_menu.Append(wx.ID_HELP, "&Help", "Open the illustrated help")
        menu_bar.Append(help_menu, "&Help")

        self.Bind(wx.EVT_MENU, self.on_show_help, id=wx.ID_HELP)


        item_about = help_menu.Append(wx.ID_ABOUT, "&About", "Show info about this app")
        self.Bind(wx.EVT_MENU, self.on_about, item_about)
        
        donate_menu = wx.Menu()
        item_donate = donate_menu.Append(wx.ID_ANY, "Development Appreciation : Donate via PayPal", "Donate via PayPal")
        menu_bar.Append(donate_menu, "&Donate")
        self.Bind(wx.EVT_MENU, self.on_donate_click, item_donate)

        
        self.SetMenuBar(menu_bar)

    def on_show_help(self, _evt):
        dlg = HelpDialog(self)
        dlg.ShowModal()
        dlg.Destroy()

    def on_close(self, evt):
        print("Closing")
        
        # save the cc user notes
        self.ccframe.cc.save_notes()
        # # — save current port names before we actually close —
        if hasattr(self, "out_name") and self.out_name:
            self.cfg.Write("MIDI/OutPort", self.out_name)
        if hasattr(self, "in_name") and self.in_name:
            self.cfg.Write("MIDI/InPort",  self.in_name)
        # make sure it really writes out to settings.ini
        self.cfg.Flush()
        self.should_run_sysex_thread = False
        # now close your ports
        try: self.outport.close()
        except: pass
        try: self.inport.close()
        except: pass
        self.ccframe.Destroy()
        self.Destroy()
        evt.Skip()
        

    def on_about(self, event):
        wx.MessageBox("E4 Open Interface", "Author : JohnnyGadget \nE4 Open Interface v.1111", wx.OK | wx.ICON_INFORMATION)

    
    
    
#===============================================================================================================
#===============================================================================================================
#===============================================================================================================

console_text = '''
o--o o  o      o-o                    o-O-o       o           o-o             
|    |  |     o   o                     |         |           |               
O-o  o--O     |   | o-o  o-o o-o        |   o-o  -o- o-o o-o -O-  oo  o-o o-o 
|       |     o   o |  | |-' |  |       |   |  |  |  |-' |    |  | | |    |-' 
o--o    o      o-o  O-o  o-o o  o     o-O-o o  o  o  o-o o    o  o-o- o-o o-o 
                    |                                                         
                    o                                                         
    
┏┳  ┓            ┓     
 ┃┏┓┣┓┏┓┏┓┓┏┏┓┏┓┏┫┏┓┏┓╋
┗┛┗┛┛┗┛┗┛┗┗┫┗┫┗┻┗┻┗┫┗ ┗
           ┛ ┛     ┛   
    '''

if __name__ == "__main__":
    
    app = wx.App(False)
    MainFrame().Show()
    app.MainLoop()
    print(console_text)  # Should always print!
    
#  _______ _     _    _______                      _                           ___                   
# (_______) |   (_)  (_______)                    | |       _                 / __)                  
#  _____  | |_____    _     _ ____  _____ ____    | |____ _| |_ _____  ____ _| |__ _____  ____ _____ 
# |  ___) |_____  |  | |   | |  _ \| ___ |  _ \   | |  _ (_   _) ___ |/ ___|_   __|____ |/ ___) ___ |
# | |_____      | |  | |___| | |_| | ____| | | |  | | | | || |_| ____| |     | |  / ___ ( (___| ____|
# |_______)     |_|   \_____/|  __/|_____)_| |_|  |_|_| |_| \__)_____)_|     |_|  \_____|\____)_____)
#                            |_|                                                                     

# 
# 
# +-+-+ +-+-+-+-+-+-+-+-+-+-+-+-+
# |b|y| |J|o|h|n|n|y|g|a|d|g|e|t|    
# +-+-+ +-+-+-+-+-+-+-+-+-+-+-+-+ 
    

    
    
