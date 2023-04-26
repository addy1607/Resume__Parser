import fitz
import logging
from pdf2image import convert_from_path
import os
import pytesseract
from PIL import Image

def convert_pdf_to_image(pdf_file):
    """load the Pdf document 
            # apply pdf2image
            save the image in ImageOutputs/{name} folder 
            rtype: Boolean
    """

    try:
        logging.debug(f'Processing File using tesseract')
        images = convert_from_path(pdf_file)
        
        try:
            newpath=os.path.join('ImageOUTPUTS',pdf_file.split('/')[-1].split('.')[0])
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            else:
                return True
        
        except OSError as e:
            logging.error("error in tesseract extraction")
            return False
    
        
        newpath=os.path.join('ImageOUTPUTS',pdf_file.split('/')[-1].split('.')[0])
        whole_text=""
        for i in range(len(images)):
            images[i].save(newpath + '/'  + '_page_' + str(i) + '.jpg', 'JPEG')
            image_file=newpath + '/'  + '_page_' + str(i) + '.jpg'
            text = str(((pytesseract.image_to_string(Image.open(image_file)))))
            whole_text=whole_text+" "+text
        return whole_text
    except Exception as e:
        logging.error("Entered except with error in convert_pdf_to_image func: {}".format(e), exc_info=True)
        return False
    



async def get_text_resume(path):
    try:
        logging.debug(f'Processing File using pymupdf:  {path}')
        text = ''
        doc=fitz.open(path) 
        for page in doc:
                text+= page.get_text()
        if text:
           return text
        else:
            text=convert_pdf_to_image(path)
            return text
    except Exception as e:
        logging.error(f'Processing file does not support by pymupdf:  {path}')
        text=convert_pdf_to_image(path)
        return text
