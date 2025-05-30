
import mido
from mido import Message
import queue
import threading
import time

_midi_out = None
_midi_in  = None
in_name = 'UMC1820 MIDI In 0'
out_name = 'UMC1820 MIDI Out 1'


_sysex_queue = queue.Queue()
_sysex_send_delay = 0.02  # delay in seconds between messages (e.g. 50 ms)

def init_midi_out(port_name: str = None):
    global _midi_out
    _midi_out = mido.open_output(port_name or mido.get_output_names()[0])
    threading.Thread(target=_process_sysex_queue, daemon=True).start()
    return _midi_out

def init_midi_in(callback, port_name):
    global _midi_in
    _midi_in = mido.open_input(port_name, callback=callback)
    return _midi_in

def send_sysex(data):
    if _midi_out is None:
        raise RuntimeError("MIDI out not initialized")
    print(data)
    msg = Message('sysex', data=data)
    print("Queued SysEx:", msg)
    _sysex_queue.put(msg)

def _process_sysex_queue():
    while True:
        try:
            msg = _sysex_queue.get(timeout=0.1)
            _midi_out.send(msg)
            print("Sent SysEx:", msg)
            time.sleep(_sysex_send_delay)
        except queue.Empty:
            continue
        
def send_midi_message(msg):
    print("send_midi_message", msg)
    print(msg)
    if _midi_out is None:
        raise RuntimeError("MIDI out not initialized")
    _midi_out.send(msg)

    

