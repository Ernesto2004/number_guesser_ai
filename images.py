from PIL import Image, ImageChops
from os import scandir

def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
    else:
        return im

def match(data_img, scan_img):
    im1 = Image.open(data_img)
    im2 = trim(Image.open(scan_img)).resize(im1.size)

    im1_data = im1.load()
    im2_data = im2.load()
    
    pixel_match = 0
    black_pixels = 0
    if im1.size == im2.size:
        for x in range(im1.size[0]):
            for y in range(im1.size[1]):
                px1 = im1_data[x,y]
                px2 = im2_data[x,y]
                if px1 == px2 and (px1 and px2 == (0,0,0)):
                    pixel_match += 1
                if px1 == (0,0,0):
                    black_pixels += 1
    
    percentage = str((pixel_match/black_pixels)*100)[:4] + "%"
    return percentage

def create_reference_image():
    name = f"num{len([1 for x in list(scandir(dir)) if x.is_file()])}.png"
    img = trim(Image.open("board.png"))
    img.save("numbers/"+name)

def guess(board_img):
    results = [(num, match(f"numbers/num{num}.png", board_img)) for num in range(1, 4)]
    return results
