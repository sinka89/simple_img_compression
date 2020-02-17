import io
import logging
import os
import tempfile

import imageio
import rawpy
from PIL import Image

from api.util.allowed_extension_and_mime_enum import AllowedExtension
from api.util.converting_exception import ConvertingException

log = logging.getLogger(__name__)


class ConvertService:
    # set supported raw conversion extensions!
    extensionsForRawConversion = ['.dng', '.raw', '.cr2', '.crw', '.erf', '.raf', '.tif', '.kdc', '.dcr', '.mos',
                                  '.mef', '.nef', '.orf', '.rw2', '.pef', '.x3f', '.srw', '.srf', '.sr2', '.arw',
                                  '.mdc',
                                  '.mrw']

    @staticmethod
    def convert_to_extension(file, **kwargs):
        try:
            temp = io.BytesIO()
            temp_file = None
            image = None
            if ConvertService.check_raw_extension(file.filename):
                with rawpy.imread(file) as raw:
                    rgb = raw.postprocess()
                    temp_file = tempfile.NamedTemporaryFile(prefix="temp_img", suffix=".jpeg", delete=False)
                    imageio.imwrite(temp_file.name, rgb)
                    image = Image.open(temp_file)
            else:
                img = file.read()
                image = Image.open(io.BytesIO(img))
            rgb_im = image.convert('RGB')
            rgb_im = ConvertService.resize_img(rgb_im, kwargs.get('bW'), kwargs.get('height'),
                                               kwargs.get('absolute_resize'))
            if kwargs.get('ext') == AllowedExtension.JPEG2000.value[2]:
                rgb_im.save(temp, kwargs.get('ext'), quality_mode='dB', quality_layers=[kwargs.get('opt_percent')])
            else:
                rgb_im.save(temp, kwargs.get('ext'), quality=kwargs.get('opt_percent'), optimize=kwargs.get('img_opt'))
            return temp.getvalue()
        except:
            msg = "Error converting file this could be caused by the fact that the file wasn't a valid image or the " \
                  "server doesn't support the format uploaded "
            log.error(msg, exc_info=True)
            raise ConvertingException(msg)
        finally:
            if temp_file is not None:
                temp_file.close()
                os.unlink(temp_file.name)

    @staticmethod
    def check_raw_extension(extension):
        for i in ConvertService.extensionsForRawConversion:
            if extension.lower().endswith(i):
                return True
            else:
                return False

    @staticmethod
    def resize_img(img, base_width, height, abs_resize):
        # if not absolute resize return img: else convert
        if not abs_resize and base_width > img.size[0] and base_width > img.size[1]:
            return img
        if height is not None:
            return img.resize((int(base_width), int(height)), Image.ANTIALIAS)
        else:
            return img.resize(calculate_new_size_based_on_ration(base_width, img.size[0], img.size[1]),
                              Image.ANTIALIAS)


def calculate_new_size_based_on_ration(width, img_width, img_height):
    if img_width >= img_height:
        w_percent = (width / float(img_width))
        mod_size = int((float(img_height)) * float(w_percent))
        return width, mod_size
    else:
        w_percent = (width / float(img_height))
        mod_size = int((float(img_width)) * float(w_percent))
        return mod_size, width
