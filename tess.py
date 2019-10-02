import pytesseract
from pyocr import builders
from pyocr import pyocr
from PIL import Image

def getText(img):
        #text = pytesseract.image_to_string(img, lang="letsgodigital",config='outputbase digits')
        text = pytesseract.image_to_string(img, lang='letsgodigital',config='--oem 2 --psm 10 -c tessedit_char_whitelist=0123456789' )
        #text = pytesseract.image_to_string(img, lang="letsgodigital", config='--oem 1 --psm 3')
        #os.remove(imgPath)
        return text
"""
        tool = pyocr.get_available_tools()[0] # 
        lang = 'letsgodigital'
        text= tool.image_to_string(Image.fromarray(img), lang=lang, builder=builders.TextBuilder())
        return text      
"""

"""
      "Page segmentation modes:\n"
        "  0    Orientation and script detection (OSD) only.\n"
        "  1    Automatic page segmentation with OSD.\n"
        "  2    Automatic page segmentation, but no OSD, or OCR.\n"
        "  3    Fully automatic page segmentation, but no OSD. (Default)\n"
        "  4    Assume a single column of text of variable sizes.\n"
        "  5    Assume a single uniform block of vertically aligned text.\n"
        "  6    Assume a single uniform block of text.\n"
        "  7    Treat the image as a single text line.\n"
        "  8    Treat the image as a single word.\n"
        "  9    Treat the image as a single word in a circle.\n"
        " 10    Treat the image as a single character.\n"
"""