import qrcode, os
from PIL import Image, ImageDraw

def add_corners(im, rad):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im


def qrimg(data, title):
    logo = Image.open('assets/logo_qrcode.png')
    wpercent = (200/float(logo.size[0]))
    hsize = int((float(logo.size[1])*float(wpercent)))
    logo = logo.resize((200,hsize), Image.ANTIALIAS)
    qr_big = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr_big.add_data(data)
    qr_big.make()
    img_qr_big = qr_big.make_image(fill_color='#182533', back_color="#c1cdca").convert('RGB')
    pos = ((img_qr_big.size[0] - logo.size[0]) // 2, (img_qr_big.size[1] - logo.size[1]) // 2)
    img_qr_big.paste(logo, pos, mask=logo)
    im = add_corners(img_qr_big, 15)
    img2 = im
    img = img2.resize((600,600), Image.ANTIALIAS)
    img_w, img_h = img.size
    background = Image.open('assets/template.png', 'r')
    bg_w, bg_h = background.size
    offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
    background.paste(img, offset, mask=img)
    background.save(f'temp/{title}.png')


def remove(title):
    try:
        os.remove(f'temp/{title}.png')

    except:
        pass


