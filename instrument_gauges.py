from PIL import ImageTk, Image, ImageFont, ImageDraw
import math
import PIL

def rotery_gauge(low,high,val):

    rotation_angle = val/(high-low)*(360-90)+45
    corrected_angle = -(rotation_angle-180)

    gauge_bg = Image.open("images/gauge_bg5.png")
    g_width, g_height = gauge_bg.size

    font = ImageFont.truetype("images/font/arial.ttf", size=45);
    ImageDraw.Draw(gauge_bg).text((g_width//2-50, g_height//2-100), text = "PSI", fill=(0, 0, 0), font=font)
    ImageDraw.Draw(gauge_bg).text((g_width//2-200, g_height-200), text = str(low), fill=(0, 0, 0), font=font)
    ImageDraw.Draw(gauge_bg).text((g_width//2-75, 90), text = str((high+low)//2), fill=(0, 0, 0), font=font)
    ImageDraw.Draw(gauge_bg).text((g_width//2+75, g_height-200), text = str(high), fill=(0, 0, 0), font=font)


    gauge_ind = Image.open("images/gauge-indicator.png")
    gauge_ind = gauge_ind.rotate(corrected_angle, PIL.Image.Resampling.NEAREST, expand = 1)
    ind_width, ind_height = gauge_ind.size
    # print(g_width)
    # print(ind_width)
    gauge = gauge_bg

    area = (ind_width//2-g_width//2, ind_height//2-g_height//2, ind_width//2+g_width//2, ind_height//2+g_height//2)
    gauge_ind = gauge_ind.crop(area)

    gauge.paste(gauge_ind, (0, 0), mask=gauge_ind)

    return gauge
