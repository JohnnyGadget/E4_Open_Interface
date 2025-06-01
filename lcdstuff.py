import numpy as np

def decode_lcd_payload(data: list[int],
                       pixels: np.ndarray,
                       state: dict):
    """
    Decode one SysEx “LCD dump” packet (full or delta) into `pixels`.
    
    Parameters
    ----------
    data : list[int]
        The 7-bit payload words (c in your JS), e.g. msg.data[6:-1].
    pixels : np.ndarray, dtype=np.uint8
        1D array of length (lcd_w * lcd_h // 8).  This is your `p` buffer.
    state : dict
        Must contain:
          - 'need_full': bool
          - 'lcd_refresh': int
        Will set need_full=False once a delta arrives, and bump lcd_refresh.
    """
    # early exit if this isn’t actually an LCD packet
    if data[0] != 1:
        return

    # JS: const d = c[1]
    session_id = data[1]

    # JS: const e = c[5]<<21 | c[4]<<14 | c[3]<<7 | c[2]
    e = ((data[5] << 21)
         | (data[4] << 14)
         | (data[3] << 7)
         |  data[2])

    # JS: const f = c[7]<<7 | c[6]
    f_len = (data[7] << 7) | data[6]

    # JS: const g = c[9]<<7 | c[8]
    g_len = (data[9] << 7) | data[8]

    # full‐vs‐delta test: JS uses c.length<2205
    full = len(data) < 2205

    # allocate/zero the unpack buffer j[]
    if full:
        j = np.zeros(len(data), dtype=np.uint8)
    else:
        j = np.zeros_like(pixels)
        # in JS: h || (u.need_full = !1)
        state['need_full'] = False

    # unpack each 14-bit word’s bits into j[]
    inp_i, in_bit = 10, 6    # start reading at data[10], bit 6..0
    out_idx, out_bit = 0, 7  # write into j[out_idx] bit 7..0

    while inp_i < len(data) and out_idx < j.size:
        if data[inp_i] & (1 << in_bit):
            j[out_idx] |= (1 << out_bit)

        in_bit -= 1
        if in_bit < 0:
            in_bit = 6
            inp_i += 1

        out_bit -= 1
        if out_bit < 0:
            out_bit = 7
            out_idx += 1

    if not full:
        # run-length “delta” decode back into pixels
        toggle = False
        bptr, cbit = 0, 7
        for count in j[:out_idx]:
            if toggle:
                for _ in range(count):
                    pixels[bptr] ^= (1 << cbit)
                    cbit -= 1
                    if cbit < 0:
                        cbit = 7
                        bptr += 1
            else:
                # skip count bits
                bptr += (count >> 3)
                cbit  -= (count & 7)
                if cbit < 0:
                    bptr += 1
                    cbit += 8

            if count != 255:
                toggle = not toggle

    else:
        # full image → copy j → pixels
        pixels[:] = j[:pixels.size]

    # bump the Angular watch flag (or your equivalent)
    state['lcd_refresh'] += 1




import wx

def draw_lcd(fb: np.ndarray, ctrl: wx.Window):
    """
    fb: output of lcd_link_py (1D uint32 array of length 240*64)
    ctrl: the wx.Panel or similar to draw into
    """
    width, height = 240, 64
    # reinterpret the uint32 array as BGRA bytes (little-endian)
    raw = fb.view(np.uint8).reshape((-1, 4))  # each row is [B, G, R, A]
    img = wx.Image(width, height)
    # copy channels
    buf = img.GetDataBuffer()   # RGB interleaved
    buf[:] = raw[:, [2,1,0]].ravel()  # pick R, G, B
    bmp = img.ConvertToBitmap()
    dc = wx.BufferedPaintDC(ctrl)
    dc.DrawBitmap(bmp, 0, 0)




import numpy as np

def lcd_link_py(pixels: bytes) -> np.ndarray:
    """
    pixels: a byte‐length = 240*64//8 array of 1‐bit rows (row‐major, MSB first).
    returns: a 1-D numpy uint32 array of length 240*64, where each element
             is 0xFF00FF00 (opaque green) if the pixel is “on”, or 0 otherwise.
    """
    # 1) turn your byte array into a flat bit array of 0/1 values
    #    np.unpackbits treats each byte as 8 bits, MSB first by default
    bits = np.unpackbits(np.frombuffer(pixels, dtype=np.uint8))
    # bits.size == (240*64//8)*8 == 240*64

    # 2) reshape into (height, width)
    height, width = 64, 240
    bits = bits.reshape((height, width))

    # 3) allocate our uint32 “framebuffer”
    fb = np.zeros(height * width, dtype=np.uint32)

    # 4) set “on” pixels to the same value your JS used (0xFF00FF00)
    mask = np.uint32(0xFF00FF00)
    fb[bits.ravel() == 1] = mask

    return fb
