import wx
import wx.lib.scrolledpanel as scrolled
from custom_widgets import DraggableNumber,  EVT_DRAGGABLENUMBER
import math
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
# from popperouter import Popperouter
E4_VOICE_FTYPE           = 82
E4_VOICE_FMORPH          = 83
E4_VOICE_FKEY_XFORM      = 84
E4_VOICE_FILT_GEN_PARM3  = 87
E4_VOICE_FILT_GEN_PARM4  = 88
E4_VOICE_FILT_GEN_PARM5  = 89
E4_VOICE_FILT_GEN_PARM6  = 90
E4_VOICE_FILT_GEN_PARM7  = 91
E4_VOICE_FILT_GEN_PARM8  = 92

FILTER_PARAMS = {
    82: "E4_VOICE_FTYPE",
    83: "E4_VOICE_FMORPH",
    84:"E4_VOICE_FKEY_XFORM",
    87:"E4_VOICE_FILT_GEN_PARM3",
    88:"E4_VOICE_FILT_GEN_PARM4",
    89:"E4_VOICE_FILT_GEN_PARM5",
    90:"E4_VOICE_FILT_GEN_PARM6",
    91:"E4_VOICE_FILT_GEN_PARM7",
    92:"E4_VOICE_FILT_GEN_PARM8"
    }

# Mapping from ID → parameter name
FILTER_PARAMETERS = {
    E4_VOICE_FTYPE:            "E4_VOICE_FTYPE",
    E4_VOICE_FMORPH:         "E4_VOICE_FMORPH",
    E4_VOICE_FKEY_XFORM:     "E4_VOICE_FKEY_XFORM",
    E4_VOICE_FILT_GEN_PARM3: "E4_VOICE_FILT_GEN_PARM3",
    E4_VOICE_FILT_GEN_PARM4: "E4_VOICE_FILT_GEN_PARM4",
    E4_VOICE_FILT_GEN_PARM5: "E4_VOICE_FILT_GEN_PARM5",
    E4_VOICE_FILT_GEN_PARM6: "E4_VOICE_FILT_GEN_PARM6",
    E4_VOICE_FILT_GEN_PARM7: "E4_VOICE_FILT_GEN_PARM7",
    E4_VOICE_FILT_GEN_PARM8: "E4_VOICE_FILT_GEN_PARM8",
}



# -----------------------------------------------------------------------------
# Conversion routines
# -----------------------------------------------------------------------------
def fil_freq(inp: int, maxfreq: int, mul: int) -> int:
    """
    C equivalent:
      int f = maxfreq;
      input = 255 - input;
      while (input-- > 0) f *= mul, f /= 1024;
      return f;
    """
    f = maxfreq
    countdown = 255 - inp
    for _ in range(countdown):
        f = (f * mul) // 1024
    return f

def format_table1(inp: int) -> str:
    # Filter Table 1: maxfreq=20000, mul=1002
    return f"{fil_freq(inp, 20000, 1002)}Hz"

def format_table2(inp: int) -> str:
    # Filter Table 2: maxfreq=18000, mul=1003
    return f"{fil_freq(inp, 18000, 1003)}Hz"

def format_table3(inp: int) -> str:
    # Filter Table 3: maxfreq=10000, mul=1006
    return f"{fil_freq(inp, 10000, 1006)}Hz"

def format_gain(inp: int) -> str:
    # C: gain10x = -240 + ((input * 120) / 32);
    # out_i = gain10x/10; out_f = abs(gain10x%10);
    gain10x = -240 + ((inp * 120) // 32)
    gain_i = gain10x // 10
    gain_f = abs(gain10x % 10)
    sign = "+" if gain10x >= 0 else "-"
    return f"{sign}{abs(gain_i)}.{gain_f}dB"

def format_table5(inp: int) -> str:
    # Filter Table 5: cnv_morph_freq(2*input)
    return f"{fil_freq(2*inp, 10000, 1006)}Hz"

def format_table6(inp: int) -> str:
    # Filter Table 5: cnv_morph_freq(2*input)
    return inp - 64



# ---------------------------------------------------------------------------
# Parameter definitions for each filter type
# Each entry has min, max, a comment string, and whether it's int or float.
# ---------------------------------------------------------------------------
    

# Parameter definitions for each filter type
# lp_params = {
#     "Frequency Morph":{"name":"Frequency Morph", "id": 83, "value":0, "min": 0,   "max": 255,   "comment": "Morph: 0 to 255, Frequency: 57Hz to 20000Hz", "display": format_table1,  "table":1,               "type": "int", "frequency line":"Vertical"},
#     "Q": {"name":"Q", "id": 84, "value":0, "min": 0,   "max": 127,   "comment": "Key Transform Q: 0 to 127",          "type": "int", "frequency line":"Horizontal"},
# }




# hp_params = {
#     "Frequency Morph":{"name":"Frequency Morph", "id": 83, "value":0, "min": 0,   "max": 255,   "comment": "Morph: 0 to 255, Frequency: 69Hz to 18000Hz", "display": format_table2, "table":2,                 "type": "int", "frequency line":"Vertical"},
#     "Q": {"name":"Q", "id": 84, "min": 0, "value":0,   "max": 127,   "comment": "Key Transform Q: 0 to 127",           "type": "int", "frequency line":"Horizontal"},
# }

# bp_params = {
#     "Frequency Morph":{"name":"Frequency Morph", "id": 83, "value":0, "min": 0,   "max": 255,   "comment": "Morph: 0 to 255, Frequency: 57Hz to 10000Hz","display": format_table3,   "table":3,               "type": "int", "frequency line":"Vertical"},
#     "Q": {"name":"Q", "id": 84, "value":0, "min": 0,   "max": 127,   "comment": "Key Transform Q: 0 to 127",          "type": "int"    , "frequency line":"Horizontal"},
# }

# swept_eq_params = {
#     "Frequency Morph":{"name":"Frequency Morph", "id": 83, "value":0, "min": 0,   "max": 255,   "comment": "Morph: 0 to 255, Frequency: 83Hz to 10000Hz",      "display": format_table3,       "table":3,               "type": "int"  , "frequency line":"Vertical"},
#     "Gain":             {"name":"Gain", "id": 84, "value":0, "min": 0,   "max": 127,   "comment": "Key Transform Gain: -24.0 dB to +23.6 dB",         "display": format_gain,         "table":4,               "type": "int"  , "frequency line":"Horizontal"},    

# }

# phaser_params = {
#     "Frequency Morph": {"name":"Frequency Morph", "id": 83, "value":0, "min": 0,   "max": 255,   "comment": "Morph: 0 to 255, Frequency: 0 to 255","type": "int", "frequency line":"Vertical"},
#     "Resonance": {"name":"Resonance", "id": 84, "value":0, "min": 0,   "max": 127,   "comment": "Key Transform Resonance: 0 to 127",       "type": "int"},
# }

# vocal_params = {
#     "Morph":     {"name":"Morph", "id": 83, "value":0, "min": 0, "max": 255, "comment": "Morph: 0 to 255",    "type": "int"},
#     "Body Size": {"name":"Body Size", "id": 84, "value":0, "min": 0, "max": 127, "comment": "Body Size: 0 to 127","type": "int"},
# }

# dual_eq_params = {
#     "Morph":     {"name":"Morph", "id": 83, "value":0, "min": 0,    "max": 255,  "comment": "Morph: 0 to 255",                 "type": "int"},
#     "Gain":      {"name":"Gain", "id": 84, "value":0, "min": 0, "max": 127, "comment": "Gain: -24.0 dB to +23.6 dB", "display": format_gain,  "table":4,     "type": "float", "frequency line":"Horizontal"},
#     "EQ1 Low":   {"name":"EQ1 Low", "id": 87, "value":0, "min": 0, "max": 127, "comment": "EQ 1 Low: 83Hz to 9824Hz", "display": format_table5,  "table":5,       "type": "int", "frequency line":"Vertical"},
#     "EQ1 High":  {"name":"EQ1 High", "id": 88, "value":0, "min": 0, "max": 127, "comment": "EQ 1 High: 83Hz to 9824Hz", "display": format_table5, "table":5,      "type": "int", "frequency line":"Vertical"},
#     "EQ1 Gain":  {"name":"EQ1 Gain", "id": 89, "value":0, "min": 0, "max": 127, "comment": "EQ 1 Gain: -24.0 dB to +23.6 dB", "display": format_gain, "table":4, "type": "float", "frequency line":"Horizontal"},
#     "EQ2 Low":   {"name":"EQ2 Low", "id": 90, "value":0, "min": 0, "max": 127, "comment": "EQ 2 Low: 83Hz to 9824Hz", "display": format_table5,  "table":5,      "type": "int", "frequency line":"Vertical"},
#     "EQ2 High":  {"name":"EQ2 High", "id": 91, "value":0, "min": 0, "max": 127, "comment": "EQ 2 High: 83Hz to 9824Hz", "display": format_table5,  "table":5,     "type": "int", "frequency line":"Vertical"},
#     "EQ2 Gain":  {"name":"EQ2 Gain", "id": 92, "value":0, "min": 0, "max": 127, "comment": "EQ 2 Gain: -24.0 dB to +23.6 dB", "display": format_gain, "table":4, "type": "float", "frequency line":"Horizontal"},
# }

# twoeq_lowpass_params = {
#     "Fc/Morph":   {"name":"Fc/Morph", "id": 83, "value":0, "min": 0,   "max": 255,   "comment": "Fc/Morph: 0 to 255",              "type": "int"},
#     "LPF Q":      {"name":"LPF Q", "id": 84, "value":0, "min": 0,   "max": 127,   "comment": "LPF Q: 0 to 127",                 "type": "int"},
#     "EQ1 Low":   {"name":"EQ1 Low", "id": 87, "value":0, "min": 0, "max": 127, "comment": "EQ 1 Low: 83Hz to 9824Hz", "display": format_table5,  "table":5,       "type": "int"},
#     "EQ1 High":  {"name":"EQ1 High", "id": 88, "value":0, "min": 0, "max": 127, "comment": "EQ 1 High: 83Hz to 9824Hz", "display": format_table5, "table":5,      "type": "int"},
#     "EQ1 Gain":  {"name":"EQ1 Gain", "id": 89, "value":0, "min": 0, "max": 127, "comment": "EQ 1 Gain: -24.0 dB to +23.6 dB", "display": format_gain, "table":4, "type": "float"},
#     "EQ2 Low":   {"name":"EQ2 Low", "id": 90, "value":0, "min": 0, "max": 127, "comment": "EQ 2 Low: 83Hz to 9824Hz", "display": format_table5,  "table":5,      "type": "int"},
#     "EQ2 High":  {"name":"EQ2 High", "id": 91, "value":0, "min": 0, "max": 127, "comment": "EQ 2 High: 83Hz to 9824Hz", "display": format_table5,  "table":5,     "type": "int"},
#     "EQ2 Gain":  {"name":"EQ2 Gain", "id": 92, "value":0, "min": 0, "max": 127, "comment": "EQ 2 Gain: -24.0 dB to +23.6 dB", "display": format_gain, "table":4, "type": "float"},
# }

# twoeq_expr_params = {
#     "Morph":      {"name":"Morph", "id": 83, "value":0, "min": 0,  "max": 255,   "comment": "Morph: 0 to 255",                 "type": "int"},
#     "Expression": {"name":"Expression", "id": 84, "value":0, "min": 0,  "max": 127,   "comment": "Expression: 0 to 127",           "type": "int"},
#      "EQ1 Low":   {"name":"EQ1 Low", "id": 87, "value":0, "min": 0, "max": 127, "comment": "EQ 1 Low: 83Hz to 9824Hz", "display": format_table5,  "table":5,       "type": "int"},
#     "EQ1 High":  {"name":"EQ1 High", "id": 88, "value":0, "min": 0, "max": 127, "comment": "EQ 1 High: 83Hz to 9824Hz", "display": format_table5, "table":5,      "type": "int"},
#     "EQ1 Gain":  {"name":"EQ1 Gain", "id": 89, "value":0, "min": 0, "max": 127, "comment": "EQ 1 Gain: -24.0 dB to +23.6 dB", "display": format_gain, "table":4, "type": "float"},
#     "EQ2 Low":   {"name":"EQ2 Low", "id": 90, "value":0, "min": 0, "max": 127, "comment": "EQ 2 Low: 83Hz to 9824Hz", "display": format_table5,  "table":5,      "type": "int"},
#     "EQ2 High":  {"name":"EQ2 High", "id": 91, "value":0, "min": 0, "max": 127, "comment": "EQ 2 High: 83Hz to 9824Hz", "display": format_table5,  "table":5,     "type": "int"},
#     "EQ2 Gain":  {"name":"EQ2 Gain", "id": 92, "value":0, "min": 0, "max": 127, "comment": "EQ 2 Gain: -24.0 dB to +23.6 dB", "display": format_gain, "table":4, "type": "float"},
# }

# peak_shelf_params = {
#     "Morph":        {"name":"Morph", "id": 83, "value":0, "min": 0,  "max": 255,  "comment": "Morph: 0 to 255",                                                                "type": "int"},
#     "Peak":         {"name":"Peak", "id": 84, "value":0, "min": 0,  "max": 127,  "comment": "Peak: -24.0 dB to +23.6 dB",                 "display": format_gain, "table":4,   "type": "float"},
#     "Low-Freq":     {"name":"Low-Freq", "id": 87, "value":0, "min": 0,  "max": 127,  "comment": "Low morph frame Freq: 83Hz to 9824Hz",       "display": format_table5,"table":5, "type":"int"},
#     "Low-Shelf":    {"name":"Low-Shelf", "id": 88, "value":0, "min": 0,  "max": 127,  "comment": "Low morph frame Shelf: -64 to 63",           "display": format_table5,"table":6, "type":"int"},
#     "Low-Peak":     {"name":"Low-Peak", "id": 89, "value":0, "min": 0,  "max": 127,  "comment": "Low morph frame Peak: -24.0 dB to +23.6 dB", "display": format_gain,"table":4, "type":"float"},
#     "High-Freq":    {"name":"High-Freq", "id": 90, "value":0, "min": 0,  "max": 127,  "comment": "High morph frame Freq: 83Hz to 9824Hz",      "display": format_table5, "table":5,"type":"int"},
#     "High-Shelf":   {"name":"High-Shelf", "id": 91, "value":0, "min": 0,  "max": 127,  "comment": "High morph frame Shelf: -64 to 63",          "display": format_table5,"table":6, "type":"int"},
#     "High-Peak":    {"name":"High-Peak", "id": 92, "value":0, "min": 0,  "max": 127,  "comment": "High morph frame Peak: -24.0 dB to +23.6 dB","display": format_gain, "table":4,"type":"float"},
# }



lp_params = {
    1:{"name":"Frequency Morph", "id": 83, "value":0, "min": 0,   "max": 255,   "comment": "Morph: 0 to 255, Frequency: 57Hz to 20000Hz", "display": format_table1,  "table":1,               "type": "int", "frequency line":"Vertical"},
    2: {"name":"Q", "id": 84, "value":0, "min": 0,   "max": 127,   "comment": "Key Transform Q: 0 to 127",          "type": "int", "frequency line":"Horizontal"},
}




hp_params = {
    1:{"name":"Frequency Morph", "id": 83, "value":0, "min": 0,   "max": 255,   "comment": "Morph: 0 to 255, Frequency: 69Hz to 18000Hz", "display": format_table2, "table":2,                 "type": "int", "frequency line":"Vertical"},
    2: {"name":"Q", "id": 84, "min": 0, "value":0,   "max": 127,   "comment": "Key Transform Q: 0 to 127",           "type": "int", "frequency line":"Horizontal"},
}

bp_params = {
    1:{"name":"Frequency Morph", "id": 83, "value":0, "min": 0,   "max": 255,   "comment": "Morph: 0 to 255, Frequency: 57Hz to 10000Hz","display": format_table3,   "table":3,               "type": "int", "frequency line":"Vertical"},
    2: {"name":"Q", "id": 84, "value":0, "min": 0,   "max": 127,   "comment": "Key Transform Q: 0 to 127",          "type": "int"    , "frequency line":"Horizontal"},
}

swept_eq_params = {
    1:{"name":"Frequency Morph", "id": 83, "value":0, "min": 0,   "max": 255,   "comment": "Morph: 0 to 255, Frequency: 83Hz to 10000Hz",      "display": format_table3,       "table":3,               "type": "int"  , "frequency line":"Vertical"},
    2:             {"name":"Gain", "id": 84, "value":0, "min": 0,   "max": 127,   "comment": "Key Transform Gain: -24.0 dB to +23.6 dB",         "display": format_gain,         "table":4,               "type": "int"  , "frequency line":"Horizontal"},    

}

phaser_params = {
    1: {"name":"Frequency Morph", "id": 83, "value":0, "min": 0,   "max": 255,   "comment": "Morph: 0 to 255, Frequency: 0 to 255","type": "int", "frequency line":"Vertical"},
    2: {"name":"Resonance", "id": 84, "value":0, "min": 0,   "max": 127,   "comment": "Key Transform Resonance: 0 to 127",       "type": "int"},
}

vocal_params = {
    1:     {"name":"Morph", "id": 83, "value":0, "min": 0, "max": 255, "comment": "Morph: 0 to 255",    "type": "int"},
    2: {"name":"Body Size", "id": 84, "value":0, "min": 0, "max": 127, "comment": "Body Size: 0 to 127","type": "int"},
}

dual_eq_params = {
    1:     {"name":"Morph", "id": 83, "value":0, "min": 0,    "max": 255,  "comment": "Morph: 0 to 255",                 "type": "int"},
    2:      {"name":"Gain", "id": 84, "value":0, "min": 0, "max": 127, "comment": "Gain: -24.0 dB to +23.6 dB", "display": format_gain,  "table":4,     "type": "float", "frequency line":"Horizontal"},
    3:   {"name":"EQ1 Low", "id": 87, "value":0, "min": 0, "max": 127, "comment": "EQ 1 Low: 83Hz to 9824Hz", "display": format_table5,  "table":5,       "type": "int", "frequency line":"Vertical"},
    4:  {"name":"EQ1 High", "id": 88, "value":0, "min": 0, "max": 127, "comment": "EQ 1 High: 83Hz to 9824Hz", "display": format_table5, "table":5,      "type": "int", "frequency line":"Vertical"},
    5:  {"name":"EQ1 Gain", "id": 89, "value":0, "min": 0, "max": 127, "comment": "EQ 1 Gain: -24.0 dB to +23.6 dB", "display": format_gain, "table":4, "type": "float", "frequency line":"Horizontal"},
    6:   {"name":"EQ2 Low", "id": 90, "value":0, "min": 0, "max": 127, "comment": "EQ 2 Low: 83Hz to 9824Hz", "display": format_table5,  "table":5,      "type": "int", "frequency line":"Vertical"},
    7:  {"name":"EQ2 High", "id": 91, "value":0, "min": 0, "max": 127, "comment": "EQ 2 High: 83Hz to 9824Hz", "display": format_table5,  "table":5,     "type": "int", "frequency line":"Vertical"},
    8:  {"name":"EQ2 Gain", "id": 92, "value":0, "min": 0, "max": 127, "comment": "EQ 2 Gain: -24.0 dB to +23.6 dB", "display": format_gain, "table":4, "type": "float", "frequency line":"Horizontal"},
}

twoeq_lowpass_params = {
    1:   {"name":"Fc/Morph", "id": 83, "value":0, "min": 0,   "max": 255,   "comment": "Fc/Morph: 0 to 255",              "type": "int"},
    2:      {"name":"LPF Q", "id": 84, "value":0, "min": 0,   "max": 127,   "comment": "LPF Q: 0 to 127",                 "type": "int"},
    3:   {"name":"EQ1 Low", "id": 87, "value":0, "min": 0, "max": 127, "comment": "EQ 1 Low: 83Hz to 9824Hz", "display": format_table5,  "table":5,       "type": "int"},
    4:  {"name":"EQ1 High", "id": 88, "value":0, "min": 0, "max": 127, "comment": "EQ 1 High: 83Hz to 9824Hz", "display": format_table5, "table":5,      "type": "int"},
    5:  {"name":"EQ1 Gain", "id": 89, "value":0, "min": 0, "max": 127, "comment": "EQ 1 Gain: -24.0 dB to +23.6 dB", "display": format_gain, "table":4, "type": "float"},
    6:   {"name":"EQ2 Low", "id": 90, "value":0, "min": 0, "max": 127, "comment": "EQ 2 Low: 83Hz to 9824Hz", "display": format_table5,  "table":5,      "type": "int"},
    7:  {"name":"EQ2 High", "id": 91, "value":0, "min": 0, "max": 127, "comment": "EQ 2 High: 83Hz to 9824Hz", "display": format_table5,  "table":5,     "type": "int"},
    8:  {"name":"EQ2 Gain", "id": 92, "value":0, "min": 0, "max": 127, "comment": "EQ 2 Gain: -24.0 dB to +23.6 dB", "display": format_gain, "table":4, "type": "float"},
}

twoeq_expr_params = {
    1:   {"name":"Morph", "id": 83, "value":0, "min": 0,   "max": 255,   "comment": "Fc/Morph: 0 to 255",              "type": "int"},
    2:      {"name":"Expression", "id": 84, "value":0, "min": 0,   "max": 127,   "comment": "Expression: 0 to 127",                 "type": "int"},
    3:   {"name":"EQ1 Low", "id": 87, "value":0, "min": 0, "max": 127, "comment": "EQ 1 Low: 83Hz to 9824Hz", "display": format_table5,  "table":5,       "type": "int"},
    4:  {"name":"EQ1 High", "id": 88, "value":0, "min": 0, "max": 127, "comment": "EQ 1 High: 83Hz to 9824Hz", "display": format_table5, "table":5,      "type": "int"},
    5:  {"name":"EQ1 Gain", "id": 89, "value":0, "min": 0, "max": 127, "comment": "EQ 1 Gain: -24.0 dB to +23.6 dB", "display": format_gain, "table":4, "type": "float"},
    6:   {"name":"EQ2 Low", "id": 90, "value":0, "min": 0, "max": 127, "comment": "EQ 2 Low: 83Hz to 9824Hz", "display": format_table5,  "table":5,      "type": "int"},
    7:  {"name":"EQ2 High", "id": 91, "value":0, "min": 0, "max": 127, "comment": "EQ 2 High: 83Hz to 9824Hz", "display": format_table5,  "table":5,     "type": "int"},
    8:  {"name":"EQ2 Gain", "id": 92, "value":0, "min": 0, "max": 127, "comment": "EQ 2 Gain: -24.0 dB to +23.6 dB", "display": format_gain, "table":4, "type": "float"},
}

peak_shelf_params = {
    1:        {"name":"Morph", "id": 83, "value":0, "min": 0,  "max": 255,  "comment": "Morph: 0 to 255",          "type": "int"},
    2:         {"name":"Peak", "id": 84, "value":0, "min": 0,  "max": 127,  "comment": "Peak: -24.0 dB to +23.6 dB",                 "display": format_gain, "table":4,   "type": "float"},
    3:     {"name":"Low-Freq", "id": 87, "value":0, "min": 0,  "max": 127,  "comment": "Low morph frame Freq: 83Hz to 9824Hz",       "display": format_table5,"table":5, "type":"int"},
    4:    {"name":"Low-Shelf", "id": 88, "value":0, "min": 0,  "max": 127,  "comment": "Low morph frame Shelf: -64 to 63",           "display": format_table5,"table":6, "type":"int"},
    5:     {"name":"Low-Peak", "id": 89, "value":0, "min": 0,  "max": 127,  "comment": "Low morph frame Peak: -24.0 dB to +23.6 dB", "display": format_gain,"table":4, "type":"float"},
    6:    {"name":"High-Freq", "id": 90, "value":0, "min": 0,  "max": 127,  "comment": "High morph frame Freq: 83Hz to 9824Hz",      "display": format_table5, "table":5,"type":"int"},
    7:   {"name":"High-Shelf", "id": 91, "value":0, "min": 0,  "max": 127,  "comment": "High morph frame Shelf: -64 to 63",          "display": format_table5,"table":6, "type":"int"},
    8:    {"name":"High-Peak", "id": 92, "value":0, "min": 0,  "max": 127,  "comment": "High morph frame Peak: -24.0 dB to +23.6 dB","display": format_gain, "table":4,"type":"float"},
}


# Map filter names to their parameter sets
FILTER_DETAILS = {
    "2 Pole Low-pass":           lp_params,
    "4 Pole Low-pass":           lp_params,
    "6 Pole Low-pass":           lp_params,

    "2nd Order High-pass":       hp_params,
    "4th Order High-pass":       hp_params,

    "2nd Order Band-pass":       bp_params,
    "4th Order Band-pass":       bp_params,
    "Contrary Band-pass":        bp_params,

    "Swept EQ 1 octave":         swept_eq_params,
    "Swept EQ 2->1 oct":         swept_eq_params,
    "Swept EQ 3->1 oct":         swept_eq_params,

    "Phaser 1":                  phaser_params,
    "Phaser 2":                  phaser_params,
    "Bat-Phaser":                phaser_params,
    "Flanger Lite":              phaser_params,

    "Vocal Ah-Ay-Ee":            vocal_params,
    "Vocal Oo-Ah":               vocal_params,

    "Dual EQ Morph":             dual_eq_params,
    "2EQ+Lowpass Morph":         twoeq_lowpass_params,
    "2EQMorph+Exprssn":          twoeq_expr_params,

    "Peak/Shelf Morph":          peak_shelf_params,
}


FILTER_SYSEX_LSB = {
    "2 Pole Low-pass":           0,
    "4 Pole Low-pass":           1,
    "6 Pole Low-pass":           2,

    "2nd Order High-pass":       hp_params,
    "4th Order High-pass":       hp_params,

    "2nd Order Band-pass":       bp_params,
    "4th Order Band-pass":       bp_params,
    "Contrary Band-pass":        bp_params,

    "Swept EQ 1 octave":         swept_eq_params,
    "Swept EQ 2->1 oct":         swept_eq_params,
    "Swept EQ 3->1 oct":         swept_eq_params,

    "Phaser 1":                  phaser_params,
    "Phaser 2":                  phaser_params,
    "Bat-Phaser":                phaser_params,
    "Flanger Lite":              phaser_params,

    "Vocal Ah-Ay-Ee":            vocal_params,
    "Vocal Oo-Ah":               vocal_params,

    "Dual EQ Morph":             dual_eq_params,
    "2EQ+Lowpass Morph":         twoeq_lowpass_params,
    "2EQMorph+Exprssn":          twoeq_expr_params,

    "Peak/Shelf Morph":          peak_shelf_params,
}



    
    


class SpectrumPanel(wx.Panel):
    """Draws a log-frequency / dB grid plus red/green lines for your filter knobs."""
    def __init__(self, parent, height=120):
        super().__init__(parent, style=wx.BORDER_SIMPLE)
        self.SetMinSize((-1, height))
        self.lines = []  # [(direction, value, min, max), ...]

        # static grid settings
        self.freq_min     = 20
        self.freq_max     = 20000
        self.freq_markers = [60,120,250,500,1000,2000,4000,8000,16000,20000]

        self.db_min = -96
        self.db_max =  36

        self.Bind(wx.EVT_PAINT, self.on_paint)

    def update_lines(self, lines):
        self.lines = lines
        self.Refresh()

    def on_paint(self, evt):
        dc = wx.PaintDC(self)
        dc.Clear()
        w,h = self.GetClientSize()

        # background border
        dc.SetPen(wx.Pen((80,80,80)))
        dc.DrawRectangle(0,0,w,h)

        # freq grid (dotted grey verticals + labels)
        log_min = math.log10(self.freq_min)
        log_max = math.log10(self.freq_max)
        dc.SetPen(wx.Pen((100,100,100),1,wx.PENSTYLE_DOT))
        for f in self.freq_markers:
            if self.freq_min <= f <= self.freq_max:
                frac = (math.log10(f)-log_min)/(log_max-log_min)
                x = int(frac*w)
                dc.DrawLine(x,0,x,h)
                txt = f"{f}Hz"
                tw,th = dc.GetTextExtent(txt)
                dc.DrawText(txt, x-tw//2, h-th-2)

        # 0 dB line (dotted yellow)
        if self.db_max>self.db_min:
            db_frac = (self.db_max - 0)/(self.db_max-self.db_min)
            y0 = int(db_frac*h)
            dc.SetPen(wx.Pen((255,255,0),1,wx.PENSTYLE_DOT))
            dc.DrawLine(0,y0,w,y0)
            dc.DrawText("0 dB", 2, y0- dc.GetTextExtent("0 dB")[1] -2)

        # control lines
        for direction,val,mn,mx in self.lines:
            if mx<=mn: continue
            frac = (val-mn)/(mx-mn)
            if direction.lower()=="vertical":
                x = int(frac*w)
                dc.SetPen(wx.Pen((255,0,0),1))
                dc.DrawLine(x,0,x,h)
            elif direction.lower()=="horizontal":
                y = int((1-frac)*h)
                dc.SetPen(wx.Pen((0,255,0),1))
                dc.DrawLine(0,y,w,y)

class FilterPanel(wx.Panel):
    def __init__(self, parent, main, voice_dict):
        super().__init__(parent)
        self.main = main
        self.device_id  = main.device_id

        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(main_sizer)

        # Filter type
        hs = wx.BoxSizer(wx.HORIZONTAL)
        hs.Add(wx.StaticText(self, label="Filter Type:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)
        self.combo = wx.ListBox(self, id = 82, choices=list(FILTER_DETAILS.keys()), style=wx.LB_SINGLE)
        self.combo.SetSelection(voice_dict["params"]["E4_VOICE_FTYPE"])
        self.combo.Bind(wx.EVT_LISTBOX, self._on_filter_change)
        self.combo.SetMinSize((150, -1))
        self.combo.SetMaxSize((150, -1))
        hs.Add(self.combo, 1, wx.EXPAND)
        main_sizer.Add(hs, 1, wx.EXPAND|wx.ALL, 8)
        main.controls.combo_by_id[82] = self.combo
        # live spectrum
        # self.spectrum = SpectrumPanel(self)
        # main_sizer.Add(self.spectrum, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 8)

        # scrolling parameter area
        self.params_panel = scrolled.ScrolledPanel(self, style=wx.VSCROLL)
        self.params_panel.SetupScrolling(scroll_x=False, scroll_y=True)
        main_sizer.Add(self.params_panel, 1, wx.EXPAND|wx.ALL, 8)

        # data holders
        self.controls = {}  # id → (DraggableNumber, info dict)

        # init
        if self.combo.GetCount():
            self.combo.SetSelection(voice_dict["params"]["E4_VOICE_FTYPE"])
            self._on_filter_change(None)
            
    def _on_filter_change(self, evt):
        # clear out any old controls
        self.main.send_parameter_edit(82, self.combo.GetSelection())
        for child in self.params_panel.GetChildren():
            child.Destroy()
        self.controls.clear()

        filtername  = self.combo.GetStringSelection()
        params = FILTER_DETAILS[filtername]
            
        # build your 3-column grid
        grid = wx.GridSizer(rows=len(params), cols=3, hgap=10, vgap=10)
        for name, info in params.items():
            
            lbl = wx.StaticText(self.params_panel, label=info['name'])
            lbl.SetMinSize((120,20))
            # print(info, info['name'])
            dn = DraggableNumber(
                self.params_panel,
                id       = info["id"],
                value    = info["value"],
                min_val  = info["min"],
                max_val  = info["max"],
                step     = info.get("step",1),
                callback = self._on_control_dragged
            )
            dn.SetMinSize((80,20))
            dn.SetBackgroundColour(greencontrol)
            self.main.controls.dragger_by_id[info["id"]] = dn
            self.main.send_parameter_request(info["id"])

            ro = wx.StaticText(
                self.params_panel,
                label=info.get("display", lambda v: str(v))(info["min"])
            )
            ro.SetMinSize((40,20))

            grid.Add(lbl, 0, wx.ALIGN_CENTER_VERTICAL)
            grid.Add(dn,  0, wx.ALIGN_CENTER_VERTICAL)
            grid.Add(ro,  0, wx.ALIGN_CENTER_VERTICAL)

            self.controls[info["id"]] = (dn, ro, info)

        # wrap the grid in a vertical BoxSizer
        vs = wx.BoxSizer(wx.VERTICAL)
        vs.Add(grid,             0, wx.EXPAND)  # only as tall as it needs
        vs.AddStretchSpacer()                  # push any extra space below

        # install & layout
        self.params_panel.SetSizer(vs)
        self.params_panel.Layout()
        self.params_panel.SetupScrolling(scroll_x=False, scroll_y=True)

    def _on_control_dragged(self, evt):
        ctrl = evt.GetEventObject()
        pid  = ctrl.GetId()
        val  = evt.GetInt()
        dn, ro, info = self.controls[pid]

        fname  = self.combo.GetStringSelection()
        params = FILTER_DETAILS.get(fname, {})
        params["value"] = val

        # update the readout
        disp = info.get("display", lambda v:str(v))(val)
        ro.SetLabel(disp)

        # update graph
        # self._refresh_spectrum()
        self.main.send_parameter_edit(ctrl.Id, ctrl.value)

    # def _refresh_spectrum(self):
    #     lines = []
    #     for pid, (dn,_,info) in self.controls.items():
    #         direction = info.get("frequency line", "").lower()
    #         if direction in ("vertical","horizontal"):
    #             lines.append((direction, dn.value, info["min"], info["max"]))
    #     self.spectrum.update_lines(lines)

