import framebuf

def draw_icon(oled_display_obj: framebuf.FrameBuffer, icon_bytes: bytes, position_x: int, position_y: int, show: bool = False):
    width = int.from_bytes(icon_bytes[:2], 'big')
    height = int.from_bytes(icon_bytes[2:4], 'big')

    y = 0
    x = 0
    for m_byte in icon_bytes[4:]:
        for byte_index in range(8):
            pixel_value = m_byte & (1 << byte_index)
            oled_display_obj.pixel(position_x + x, position_y + y, pixel_value)

            x = x + 1

            if x >= width:
                x = 0
                y = y + 1

            if y >= height:
                if show:
                    oled_display_obj.show()
                return
