
all_sysex_commands = [
    # ====================================================
    # 1. Preset Dump / Preset Parameter Dump Commands
    # ====================================================
    {
        "name": "Preset Dump Request",
        "id": 14,
        "hex_id": "0x0E",
        "tabegory": "Preset Dump",
        "category": "Preset Dump Commands",
        "sub_category": "Request",
        "parameters": {
            "preset_number": "0–999 (sent as 2 7-bit bytes)"
        },
        "recommended_ui": "Dropdown",
        "recommended_ui_alt": "numeric input",
        "recommended_ui_extra": "Numeric spinner",
        "notes": "Requests a full preset dump (or preset parameter dump) for a given preset number."
    },
    {
        "name": "Old Preset Dump Header",
        "id": 13,
        "hex_id": "0x0D (subcommand 0x01)",
        "tabegory": "Preset Dump",
        "category": "Preset Dump Commands",
        "sub_category": "Old Format",
        "sub_sub_category": "Header",
        "parameters": {
            "preset_number": "varies",
            "total_data_bytes": "4 bytes (LSB first)",
            "other header fields": "As defined in the old dump format"
        },
        "recommended_ui": "Automatic Display",
        "notes": "Header for the old preset dump format, containing dump size and additional header fields."
    },
    {
        "name": "Old Preset Dump Data Message",
        "id": 13,
        "hex_id": "0x0D (subcommand 0x02)",
        "tabegory": "Preset Dump",
        "category": "Preset Dump Commands",
        "sub_category": "Old Format",
        "sub_sub_category": "Data Message",
        "parameters": {
            "data_bytes": "256 data bytes per packet (except possibly the last)",
            "checksum": "1 byte (one’s complement of the sum of data bytes)"
        },
        "recommended_ui": "Automatic Display",
        "notes": "Data packet for the old dump format. Used to transfer bulk preset or parameter data."
    },
    {
        "name": "NEW Preset Dump Header",
        "id": 13,
        "hex_id": "0x0D (subcommand 0x03)",
        "tabegory": "Preset Dump",
        "category": "Preset Dump Commands",
        "sub_category": "New Format",
        "sub_sub_category": "Header",
        "parameters": {
            "preset_number": "2 bytes",
            "total_data_bytes": "4 bytes (LSB first)",
            "num_global_params": "2 bytes",
            "num_link_params": "2 bytes (per link)",
            "num_voice_params": "2 bytes (per voice)",
            "num_zone_params": "2 bytes (per zone)"
        },
        "recommended_ui": "Automatic Display",
        "notes": "Header for the NEW preset dump format with extended parameter counts."
    },
    {
        "name": "NEW Preset Dump Data Message",
        "id": 13,
        "hex_id": "0x0D (subcommand 0x04)",
        "tabegory": "Preset Dump",
        "category": "Preset Dump Commands",
        "sub_category": "New Format",
        "sub_sub_category": "Data Message",
        "parameters": {
            "data_bytes": "244 data bytes per packet (except possibly the last)",
            "checksum": "1 byte (one’s complement of the sum of data bytes)"
        },
        "recommended_ui": "Automatic Display",
        "notes": "Data packet for the new preset dump method; used during bulk preset transfers."
    },

    # ====================================================
    # 2. Handshaking Commands
    # ====================================================
    {
        "name": "Generic Acknowledge (ACK)",
        "id": 127,
        "hex_id": "0x7F",
        "tabegory": "Preset Dump",
        "category": "Handshaking Commands",
        "sub_category": "General",
        "recommended_ui": "Automatic Display",
        "notes": "Indicates that the last packet was received correctly."
    },
    {
        "name": "Generic Negative Acknowledge (NAK)",
        "id": 126,
        "hex_id": "0x7E",
        "tabegory": "Preset Dump",
        "category": "Handshaking Commands",
        "sub_category": "General",
        "recommended_ui": "Automatic Display",
        "notes": "Indicates an error in the last received packet; instructs the sender to resend."
    },
    {
        "name": "CANCEL",
        "id": 125,
        "hex_id": "0x7D",
        "tabegory": "Preset Dump",
        "category": "Handshaking Commands",
        "sub_category": "Flow Control",
        "recommended_ui": "Button",
        "notes": "Cancels the current transmission or dump operation."
    },
    {
        "name": "WAIT (Pause Transmission until ACK is received)",
        "id": 124,
        "hex_id": "0x7C",
        "tabegory": "Preset Dump",
        "category": "Handshaking Commands",
        "sub_category": "Flow Control",
        "recommended_ui": "Button",
        "notes": "Instructs the sender to pause transmission until an ACK is received."
    },
    {
        "name": "EOF (End Of File)",
        "id": 123,
        "hex_id": "0x7B",
        "tabegory": "Preset Dump",
        "category": "Handshaking Commands",
        "sub_category": "Flow Control",
        "recommended_ui": "Automatic Display",
        "notes": "Signals that no more packets will follow."
    },
    {
        "name": "NEW ACK (for New Dump Method)",
        "id": 122,
        "hex_id": "0x7A",
        "tabegory": "Preset Dump",
        "category": "Handshaking Commands",
        "sub_category": "New Format",
        "parameters": {
            "packet_number": "2 bytes (7-bit encoded)"
        },
        "recommended_ui": "Automatic Display",
        "notes": "Acknowledges receipt of a packet under the new dump method."
    },
    {
        "name": "NEW NAK (for New Dump Method)",
        "id": 121,
        "hex_id": "0x79",
        "tabegory": "Preset Dump",
        "category": "Handshaking Commands",
        "sub_category": "New Format",
        "parameters": {
            "packet_number": "2 bytes (7-bit encoded)"
        },
        "recommended_ui": "Automatic Display",
        "notes": "Issues a negative acknowledge for a packet in the new dump method."
    },

    # ====================================================
    # 3. Other Preset and Remote Edit Commands
    # ====================================================
    {
        "name": "Preset Select / Recall",
        "id": 12,
        "hex_id": "0x0C",
        "tabegory": "Remote Edit",
        "category": "Preset and Remote Edit",
        "sub_category": "Preset Operations",
        "parameters": {
            "preset_number": "0–999 (2 7-bit bytes)"
        },
        "recommended_ui": "Dropdown",
        "recommended_ui_alt": "numeric input",
        "notes": "Selects and recalls the indicated preset from memory."
    },
    {
        "name": "Preset Write / Store",
        "id": 11,
        "hex_id": "0x0B",
        "tabegory": "Remote Edit",
        "category": "Preset and Remote Edit",
        "sub_category": "Preset Operations",
        "parameters": {
            "preset_number": "0–999",
            "preset_data": "variable length dump data"
        },
        "recommended_ui": "Button",
        "notes": "Stores the current preset data into the internal memory."
    },
    {
        "name": "Parameter Change / Remote Edit",
        "id": 10,
        "hex_id": "0x0A",
        "tabegory": "Remote Edit",
        "category": "Preset and Remote Edit",
        "sub_category": "Parameter Editing",
        "parameters": {
            "parameter_id": "varies (ID of the parameter)",
            "value": "varies (new parameter value)"
        },
        # "recommended_ui": "Slider for continuous values, dropdown or radio for discrete options",
        # "recommended_ui_alt": "Numeric field with real-time preview",
        "notes": "Changes a specific parameter value; useful for real‑time remote editing."
    },
    {
        "name": "System Inquiry / Firmware Version Request",
        "id": 20,
        "hex_id": "0x14",
        "tabegory": "Remote Edit",
        "category": "Preset and Remote Edit",
        "sub_category": "System Inquiry",
        "recommended_ui": "Button",
        "recommended_ui_2": "sysex return readout",
        "notes": "Requests details regarding the firmware version and overall system configuration."
    },

    # ====================================================
    # 4. GLOBAL Parameters
    # ====================================================
    {
        "name": "E4_PRESET_TRANSPOSE",
        "id": 0,
        "hex_id": "00h",
        "tabegory": "Preset",
        "category": "GLOBAL",
        "sub_category": "Preset Settings",
        "min": -24,
        "max": 24,
        "recommended_ui": "Slider",
        "ui_config": "horizontal",
        "notes": "Sets the global transposition (pitch shift) for the preset in semitones."
    },
    {
        "name": "E4_PRESET_VOLUME",
        "id": 1,
        "hex_id": "01h",
        "tabegory": "Preset",
        "category": "GLOBAL",
        "sub_category": "Preset Settings",
        "min": -96,
        "max": 10,
        "recommended_ui": "Slider",
        "ui_config": "horizontal",
        "notes": "Sets the overall preset volume in decibels (dB)."
    },
    {
        "name": "E4_PRESET_CTRL_A",
        "id": 2,
        "hex_id": "02h",
        "tabegory": "Preset",
        "category": "GLOBAL",
        "sub_category": "Control Assignments",
        "min": -1,
        "max": 127,
        "recommended_ui": "Slider",
        "ui_config": "vertical",
        "notes": "Assigns Control A; a value of -1 typically indicates that it is unassigned."
    },
    {
        "name": "E4_PRESET_CTRL_B",
        "id": 3,
        "hex_id": "03h",
        "tabegory": "Preset",
        "category": "GLOBAL",
        "sub_category": "Control Assignments",
        "min": -1,
        "max": 127,
        "recommended_ui": "Slider",
        "ui_config": "vertical",
        "notes": "Assigns Control B; -1 indicates unused."
    },
    {
        "name": "E4_PRESET_CTRL_C",
        "id": 4,
        "hex_id": "04h",
        "tabegory": "Preset",
        "category": "GLOBAL",
        "sub_category": "Control Assignments",
        "min": -1,
        "max": 127,
        "recommended_ui": "Slider",
        "ui_config": "vertical",
        "notes": "Assigns Control C; -1 indicates no assignment."
    },
    {
        "name": "E4_PRESET_CTRL_D",
        "id": 5,
        "hex_id": "05h",
        "tabegory": "Preset",
        "category": "GLOBAL",
        "sub_category": "Control Assignments",
        "min": -1,
        "max": 127,
        "recommended_ui": "Slider",
        "ui_config": "vertical",
        "notes": "Assigns Control D; if set to -1, it is unused."
    },
    {
        "name": "E4_PRESET_FX_A_ALGORITHM",
        "id": 6,
        "hex_id": "06h",
        "tabegory": "Preset",
        "category": "GLOBAL",
        "sub_category": "Effects",
        "min": 0,
        "max": 44,
        "recommended_ui": "Dropdown",
        "notes": "Chooses the algorithm (signal processing method) for Effects A."
    },
    {
        "name": "E4_PRESET_FX_A_PARM_0",
        "id": 7,
        "hex_id": "07h",
        "tabegory": "Preset",
        "category": "GLOBAL",
        "sub_category": "Effects",
        "min": 0,
        "max": 90,
        "recommended_ui": "Slider",
        "ui_config": "horizontal",
        "notes": "First parameter for Effects A; alters a specific aspect of the FX algorithm."
    },
    {
        "name": "E4_PRESET_FX_A_PARM_1",
        "id": 8,
        "hex_id": "08h",
        "tabegory": "Preset",
        "category": "GLOBAL",
        "sub_category": "Effects",
        "min": 0,
        "max": 127,
        "recommended_ui": "Slider",
        "ui_config": "horizontal",
        "notes": "Second parameter for Effects A."
    },
    {
        "name": "E4_PRESET_FX_A_PARM_2",
        "id": 9,
        "hex_id": "09h",
        "tabegory": "Preset",
        "category": "GLOBAL",
        "sub_category": "Effects",
        "min": 0,
        "max": 127,
        "recommended_ui": "Slider",
        "ui_config": "horizontal",
        "notes": "Third parameter for Effects A."
    },
    {
        "name": "E4_PRESET_FX_A_AMT_0",
        "id": 10,
        "hex_id": "0Ah",
        "tabegory": "Preset",
        "category": "GLOBAL",
        "sub_category": "Effects",
        "min": 0,
        "max": 100,
        "recommended_ui": "Slider",
        "ui_config": "vertical",
        "notes": "Amount control for Effects A parameter 0."
    },
    {
        "name": "E4_PRESET_FX_A_AMT_1",
        "id": 11,
        "hex_id": "0Bh",
        "tabegory": "Preset",
        "category": "GLOBAL",
        "sub_category": "Effects",
        "min": 0,
        "max": 100,
        "recommended_ui": "Slider",
        "ui_config": "vertical",
        "notes": "Amount control for Effects A parameter 1."
    },
    {
        "name": "E4_PRESET_FX_A_AMT_2",
        "id": 12,
        "hex_id": "0Ch",
        "tabegory": "Preset",
        "category": "GLOBAL",
        "sub_category": "Effects",
        "min": 0,
        "max": 100,
        "recommended_ui": "Slider",
        "ui_config": "vertical",
        "notes": "Amount control for Effects A parameter 2."
    },
    {
        "name": "E4_PRESET_FX_A_AMT_3",
        "id": 13,
        "hex_id": "0Dh",
        "tabegory": "Preset",
        "category": "GLOBAL",
        "sub_category": "Effects",
        "min": 0,
        "max": 100,
        "recommended_ui": "Slider",
        "ui_config": "vertical",
        "notes": "Amount control for Effects A parameter 3."
    },
    {
        "name": "E4_PRESET_FX_B_ALGORITHM",
        "id": 14,
        "hex_id": "0Eh",
        "tabegory": "Preset",
        "category": "GLOBAL",
        "sub_category": "Effects",
        "min": 0,
        "max": 27,
        "recommended_ui": "Dropdown",
        "notes": "Selects the algorithm for Effects B."
    },
    {
        "name": "E4_PRESET_FX_B_PARM_0",
        "id": 15,
        "hex_id": "0Fh",
        "tabegory": "Preset",
        "category": "GLOBAL",
        "sub_category": "Effects",
        "min": 0,
        "max": 127,
        "recommended_ui": "Slider",
        "ui_config": "horizontal",
        "notes": "First parameter for Effects B."
    },
    {
        "name": "E4_PRESET_FX_B_PARM_1",
        "id": 16,
        "hex_id": "10h",
        "tabegory": "Preset",
        "category": "GLOBAL",
        "sub_category": "Effects",
        "min": 0,
        "max": 127,
        "recommended_ui": "Slider",
        "ui_config": "horizontal",
        "notes": "Second parameter for Effects B."
    },
    {
        "name": "E4_PRESET_FX_B_PARM_2",
        "id": 17,
        "hex_id": "11h",
        "tabegory": "Preset",
        "category": "GLOBAL",
        "sub_category": "Effects",
        "min": 0,
        "max": 127,
        "recommended_ui": "Slider",
        "ui_config": "horizontal",
        "notes": "Third parameter for Effects B."
    },
    {
        "name": "E4_PRESET_FX_B_AMT_0",
        "id": 18,
        "hex_id": "12h",
        "tabegory": "Preset",
        "category": "GLOBAL",
        "sub_category": "Effects",
        "min": 0,
        "max": 100,
        "recommended_ui": "Slider",
        "ui_config": "vertical",
        "notes": "Amount control for Effects B parameter 0."
    },
    {
        "name": "E4_PRESET_FX_B_AMT_1",
        "id": 19,
        "hex_id": "13h",
        "tabegory": "Preset",
        "category": "GLOBAL",
        "sub_category": "Effects",
        "min": 0,
        "max": 100,
        "recommended_ui": "Slider",
        "ui_config": "vertical",
        "notes": "Amount control for Effects B parameter 1."
    },
    {
        "name": "E4_PRESET_FX_B_AMT_2",
        "id": 20,
        "hex_id": "14h",
        "tabegory": "Preset",
        "category": "GLOBAL",
        "sub_category": "Effects",
        "min": 0,
        "max": 100,
        "recommended_ui": "Slider",
        "ui_config": "vertical",
        "notes": "Amount control for Effects B parameter 2."
    },
    {
        "name": "E4_PRESET_FX_B_AMT_3",
        "id": 21,
        "hex_id": "15h",
        "tabegory": "Preset",
        "category": "GLOBAL",
        "sub_category": "Effects",
        "min": 0,
        "max": 100,
        "recommended_ui": "Slider",
        "ui_config": "vertical",
        "notes": "Amount control for Effects B parameter 3."
    },

    # ====================================================
    # 5. LINKS Parameters
    # ====================================================
    {
        "name": "E4_LINK_PRESET",
        "id": 23,
        "hex_id": "17h",
        "tabegory": "LINKS",
        "category": "LINKS",
        "sub_category": "Link Settings",
        "min": 0,
        "max": 999,  # May vary up to 1255 depending on context
        "recommended_ui": "Numeric input",
        "recommended_ui": "Dropdown",
        "notes": "Specifies the preset number used for link settings. In some contexts, allowed range extends to 1255."
    },
    {
        "name": "E4_LINK_VOLUME",
        "id": 24,
        "hex_id": "18h",
        "tabegory": "LINKS",
        "category": "LINKS",
        "sub_category": "Link Settings",
        "min": -96,
        "max": 10,
        "recommended_ui": "Slider",
        "ui_config": "horizontal",
        "notes": "Sets the volume level for the link in decibels (dB)."
    },
    {
        "name": "E4_LINK_PAN",
        "id": 25,
        "hex_id": "19h",
        "tabegory": "LINKS",
        "category": "LINKS",
        "sub_category": "Pan & Tuning",
        "min": -64,
        "max": 63,
        "recommended_ui": "Slider",
        "ui_config": "horizontal",
        "notes": "Sets the panning for the link."
    },
    {
        "name": "E4_LINK_TRANSPOSE",
        "id": 26,
        "hex_id": "1Ah",
        "tabegory": "LINKS",
        "category": "LINKS",
        "sub_category": "Pan & Tuning",
        "min": -24,
        "max": 24,
        "recommended_ui": "Dropdown",
        "ui_config": "transpose",
        "ui_config2": "semitones",
        "notes": "Transposes the link (in semitones).",
    },
    {
        "name": "E4_LINK_FINE_TUNE",
        "id": 27,
        "hex_id": "1Bh",
        "tabegory": "LINKS",
        "category": "LINKS",
        "sub_category": "Pan & Tuning",
        "min": -64,
        "max": 64,
        "recommended_ui": "Slider",
        "ui_config": "horizontal",
        "ui_config2": "cents",
        "notes": "Adjusts fine tuning for the link (in cents)."
    },
    {
        "name": "E4_LINK_KEY_LOW",
        "id": 28,
        "hex_id": "1Ch",
        "tabegory": "LINKS",
        "category": "LINKS",
        "sub_category": "Key Settings",
        "min": 0,
        "max": 127,
        "recommended_ui": "Dropdown",
        "ui_config": "midinotes",
        "notes": "Sets the lowest MIDI note for the link."
    },
    {
        "name": "E4_LINK_KEY_LOWFADE",
        "id": 29,
        "hex_id": "1Dh",
        "tabegory": "LINKS",
        "category": "LINKS",
        "sub_category": "Key Settings",
        "min": 0,
        "max": 127,
        "recommended_ui": "Slider",
        "config_ui": "horizontal", 
        "notes": "Specifies the fade start for lower keys in the link."
    },
    {
        "name": "E4_LINK_KEY_HIGH",
        "id": 30,
        "hex_id": "1Eh",
        "tabegory": "LINKS",
        "category": "LINKS",
        "sub_category": "Key Settings",
        "min": 0,
        "max": 127,
        "recommended_ui": "Slider",
        "config_ui": "horizontal", 
        "notes": "Sets the highest MIDI note for the link."
    },
    {
        "name": "E4_LINK_KEY_HIGHFADE",
        "id": 31,
        "hex_id": "1Fh",
        "tabegory": "LINKS",
        "category": "LINKS",
        "sub_category": "Key Settings",
        "min": 0,
        "max": 127,
        "recommended_ui": "Slider",
        "config_ui": "horizontal", 
        "notes": "Specifies the fade start for upper keys in the link."
    },
    {
        "name": "E4_LINK_VEL_LOW",
        "id": 32,
        "hex_id": "20h",
        "tabegory": "LINKS",
        "category": "LINKS",
        "sub_category": "Velocity",
        "min": 0,
        "max": 127,
        "recommended_ui": "Slider",
        "config_ui": "horizontal", 
        "notes": "Sets the lower velocity limit for the link."
    },
    {
        "name": "E4_LINK_VEL_LOWFADE",
        "id": 33,
        "hex_id": "21h",
        "tabegory": "LINKS",
        "category": "LINKS",
        "sub_category": "Velocity",
        "min": 0,
        "max": 127,
        "recommended_ui": "Slider",
        "config_ui": "horizontal", 
        "notes": "Specifies the fade-in for lower velocities."
    },
    {
        "name": "E4_LINK_VEL_HIGH",
        "id": 34,
        "hex_id": "22h",
        "tabegory": "LINKS",
        "category": "LINKS",
        "sub_category": "Velocity",
        "min": 0,
        "max": 127,
        "recommended_ui": "Slider",
        "config_ui": "horizontal", 
        "notes": "Sets the upper velocity limit for the link."
    },
    {
        "name": "E4_LINK_VEL_HIGHFADE",
        "id": 35,
        "hex_id": "23h",
        "tabegory": "LINKS",
        "category": "LINKS",
        "sub_category": "Velocity",
        "min": 0,
        "max": 127,
        "recommended_ui": "Slider",
        "config_ui": "horizontal", 
        "notes": "Specifies the fade-out for higher velocities."
    },

    # ====================================================
    # 6. VOICES Parameters
    # ====================================================
    {
        "name": "E4_GEN_GROUP_NUM",
        "id": 37,
        "hex_id": "25h",
        "tabegory": "VOICES",
        "tabegory": "VOICES",
        "category": "VOICES",
        "sub_category": "Voice Settings",
        "min": 1,
        "max": 32,
        "recommended_ui": "Dropdown",
        "notes": "Designates the group number for the voice, useful for layering."
    },
    {
        "name": "E4_GEN_SAMPLE",
        "id": 38,
        "hex_id": "26h",
        "tabegory": "VOICES",
        "category": "VOICES",
        "sub_category": "Sample Assignment",
        "min": 0,
        "max": 999,
        "recommended_ui": "Numeric input",
        "recommended_ui": "Dropdown",
        "notes": ("Specifies the sample number assigned to the voice. Editable range is 0–999; "
                  "if ROM/Flash restricts changes, the maximum may be higher but not user–editable.")
    },
    {
        "name": "E4_GEN_VOLUME",
        "id": 39,
        "hex_id": "27h",
        "tabegory": "VOICES",
        "category": "VOICES",
        "sub_category": "Voice Settings",
        "min": -96,
        "max": 10,
        "recommended_ui": "Slider",
        "config_ui": "volume", 
        "notes": "Sets the volume for the voice in decibels."
    },
    {
        "name": "E4_GEN_PAN",
        "id": 40,
        "hex_id": "28h",
        "tabegory": "VOICES",
        "category": "VOICES",
        "sub_category": "Voice Settings",
        "min": -64,
        "max": 63,
        "recommended_ui": "Slider",
        "config_ui": "horizontal", 
        "notes": "Sets the panning for the voice."
    },
    {
        "name": "E4_GEN_CTUNE",
        "id": 41,
        "hex_id": "29h",
        "tabegory": "VOICES",
        "category": "VOICES",
        "sub_category": "Tuning",
        "min": -72,
        "max": 24,
        "recommended_ui": "Slider",
        "notes": "Sets the coarse tuning for the voice."
    },
    {
        "name": "E4_GEN_FTUNE",
        "id": 42,
        "hex_id": "2Ah",
        "tabegory": "VOICES",
        "category": "VOICES",
        "sub_category": "Tuning",
        "min": -64,
        "max": 64,
        "recommended_ui": "Slider",
        "notes": "Sets the fine tuning for the voice."
    },
    {
        "name": "E4_GEN_XPOSE",
        "id": 43,
        "hex_id": "2Bh",
        "tabegory": "VOICES",
        "category": "VOICES",
        "sub_category": "Tuning",
        "min": -24,
        "max": 24,
        "recommended_ui": "Dropdown",
        "config_ui": "transpose", 
        "notes": "Applies an additional pitch transposition for the voice."
    },
    {
        "name": "E4_GEN_ORIG_KEY",
        "id": 44,
        "hex_id": "2Ch",
        "tabegory": "VOICES",
        "category": "VOICES",
        "sub_category": "Key Settings",
        "min": 0,
        "max": 127,
        "recommended_ui": "Numeric input",
        "notes": "Specifies the original tuning key (MIDI note) for the sample."
    },
    {
        "name": "E4_GEN_KEY_LOW",
        "id": 45,
        "hex_id": "2Dh",
        "tabegory": "VOICES",
        "category": "VOICES",
        "sub_category": "Key Settings",
        "min": 0,
        "max": 127,
        "recommended_ui": "Slider",
        "notes": "Sets the lowest key for the voice."
    },
    {
        "name": "E4_GEN_KEY_LOWFADE",
        "id": 46,
        "hex_id": "2Eh",
        "tabegory": "VOICES",
        "category": "VOICES",
        "sub_category": "Key Settings",
        "min": 0,
        "max": 127,
        "recommended_ui": "Slider",
        "notes": "Defines the fade-in start key for the voice."
    },
    {
        "name": "E4_GEN_KEY_HIGH",
        "id": 47,
        "hex_id": "2Fh",
        "tabegory": "VOICES",
        "category": "VOICES",
        "sub_category": "Key Settings",
        "min": 0,
        "max": 127,
        "recommended_ui": "Slider",
        "notes": "Sets the highest key for the voice."
    },
    {
        "name": "E4_GEN_KEY_HIGHFADE",
        "id": 48,
        "hex_id": "30h",
        "tabegory": "VOICES",
        "category": "VOICES",
        "sub_category": "Key Settings",
        "min": 0,
        "max": 127,
        "recommended_ui": "Slider",
        "notes": "Defines the fade-out start key for the voice."
    },
    {
        "name": "E4_GEN_VEL_LOW",
        "id": 49,
        "hex_id": "31h",
        "tabegory": "VOICES",
        "category": "VOICES",
        "sub_category": "Velocity",
        "min": 0,
        "max": 127,
        "recommended_ui": "Slider",
        "notes": "Sets the lower bound for the voice’s velocity."
    },
    {
        "name": "E4_GEN_VEL_LOWFADE",
        "id": 50,
        "hex_id": "32h",
        "tabegory": "VOICES",
        "category": "VOICES",
        "sub_category": "Velocity",
        "min": 0,
        "max": 127,
        "recommended_ui": "Slider",
        "notes": "Specifies the fade-in region for lower velocity values."
    },
    {
        "name": "E4_GEN_VEL_HIGH",
        "id": 51,
        "hex_id": "33h",
        "tabegory": "VOICES",
        "category": "VOICES",
        "sub_category": "Velocity",
        "min": 0,
        "max": 127,
        "recommended_ui": "Slider",
        "notes": "Sets the upper bound for the voice’s velocity."
    },
    {
        "name": "E4_GEN_VEL_HIGHFADE",
        "id": 52,
        "hex_id": "34h",
        "tabegory": "VOICES",
        "category": "VOICES",
        "sub_category": "Velocity",
        "min": 0,
        "max": 127,
        "recommended_ui": "Slider",
        "notes": "Specifies the fade-out region for higher velocity values."
    },
    {
        "name": "E4_GEN_RT_LOW",
        "id": 53,
        "hex_id": "35h",
        "tabegory": "VOICES",
        "category": "VOICES",
        "sub_category": "Reverb/Delay",
        "min": 0,
        "max": 127,
        "recommended_ui": "Slider",
        "notes": "Sets the reverb (or delay) level for low frequencies."
    },
    {
        "name": "E4_GEN_RT_LOWFADE",
        "id": 54,
        "hex_id": "36h",
        "tabegory": "VOICES",
        "category": "VOICES",
        "sub_category": "Reverb/Delay",
        "min": 0,
        "max": 127,
        "recommended_ui": "Slider",
        "notes": "Specifies the fade-in for low-frequency reverb/delay levels."
    },
    {
        "name": "E4_GEN_RT_HIGH",
        "id": 55,
        "hex_id": "37h",
        "tabegory": "VOICES",
        "category": "VOICES",
        "sub_category": "Reverb/Delay",
        "min": 0,
        "max": 127,
        "recommended_ui": "Slider",
        "notes": "Sets the reverb (or delay) level for high frequencies."
    },
    {
        "name": "E4_GEN_RT_HIGHFADE",
        "id": 56,
        "hex_id": "38h",
        "tabegory": "VOICES",
        "category": "VOICES",
        "sub_category": "Reverb/Delay",
        "min": 0,
        "max": 127,
        "recommended_ui": "Slider",
        "notes": "Specifies the fade-out for high-frequency reverb/delay levels."
    },

    # ====================================================
    # 7. Tuning Parameters
    # ====================================================
    {
        "name": "E4_VOICE_NON_TRANSPOSE",
        "id": 57,
        "hex_id": "39h,00h",
        "tabegory": "VOICES",
        "category": "Tuning",
        "sub_category": "Options",
        "min": 0,
        "max": 1,
        "options": {0: "off", 1: "on"},
        "recommended_ui": "Toggle",
        "notes": "Determines whether the voice is affected by transposition."
    },
    {
        "name": "E4_VOICE_CHORUS_AMOUNT",
        "id": 58,
        "hex_id": "3Ah,00h",
        "tabegory": "VOICES",
        "category": "Tuning",
        "sub_category": "Chorus",
        "min": 0,
        "max": 100,
        "recommended_ui": "Slider",
        "ui_config": "percentage readout",
        "notes": "Sets the amount of the chorus effect."
    },
    {
        "name": "E4_VOICE_CHORUS_WIDTH",
        "id": 59,
        "hex_id": "3Bh,00h",
        "tabegory": "VOICES",
        "category": "Tuning",
        "sub_category": "Chorus",
        "min": -128,
        "max": 0,
        "notes": "Displayed value is calculated as: pct = ((value + 128) * 100) / 128, then formatted (e.g. '%3d%%').",
        "recommended_ui": "Slider",
        "ui_config": "horizontal",
        "ui_config2": "percentage readout",
        "recommended_ui_alt": "Numeric input with live percent update"
    },
    {
        "name": "E4_VOICE_CHORUS_X",
        "id": 60,
        "hex_id": "3Ch,00h",
        "tabegory": "VOICES",
        "category": "Tuning",
        "sub_category": "Chorus",
        "min": -32,
        "max": 32,
        "notes": ("Sets the initial inter-aural time delay (ITD) for the chorus. "
                  "Mapping: 0=0.000ms, 1=0.045ms, …, 32=1.451ms. Positive values delay left channel more; negative, the right."),
        "recommended_ui": "Slider",
        "ui_config": "ITD conversion display",
    },
    {
        "name": "E4_VOICE_DELAY",
        "id": 61,
        "hex_id": "3Dh,00h",
        "tabegory": "VOICES",
        "category": "Tuning",
        "sub_category": "Delay/Glide",
        "min": 0,
        "max": 10000,
        "notes": "Sets the delay time in milliseconds for the voice.",
        "recommended_ui": "Slider",
        "ui_config": "horizontal",
        "ui_config2": "ms readout",
    },
    {
        "name": "E4_VOICE_START_OFFSET",
        "id": 62,
        "hex_id": "3Eh,00h",
        "tabegory": "VOICES",
        "category": "Tuning",
        "sub_category": "Delay/Glide",
        "min": 0,
        "max": 127,
        "notes": "Specifies the starting offset for voice sample playback.",
        "recommended_ui": "Slider",
        "ui_config": "horizontal",
    },
    # {
    #     "name": "E4_VOICE_GLIDE_RATE",
    #     "id": 63,
    #     "hex_id": "3Fh,00h",
    #     "tabegory": "VOICES",
#        "category": "Tuning",
    #     "sub_category": "Portamento",
    #     "min": 0,
    #     "max": 127,
    #     "notes": ("Sets the glide (portamento) rate in sec/oct. The raw value is converted via "
    #               "the envunits1 and envunits2 tables to produce a time value (e.g. 'X.XXX sec/oct')."),
    #     "recommended_ui": "Slider with custom sec/oct conversion display"
    # },
    # {
    #     "name": "E4_VOICE_GLIDE_CURVE",
    #     "id": 64,
    #     "hex_id": "40h,00h",
    #     "tabegory": "VOICES",
    #    "category": "Tuning",
    #     "sub_category": "Portamento",
    #     "min": 0,
    #     "max": 8,
    #     "notes": "Specifies the portamento curve shape (0 = linear, 8 = most exponential).",
    #     "recommended_ui": "Slider or dropdown",
    #     "recommended_ui_alt": "Graphical curve editor"
    # },
    {
        "name": "E4_VOICE_SOLO",
        "id": 65,
        "hex_id": "41h,00h",
        "tabegory": "VOICES",
        "category": "Tuning",
        "sub_category": "Modes",
        "min": 0,
        "max": 8,
        "options": {
            0: "Off",
            1: "Multiple Trigger",
            2: "Melody (last)",
            3: "Melody (low)",
            4: "Melody (high)",
            5: "Synth (last)",
            6: "Synth (low)",
            7: "Synth (high)",
            8: "Fingered Glide"
        },
        "recommended_ui": "Radio buttons",
        "notes": "Selects a solo mode for the voice, such as multiple triggering or fingered glide."
    },
    {
        "name": "E4_VOICE_ASSIGN_GROUP",
        "id": 66,
        "hex_id": "42h,00h",
        "tabegory": "VOICES",
        "category": "Tuning",
        "sub_category": "Grouping",
        "min": 0,
        "max": 23,
        "options": {
            0: "Poly All",
            1: "Poly16 A",
            2: "Poly16 B",
            3: "Poly 8 A",
            4: "Poly 8 B",
            5: "Poly 8 C",
            6: "Poly 8 D",
            7: "Poly 4 A",
            8: "Poly 4 B",
            9: "Poly 4 C",
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
            23: "Mono I"
        },
        "recommended_ui": "Dropdown",
        "notes": "Assigns the voice to a group for layering or splitting purposes."
    },
    {
        "name": "E4_VOICE_LATCHMODE",
        "id": 67,
        "hex_id": "43h,00h",
        "tabegory": "VOICES",
        "category": "Tuning",
        "sub_category": "Modes",
        "min": 0,
        "max": 1,
        "options": {0: "off", 1: "on"},
        "recommended_ui": "Toggle",
        "notes": "Determines whether the voice latches its assigned parameters."
    },

    # ====================================================
    # 8. Amplifier Parameters
    # ====================================================
    {
        "name": "E4_VOICE_VOLENV_DEPTH",
        "id": 68,
        "hex_id": "44h,00h",
        "tabegory": "VOICES",
        "category": "Amplifier",
        "sub_category": "Envelope",
        "min": 0,
        "max": 16,
        "recommended_ui": "Slider",
        "ui_config": "db",
        "db_lo": -96,
        "db_hi": -48,
        "notes": "Sets the amplifier envelope depth. This corresponds to a range from -96dB to -48dB in 3dB steps."
    },
    {
        "name": "E4_VOICE_SUBMIX",
        "id": 69,
        "hex_id": "45h,00h",
        "tabegory": "VOICES",
        "category": "Amplifier",
        "sub_category": "Routing",
        "min": -1,
        "max": 3,
        "options": {
            -1: "Voice",
            0: "Main",
            1: "Sub1",
            2: "Sub2",
            3: "Sub3"
        },
        "recommended_ui": "Dropdown",
        "notes": "Selects the output routing for the voice. (Additional options may be available with expansion cards.)"
    },
    {
        "name": "E4_VOICE_VENV_SEG0_RATE",
        "alt_name": "Attack 1 Rate",
        "id": 70,
        "hex_id": "46h,00h",
        "tabegory": "VOICES",
        "category": "Amplifier",
        "sub_category": "Envelope Segments",
        "min": 0,
        "max": 127,
        "recommended_ui": "Slider",
        "notes": "Sets the attack rate of envelope segment 0 (Atk1 Rate)."
    },
    {
        "name": "E4_VOICE_VENV_SEG0_TGTLVL",
        "alt_name": "Attack 1 Level",
        "id": 71,
        "hex_id": "47h,00h",
        "tabegory": "VOICES",
        "category": "Amplifier",
        "sub_category": "Envelope Segments",
        "min": 0,
        "max": 100,
        "recommended_ui": "Slider",
        "notes": "Specifies the attack level (in percentage) for envelope segment 0 (Atk1 Level)."
    },
    {
        "name": "E4_VOICE_VENV_SEG1_RATE",
        "alt_name": "Decay 1 Rate",
        "id": 72,
        "hex_id": "48h,00h",
        "tabegory": "VOICES",
        "category": "Amplifier",
        "sub_category": "Envelope Segments",
        "min": 0,
        "max": 127,
        "recommended_ui": "Slider",
        "notes": "Sets the decay rate for envelope segment 1 (Dcy1 Rate)."
    },
    {
        "name": "E4_VOICE_VENV_SEG1_TGTLVL",
        "alt_name": "Decay 1 Level",
        "id": 73,
        "hex_id": "49h,00h",
        "tabegory": "VOICES",
        "category": "Amplifier",
        "sub_category": "Envelope Segments",
        "min": 0,
        "max": 100,
        "recommended_ui": "Slider",
        "notes": "Specifies the decay target level (in percentage) for envelope segment 1 (Dcy1 Level)."
    },
    {
        "name": "E4_VOICE_VENV_SEG2_RATE",
        "alt_name": "Release 1 Rate",
        "id": 74,
        "hex_id": "4Ah,00h",
        "tabegory": "VOICES",
        "category": "Amplifier",
        "sub_category": "Envelope Segments",
        "min": 0,
        "max": 127,
        "recommended_ui": "Slider",
        "notes": "Sets the release rate for envelope segment 2 (Rls1 Rate)."
    },
    {
        "name": "E4_VOICE_VENV_SEG2_TGTLVL",
        "alt_name": "Release 1 Level",
        "id": 75,
        "hex_id": "4Bh,00h",
        "tabegory": "VOICES",
        "category": "Amplifier",
        "sub_category": "Envelope Segments",
        "min": 0,
        "max": 100,
        "recommended_ui": "Slider",
        "notes": "Specifies the release target level (in percentage) for envelope segment 2 (Rls1 Level)."
    },
    {
        "name": "E4_VOICE_VENV_SEG3_RATE",
        "alt_name": "Attack 2 Rate",
        "id": 76,
        "hex_id": "4Ch,00h",
        "tabegory": "VOICES",
        "category": "Amplifier",
        "sub_category": "Envelope Segments",
        "min": 0,
        "max": 127,
        "recommended_ui": "Slider",
        "notes": "Sets the attack rate for envelope segment 3 (Atk2 Rate)."
    },
    {
        "name": "E4_VOICE_VENV_SEG3_TGTLVL",
        "alt_name": "Attack 2 Level",
        "id": 77,
        "hex_id": "4Dh,00h",
        "tabegory": "VOICES",
        "category": "Amplifier",
        "sub_category": "Envelope Segments",
        "min": 0,
        "max": 100,
        "recommended_ui": "Slider",
        "notes": "Specifies the attack target level for envelope segment 3 (Atk2 Level)."
    },
    {
        "name": "E4_VOICE_VENV_SEG4_RATE",
        "alt_name": "Decay 2 Rate",
        "id": 78,
        "hex_id": "4Eh,00h",
        "tabegory": "VOICES",
        "category": "Amplifier",
        "sub_category": "Envelope Segments",
        "min": 0,
        "max": 127,
        "recommended_ui": "Slider",
        "notes": "Sets the decay rate for envelope segment 4 (Dcy2 Rate)."
    },
    {
        "name": "E4_VOICE_VENV_SEG4_TGTLVL",
        "alt_name": "Decay 2 Level",
        "id": 79,
        "hex_id": "4Fh,00h",
        "tabegory": "VOICES",
        "category": "Amplifier",
        "sub_category": "Envelope Segments",
        "min": 0,
        "max": 100,
        "recommended_ui": "Slider",
        "notes": "Specifies the decay target level (in percentage) for envelope segment 4 (Dcy2 Level)."
    },
    {
        "name": "E4_VOICE_VENV_SEG5_RATE",
        "alt_name": "Release 2 Rate",
        "id": 80,
        "hex_id": "50h,00h",
        "tabegory": "VOICES",
        "category": "Amplifier",
        "sub_category": "Envelope Segments",
        "min": 0,
        "max": 127,
        "recommended_ui": "Slider",
        "notes": "Sets the release rate for envelope segment 5 (Rls2 Rate)."
    },
    {
        "name": "E4_VOICE_VENV_SEG5_TGTLVL",
        "alt_name": "Release 2 Level",
        "id": 81,
        "hex_id": "51h,00h",
        "tabegory": "VOICES",
        "category": "Amplifier",
        "sub_category": "Envelope Segments",
        "min": 0,
        "max": 100,
        "recommended_ui": "Slider",
        "notes": "Specifies the release target level (in percentage) for envelope segment 5 (Rls2 Level)."
    },

    # ====================================================
    # 9. Filter Parameters
    # ====================================================
    {
        "name": "E4_VOICE_FTYPE",
        "alt_name": "Filter Type",
        "id": 82,
        "hex_id": "52h,00h",
        "tabegory": "VOICES",
        "category": "Filter",
        "sub_category": "Type Selection",
        "min": 0,
        "max": "variable",
        "recommended_ui": "Dropdown",
        "notes": "Selects the filter type. Maximum allowed value depends on the specific design."
    },
    {
        "name": "E4_VOICE_FMORPH",
        "alt_name": "Filter Morph Frequency",
        "id": 83,
        "hex_id": "53h,00h",
        "tabegory": "VOICES",
        "category": "Filter",
        "sub_category": "Parameter Control",
        "min": 0,
        "max": 255,
        "recommended_ui": "Slider",
        "ui_config": "hz",
        "notes": "Controls the filter morph frequency parameter. Raw value may need conversion to Hertz."
    },
    {
        "name": "E4_VOICE_FKEY_XFORM",
        "alt_name": "Q Factor / Key Tracking",
        "id": 84,
        "hex_id": "54h,00h",
        "tabegory": "VOICES",
        "category": "Filter",
        "sub_category": "Parameter Control",
        "min": 0,
        "max": 127,
        "recommended_ui": "Slider",
        "notes": "Adjusts filter key scaling (commonly interpreted as Q factor or key tracking)."
    },
    {
        "name": "E4_VOICE_FILT_GEN_PARM1",
        "id": 85,
        "hex_id": "55h,00h",
        "tabegory": "VOICES",
        "category": "Filter",
        "sub_category": "General Parameters",
        "min": 0,
        "max": 255,
        "recommended_ui": "Slider",
        "notes": "General filter parameter 1."
    },
    {
        "name": "E4_VOICE_FILT_GEN_PARM2",
        "id": 86,
        "hex_id": "56h,00h",
        "tabegory": "VOICES",
        "category": "Filter",
        "sub_category": "General Parameters",
        "min": 0,
        "max": 255,
        "recommended_ui": "Slider",
        "notes": "General filter parameter 2."
    },
    {
        "name": "E4_VOICE_FILT_GEN_PARM3",
        "id": 87,
        "hex_id": "57h,00h",
        "tabegory": "VOICES",
        "category": "Filter",
        "sub_category": "General Parameters",
        "min": 0,
        "max": 255,
        "recommended_ui": "Slider",
        "notes": "General filter parameter 3."
    },
    {
        "name": "E4_VOICE_FILT_GEN_PARM4",
        "id": 88,
        "hex_id": "58h,00h",
        "tabegory": "VOICES",
        "category": "Filter",
        "sub_category": "General Parameters",
        "min": 0,
        "max": 255,
        "recommended_ui": "Slider",
        "notes": "General filter parameter 4."
    },
    {
        "name": "E4_VOICE_FILT_GEN_PARM5",
        "id": 89,
        "hex_id": "59h,00h",
        "tabegory": "VOICES",
        "category": "Filter",
        "sub_category": "General Parameters",
        "min": 0,
        "max": 255,
        "recommended_ui": "Slider",
        "notes": "General filter parameter 5."
    },
    {
        "name": "E4_VOICE_FILT_GEN_PARM6",
        "id": 90,
        "hex_id": "5Ah,00h",
        "tabegory": "VOICES",
        "category": "Filter",
        "sub_category": "General Parameters",
        "min": 0,
        "max": 255,
        "recommended_ui": "Slider",
        "notes": "General filter parameter 6."
    },
    {
        "name": "E4_VOICE_FILT_GEN_PARM7",
        "id": 91,
        "hex_id": "5Bh,00h",
        "tabegory": "VOICES",
        "category": "Filter",
        "sub_category": "General Parameters",
        "min": 0,
        "max": 255,
        "recommended_ui": "Slider",
        "notes": "General filter parameter 7."
    },
    {
        "name": "E4_VOICE_FILT_GEN_PARM8",
        "id": 92,
        "hex_id": "5Ch,00h",
        "tabegory": "VOICES",
        "category": "Filter",
        "sub_category": "General Parameters",
        "min": 0,
        "max": 255,
        "recommended_ui": "Slider",
        "notes": "General filter parameter 8."
    },
    {
        "name": "E4_VOICE_FENV_SEG0_RATE",
        "id": 93,
        "hex_id": "5Dh,00h",
        "tabegory": "VOICES",
        "category": "Filter",
        "sub_category": "Envelope",
        "min": 0,
        "max": 127,
        "recommended_ui": "Slider",
        "notes": "Sets the attack rate for filter envelope segment 0 (Atk1 Rate)."
    },
    {
        "name": "E4_VOICE_FENV_SEG0_TGTLVL",
        "id": 94,
        "hex_id": "5Eh,00h",
        "tabegory": "VOICES",
        "category": "Filter",
        "sub_category": "Envelope",
        "min": 0,
        "max": 100,
        "recommended_ui": "Slider",
        "notes": "Sets the target level (percentage) for filter envelope segment 0 (Atk1 Level)."
    },
    {
        "name": "E4_VOICE_FENV_SEG1_RATE",
        "id": 95,
        "hex_id": "5Fh,00h",
        "tabegory": "VOICES",
        "category": "Filter",
        "sub_category": "Envelope",
        "min": 0,
        "max": 127,
        "recommended_ui": "Slider",
        "notes": "Sets the decay rate for filter envelope segment 1 (Dcy1 Rate)."
    },
    {
        "name": "E4_VOICE_FENV_SEG1_TGTLVL",
        "id": 96,
        "hex_id": "60h,00h",
        "tabegory": "VOICES",
        "category": "Filter",
        "sub_category": "Envelope",
        "min": 0,
        "max": 100,
        "recommended_ui": "Slider",
        "notes": "Specifies the target level (percentage) for filter envelope segment 1 (Dcy1 Level)."
    },
    {
        "name": "E4_VOICE_FENV_SEG2_RATE",
        "id": 97,
        "hex_id": "61h,00h",
        "tabegory": "VOICES",
        "category": "Filter",
        "sub_category": "Envelope",
        "min": 0,
        "max": 127,
        "recommended_ui": "Slider",
        "notes": "Sets the release rate for filter envelope segment 2 (Rls1 Rate)."
    },
    {
        "name": "E4_VOICE_FENV_SEG2_TGTLVL",
        "id": 98,
        "hex_id": "62h,00h",
        "tabegory": "VOICES",
        "category": "Filter",
        "sub_category": "Envelope",
        "min": 0,
        "max": 100,
        "recommended_ui": "Slider",
        "notes": "Specifies the target level (percentage) for filter envelope segment 2 (Rls1 Level)."
    },
    {
        "name": "E4_VOICE_FENV_SEG3_RATE",
        "id": 99,
        "hex_id": "63h,00h",
        "tabegory": "VOICES",
        "category": "Filter",
        "sub_category": "Envelope",
        "min": 0,
        "max": 127,
        "recommended_ui": "Slider",
        "notes": "Sets the attack rate for filter envelope segment 3 (Atk2 Rate)."
    },
    {
        "name": "E4_VOICE_FENV_SEG3_TGTLVL",
        "id": 100,
        "hex_id": "64h,00h",
        "tabegory": "VOICES",
        "category": "Filter",
        "sub_category": "Envelope",
        "min": 0,
        "max": 100,
        "recommended_ui": "Slider",
        "notes": "Specifies the target level (percentage) for filter envelope segment 3 (Atk2 Level)."
    },
    {
        "name": "E4_VOICE_FENV_SEG4_RATE",
        "id": 101,
        "hex_id": "65h,00h",
        "tabegory": "VOICES",
        "category": "Filter",
        "sub_category": "Envelope",
        "min": 0,
        "max": 127,
        "recommended_ui": "Slider",
        "notes": "Sets the decay rate for filter envelope segment 4 (Dcy2 Rate)."
    },
    {
        "name": "E4_VOICE_FENV_SEG4_TGTLVL",
        "id": 102,
        "hex_id": "66h,00h",
        "tabegory": "VOICES",
        "category": "Filter",
        "sub_category": "Envelope",
        "min": 0,
        "max": 100,
        "recommended_ui": "Slider",
        "notes": "Specifies the target level (percentage) for filter envelope segment 4 (Dcy2 Level)."
    },
    {
        "name": "E4_VOICE_FENV_SEG5_RATE",
        "id": 103,
        "hex_id": "67h,00h",
        "tabegory": "VOICES",
        "category": "Filter",
        "sub_category": "Envelope",
        "min": 0,
        "max": 127,
        "recommended_ui": "Slider",
        "notes": "Sets the release rate for filter envelope segment 5 (Rls2 Rate)."
    },
    {
        "name": "E4_VOICE_FENV_SEG5_TGTLVL",
        "id": 104,
        "hex_id": "68h,00h",
        "tabegory": "VOICES",
        "category": "Filter",
        "sub_category": "Envelope",
        "min": 0,
        "max": 100,
        "recommended_ui": "Slider",
        "notes": "Specifies the target level (percentage) for filter envelope segment 5 (Rls2 Level)."
    },

    # ====================================================
    # 10. LFO Parameters
    # ====================================================
    {
        "name": "E4_VOICE_LFO_RATE",
        "id": 105,
        "hex_id": "69h,00h",
        "tabegory": "VOICES",
        "category": "LFO",
        "sub_category": "Modulation",
        "min": 0,
        "max": 127,
        "recommended_ui": "Slider",
        "notes": "Sets the LFO’s modulation rate."
    },
    {
        "name": "E4_VOICE_LFO_SHAPE",
        "id": 106,
        "hex_id": "6Ah,00h",
        "tabegory": "VOICES",
        "category": "LFO",
        "sub_category": "Modulation",
        "min": 0,
        "max": 7,
        "options": {
            0: "triangle",
            1: "sine",
            2: "sawtooth",
            3: "square",
            4: "0,1,0,-1",
            5: "C,E,G,C",
            6: "C,D,F,G",
            7: "8st Pent"
        },
        "recommended_ui": "Radio",
        "notes": "Specifies the shape of the primary LFO waveform."
    },
    {
        "name": "E4_VOICE_LFO_DELAY",
        "id": 107,
        "hex_id": "6Bh,00h",
        "tabegory": "VOICES",
        "category": "LFO",
        "sub_category": "Modulation",
        "min": 0,
        "max": 127,
        "recommended_ui": "Slider",
        "notes": "Sets the delay (in LFO units) before the primary LFO takes effect."
    },
    {
        "name": "E4_VOICE_LFO_VAR",
        "id": 108,
        "hex_id": "6Ch,00h",
        "tabegory": "VOICES",
        "category": "LFO",
        "sub_category": "Modulation",
        "min": 0,
        "max": 100,
        "recommended_ui": "Slider",
        "notes": "Controls the modulation variation depth for the primary LFO."
    },
    {
        "name": "E4_VOICE_LFO_SYNC",
        "id": 109,
        "hex_id": "6Dh,00h",
        "tabegory": "VOICES",
        "category": "LFO",
        "sub_category": "Sync Options",
        "min": 0,
        "max": 1,
        "options": {0: "key sync", 1: "free run"},
        "recommended_ui": "Toggle",
        "notes": "Selects whether the primary LFO is synchronized to key press events."
    },
    {
        "name": "E4_VOICE_LFO2_RATE",
        "id": 110,
        "hex_id": "6Eh,00h",
        "tabegory": "VOICES",
        "category": "LFO",
        "sub_category": "Modulation (Secondary)",
        "min": 0,
        "max": 127,
        "recommended_ui": "Slider",
        "notes": "Sets the rate for the secondary LFO modulation."
    },
    {
        "name": "E4_VOICE_LFO2_SHAPE",
        "id": 111,
        "hex_id": "6Fh,00h",
        "tabegory": "VOICES",
        "category": "LFO",
        "sub_category": "Modulation (Secondary)",
        "min": 0,
        "max": 7,
        "options": {
            0: "triangle",
            1: "sine",
            2: "sawtooth",
            3: "square",
            4: "0,1,0,-1",
            5: "C,E,G,C",
            6: "C,D,F,G",
            7: "8st Pent"
        },
        "recommended_ui": "Dropdown",
        "notes": "Specifies the waveform shape for the secondary LFO."
    },
    {
        "name": "E4_VOICE_LFO2_DELAY",
        "id": 112,
        "hex_id": "70h,00h",
        "tabegory": "VOICES",
        "category": "LFO",
        "sub_category": "Modulation (Secondary)",
        "min": 0,
        "max": 127,
        "recommended_ui": "Slider",
        "notes": "Sets the delay before the secondary LFO engages."
    },
    {
        "name": "E4_VOICE_LFO2_VAR",
        "id": 113,
        "hex_id": "71h,00h",
        "tabegory": "VOICES",
        "category": "LFO",
        "sub_category": "Modulation (Secondary)",
        "min": 0,
        "max": 100,
        "recommended_ui": "Slider",
        "notes": "Controls the variation depth for the secondary LFO."
    },
    {
        "name": "E4_VOICE_LFO2_SYNC",
        "id": 114,
        "hex_id": "72h,00h",
        "tabegory": "VOICES",
        "category": "LFO",
        "sub_category": "Sync Options (Secondary)",
        "min": 0,
        "max": 1,
        "options": {0: "key sync", 1: "free run"},
        "recommended_ui": "Toggle",
        "notes": "Determines whether the secondary LFO is synchronized or free-running."
    },
    {
        "name": "E4_VOICE_LFO2_OP0_PARM",
        "id": 115,
        "hex_id": "73h,00h",
        "tabegory": "VOICES",
        "category": "LFO",
        "sub_category": "Operator Parameters",
        "min": 0,
        "max": 10,
        "recommended_ui": "Slider",
        "notes": "Controls operator parameter 0 for the secondary LFO."
    },
    {
        "name": "E4_VOICE_LFO2_OP1_PARM",
        "id": 116,
        "hex_id": "74h,00h",
        "tabegory": "VOICES",
        "category": "LFO",
        "sub_category": "Operator Parameters",
        "min": 0,
        "max": 10,
        "recommended_ui": "Slider",
        "notes": "Controls operator parameter 1 for the secondary LFO."
    },

    # ====================================================
    # 11. AENV (Auxiliary Envelope) Parameters
    # ====================================================
    {
        "name": "E4_VOICE_AENV_SEG0_RATE",
        "id": 117,
        "hex_id": "75h,00h",
        "tabegory": "VOICES",
        "category": "Auxiliary Envelope",
        "sub_category": "Aux Envelope",
        "min": 0,
        "max": 127,
        "recommended_ui": "Slider",
        "notes": "Sets the rate for the first segment of the auxiliary envelope."
    },
    {
        "name": "E4_VOICE_AENV_SEG0_TGTLVL",
        "id": 118,
        "hex_id": "76h,00h",
        "tabegory": "VOICES",
        "category": "Auxiliary Envelope",
        "sub_category": "Aux Envelope",
        "min": 0,
        "max": 100,
        "recommended_ui": "Slider",
        "notes": "Specifies the target level (percentage) for the first auxiliary envelope segment."
    },
    {
        "name": "E4_VOICE_AENV_SEG1_RATE",
        "id": 119,
        "hex_id": "77h,00h",
        "tabegory": "VOICES",
        "category": "Auxiliary Envelope",
        "sub_category": "Aux Envelope",
        "min": 0,
        "max": 127,
        "recommended_ui": "Slider",
        "notes": "Sets the rate for the second auxiliary envelope segment."
    },
    {
        "name": "E4_VOICE_AENV_SEG1_TGTLVL",
        "id": 120,
        "hex_id": "78h,00h",
        "tabegory": "VOICES",
        "category": "Auxiliary Envelope",
        "sub_category": "Aux Envelope",
        "min": 0,
        "max": 100,
        "recommended_ui": "Slider",
        "notes": "Specifies the target level (percentage) for the second auxiliary envelope segment."
    },
    {
        "name": "E4_VOICE_AENV_SEG2_RATE",
        "id": 121,
        "hex_id": "79h,00h",
        "tabegory": "VOICES",
        "category": "Auxiliary Envelope",
        "sub_category": "Aux Envelope",
        "min": 0,
        "max": 127,
        "recommended_ui": "Slider",
        "notes": "Sets the rate for the third auxiliary envelope segment."
    },
    {
        "name": "E4_VOICE_AENV_SEG2_TGTLVL",
        "id": 122,
        "hex_id": "7Ah,00h",
        "tabegory": "VOICES",
        "category": "Auxiliary Envelope",
        "sub_category": "Aux Envelope",
        "min": 0,
        "max": 100,
        "recommended_ui": "Slider",
        "notes": "Specifies the target level (percentage) for the third auxiliary envelope segment."
    },
    {
        "name": "E4_VOICE_AENV_SEG3_RATE",
        "id": 123,
        "hex_id": "7Bh,00h",
        "tabegory": "VOICES",
        "category": "Auxiliary Envelope",
        "sub_category": "Aux Envelope",
        "min": 0,
        "max": 127,
        "recommended_ui": "Slider",
        "notes": "Sets the rate for the fourth auxiliary envelope segment."
    },
    {
        "name": "E4_VOICE_AENV_SEG3_TGTLVL",
        "id": 124,
        "hex_id": "7Ch,00h",
        "tabegory": "VOICES",
        "category": "Auxiliary Envelope",
        "sub_category": "Aux Envelope",
        "min": 0,
        "max": 100,
        "recommended_ui": "Slider",
        "notes": "Specifies the target level (percentage) for the fourth auxiliary envelope segment."
    },
    {
        "name": "E4_VOICE_AENV_SEG4_RATE",
        "id": 125,
        "hex_id": "7Dh,00h",
        "tabegory": "VOICES",
        "category": "Auxiliary Envelope",
        "sub_category": "Aux Envelope",
        "min": 0,
        "max": 127,
        "recommended_ui": "Slider",
        "notes": "Sets the rate for the fifth auxiliary envelope segment."
    },
    {
        "name": "E4_VOICE_AENV_SEG4_TGTLVL",
        "id": 126,
        "hex_id": "7Eh,00h",
        "tabegory": "VOICES",
        "category": "Auxiliary Envelope",
        "sub_category": "Aux Envelope",
        "min": 0,
        "max": 100,
        "recommended_ui": "Slider",
        "notes": "Specifies the target level (percentage) for the fifth auxiliary envelope segment."
    },
    {
        "name": "E4_VOICE_AENV_SEG5_RATE",
        "id": 127,
        "hex_id": "7Fh,00h",
        "tabegory": "VOICES",
        "category": "Auxiliary Envelope",
        "sub_category": "Aux Envelope",
        "min": 0,
        "max": 127,
        "recommended_ui": "Slider",
        "notes": "Sets the rate for the sixth auxiliary envelope segment."
    },
    {
        "name": "E4_VOICE_AENV_SEG5_TGTLVL",
        "id": 128,
        "hex_id": "00h,01h",
        "tabegory": "VOICES",
        "category": "Auxiliary Envelope",
        "sub_category": "Aux Envelope",
        "min": 0,
        "max": 100,
        "recommended_ui": "Slider",
        "notes": "Specifies the target level (percentage) for the sixth auxiliary envelope segment."
    },

    # ====================================================
    # 12. Cord Parameters
    # ====================================================
    {
        "name": "E4_VOICE_CORD0_SRC",
        "id": 129,
        "hex_id": "01h,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Source/Destination",
        "min": 0,
        "max": 255,
        "recommended_ui": "Dropdown",
        "notes": "Specifies the source of modulation for Cord 0."
    },
    {
        "name": "E4_VOICE_CORD0_DST",
        "id": 130,
        "hex_id": "02h,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Source/Destination",
        "min": 0,
        "max": 255,
        "recommended_ui": "Dropdown",
        "notes": "Specifies the destination for modulation for Cord 0."
    },
    {
        "name": "E4_VOICE_CORD0_AMT",
        "id": 131,
        "hex_id": "03h,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Amount",
        "min": -100,
        "max": 100,
        "recommended_ui": "Slider",
        "notes": "Sets the modulation amount for Cord 0."
    },
    {
        "name": "E4_VOICE_CORD1_SRC",
        "id": 132,
        "hex_id": "04h,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Source/Destination",
        "min": 0,
        "max": 255,
        "recommended_ui": "Dropdown",
        "notes": "Specifies the source for Cord 1 modulation."
    },
    {
        "name": "E4_VOICE_CORD1_DST",
        "id": 133,
        "hex_id": "05h,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Source/Destination",
        "min": 0,
        "max": 255,
        "recommended_ui": "Dropdown",
        "notes": "Specifies the destination for Cord 1 modulation."
    },
    {
        "name": "E4_VOICE_CORD1_AMT",
        "id": 134,
        "hex_id": "06h,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Amount",
        "min": -100,
        "max": 100,
        "recommended_ui": "Slider",
        "notes": "Sets the modulation amount for Cord 1."
    },
    {
        "name": "E4_VOICE_CORD2_SRC",
        "id": 135,
        "hex_id": "07h,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Source/Destination",
        "min": 0,
        "max": 255,
        "recommended_ui": "Dropdown",
        "notes": "Specifies the source for Cord 2 modulation."
    },
    {
        "name": "E4_VOICE_CORD2_DST",
        "id": 136,
        "hex_id": "08h,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Source/Destination",
        "min": 0,
        "max": 255,
        "recommended_ui": "Dropdown",
        "notes": "Specifies the destination for Cord 2 modulation."
    },
    {
        "name": "E4_VOICE_CORD2_AMT",
        "id": 137,
        "hex_id": "09h,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Amount",
        "min": -100,
        "max": 100,
        "recommended_ui": "Slider",
        "notes": "Sets the modulation amount for Cord 2."
    },
    {
        "name": "E4_VOICE_CORD3_SRC",
        "id": 138,
        "hex_id": "0Ah,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Source/Destination",
        "min": 0,
        "max": 255,
        "recommended_ui": "Dropdown",
        "notes": "Specifies the source for Cord 3 modulation."
    },
    {
        "name": "E4_VOICE_CORD3_DST",
        "id": 139,
        "hex_id": "0Bh,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Source/Destination",
        "min": 0,
        "max": 255,
        "recommended_ui": "Dropdown",
        "notes": "Specifies the destination for Cord 3 modulation."
    },
    {
        "name": "E4_VOICE_CORD3_AMT",
        "id": 140,
        "hex_id": "0Ch,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Amount",
        "min": -100,
        "max": 100,
        "recommended_ui": "Slider",
        "notes": "Sets the modulation amount for Cord 3."
    },
    {
        "name": "E4_VOICE_CORD4_SRC",
        "id": 141,
        "hex_id": "0Dh,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Source/Destination",
        "min": 0,
        "max": 255,
        "recommended_ui": "Dropdown",
        "notes": "Specifies the source for Cord 4 modulation."
    },
    {
        "name": "E4_VOICE_CORD4_DST",
        "id": 142,
        "hex_id": "0Eh,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Source/Destination",
        "min": 0,
        "max": 255,
        "recommended_ui": "Dropdown",
        "notes": "Specifies the destination for Cord 4 modulation."
    },
    {
        "name": "E4_VOICE_CORD4_AMT",
        "id": 143,
        "hex_id": "0Fh,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Amount",
        "min": -100,
        "max": 100,
        "recommended_ui": "Slider",
        "notes": "Sets the modulation amount for Cord 4."
    },
    {
        "name": "E4_VOICE_CORD5_SRC",
        "id": 144,
        "hex_id": "10h,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Source/Destination",
        "min": 0,
        "max": 255,
        "recommended_ui": "Dropdown",
        "notes": "Specifies the source for Cord 5 modulation."
    },
    {
        "name": "E4_VOICE_CORD5_DST",
        "id": 145,
        "hex_id": "11h,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Source/Destination",
        "min": 0,
        "max": 255,
        "recommended_ui": "Dropdown",
        "notes": "Specifies the destination for Cord 5 modulation."
    },
    {
        "name": "E4_VOICE_CORD5_AMT",
        "id": 146,
        "hex_id": "12h,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Amount",
        "min": -100,
        "max": 100,
        "recommended_ui": "Slider",
        "notes": "Sets the modulation amount for Cord 5."
    },
    {
        "name": "E4_VOICE_CORD6_SRC",
        "id": 147,
        "hex_id": "13h,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Source/Destination",
        "min": 0,
        "max": 255,
        "recommended_ui": "Dropdown",
        "notes": "Specifies the source for Cord 6 modulation."
    },
    {
        "name": "E4_VOICE_CORD6_DST",
        "id": 148,
        "hex_id": "14h,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Source/Destination",
        "min": 0,
        "max": 255,
        "recommended_ui": "Dropdown",
        "notes": "Specifies the destination for Cord 6 modulation."
    },
    {
        "name": "E4_VOICE_CORD6_AMT",
        "id": 149,
        "hex_id": "15h,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Amount",
        "min": -100,
        "max": 100,
        "recommended_ui": "Slider",
        "notes": "Sets the modulation amount for Cord 6."
    },
    {
        "name": "E4_VOICE_CORD7_SRC",
        "id": 150,
        "hex_id": "16h,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Source/Destination",
        "min": 0,
        "max": 255,
        "recommended_ui": "Dropdown",
        "notes": "Specifies the source for Cord 7 modulation."
    },
    {
        "name": "E4_VOICE_CORD7_DST",
        "id": 151,
        "hex_id": "17h,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Source/Destination",
        "min": 0,
        "max": 255,
        "recommended_ui": "Dropdown",
        "notes": "Specifies the destination for Cord 7 modulation."
    },
    {
        "name": "E4_VOICE_CORD7_AMT",
        "id": 152,
        "hex_id": "18h,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Amount",
        "min": -100,
        "max": 100,
        "recommended_ui": "Slider",
        "notes": "Sets the modulation amount for Cord 7."
    },
    {
        "name": "E4_VOICE_CORD8_SRC",
        "id": 153,
        "hex_id": "19h,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Source/Destination",
        "min": 0,
        "max": 255,
        "recommended_ui": "Dropdown",
        "notes": "Specifies the source for Cord 8 modulation."
    },
    {
        "name": "E4_VOICE_CORD8_DST",
        "id": 154,
        "hex_id": "1Ah,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Source/Destination",
        "min": 0,
        "max": 255,
        "recommended_ui": "Dropdown",
        "notes": "Specifies the destination for Cord 8 modulation."
    },
    {
        "name": "E4_VOICE_CORD8_AMT",
        "id": 155,
        "hex_id": "1Bh,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Amount",
        "min": -100,
        "max": 100,
        "recommended_ui": "Slider",
        "notes": "Sets the modulation amount for Cord 8."
    },
    {
        "name": "E4_VOICE_CORD9_SRC",
        "id": 156,
        "hex_id": "1Ch,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Source/Destination",
        "min": 0,
        "max": 255,
        "recommended_ui": "Dropdown",
        "notes": "Specifies the source for Cord 9 modulation."
    },
    {
        "name": "E4_VOICE_CORD9_DST",
        "id": 157,
        "hex_id": "1Dh,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Source/Destination",
        "min": 0,
        "max": 255,
        "recommended_ui": "Dropdown",
        "notes": "Specifies the destination for Cord 9 modulation."
    },
    {
        "name": "E4_VOICE_CORD9_AMT",
        "id": 158,
        "hex_id": "1Eh,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Amount",
        "min": -100,
        "max": 100,
        "recommended_ui": "Slider",
        "notes": "Sets the modulation amount for Cord 9."
    },
    {
        "name": "E4_VOICE_CORD10_SRC",
        "id": 159,
        "hex_id": "1Fh,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Source/Destination",
        "min": 0,
        "max": 255,
        "recommended_ui": "Dropdown",
        "notes": "Specifies the source for Cord 10 modulation."
    },
    {
        "name": "E4_VOICE_CORD10_DST",
        "id": 160,
        "hex_id": "20h,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Source/Destination",
        "min": 0,
        "max": 255,
        "recommended_ui": "Dropdown",
        "notes": "Specifies the destination for Cord 10 modulation."
    },
    {
        "name": "E4_VOICE_CORD10_AMT",
        "id": 161,
        "hex_id": "21h,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Amount",
        "min": -100,
        "max": 100,
        "recommended_ui": "Slider",
        "notes": "Sets the modulation amount for Cord 10."
    },
    {
        "name": "E4_VOICE_CORD11_SRC",
        "id": 162,
        "hex_id": "22h,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Source/Destination",
        "min": 0,
        "max": 255,
        "recommended_ui": "Dropdown",
        "notes": "Specifies the source for Cord 11 modulation."
    },
    {
        "name": "E4_VOICE_CORD11_DST",
        "id": 163,
        "hex_id": "23h,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Source/Destination",
        "min": 0,
        "max": 255,
        "recommended_ui": "Dropdown",
        "notes": "Specifies the destination for Cord 11 modulation."
    },
    {
        "name": "E4_VOICE_CORD11_AMT",
        "id": 164,
        "hex_id": "24h,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Amount",
        "min": -100,
        "max": 100,
        "recommended_ui": "Slider",
        "notes": "Sets the modulation amount for Cord 11."
    },
    {
        "name": "E4_VOICE_CORD12_SRC",
        "id": 165,
        "hex_id": "25h,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Source/Destination",
        "min": 0,
        "max": 255,
        "recommended_ui": "Dropdown",
        "notes": "Specifies the source for Cord 12 modulation."
    },
    {
        "name": "E4_VOICE_CORD12_DST",
        "id": 166,
        "hex_id": "26h,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Source/Destination",
        "min": 0,
        "max": 255,
        "recommended_ui": "Dropdown",
        "notes": "Specifies the destination for Cord 12 modulation."
    },
    {
        "name": "E4_VOICE_CORD12_AMT",
        "id": 167,
        "hex_id": "27h,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Amount",
        "min": -100,
        "max": 100,
        "recommended_ui": "Slider",
        "notes": "Sets the modulation amount for Cord 12."
    },
    {
        "name": "E4_VOICE_CORD13_SRC",
        "id": 168,
        "hex_id": "28h,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Source/Destination",
        "min": 0,
        "max": 255,
        "recommended_ui": "Dropdown",
        "notes": "Specifies the source for Cord 13 modulation."
    },
    {
        "name": "E4_VOICE_CORD13_DST",
        "id": 169,
        "hex_id": "29h,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Source/Destination",
        "min": 0,
        "max": 255,
        "recommended_ui": "Dropdown",
        "notes": "Specifies the destination for Cord 13 modulation."
    },
    {
        "name": "E4_VOICE_CORD13_AMT",
        "id": 170,
        "hex_id": "2Ah,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Amount",
        "min": -100,
        "max": 100,
        "recommended_ui": "Slider",
        "notes": "Sets the modulation amount for Cord 13."
    },
    {
        "name": "E4_VOICE_CORD14_SRC",
        "id": 171,
        "hex_id": "2Bh,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Source/Destination",
        "min": 0,
        "max": 255,
        "recommended_ui": "Dropdown",
        "notes": "Specifies the source for Cord 14 modulation."
    },
    {
        "name": "E4_VOICE_CORD14_DST",
        "id": 172,
        "hex_id": "2Ch,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Source/Destination",
        "min": 0,
        "max": 255,
        "recommended_ui": "Dropdown",
        "notes": "Specifies the destination for Cord 14 modulation."
    },
    {
        "name": "E4_VOICE_CORD14_AMT",
        "id": 173,
        "hex_id": "2Dh,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Amount",
        "min": -100,
        "max": 100,
        "recommended_ui": "Slider",
        "notes": "Sets the modulation amount for Cord 14."
    },
    {
        "name": "E4_VOICE_CORD15_SRC",
        "id": 174,
        "hex_id": "2Eh,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Source/Destination",
        "min": 0,
        "max": 255,
        "recommended_ui": "Dropdown",
        "notes": "Specifies the source for Cord 15 modulation."
    },
    {
        "name": "E4_VOICE_CORD15_DST",
        "id": 175,
        "hex_id": "2Fh,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Source/Destination",
        "min": 0,
        "max": 255,
        "recommended_ui": "Dropdown",
        "notes": "Specifies the destination for Cord 15 modulation."
    },
    {
        "name": "E4_VOICE_CORD15_AMT",
        "id": 176,
        "hex_id": "30h,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Amount",
        "min": -100,
        "max": 100,
        "recommended_ui": "Slider",
        "notes": "Sets the modulation amount for Cord 15."
    },
    {
        "name": "E4_VOICE_CORD16_SRC",
        "id": 177,
        "hex_id": "31h,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Source/Destination",
        "min": 0,
        "max": 255,
        "recommended_ui": "Dropdown",
        "notes": "Specifies the source for Cord 16 modulation."
    },
    {
        "name": "E4_VOICE_CORD16_DST",
        "id": 178,
        "hex_id": "32h,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Source/Destination",
        "min": 0,
        "max": 255,
        "recommended_ui": "Dropdown",
        "notes": "Specifies the destination for Cord 16 modulation."
    },
    {
        "name": "E4_VOICE_CORD16_AMT",
        "id": 179,
        "hex_id": "33h,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Amount",
        "min": -100,
        "max": 100,
        "recommended_ui": "Slider",
        "notes": "Sets the modulation amount for Cord 16."
    },
    {
        "name": "E4_VOICE_CORD17_SRC",
        "id": 180,
        "hex_id": "34h,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Source/Destination",
        "min": 0,
        "max": 255,
        "recommended_ui": "Dropdown",
        "notes": "Specifies the source for Cord 17 modulation."
    },
    {
        "name": "E4_VOICE_CORD17_DST",
        "id": 181,
        "hex_id": "35h,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Source/Destination",
        "min": 0,
        "max": 255,
        "recommended_ui": "Dropdown",
        "notes": "Specifies the destination for Cord 17 modulation."
    },
    {
        "name": "E4_VOICE_CORD17_AMT",
        "id": 182,
        "hex_id": "36h,01h",
        "tabegory": "Cords",
        "category": "Cords",
        "sub_category": "Amount",
        "min": -100,
        "max": 100,
        "recommended_ui": "Slider",
        "notes": "Sets the modulation amount for Cord 17."
    },

    # ====================================================
    # 13. Master Setup Tuning
    # ====================================================
    {
        "name": "MASTER_TUNING_OFFSET",
        "id": 183,
        "hex_id": "37h,01h",
        "tabegory": "Master Setup",
        "category": "Master Setup Tuning",
        "sub_category": "Tuning",
        "min": -64,
        "max": 64,
        "display_options": [0.0, 1.2, 3.5, 4.7, 6.0, 7.2, 9.5, 10.7, 12.0, 14.2, 15.5, 17.7,
                            18.0, 20.2, 21.5, 23.7, 25.0, 26.2, 28.5, 29.7, 31.0, 32.2, 34.5,
                            35.7, 37.0, 39.2, 40.5, 42.7, 43.0, 45.2, 46.5, 48.7, 50.0, 51.2,
                            53.5, 54.7, 56.0, 57.2, 59.5, 60.7, 62.0, 64.2, 65.5, 67.7, 68.0,
                            70.2, 71.5, 73.7, 75.0, 76.2, 78.5, 79.7, 81.0, 82.2, 84.5, 85.7,
                            87.0, 89.2, 90.5, 92.7, 93.0, 95.2, 96.5, 98.7, 100.0],
        "recommended_ui": "Slider with a custom display converter",
        "notes": "Specifies the master tuning offset; displayed using a custom converter (e.g. to semitones or Hz offset)."
    },
    {
        "name": "MASTER_TRANSPOSE",
        "id": 184,
        "hex_id": "38h,01h",
        "tabegory": "Master Setup",
        "category": "Master Setup Tuning",
        "sub_category": "Tuning",
        "min": -12,
        "max": 12,
        "display_options": {
            -12: "C",
            -11: "C#",
            -10: "D",
            -9:  "D#",
            -8:  "E",
            -7:  "F",
            -6:  "F#",
            -5:  "G",
            -4:  "G#",
            -3:  "A",
            -2:  "A#",
            -1:  "B",
             0:  "off (C)",
             1:  "C#",
             2:  "D",
             3:  "D#",
             4:  "E",
             5:  "F",
             6:  "F#",
             7:  "G",
             8:  "G#",
             9:  "A",
            10:  "A#",
            11:  "B",
            12:  "C"
        },
        "recommended_ui": "Dropdown or radio buttons",
        "notes": "Sets the master transposition for the output (alternatively displays note names)."
    },

    # ====================================================
    # 14. Master Setup Output
    # ====================================================
    {
        "name": "MASTER_HEADROOM",
        "id": 185,
        "hex_id": "39h,01h",
        "tabegory": "Master Setup",
        "category": "Master Setup Output",
        "sub_category": "Output",
        "min": 0,
        "max": 15,
        "recommended_ui": "Slider",
        "notes": "Adjusts the headroom reserve in decibels (dB) for the master output."
    },
    {
        "name": "MASTER_HCHIP_BOOST",
        "id": 186,
        "hex_id": "3Ah,01h",
        "tabegory": "Master Setup",
        "category": "Master Setup Output",
        "sub_category": "Output",
        "min": 0,
        "max": 1,
        "display_options": {0: "+0dB", 1: "+12dB"},
        "recommended_ui": "Toggle (radio buttons)",
        "notes": "Engages an extra boost (+12dB) on the output chip when enabled."
    },
    {
        "name": "MASTER_OUTPUT_FORMAT",
        "id": 187,
        "hex_id": "3Bh,01h",
        "tabegory": "Master Setup",
        "category": "Master Setup Output",
        "sub_category": "Output",
        "min": 0,
        "max": 2,
        "display_options": {0: "Analog", 1: "AES pro", 2: "S/PDIF"},
        "recommended_ui": "Dropdown or radio buttons",
        "notes": "Selects the output format for the master signal."
    },
    {
        "name": "MASTER_OUTPUT_CLOCK",
        "id": 188,
        "hex_id": "3Ch,01h",
        "tabegory": "Master Setup",
        "category": "Master Setup Output",
        "sub_category": "Output",
        "min": 0,
        "max": 1,
        "display_options": {0: "44.1kHz", 1: "48kHz"},
        "recommended_ui": "Toggle",
        "notes": "Sets the master output clock frequency."
    },
    {
        "name": "MASTER_AES_BOOST",
        "id": 189,
        "hex_id": "3Dh,01h",
        "tabegory": "Master Setup",
        "category": "Master Setup Output",
        "sub_category": "Output",
        "min": 0,
        "max": 1,
        "display_options": {0: "off", 1: "on"},
        "recommended_ui": "Toggle",
        "notes": "Enables AES boost on the digital output when active."
    },

    # ====================================================
    # 15. Master Setup Misc
    # ====================================================
    {
        "name": "MASTER_SCSI_ID",
        "id": 190,
        "hex_id": "3Eh,01h",
        "tabegory": "Master Setup",
        "category": "Master Setup Misc",
        "sub_category": "Miscellaneous",
        "min": 0,
        "max": 7,
        "recommended_ui": "Dropdown",
        "notes": "Sets the SCSI ID for the device."
    },
    {
        "name": "MASTER_SCSI_TERM",
        "id": 191,
        "hex_id": "3Fh,01h",
        "tabegory": "Master Setup",
        "category": "Master Setup Misc",
        "sub_category": "Miscellaneous",
        "min": 0,
        "max": 1,
        "display_options": {0: "on", 1: "off"},
        "recommended_ui": "Toggle",
        "notes": "Turns SCSI termination on or off."
    },
    {
        "name": "MASTER_USING_MAC",
        "id": 192,
        "hex_id": "40h,01h",
        "tabegory": "Master Setup",
        "category": "Master Setup Misc",
        "sub_category": "Miscellaneous",
        "min": -1,
        "max": 7,
        "display_options": {
            -1: "none",
             0: "ID 0",
             1: "ID 1",
             2: "ID 2",
             3: "ID 3",
             4: "ID 4",
             5: "ID 5",
             6: "ID 6",
             7: "ID 7 (Mac)"
        },
        "recommended_ui": "Dropdown",
        "notes": "Indicates if the device is configured for use with a Macintosh; -1 means not used."
    },

    # ====================================================
    # 16. Master Setup Import
    # ====================================================
    {
        "name": "MASTER_COMBINE_LR",
        "id": 193,
        "hex_id": "41h,01h",
        "tabegory": "Master Setup",
        "category": "Master Setup Import",
        "sub_category": "Import/Links",
        "min": 0,
        "max": 1,
        "display_options": {0: "on", 1: "off"},
        "recommended_ui": "Toggle",
        "notes": "Combines left and right channels into a single output."
    },
    {
        "name": "MASTER_AKAI_LOOP_ADJ",
        "id": 194,
        "hex_id": "42h,01h",
        "tabegory": "Master Setup",
        "category": "Master Setup Import",
        "sub_category": "Import/Links",
        "min": 0,
        "max": 1,
        "display_options": {0: "off", 1: "on"},
        "recommended_ui": "Toggle",
        "notes": "Adjusts loop settings when importing from an Akai sampler."
    },
    {
        "name": "MASTER_AKAI_SAMPLER_ID",
        "id": 195,
        "hex_id": "43h,01h",
        "tabegory": "Master Setup",
        "category": "Master Setup Import",
        "sub_category": "Import/Links",
        "min": -1,
        "max": 7,
        "display_options": {
            -1: "none",
             0: "0",
             1: "1",
             2: "2",
             3: "3",
             4: "4",
             5: "5",
             6: "6",
             7: "7"
        },
        "recommended_ui": "Dropdown",
        "notes": "Specifies the Akai sampler ID used during preset import."
    },
    # IDs 196, 197 not used

    # ====================================================
    # 17. Master MIDI Mode
    # ====================================================
    {
        "name": "MIDIGLO_BASIC_CHANNEL",
        "id": 198,
        "hex_id": "46h,01h",
        "tabegory": "Master MIDI",
        "category": "MIDI Mode",
        "sub_category": "Channel Settings",
        "min": 0,
        "max": 15,
        "notes": "Specifies the basic MIDI channel (0-15 corresponding to channels 1-16).",
        "recommended_ui": "Numeric input or slider"
    },
    {
        "name": "MIDIGLO_MIDI_MODE",
        "id": 199,
        "hex_id": "47h,01h",
        "tabegory": "Master MIDI",
        "category": "MIDI Mode",
        "sub_category": "Mode Selection",
        "min": 0,
        "max": 2,
        "display_options": {0: "omni", 1: "poly", 2: "multi"},
        "recommended_ui": "Dropdown or radio buttons",
        "notes": "Sets the MIDI operating mode (omni, poly, or multi)."
    },

    # ====================================================
    # 18. Master MIDI Cntrls1
    # ====================================================
    {
        "name": "MIDIGLO_PITCH_CONTROL",
        "id": 201,
        "hex_id": "49h,01h",
        "tabegory": "Master MIDI",
        "category": "MIDI Controls 1",
        "sub_category": "Control Mapping",
        "min": -1,
        "max": 33,
        "notes": "Maps pitch control; -1 = off, 0-31 = direct mapping, 32 = pitch wheel, 33 = channel pressure.",
        "recommended_ui": "Slider"
    },
    {
        "name": "MIDIGLO_MOD_CONTROL",
        "id": 202,
        "hex_id": "4Ah,01h",
        "tabegory": "Master MIDI",
        "category": "MIDI Controls 1",
        "sub_category": "Control Mapping",
        "min": -1,
        "max": 33,
        "notes": "Maps modulation control; similar display settings as pitch control.",
        "recommended_ui": "Slider"
    },
    {
        "name": "MIDIGLO_PRESSURE_CONTROL",
        "id": 203,
        "hex_id": "4Bh,01h",
        "tabegory": "Master MIDI",
        "category": "MIDI Controls 1",
        "sub_category": "Control Mapping",
        "min": -1,
        "max": 33,
        "notes": "Maps aftertouch/pressure control; -1 means disabled.",
        "recommended_ui": "Slider"
    },
    {
        "name": "MIDIGLO_PEDAL_CONTROL",
        "id": 204,
        "hex_id": "4Ch,01h",
        "tabegory": "Master MIDI",
        "category": "MIDI Controls 1",
        "sub_category": "Control Mapping",
        "min": -1,
        "max": 33,
        "notes": "Maps pedal control; follows the same display as other controllers.",
        "recommended_ui": "Slider"
    },
    {
        "name": "MIDIGLO_SWITCH_1_CONTROL",
        "id": 205,
        "hex_id": "4Dh,01h",
        "tabegory": "Master MIDI",
        "category": "MIDI Controls 1",
        "sub_category": "Control Mapping",
        "min": -1,
        "max": 33,
        "notes": "Maps switch 1 control; same display conventions apply.",
        "recommended_ui": "Slider"
    },
    {
        "name": "MIDIGLO_SWITCH_2_CONTROL",
        "id": 206,
        "hex_id": "4Eh,01h",
        "tabegory": "Master MIDI",
        "category": "MIDI Controls 1",
        "sub_category": "Control Mapping",
        "min": -1,
        "max": 33,
        "notes": "Maps switch 2 control; same display conventions as above.",
        "recommended_ui": "Slider"
    },
    {
        "name": "MIDIGLO_THUMB_CONTROL",
        "id": 207,
        "hex_id": "4Fh,01h",
        "tabegory": "Master MIDI",
        "category": "MIDI Controls 1",
        "sub_category": "Control Mapping",
        "min": -1,
        "max": 33,
        "notes": "Maps thumb control; same numeric display as other controls.",
        "recommended_ui": "Slider"
    },

    # ====================================================
    # 19. Master MIDI Cntrls2
    # ====================================================
    {
        "name": "MIDIGLO_MIDI_A_CONTROL",
        "id": 208,
        "hex_id": "50h,01h",
        "tabegory": "Master MIDI",
        "category": "MIDI Controls 2",
        "sub_category": "Control Mapping",
        "min": -1,
        "max": 33,
        "notes": "Maps MIDI A control; uses the same mapping as other controls.",
        "recommended_ui": "Slider"
    },
    {
        "name": "MIDIGLO_MIDI_B_CONTROL",
        "id": 209,
        "hex_id": "51h,01h",
        "tabegory": "Master MIDI",
        "category": "MIDI Controls 2",
        "sub_category": "Control Mapping",
        "min": -1,
        "max": 33,
        "notes": "Maps MIDI B control; same value conventions apply.",
        "recommended_ui": "Slider"
    },
    {
        "name": "MIDIGLO_MIDI_C_CONTROL",
        "id": 210,
        "hex_id": "52h,01h",
        "tabegory": "Master MIDI",
        "category": "MIDI Controls 2",
        "sub_category": "Control Mapping",
        "min": -1,
        "max": 33,
        "notes": "Maps MIDI C control; same display as other controls.",
        "recommended_ui": "Slider"
    },
    {
        "name": "MIDIGLO_MIDI_D_CONTROL",
        "id": 211,
        "hex_id": "53h,01h",
        "tabegory": "Master MIDI",
        "category": "MIDI Controls 2",
        "sub_category": "Control Mapping",
        "min": -1,
        "max": 33,
        "notes": "Maps MIDI D control; follows same conventions.",
        "recommended_ui": "Slider"
    },
    {
        "name": "MIDIGLO_MIDI_E_CONTROL",
        "id": 212,
        "hex_id": "54h,01h",
        "tabegory": "Master MIDI",
        "category": "MIDI Controls 2",
        "sub_category": "Control Mapping",
        "min": -1,
        "max": 33,
        "notes": "Maps MIDI E control; same display parameters apply.",
        "recommended_ui": "Slider"
    },
    {
        "name": "MIDIGLO_MIDI_F_CONTROL",
        "id": 213,
        "hex_id": "55h,01h",
        "tabegory": "Master MIDI",
        "category": "MIDI Controls 2",
        "sub_category": "Control Mapping",
        "min": -1,
        "max": 33,
        "notes": "Maps MIDI F control; same numeric mapping as others.",
        "recommended_ui": "Slider"
    },
    {
        "name": "MIDIGLO_MIDI_G_CONTROL",
        "id": 214,
        "hex_id": "56h,01h",
        "tabegory": "Master MIDI",
        "category": "MIDI Controls 2",
        "sub_category": "Control Mapping",
        "min": -1,
        "max": 33,
        "notes": "Maps MIDI G control; same display as for other controls.",
        "recommended_ui": "Slider"
    },
    {
        "name": "MIDIGLO_MIDI_H_CONTROL",
        "id": 215,
        "hex_id": "57h,01h",
        "tabegory": "Master MIDI",
        "category": "MIDI Controls 2",
        "sub_category": "Control Mapping",
        "min": -1,
        "max": 33,
        "notes": "Maps MIDI H control; same value and display rules apply.",
        "recommended_ui": "Slider"
    },

    # ====================================================
    # 20. Master MIDI Prefs1
    # ====================================================
    {
        "name": "MIDIGLO_VEL_CURVE",
        "id": 216,
        "hex_id": "58h,01h",
        "tabegory": "Master MIDI",
        "category": "MIDI Preferences 1",
        "sub_category": "Preferences",
        "min": 0,
        "max": 13,
        "display_options": {
            0: "linear",
            1: "1",
            2: "2",
            3: "3",
            4: "4",
            5: "5",
            6: "6",
            7: "7",
            8: "8",
            9: "9",
            10: "10",
            11: "11",
            12: "12",
            13: "13"
        },
        "recommended_ui": "Slider",
        "notes": "Sets the velocity curve; defines how incoming velocity values are mapped."
    },
    {
        "name": "MIDIGLO_VOLUME_SENSITIVITY",
        "id": 217,
        "hex_id": "59h,01h",
        "tabegory": "Master MIDI",
        "category": "MIDI Preferences 1",
        "sub_category": "Preferences",
        "min": 0,
        "max": 31,
        "recommended_ui": "Slider",
        "notes": "Specifies the sensitivity of the volume control."
    },
    {
        "name": "MIDIGLO_CTRL7_CURVE",
        "id": 218,
        "hex_id": "5Ah,01h",
        "tabegory": "Master MIDI",
        "category": "MIDI Preferences 1",
        "sub_category": "Preferences",
        "min": 0,
        "max": 2,
        "display_options": {0: "linear", 1: "squared", 2: "logarithmic"},
        "recommended_ui": "Dropdown or radio buttons",
        "notes": "Determines the response curve for MIDI control 7."
    },
    {
        "name": "MIDIGLO_PEDAL_OVERRIDE",
        "id": 219,
        "hex_id": "5Bh,01h",
        "tabegory": "Master MIDI",
        "category": "MIDI Preferences 1",
        "sub_category": "Preferences",
        "min": 0,
        "max": 1,
        "display_options": {0: "off", 1: "on"},
        "recommended_ui": "Toggle",
        "notes": "If enabled, overrides the pedal’s behavior with preset values."
    },

    # ====================================================
    # 21. Master MIDI Prefs2
    # ====================================================
    {
        "name": "MIDIGLO_RCV_PROGRAM_CHANGE",
        "id": 220,
        "hex_id": "5Ch,01h",
        "tabegory": "Master MIDI",
        "category": "MIDI Preferences 2",
        "sub_category": "Preferences",
        "min": 0,
        "max": 1,
        "display_options": {0: "off", 1: "on"},
        "recommended_ui": "Toggle",
        "notes": "Determines if the device will receive program change messages."
    },
    {
        "name": "MIDIGLO_SEND_PROGRAM_CHANGE",
        "id": 221,
        "hex_id": "5Dh,01h",
        "tabegory": "Master MIDI",
        "category": "MIDI Preferences 2",
        "sub_category": "Preferences",
        "min": 0,
        "max": 1,
        "display_options": {0: "off", 1: "on"},
        "recommended_ui": "Toggle",
        "notes": "Determines if the device will send program change messages."
    },
    {
        "name": "MIDIGLO_MAGIC_PRESET",
        "id": 222,
        "hex_id": "5Eh,01h",
        "tabegory": "Master MIDI",
        "category": "MIDI Preferences 2",
        "sub_category": "Preferences",
        "min": 0,
        "max": 128,
        "display_options": {0: "off", **{i: f"Preset {i:03d}" for i in range(1,129)}},
        "recommended_ui": "Dropdown",
        "notes": "Selects a 'magic' preset to quickly recall a set of parameters."
    },
    {
        "name": "PRESET_SELECT",
        "id": 223,
        "hex_id": "5Fh,01h",
        "tabegory": "Master MIDI",
        "category": "MIDI Preferences 2",
        "sub_category": "Preferences",
        "min": 0,
        "max": 999,
        "recommended_ui": "Numeric input",
        "notes": "Specifies the preset number used for MIDI operations."
    },
    {
        "name": "LINK_SELECT",
        "id": 224,
        "hex_id": "60h,01h",
        "tabegory": "Master MIDI",
        "category": "MIDI Preferences 2",
        "sub_category": "Preferences",
        "min": 0,
        "max": "255 - (Num of Voices)",
        "recommended_ui": "Numeric input",
        "notes": "Dynamically sets the link selection based on the number of voices."
    },
    {
        "name": "VOICE_SELECT",
        "id": 225,
        "hex_id": "61h,01h",
        "tabegory": "Master MIDI",
        "category": "MIDI Preferences 2",
        "sub_category": "Preferences",
        "min": 0,
        "max": "255 - (Num of Links)",
        "recommended_ui": "Numeric input",
        "notes": "Dynamically sets the voice selection based on the number of links."
    },
    {
        "name": "SAMPLE_ZONE_SELECT",
        "id": 226,
        "hex_id": "62h,01h",
        "tabegory": "Master MIDI",
        "category": "MIDI Preferences 2",
        "sub_category": "Preferences",
        "min": 0,
        "max": 255,
        "recommended_ui": "Numeric input",
        "notes": "Selects the sample zone number for MIDI operations."
    },
    {
        "name": "GROUP_SELECT",
        "id": 227,
        "hex_id": "63h,01h",
        "tabegory": "Master MIDI",
        "category": "MIDI Preferences 2",
        "sub_category": "Preferences",
        "min": 0,
        "max": 31,
        "recommended_ui": "Dropdown",
        "recommended_ui_alt": "Numeric input",
        "notes": "Specifies the group number for MIDI control, typically used in multichannel setups."
    },

    # ====================================================
    # 22. Master Effects Parameters (Section A)
    # ====================================================
    {
        "name": "MASTER_FX_A_ALGORITHM",
        "id": 228,
        "hex_id": "64h,01h",
        "tabegory": "Master Effects",
        "tabegory": "Master Effects",
        "category": "Master Effects / Links",
        "sub_category": "Section A",
        "min": 0,
        "max": 44,
        "default": 14,
        "recommended_ui": "Dropdown",
        "notes": "Selects the algorithm for Master Effects section A."
    },
    {
        "name": "MASTER_FX_A_PARM_0",
        "id": 229,
        "hex_id": "65h,01h",
        "tabegory": "Master Effects",
        "tabegory": "Master Effects",
        "category": "Master Effects / Links",
        "sub_category": "Section A",
        "min": 0,
        "max": 90,
        "default": 54,
        "recommended_ui": "Slider",
        "ui_config": "horizontal",
        "notes": "First parameter for Master Effects A."
    },
    {
        "name": "MASTER_FX_A_PARM_1",
        "id": 230,
        "hex_id": "66h,01h",
        "tabegory": "Master Effects",
        "tabegory": "Master Effects",
        "category": "Master Effects / Links",
        "sub_category": "Section A",
        "min": 0,
        "max": 127,
        "default": 64,
        "recommended_ui": "Slider",
        "ui_config": "horizontal",
        "notes": "Second parameter for Master Effects A."
    },
    {
        "name": "MASTER_FX_A_PARM_2",
        "id": 231,
        "hex_id": "67h,01h",
        "tabegory": "Master Effects",
        "tabegory": "Master Effects",
        "category": "Master Effects / Links",
        "sub_category": "Section A",
        "min": 0,
        "max": 127,
        "default": 0,
        "recommended_ui": "Slider",
        "ui_config": "horizontal",
        "notes": "Third parameter for Master Effects A."
    },
    {
        "name": "MASTER_FX_A_AMT_0",
        "id": 232,
        "hex_id": "68h,01h",
        "tabegory": "Master Effects",
        "tabegory": "Master Effects",
        "category": "Master Effects / Links",
        "sub_category": "Section A",
        "min": 0,
        "max": 100,
        "default": 10,
        "recommended_ui": "Slider",
        "ui_config": "vertical",
        "notes": "Sets the amount for Master Effects A parameter 0."
    },
    {
        "name": "MASTER_FX_A_AMT_1",
        "id": 233,
        "hex_id": "69h,01h",
        "tabegory": "Master Effects",
        "tabegory": "Master Effects",
        "category": "Master Effects / Links",
        "sub_category": "Section A",
        "min": 0,
        "max": 100,
        "default": 20,
        "recommended_ui": "Slider",
        "ui_config": "vertical",
        "notes": "Sets the amount for Master Effects A parameter 1."
    },
    {
        "name": "MASTER_FX_A_AMT_2",
        "id": 234,
        "hex_id": "6Ah,01h",
        "tabegory": "Master Effects",
        "tabegory": "Master Effects",
        "category": "Master Effects / Links",
        "sub_category": "Section A",
        "min": 0,
        "max": 100,
        "default": 30,
        "recommended_ui": "Slider",
        "ui_config": "vertical",
        "notes": "Sets the amount for Master Effects A parameter 2."
    },
    {
        "name": "MASTER_FX_A_AMT_3",
        "id": 235,
        "hex_id": "6Bh,01h",
        "tabegory": "Master Effects",
        "tabegory": "Master Effects",
        "category": "Master Effects / Links",
        "sub_category": "Section A",
        "min": 0,
        "max": 100,
        "default": 40,
        "recommended_ui": "Slider",
        "ui_config": "vertical",
        "notes": "Sets the amount for Master Effects A parameter 3."
    },

    # ====================================================
    # 23. Master Effects Parameters (Section B)
    # ====================================================
    {
        "name": "MASTER_FX_B_ALGORITHM",
        "id": 236,
        "hex_id": "6Ch,01h",
        "tabegory": "Master Effects",
        "tabegory": "Master Effects",
        "category": "Master Effects / Links",
        "sub_category": "Section B",
        "min": 0,
        "max": 27,
        "default": 1,
        "recommended_ui": "Dropdown",
        "notes": "Selects the algorithm for Master Effects section B."
    },
    {
        "name": "MASTER_FX_B_PARM_0",
        "id": 237,
        "hex_id": "6Dh,01h",
        "tabegory": "Master Effects",
        "tabegory": "Master Effects",
        "category": "Master Effects / Links",
        "sub_category": "Section B",
        "min": 0,
        "max": 127,
        "default": 0,
        "recommended_ui": "Slider",
        "ui_config": "horizontal",
        "notes": "First parameter for Master Effects section B."
    },
    {
        "name": "MASTER_FX_B_PARM_1",
        "id": 238,
        "hex_id": "6Eh,01h",
        "tabegory": "Master Effects",
        "tabegory": "Master Effects",
        "category": "Master Effects / Links",
        "sub_category": "Section B",
        "min": 0,
        "max": 127,
        "default": 3,
        "recommended_ui": "Slider",
        "ui_config": "horizontal",
        "notes": "Second parameter for Master Effects section B."
    },
    {
        "name": "MASTER_FX_B_PARM_2",
        "id": 239,
        "hex_id": "6Fh,01h",
        "tabegory": "Master Effects",
        "tabegory": "Master Effects",
        "category": "Master Effects / Links",
        "sub_category": "Section B",
        "min": 0,
        "max": 127,
        "default": 0,
        "recommended_ui": "Slider",
        "ui_config": "horizontal",
        "notes": "Third parameter for Master Effects section B."
    },
    {
        "name": "MASTER_FX_B_AMT_0",
        "id": 240,
        "hex_id": "70h,01h",
        "tabegory": "Master Effects",
        "tabegory": "Master Effects",
        "category": "Master Effects / Links",
        "sub_category": "Section B",
        "min": 0,
        "max": 100,
        "default": 10,
        "recommended_ui": "Slider",
        "ui_config": "vertical",
        "notes": "Amount control for Master Effects B parameter 0."
    },
    {
        "name": "MASTER_FX_B_AMT_1",
        "id": 241,
        "hex_id": "71h,01h",
        "tabegory": "Master Effects",
        "tabegory": "Master Effects",
        "category": "Master Effects / Links",
        "sub_category": "Section B",
        "min": 0,
        "max": 100,
        "default": 15,
        "recommended_ui": "Slider",
        "ui_config": "vertical",
        "notes": "Amount control for Master Effects B parameter 1."
    },
    {
        "name": "MASTER_FX_B_AMT_2",
        "id": 242,
        "hex_id": "72h,01h",
        "tabegory": "Master Effects",
        "tabegory": "Master Effects",
        "category": "Master Effects / Links",
        "sub_category": "Section B",
        "min": 0,
        "max": 100,
        "default": 30,
        "recommended_ui": "Slider",
        "ui_config": "vertical",
        "notes": "Amount control for Master Effects B parameter 2."
    },
    {
        "name": "MASTER_FX_B_AMT_3",
        "id": 243,
        "hex_id": "73h,01h",
        "tabegory": "Master Effects",
        "tabegory": "Master Effects",
        "category": "Master Effects / Links",
        "sub_category": "Section B",
        "min": 0,
        "max": 100,
        "default": 0,
        "recommended_ui": "Slider",
        "ui_config": "vertical",
        "notes": "Amount control for Master Effects B parameter 3."
    },
    {
        "name": "MASTER_FX_BYPASS",
        "id": 244,
        "hex_id": "74h,01h",
        "tabegory": "Master Effects",
        "tabegory": "Master Effects",
        "category": "Master Effects / Links",
        "sub_category": "Bypass",
        "min": 0,
        "max": 1,
        "default": 0,
        "display_options": {0: "active", 1: "bypassed"},
        "recommended_ui": "Toggle",
        "notes": "Bypasses Master Effects section B when set to 1."
    },
    {
        "name": "MASTER_FX_MM_CTRL_CHANNEL",
        "id": 245,
        "hex_id": "75h,01h",
        "tabegory": "Master Effects",
        "tabegory": "Master Effects",
        "category": "Master Effects / Links",
        "sub_category": "Control",
        "min": -1,
        "max": 15,
        "default": -1,
        "recommended_ui": "Numeric input (or dropdown)",
        "notes": "Sets the MIDI control channel for multimode FX; -1 indicates no control."
    },
    {
        "name": "MULTIMODE_CHANNEL",
        "id": 246,
        "hex_id": "76h,01h",
        "tabegory": "Master Effects",
        "tabegory": "Master Effects",
        "category": "Master Effects / Links",
        "sub_category": "Multimode",
        "min": 1,
        "max": 16,
        "default": 1,
        "recommended_ui": "Dropdown (if limited to 16, otherwise slider)",
        "notes": "Selects the channel used in multimode FX; range depends on installed MIDI expansion."
    },
    {
        "name": "MULTIMODE_PRESET",
        "id": 247,
        "hex_id": "77h,01h",
        "tabegory": "Master Effects",
        "tabegory": "Master Effects",
        "category": "Master Effects / Links",
        "sub_category": "Multimode",
        "min": -1,
        "max": 999,
        "default": -1,
        "recommended_ui": "Numeric input (read-only for ROM presets)",
        "notes": "Selects the preset used for multimode effects. A value of -1 indicates an unavailable preset."
    },
    {
        "name": "MULTIMODE_VOLUME",
        "id": 248,
        "hex_id": "78h,01h",
        "tabegory": "Master Effects",
        "tabegory": "Master Effects",
        "category": "Master Effects / Links",
        "sub_category": "Multimode",
        "min": 0,
        "max": 127,
        "default": 127,
        "recommended_ui": "Slider",
        "notes": "Sets the overall volume for multimode operation."
    },
    {
        "name": "MULTIMODE_PAN",
        "id": 249,
        "hex_id": "79h,01h",
        "tabegory": "Master Effects",
        "tabegory": "Master Effects",
        "category": "Master Effects / Links",
        "sub_category": "Multimode",
        "min": -64,
        "max": 63,
        "default": 0,
        "recommended_ui": "Slider",
        "notes": "Sets the panning for multimode effects."
    },
    {
        "name": "MULTIMODE_SUBMIX",
        "id": 250,
        "hex_id": "7Ah,01h",
        "tabegory": "Master Effects",
        "tabegory": "Master Effects",
        "category": "Master Effects / Links",
        "sub_category": "Multimode",
        "min": -1,
        "max": 3,
        "default": -1,
        "recommended_ui": "Dropdown",
        "notes": "Selects the submix channel for multimode operation."
    },

    # ====================================================
    # 24. Master Effects / Links
    # ====================================================
    {
        "name": "E4_LINK_INTERNAL_EXTERNAL",
        "id": 251,
        "hex_id": "7Bh,01h",
        "category": "Master Effects / Links",
        "sub_category": "Link Routing",
        "min": 0,
        "max": 16,
        "default": 0,
        "recommended_ui": "Dropdown",
        "notes": "Specifies whether the link is set to internal or external routing."
    },
    {
        "name": "E4_LINK_FILTER_PITCH",
        "id": 252,
        "hex_id": "7Ch,01h",
        "category": "Master Effects / Links",
        "sub_category": "Filter Control",
        "min": 0,
        "max": 1,
        "default": 0,
        "recommended_ui": "Toggle",
        "notes": "Enables or disables the pitch control for the link filter."
    },
    {
        "name": "E4_LINK_FILTER_MOD",
        "id": 253,
        "hex_id": "7Dh,01h",
        "category": "Master Effects / Links",
        "sub_category": "Filter Control",
        "min": 0,
        "max": 1,
        "default": 0,
        "recommended_ui": "Toggle",
        "notes": "Enables or disables the modulation control for the link filter."
    },
    {
        "name": "E4_LINK_FILTER_PRESSURE",
        "id": 254,
        "hex_id": "7Eh,01h",
        "category": "Master Effects / Links",
        "sub_category": "Filter Control",
        "min": 0,
        "max": 1,
        "default": 0,
        "recommended_ui": "Toggle",
        "notes": "Enables or disables pressure control for the link filter."
    },
    {
        "name": "E4_LINK_FILTER_PEDAL",
        "id": 255,
        "hex_id": "7Fh,01h",
        "category": "Master Effects / Links",
        "sub_category": "Filter Control",
        "min": 0,
        "max": 1,
        "default": 0,
        "recommended_ui": "Toggle",
        "notes": "Enables or disables pedal control for the link filter."
    },
    {
        "name": "E4_LINK_FILTER_CTRL_A",
        "id": 256,
        "hex_id": "00h,02h",
        "category": "Master Effects / Links",
        "sub_category": "Filter Control",
        "min": 0,
        "max": 1,
        "default": 0,
        "recommended_ui": "Toggle",
        "notes": "Control A for link filtering; typically toggles a specific filter behavior."
    },
    {
        "name": "E4_LINK_FILTER_CTRL_B",
        "id": 257,
        "hex_id": "01h,02h",
        "category": "Master Effects / Links",
        "sub_category": "Filter Control",
        "min": 0,
        "max": 1,
        "default": 0,
        "recommended_ui": "Toggle",
        "notes": "Control B for link filtering."
    },
    {
        "name": "E4_LINK_FILTER_CTRL_C",
        "id": 258,
        "hex_id": "02h,02h",
        "category": "Master Effects / Links",
        "sub_category": "Filter Control",
        "min": 0,
        "max": 1,
        "default": 0,
        "recommended_ui": "Toggle",
        "notes": "Control C for link filtering."
    },
    {
        "name": "E4_LINK_FILTER_CTRL_D",
        "id": 259,
        "hex_id": "03h,02h",
        "category": "Master Effects / Links",
        "sub_category": "Filter Control",
        "min": 0,
        "max": 1,
        "default": 0,
        "recommended_ui": "Toggle",
        "notes": "Control D for link filtering."
    },
    {
        "name": "E4_LINK_FILTER_CTRL_E",
        "id": 260,
        "hex_id": "04h,02h",
        "category": "Master Effects / Links",
        "sub_category": "Filter Control",
        "min": 0,
        "max": 1,
        "default": 0,
        "recommended_ui": "Toggle",
        "notes": "Control E for link filtering."
    },
    {
        "name": "E4_LINK_FILTER_CTRL_F",
        "id": 261,
        "hex_id": "05h,02h",
        "category": "Master Effects / Links",
        "sub_category": "Filter Control",
        "min": 0,
        "max": 1,
        "default": 0,
        "recommended_ui": "Toggle",
        "notes": "Control F for link filtering."
    },
    {
        "name": "E4_LINK_FILTER_CTRL_G",
        "id": 262,
        "hex_id": "06h,02h",
        "category": "Master Effects / Links",
        "sub_category": "Filter Control",
        "min": 0,
        "max": 1,
        "default": 0,
        "recommended_ui": "Toggle",
        "notes": "Control G for link filtering."
    },
    {
        "name": "E4_LINK_FILTER_CTRL_H",
        "id": 263,
        "hex_id": "07h,02h",
        "category": "Master Effects / Links",
        "sub_category": "Filter Control",
        "min": 0,
        "max": 1,
        "default": 0,
        "recommended_ui": "Toggle",
        "notes": "Control H for link filtering."
    },
    {
        "name": "E4_LINK_FILTER_SWITCH_1",
        "id": 264,
        "hex_id": "08h,02h",
        "category": "Master Effects / Links",
        "sub_category": "Filter Control",
        "min": 0,
        "max": 1,
        "default": 0,
        "recommended_ui": "Toggle",
        "notes": "First switch for controlling link filtering."
    },
    {
        "name": "E4_LINK_FILTER_SWITCH_2",
        "id": 265,
        "hex_id": "09h,02h",
        "category": "Master Effects / Links",
        "sub_category": "Filter Control",
        "min": 0,
        "max": 1,
        "default": 0,
        "recommended_ui": "Toggle",
        "notes": "Second switch for controlling link filtering."
    },
    {
        "name": "E4_LINK_FILTER_THUMB",
        "id": 266,
        "hex_id": "0Ah,02h",
        "category": "Master Effects / Links",
        "sub_category": "Filter Control",
        "min": 0,
        "max": 1,
        "default": 0,
        "recommended_ui": "Toggle",
        "notes": "Thumb control for link filtering."
    },

    # ====================================================
    # 25. Ultra Only Parameters
    # ====================================================
    {
        "name": "MASTER_WORD_CLOCK_IN",
        "id": 267,
        "hex_id": "0Bh,02h",
        "category": "Master Effects / Ultra Only",
        "sub_category": "Clock",
        "min": 0,
        "max": 4,
        "default": 0,
        "display_options": {0: "Internal", 1: "BNC", 2: "AES", 3: "ADAT", 4: "(future)"},
        "recommended_ui": "Dropdown",
        "notes": "Selects the source for the word clock input."
    },
    {
        "name": "MASTER_WORD_CLOCK_PHASE_IN",
        "id": 268,
        "hex_id": "0Ch,02h",
        "category": "Master Effects / Ultra Only",
        "sub_category": "Clock",
        "min": 0,
        "max": 511,
        "recommended_ui": "Slider",
        "notes": "Sets the phase of the incoming word clock."
    },
    {
        "name": "MASTER_WORD_CLOCK_PHASE_OUT",
        "id": 269,
        "hex_id": "0Dh,02h",
        "category": "Master Effects / Ultra Only",
        "sub_category": "Clock",
        "min": 0,
        "max": 511,
        "recommended_ui": "Slider",
        "notes": "Sets the phase of the outgoing word clock."
    },
    {
        "name": "MASTER_OUTPUT_DITHER",
        "id": 270,
        "hex_id": "0Eh,02h",
        "category": "Master Effects / Ultra Only",
        "sub_category": "Output",
        "min": 0,
        "max": 1,
        "default": 0,
        "display_options": {0: "off", 1: "on"},
        "recommended_ui": "Toggle",
        "notes": "Enables or disables dithering on the master output."
    },

    # ====================================================
    # 26. Master Effects / Audition
    # ====================================================
    {
        "name": "MASTER_AUDITION_KEY",
        "id": 271,
        "hex_id": "0Fh,02h",
        "category": "Master Effects / Audition",
        "sub_category": "Key Selection",
        "min": 0,
        "max": 127,
        "recommended_ui": "Slider or numeric input",
        "notes": "Specifies the audition key for monitoring and test playback."
    },

    # ====================================================
    # 27. Parameter Value Edit / Request / Min/Max/Default Commands
    # (IDs derived from hex_id strings where necessary)
    # ====================================================
    {
        "name": "Parameter Value Edit",
        "id": 1,  # Derived from hex "01h"
        "hex_id": "01h followed by Byte Count, Parameter ID, Parameter Data, Checksum",
        "category": "Parameter Value Edit",
        "sub_category": "Parameter Modification",
        "notes": (
            "Edits a parameter’s value. The message consists of a byte count, the Parameter ID "
            "(LSB-first), followed by the parameter data, and a checksum computed as the 1’s complement XOR of the sum of data bytes. "
            "A special checksum flag (7Fh) may be used to bypass checksum validation. "
            "This command is typically transmitted as a single packet."
        ),
        "recommended_ui": "Parameter editing interface (e.g., slider and numeric display)"
    },
    {
        "name": "Parameter Value Request",
        "id": 2,  # Derived from hex "02h"
        "hex_id": "02h followed by Byte Count, Parameter ID, Checksum",
        "category": "Parameter Value Request",
        "sub_category": "Parameter Query",
        "notes": (
            "Requests the current value of a parameter. The device will respond with a complete Parameter Value Edit message "
            "that contains the requested parameter’s current setting."
        ),
        "recommended_ui": "Button"
    },
    {
        "name": "Parameter Min/Max/Default Request",
        "id": 3,  # Derived from hex "03h"
        "hex_id": "03h followed by Parameter ID",
        "category": "Parameter Min/Max/Default Request",
        "sub_category": "Parameter Information",
        "notes": "Queries for the minimum, maximum, and default values for a specified parameter; used for display and validation purposes.",
        "recommended_ui": "Internal/diagnostic"
    },
    {
        "name": "Parameter Min/Max/Default Response",
        "id": 4,  # Derived from hex "04h"
        "hex_id": "04h followed by Parameter ID, Min, Max, Default, F7h",
        "category": "Parameter Min/Max/Default Response",
        "sub_category": "Parameter Information",
        "notes": "Returns the minimum, maximum, and default settings for the queried parameter.",
        "recommended_ui": "Display only"
    },


# ====================================================
# 28. Preset / Sample Naming Commands
# ====================================================
{
    "name": "ASCII Preset Name",
    "id": 5,  # Derived from hex "05h"
    "hex_id": "05h followed by Preset Number, 16-character string",
    "category": "Preset Naming",
    "sub_category": "Name Transmission",
    "notes": "Sends the full 16-character preset name as an ASCII string.",
    "recommended_ui": "Text field"
},
{
    "name": "ASCII Preset Name Request",
    "id": 6,  # Derived from hex "06h"
    "hex_id": "06h followed by Preset Number",
    "category": "Preset Naming",
    "sub_category": "Name Query",
    "notes": "Requests the full 16-character preset name for a specified preset number.",
    "recommended_ui": "Button"
},
{
    "name": "Preset Name Character Update",
    "id": 7,  # Derived from hex "07h"
    "hex_id": "07h followed by Preset Number, Character Number, ASCII Character",
    "category": "Preset Naming",
    "sub_category": "Name Editing",
    "notes": "Updates a single character in the preset name at a specified position.",
    "recommended_ui": "Text input"
},
{
    "name": "Preset Name Character Request",
    "id": 8,  # Derived from hex "08h"
    "hex_id": "08h followed by Preset Number, Character Number",
    "category": "Preset Naming",
    "sub_category": "Name Query",
    "notes": "Requests one character from the preset name.",
    "recommended_ui": "Internal"
},
{
    "name": "ASCII Sample Name",
    "id": 9,  # Derived from hex "09h"
    "hex_id": "09h followed by Sample Number, 16-character string",
    "category": "Sample Naming",
    "sub_category": "Name Transmission",
    "notes": "Sends the full 16-character sample name as an ASCII string.",
    "recommended_ui": "Text field"
},
{
    "name": "ASCII Sample Name Request",
    "id": 10,  # Derived from hex "0Ah"
    "hex_id": "0Ah followed by Sample Number",
    "category": "Sample Naming",
    "sub_category": "Name Query",
    "notes": "Requests the 16-character sample name for a given sample number.",
    "recommended_ui": "Button"
},
{
    "name": "Sample Name Character Update",
    "id": 11,  # Derived from hex "0Bh"
    "hex_id": "0Bh followed by Sample Number, Character Number, ASCII Character",
    "category": "Sample Naming",
    "sub_category": "Name Editing",
    "notes": "Updates one character within the sample name.",
    "recommended_ui": "Text input"
},
{
    "name": "Sample Name Character Request",
    "id": 12,  # Derived from hex "0Ch"
    "hex_id": "0Ch followed by Sample Number, Character Number",
    "category": "Sample Naming",
    "sub_category": "Name Query",
    "notes": "Requests a specific character of the sample name.",
    "recommended_ui": "Internal"
},

# ====================================================
# Dump Format Commands
# ====================================================
{
    "name": "ACK",
    "id": 127,
    "hex_id": "7Fh",
    "category": "Dump/Handshaking",
    "sub_category": "Acknowledge",
    "notes": "Indicates successful receipt of the last packet. The message includes a packet number for reference.",
    "recommended_ui": "Automatic (handshaking)"
},
{
    "name": "NAK",
    "id": 126,
    "hex_id": "7Eh",
    "category": "Dump/Handshaking",
    "sub_category": "Error Handling",
    "notes": "Indicates that the last packet was received with errors, prompting the sender to resend. Includes the packet number for reference.",
    "recommended_ui": "Automatic (handshaking)"
},
{
    "name": "CANCEL",
    "id": 125,
    "hex_id": "7Dh",
    "category": "Dump/Handshaking",
    "sub_category": "Flow Control",
    "notes": "Aborts the current dump transfer immediately.",
    "recommended_ui": "Button (user-triggered)"
},
{
    "name": "WAIT",
    "id": 124,
    "hex_id": "7Ch",
    "category": "Dump/Handshaking",
    "sub_category": "Flow Control",
    "notes": "Instructs the sender to pause transmission until an ACK is received.",
    "recommended_ui": "Automatic / Status indicator"
},
{
    "name": "EOF (End Of File)",
    "id": 123,
    "hex_id": "7Bh",
    "category": "Dump/Handshaking",
    "sub_category": "Flow Control",
    "notes": "Signals that no more packets will follow. This is sent as the final message in a dump; no response is expected.",
    "recommended_ui": "Display only (end-of-transfer indicator)"
},
{
    "name": "Dump Header",
    "id": 13,
    "subcommand": 1,
    "hex_id": "0Dh,01h",
    "category": "Dump Format",
    "sub_category": "Header",
    "notes": "The Dump Header is the first message in a preset dump. It includes the preset number, total data byte count (4 bytes, LSB-first), and the counts for Global Parameters, Link Parameters (per link), Voice Parameters (per voice), and Sample Zone Parameters.",
    "recommended_ui": "Display only (read-only)"
},
{
    "name": "Dump Data Message",
    "id": 13,
    "subcommand": 2,
    "hex_id": "0Dh,02h",
    "category": "Dump Format",
    "sub_category": "Data Message",
    "notes": "Each Dump Data Message contains 244 data bytes (except possibly the last) followed by a 1-byte checksum (the one’s complement of the sum of data bytes) and a running packet count (LSB-first starting at 1).",
    "recommended_ui": "Display only (read-only)"
},
# {
#     "name": "Dump Data Format - Short Form",
#     "id": null,
#     "hex_id": null,
#     "category": "Dump Format",
#     "sub_category": "Data Structure",
#     "notes": "Short Form Structure: {PresetNumber, Name, GlobalParms, NoOfLinks, {Link}*, NoOfVoices, {Voice}*}. For example, PresetNumber is 0-999, Name consists of 16 ASCII characters, and the first 6 Global Parameters are 2 bytes each.",
#     "recommended_ui": "Display only"
# },
# {
#     "name": "Dump Data Format - Long Form",
#     "id": null,
#     "hex_id": null,
#     "category": "Dump Format",
#     "sub_category": "Data Structure",
#     "notes": "Long Form Structure: Data is divided into 244-byte chunks. The dump consists of a 16-byte Name field, 44 bytes of Global Parameters, a 2-byte Link count followed by Link data blocks (58 bytes each), a 2-byte Voice count followed by Voice data blocks (292 bytes each), and Sample Zone data blocks (26 bytes each) following a 2-byte zone count per voice. The total size is defined in the Dump Header.",
#     "recommended_ui": "Display only"
# },

# ====================================================
# Tuning Display Parameters
# ====================================================
{
    "name": "E4_VOICE_CHORUS_WIDTH",
    "id": 59,
    "hex_id": "3Bh,00h",
    "category": "Tuning - Chorus",
    "sub_category": "Display",
    "min": -128,
    "max": 0,
    "notes": "Displayed value is calculated as: pct = ((value + 128) * 100) / 128, then formatted (e.g., '%3d%%').",
    "recommended_ui": "Slider with percentage display",
    "recommended_ui_alt": "Numeric input with live percent update"
},
{
    "name": "E4_VOICE_CHORUS_X",
    "id": 60,
    "hex_id": "3Ch,00h",
    "category": "Tuning - Chorus",
    "sub_category": "Display",
    "min": -32,
    "max": 32,
    "notes": "Sets the initial inter-aural time delay (ITD) for the chorus. Mapping: 0=0.000ms, 1=0.045ms, …, 32=1.451ms. Positive values delay left channel more; negative, the right.",
    "recommended_ui": "Slider with ITD conversion display"
},
{
    "name": "E4_VOICE_DELAY",
    "id": 61,
    "hex_id": "3Dh,00h",
    "category": "Tuning - Delay/Glide",
    "sub_category": "Display",
    "min": 0,
    "max": 10000,
    "notes": "Sets the delay time in milliseconds for the voice.",
    "recommended_ui": "Slider or numeric input (ms)",
    "recommended_ui_alt": "Spinner control for fine delay adjustment"
},
{
    "name": "E4_VOICE_START_OFFSET",
    "id": 62,
    "hex_id": "3Eh,00h",
    "category": "Tuning - Delay/Glide",
    "sub_category": "Display",
    "min": 0,
    "max": 127,
    "notes": "Specifies the starting offset for voice sample playback.",
    "recommended_ui": "Slider"
},
# {
#     "name": "E4_VOICE_GLIDE_RATE",
#     "id": 63,
#     "hex_id": "3Fh,00h",
#     "category": "Tuning - Portamento",
#     "sub_category": "Display",
#     "min": 0,
#     "max": 127,
#     "notes": "Sets the glide (portamento) rate in sec/oct. The raw value is converted via the envunits1 and envunits2 tables to produce a time value (e.g., 'X.XXX sec/oct').",
#     "recommended_ui": "Slider with custom sec/oct conversion display"
# }
]

# ====================================================
# Conversion Tables for Glide Rate
# ====================================================
envunits1 = [
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 2, 2, 2, 2,
    2, 2, 2, 3, 3, 3, 3, 3,
    4, 4, 4, 4, 5, 5, 5, 5,
    6, 6, 7, 7, 7, 8, 8, 9,
    9, 10, 11, 11, 12, 13, 13, 14,
    15, 16, 17, 18, 19, 20, 22, 23,
    24, 26, 28, 30, 32, 34, 36, 38,
    41, 44, 47, 51, 55, 59, 64, 70,
    76, 83, 91, 100, 112, 125, 142, 163
]

envunits2 = [
    0, 1, 2, 3, 4, 5, 6, 7,
    8, 9, 10, 11, 12, 13, 14, 15,
    16, 17, 18, 19, 20, 21, 22, 23,
    25, 26, 28, 29, 32, 34, 36, 38,
    41, 43, 46, 49, 52, 55, 58, 62,
    65, 70, 74, 79, 83, 88, 93, 98,
    4, 10, 17, 24, 31, 39, 47, 56,
    65, 74, 84, 95, 6, 18, 31, 44,
    59, 73, 89, 6, 23, 42, 62, 82,
    4, 28, 52, 78, 5, 34, 64, 97,
    32, 67, 6, 46, 90, 35, 83, 34,
    87, 45, 6, 70, 38, 11, 88, 70,
    56, 49, 48, 53, 65, 85, 13, 50,
    97, 54, 24, 6, 2, 15, 44, 93,
    64, 60, 84, 41, 34, 70, 56, 3,
    22, 28, 40, 87, 9, 65, 36, 69
]





























filter_groups = [
    {
        "filter_type": "2 Pole / 4 Pole / 6 Pole Low-pass",
        "parameters": [
            {
                "name": "E4_VOICE_FMORPH",
                "id": 83,
                "min": 0,
                "max": 255,
                "display_range": "57Hz to 20000Hz",
                "frequency_table": "Filter Table 1: fil_freq(input, 20000, 1002)"
            },
            {
                "name": "E4_VOICE_FKEY_XFORM",
                "id": 84,
                "min": 0,
                "max": 127,
                "label": "Q",
                "display_range": "0 to 127"
            }
        ],
        "recommended_ui": "Sliders with Hz conversion (via Filter Table 1) and Q display"
    },
    {
        "filter_type": "2nd / 4th Order High-pass",
        "parameters": [
            {
                "name": "E4_VOICE_FMORPH",
                "id": 83,
                "min": 0,
                "max": 255,
                "display_range": "69Hz to 18000Hz",
                "frequency_table": "Filter Table 2: fil_freq(input, 18000, 1003)"
            },
            {
                "name": "E4_VOICE_FKEY_XFORM",
                "id": 84,
                "min": 0,
                "max": 127,
                "label": "Q",
                "display_range": "0 to 127"
            }
        ],
        "recommended_ui": "Sliders with Hz conversion (via Filter Table 2) and Q display"
    },
    {
        "filter_type": "2nd / 4th Order Band-pass / Contrary Band-pass",
        "parameters": [
            {
                "name": "E4_VOICE_FMORPH",
                "id": 83,
                "min": 0,
                "max": 255,
                "display_range": "57Hz to 10000Hz",
                "frequency_table": "Filter Table 3: fil_freq(input, 10000, 1006)"
            },
            {
                "name": "E4_VOICE_FKEY_XFORM",
                "id": 84,
                "min": 0,
                "max": 127,
                "label": "Q",
                "display_range": "0 to 127"
            }
        ],
        "recommended_ui": "Sliders with Hz conversion (via Filter Table 3) and Q display"
    },
    {
        "filter_type": "Swept EQ (1 octave / 2->1 oct / 3->1 oct)",
        "parameters": [
            {
                "name": "E4_VOICE_FMORPH",
                "id": 83,
                "min": 0,
                "max": 255,
                "display_range": "83Hz to 10000Hz",
                "frequency_table": "Filter Table 3: fil_freq(input, 10000, 1006)"
            },
            {
                "name": "E4_VOICE_FKEY_XFORM",
                "id": 84,
                "min": 0,
                "max": 127,
                "label": "Gain",
                "display_range": "-24.0dB to +23.6dB",
                "gain_table": "Filter Table 4: cnv_morph_gain(input, value)"
            }
        ],
        "recommended_ui": "Sliders with conversion to Hz (Filter Table 3) and dB (Filter Table 4)"
    },
    {
        "filter_type": "Phaser / Flanger / Bat-Phaser",
        "parameters": [
            {
                "name": "E4_VOICE_FMORPH",
                "id": 83,
                "min": 0,
                "max": 255,
                "label": "Frequency",
                "display_range": "0 to 255"
            },
            {
                "name": "E4_VOICE_FKEY_XFORM",
                "id": 84,
                "min": 0,
                "max": 127,
                "label": "Resonance",
                "display_range": "0 to 127"
            }
        ],
        "recommended_ui": "Simple sliders (values displayed directly)"
    },
    {
        "filter_type": "Vocal Effects (Ah-Ay-Ee / Oo-Ah)",
        "parameters": [
            {
                "name": "E4_VOICE_FMORPH",
                "id": 83,
                "min": 0,
                "max": 255,
                "label": "Morph",
                "display_range": "0 to 255"
            },
            {
                "name": "E4_VOICE_FKEY_XFORM",
                "id": 84,
                "min": 0,
                "max": 127,
                "label": "Body Size",
                "display_range": "0 to 127"
            }
        ],
        "recommended_ui": "Sliders"
    },
    {
        "filter_type": "Dual EQ Morph",
        "parameters": [
            {
                "name": "E4_VOICE_FMORPH",
                "id": 83,
                "min": 0,
                "max": 255,
                "label": "Morph",
                "display_range": "0 to 255"
            },
            {
                "name": "E4_VOICE_FKEY_XFORM",
                "id": 84,
                "min": 0,
                "max": 127,
                "label": "Gain",
                "display_range": "-24.0dB to +23.6dB",
                "gain_table": "Filter Table 4: cnv_morph_gain(input, value)"
            },
            {
                "name": "E4_VOICE_FILT_GEN_PARM3",
                "id": 87,
                "min": 0,
                "max": 127,
                "label": "EQ 1 Low",
                "display_range": "83Hz to 9824Hz",
                "frequency_table": "Filter Table 5: cnv_morph_freq(2*input, value)"
            },
            {
                "name": "E4_VOICE_FILT_GEN_PARM4",
                "id": 88,
                "min": 0,
                "max": 127,
                "label": "EQ 1 High",
                "display_range": "83Hz to 9824Hz",
                "frequency_table": "Filter Table 5: cnv_morph_freq(2*input, value)"
            },
            {
                "name": "E4_VOICE_FILT_GEN_PARM5",
                "id": 89,
                "min": 0,
                "max": 127,
                "label": "EQ 1 Gain",
                "display_range": "-24.0dB to +23.6dB",
                "gain_table": "Filter Table 4: cnv_morph_gain(input, value)"
            },
            {
                "name": "E4_VOICE_FILT_GEN_PARM6",
                "id": 90,
                "min": 0,
                "max": 127,
                "label": "EQ 2 Low",
                "display_range": "83Hz to 9824Hz",
                "frequency_table": "Filter Table 5: cnv_morph_freq(2*input, value)"
            },
            {
                "name": "E4_VOICE_FILT_GEN_PARM7",
                "id": 91,
                "min": 0,
                "max": 127,
                "label": "EQ 2 High",
                "display_range": "83Hz to 9824Hz",
                "frequency_table": "Filter Table 5: cnv_morph_freq(2*input, value)"
            },
            {
                "name": "E4_VOICE_FILT_GEN_PARM8",
                "id": 92,
                "min": 0,
                "max": 127,
                "label": "EQ 2 Gain",
                "display_range": "-24.0dB to +23.6dB",
                "gain_table": "Filter Table 4: cnv_morph_gain(input, value)"
            }
        ],
        "recommended_ui": "Grouped sliders with frequency (Hz) and gain (dB) conversion"
    },
    {
        "filter_type": "2EQ+Lowpass Morph",
        "parameters": [
            {
                "name": "E4_VOICE_FMORPH",
                "id": 83,
                "min": 0,
                "max": 255,
                "label": "Fc/Morph",
                "display_range": "0 to 255 (raw value)"
            },
            {
                "name": "E4_VOICE_FKEY_XFORM",
                "id": 84,
                "min": 0,
                "max": 127,
                "label": "LPF Q",
                "display_range": "0 to 127"
            }
        ],
        "recommended_ui": "Sliders (raw values)"
    },
    {
        "filter_type": "2EQMorph+Expression",
        "parameters": [
            {
                "name": "E4_VOICE_FMORPH",
                "id": 83,
                "min": 0,
                "max": 255,
                "label": "Morph",
                "display_range": "0 to 255"
            },
            {
                "name": "E4_VOICE_FKEY_XFORM",
                "id": 84,
                "min": 0,
                "max": 127,
                "label": "Expression",
                "display_range": "0 to 127"
            },
            # It also uses the EQ parameters as in Dual EQ Morph:  ===========================================
            {
                "name": "E4_VOICE_FILT_GEN_PARM3",
                "id": 87,
                "min": 0,
                "max": 127,
                "label": "EQ 1 Low",
                "display_range": "83Hz to 9824Hz",
                "frequency_table": "Filter Table 5"
            },
            {
                "name": "E4_VOICE_FILT_GEN_PARM4",
                "id": 88,
                "min": 0,
                "max": 127,
                "label": "EQ 1 High",
                "display_range": "83Hz to 9824Hz",
                "frequency_table": "Filter Table 5"
            },
            {
                "name": "E4_VOICE_FILT_GEN_PARM5",
                "id": 89,
                "min": 0,
                "max": 127,
                "label": "EQ 1 Gain",
                "display_range": "-24.0dB to +23.6dB",
                "gain_table": "Filter Table 4"
            },
            {
                "name": "E4_VOICE_FILT_GEN_PARM6",
                "id": 90,
                "min": 0,
                "max": 127,
                "label": "EQ 2 Low",
                "display_range": "83Hz to 9824Hz",
                "frequency_table": "Filter Table 5"
            },
            {
                "name": "E4_VOICE_FILT_GEN_PARM7",
                "id": 91,
                "min": 0,
                "max": 127,
                "label": "EQ 2 High",
                "display_range": "83Hz to 9824Hz",
                "frequency_table": "Filter Table 5"
            },
            {
                "name": "E4_VOICE_FILT_GEN_PARM8",
                "id": 92,
                "min": 0,
                "max": 127,
                "label": "EQ 2 Gain",
                "display_range": "-24.0dB to +23.6dB",
                "gain_table": "Filter Table 4"
            }
        ],
        "recommended_ui": "Sliders with expression display"
    },
    {
        "filter_type": "Peak/Shelf Morph",
        "parameters": [
            {
                "name": "E4_VOICE_FMORPH",
                "id": 83,
                "min": 0,
                "max": 255,
                "label": "Morph",
                "display_range": "0 to 255"
            },
            {
                "name": "E4_VOICE_FKEY_XFORM",
                "id": 84,
                "min": 0,
                "max": 127,
                "label": "Peak",
                "display_range": "-24.0dB to +23.6dB",
                "gain_table": "Filter Table 4"
            },
            {
                "name": "E4_VOICE_FILT_GEN_PARM3",
                "id": 87,
                "min": 0,
                "max": 127,
                "label": "Low Morph Freq",
                "display_range": "83Hz to 9824Hz",
                "frequency_table": "Filter Table 5"
            },
            {
                "name": "E4_VOICE_FILT_GEN_PARM4",
                "id": 88,
                "min": 0,
                "max": 127,
                "label": "Low Morph Shelf",
                "display_range": "-64 to 63"
            },
            {
                "name": "E4_VOICE_FILT_GEN_PARM5",
                "id": 89,
                "min": 0,
                "max": 127,
                "label": "Low Morph Peak",
                "display_range": "-24.0dB to +23.6dB",
                "gain_table": "Filter Table 4"
            },
            {
                "name": "E4_VOICE_FILT_GEN_PARM6",
                "id": 90,
                "min": 0,
                "max": 127,
                "label": "High Morph Freq",
                "display_range": "83Hz to 9824Hz",
                "frequency_table": "Filter Table 5"
            },
            {
                "name": "E4_VOICE_FILT_GEN_PARM7",
                "id": 91,
                "min": 0,
                "max": 127,
                "label": "High Morph Shelf",
                "display_range": "-64 to 63"
            },
            {
                "name": "E4_VOICE_FILT_GEN_PARM8",
                "id": 92,
                "min": 0,
                "max": 127,
                "label": "High Morph Peak",
                "display_range": "-24.0dB to +23.6dB",
                "gain_table": "Filter Table 4"
            }
        ],
        "recommended_ui": "Sliders with dB conversion"
    }]




# Global Parameters
# (Preset-wide settings that affect tone, effects, and performance)

# 0: E4_PRESET_TRANSPOSE

# 1: E4_PRESET_VOLUME

# 2: E4_PRESET_CTRL_A

# 3: E4_PRESET_CTRL_B

# 4: E4_PRESET_CTRL_C

# 5: E4_PRESET_CTRL_D

# 6: E4_PRESET_FX_A_ALGORITHM

# 7: E4_PRESET_FX_A_PARM_0

# 8: E4_PRESET_FX_A_PARM_1

# 9: E4_PRESET_FX_A_PARM_2

# 10: E4_PRESET_FX_A_AMT_0

# 11: E4_PRESET_FX_A_AMT_1

# 12: E4_PRESET_FX_A_AMT_2

# 13: E4_PRESET_FX_A_AMT_3

# 14: E4_PRESET_FX_B_ALGORITHM

# 15: E4_PRESET_FX_B_PARM_0

# 16: E4_PRESET_FX_B_PARM_1

# 17: E4_PRESET_FX_B_PARM_2

# 18: E4_PRESET_FX_B_AMT_0

# 19: E4_PRESET_FX_B_AMT_1

# 20: E4_PRESET_FX_B_AMT_2

# 21: E4_PRESET_FX_B_AMT_3

# Links Parameters
# (Parameters affecting the linking of voices)

# 23: E4_LINK_PRESET

# 24: E4_LINK_VOLUME

# 25: E4_LINK_PAN

# 26: E4_LINK_TRANSPOSE

# 27: E4_LINK_FINE_TUNE

# 28: E4_LINK_KEY_LOW

# 29: E4_LINK_KEY_LOWFADE

# 30: E4_LINK_KEY_HIGH

# 31: E4_LINK_KEY_HIGHFADE

# 32: E4_LINK_VEL_LOW

# 33: E4_LINK_VEL_LOWFADE

# 34: E4_LINK_VEL_HIGH

# 35: E4_LINK_VEL_HIGHFADE

# Voices Parameters
# (Parameters that control individual voice settings)

# 37: E4_GEN_GROUP_NUM

# 38: E4_GEN_SAMPLE

# 39: E4_GEN_VOLUME

# 40: E4_GEN_PAN

# 41: E4_GEN_CTUNE

# 42: E4_GEN_FTUNE

# 43: E4_GEN_XPOSE

# 44: E4_GEN_ORIG_KEY

# 45: E4_GEN_KEY_LOW

# 46: E4_GEN_KEY_LOWFADE

# 47: E4_GEN_KEY_HIGH

# 48: E4_GEN_KEY_HIGHFADE

# 49: E4_GEN_VEL_LOW

# 50: E4_GEN_VEL_LOWFADE

# 51: E4_GEN_VEL_HIGH

# 52: E4_GEN_VEL_HIGHFADE

# 53: E4_GEN_RT_LOW

# 54: E4_GEN_RT_LOWFADE

# 55: E4_GEN_RT_HIGH

# 56: E4_GEN_RT_HIGHFADE

# Tuning Parameters
# (Settings that affect modulation, chorus, delay, and portamento)

# 57: E4_VOICE_NON_TRANSPOSE

# 58: E4_VOICE_CHORUS_AMOUNT

# 59: E4_VOICE_CHORUS_WIDTH

# 60: E4_VOICE_CHORUS_X

# 61: E4_VOICE_DELAY

# 62: E4_VOICE_START_OFFSET

# 63: E4_VOICE_GLIDE_RATE

# 64: E4_VOICE_GLIDE_CURVE

# 65: E4_VOICE_SOLO

# 66: E4_VOICE_ASSIGN_GROUP

# 67: E4_VOICE_LATCHMODE

# Amplifier Parameters
# (Controlling envelope rates/levels and the submix routing)

# 68: E4_VOICE_VOLENV_DEPTH

# 69: E4_VOICE_SUBMIX

# 70: E4_VOICE_VENV_SEG0_RATE

# 71: E4_VOICE_VENV_SEG0_TGTLVL

# 72: E4_VOICE_VENV_SEG1_RATE

# 73: E4_VOICE_VENV_SEG1_TGTLVL

# 74: E4_VOICE_VENV_SEG2_RATE

# 75: E4_VOICE_VENV_SEG2_TGTLVL

# 76: E4_VOICE_VENV_SEG3_RATE

# 77: E4_VOICE_VENV_SEG3_TGTLVL

# 78: E4_VOICE_VENV_SEG4_RATE

# 79: E4_VOICE_VENV_SEG4_TGTLVL

# 80: E4_VOICE_VENV_SEG5_RATE

# 81: E4_VOICE_VENV_SEG5_TGTLVL

# Filter Parameters
# (For tone-shaping using filters and envelope followers)

# 82: E4_VOICE_FTYPE

# 83: E4_VOICE_FMORPH

# 84: E4_VOICE_FKEY_XFORM

# 85: E4_VOICE_FILT_GEN_PARM1

# 86: E4_VOICE_FILT_GEN_PARM2

# 87: E4_VOICE_FILT_GEN_PARM3

# 88: E4_VOICE_FILT_GEN_PARM4

# 89: E4_VOICE_FILT_GEN_PARM5

# 90: E4_VOICE_FILT_GEN_PARM6

# 91: E4_VOICE_FILT_GEN_PARM7

# 92: E4_VOICE_FILT_GEN_PARM8

# 93: E4_VOICE_FENV_SEG0_RATE

# 94: E4_VOICE_FENV_SEG0_TGTLVL

# 95: E4_VOICE_FENV_SEG1_RATE

# 96: E4_VOICE_FENV_SEG1_TGTLVL

# 97: E4_VOICE_FENV_SEG2_RATE

# 98: E4_VOICE_FENV_SEG2_TGTLVL

# 99: E4_VOICE_FENV_SEG3_RATE

# 100: E4_VOICE_FENV_SEG3_TGTLVL

# 101: E4_VOICE_FENV_SEG4_RATE

# 102: E4_VOICE_FENV_SEG4_TGTLVL

# 103: E4_VOICE_FENV_SEG5_RATE

# 104: E4_VOICE_FENV_SEG5_TGTLVL

# LFO Parameters
# (Low-Frequency Oscillator settings for vibrato, tremolo, etc.)

# 105: E4_VOICE_LFO_RATE

# 106: E4_VOICE_LFO_SHAPE

# 107: E4_VOICE_LFO_DELAY

# 108: E4_VOICE_LFO_VAR

# 109: E4_VOICE_LFO_SYNC

# 110: E4_VOICE_LFO2_RATE

# 111: E4_VOICE_LFO2_SHAPE

# 112: E4_VOICE_LFO2_DELAY

# 113: E4_VOICE_LFO2_VAR

# 114: E4_VOICE_LFO2_SYNC

# 115: E4_VOICE_LFO2_OP0_PARM

# 116: E4_VOICE_LFO2_OP1_PARM

# AENV (Amp Envelope) Parameters
# (For shaping the amplifier envelope in multiple segments)

# 117: E4_VOICE_AENV_SEG0_RATE

# 118: E4_VOICE_AENV_SEG0_TGTLVL

# 119: E4_VOICE_AENV_SEG1_RATE

# 120: E4_VOICE_AENV_SEG1_TGTLVL

# 121: E4_VOICE_AENV_SEG2_RATE

# 122: E4_VOICE_AENV_SEG2_TGTLVL

# 123: E4_VOICE_AENV_SEG3_RATE

# 124: E4_VOICE_AENV_SEG3_TGTLVL

# 125: E4_VOICE_AENV_SEG4_RATE

# 126: E4_VOICE_AENV_SEG4_TGTLVL

# 127: E4_VOICE_AENV_SEG5_RATE

# 128: E4_VOICE_AENV_SEG5_TGTLVL

# Cord Parameters
# (These control routing and modulation amounts for various “cords” in the voice)

# 129: E4_VOICE_CORD0_SRC

# 130: E4_VOICE_CORD0_DST

# 131: E4_VOICE_CORD0_AMT

# 132: E4_VOICE_CORD1_SRC

# 133: E4_VOICE_CORD1_DST

# 134: E4_VOICE_CORD1_AMT

# 135: E4_VOICE_CORD2_SRC

# 136: E4_VOICE_CORD2_DST

# 137: E4_VOICE_CORD2_AMT

# 138: E4_VOICE_CORD3_SRC

# 139: E4_VOICE_CORD3_DST

# 140: E4_VOICE_CORD3_AMT

# 141: E4_VOICE_CORD4_SRC

# 142: E4_VOICE_CORD4_DST

# 143: E4_VOICE_CORD4_AMT

# 144: E4_VOICE_CORD5_SRC

# 145: E4_VOICE_CORD5_DST

# 146: E4_VOICE_CORD5_AMT

# 147: E4_VOICE_CORD6_SRC

# 148: E4_VOICE_CORD6_DST

# 149: E4_VOICE_CORD6_AMT

# 150: E4_VOICE_CORD7_SRC

# 151: E4_VOICE_CORD7_DST

# 152: E4_VOICE_CORD7_AMT

# 153: E4_VOICE_CORD8_SRC

# 154: E4_VOICE_CORD8_DST

# 155: E4_VOICE_CORD8_AMT

# 156: E4_VOICE_CORD9_SRC

# 157: E4_VOICE_CORD9_DST

# 158: E4_VOICE_CORD9_AMT

# 159: E4_VOICE_CORD10_SRC

# 160: E4_VOICE_CORD10_DST

# 161: E4_VOICE_CORD10_AMT

# 162: E4_VOICE_CORD11_SRC

# 163: E4_VOICE_CORD11_DST

# 164: E4_VOICE_CORD11_AMT

# 165: E4_VOICE_CORD12_SRC

# 166: E4_VOICE_CORD12_DST

# 167: E4_VOICE_CORD12_AMT

# 168: E4_VOICE_CORD13_SRC

# 169: E4_VOICE_CORD13_DST

# 170: E4_VOICE_CORD13_AMT

# 171: E4_VOICE_CORD14_SRC

# 172: E4_VOICE_CORD14_DST

# 173: E4_VOICE_CORD14_AMT

# 174: E4_VOICE_CORD15_SRC

# 175: E4_VOICE_CORD15_DST

# 176: E4_VOICE_CORD15_AMT

# 177: E4_VOICE_CORD16_SRC

# 178: E4_VOICE_CORD16_DST

# 179: E4_VOICE_CORD16_AMT

# 180: E4_VOICE_CORD17_SRC

# 181: E4_VOICE_CORD17_DST

# 182: E4_VOICE_CORD17_AMT

# Master Setup Tuning & Output, Setup Misc, & Import, etc.
# (These parameters often relate to system‑wide settings. They too are changeable remotely if the device supports editing them.)

# 183: MASTER_TUNING_OFFSET

# 184: MASTER_TRANSPOSE

# 185: MASTER_HEADROOM

# 186: MASTER_HCHIP_BOOST

# 187: MASTER_OUTPUT_FORMAT

# 188: MASTER_OUTPUT_CLOCK

# 189: MASTER_AES_BOOST

# 190: MASTER_SCSI_ID

# 191: MASTER_SCSI_TERM

# 192: MASTER_USING_MAC

# 193: MASTER_COMBINE_LR

# 194: MASTER_AKAI_LOOP_ADJ

# 195: MASTER_AKAI_SAMPLER_ID

# Master MIDI Mode and Controls:

# 198: MIDIGLO_BASIC_CHANNEL

# 199: MIDIGLO_MIDI_MODE

# 201: MIDIGLO_PITCH_CONTROL

# 202: MIDIGLO_MOD_CONTROL

# 203: MIDIGLO_PRESSURE_CONTROL

# 204: MIDIGLO_PEDAL_CONTROL

# 205: MIDIGLO_SWITCH_1_CONTROL

# 206: MIDIGLO_SWITCH_2_CONTROL

# 207: MIDIGLO_THUMB_CONTROL

# 208: MIDIGLO_MIDI_A_CONTROL

# 209: MIDIGLO_MIDI_B_CONTROL

# 210: MIDIGLO_MIDI_C_CONTROL

# 211: MIDIGLO_MIDI_D_CONTROL

# 212: MIDIGLO_MIDI_E_CONTROL

# 213: MIDIGLO_MIDI_F_CONTROL

# 214: MIDIGLO_MIDI_G_CONTROL

# 215: MIDIGLO_MIDI_H_CONTROL

# Master MIDI Preferences:

# 216: MIDIGLO_VEL_CURVE

# 217: MIDIGLO_VOLUME_SENSITIVITY

# 218: MIDIGLO_CTRL7_CURVE

# 219: MIDIGLO_PEDAL_OVERRIDE

# 220: MIDIGLO_RCV_PROGRAM_CHANGE

# 221: MIDIGLO_SEND_PROGRAM_CHANGE

# 222: MIDIGLO_MAGIC_PRESET

# 223: PRESET_SELECT

# 224: LINK_SELECT

# 225: VOICE_SELECT

# 226: SAMPLE_ZONE_SELECT

# 227: GROUP_SELECT

# Master Effects – Section A (Signal processing on presets):

# 228: MASTER_FX_A_ALGORITHM

# 229: MASTER_FX_A_PARM_0

# 230: MASTER_FX_A_PARM_1

# 231: MASTER_FX_A_PARM_2

# 232: MASTER_FX_A_AMT_0

# 233: MASTER_FX_A_AMT_1

# 234: MASTER_FX_A_AMT_2

# 235: MASTER_FX_A_AMT_3

# Master Effects – Section B (Additional effects and multimode settings):

# 236: MASTER_FX_B_ALGORITHM

# 237: MASTER_FX_B_PARM_0

# 238: MASTER_FX_B_PARM_1

# 239: MASTER_FX_B_PARM_2

# 240: MASTER_FX_B_AMT_0

# 241: MASTER_FX_B_AMT_1

# 242: MASTER_FX_B_AMT_2

# 243: MASTER_FX_B_AMT_3

# 244: MASTER_FX_BYPASS

# 245: MASTER_FX_MM_CTRL_CHANNEL

# 246: MULTIMODE_CHANNEL

# 247: MULTIMODE_PRESET

# 248: MULTIMODE_VOLUME

# 249: MULTIMODE_PAN

# 250: MULTIMODE_SUBMIX

# Master Effects / Links:

# 251: E4_LINK_INTERNAL_EXTERNAL

# 252: E4_LINK_FILTER_PITCH

# 253: E4_LINK_FILTER_MOD

# 254: E4_LINK_FILTER_PRESSURE

# 255: E4_LINK_FILTER_PEDAL

# 256: E4_LINK_FILTER_CTRL_A

# 257: E4_LINK_FILTER_CTRL_B

# 258: E4_LINK_FILTER_CTRL_C

# 259: E4_LINK_FILTER_CTRL_D

# 260: E4_LINK_FILTER_CTRL_E

# 261: E4_LINK_FILTER_CTRL_F

# 262: E4_LINK_FILTER_CTRL_G

# 263: E4_LINK_FILTER_CTRL_H

# 264: E4_LINK_FILTER_SWITCH_1

# 265: E4_LINK_FILTER_SWITCH_2

# 266: E4_LINK_FILTER_THUMB

# Master Effects / Ultra Only:

# 267: MASTER_WORD_CLOCK_IN

# 268: MASTER_WORD_CLOCK_PHASE_IN

# 269: MASTER_WORD_CLOCK_PHASE_OUT

# 270: MASTER_OUTPUT_DITHER

# Master Effects / Audition:

# 271: MASTER_AUDITION_KEY






























