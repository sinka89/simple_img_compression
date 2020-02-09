# defaults overridden by properties file
import configparser

from api.util.boolean_parse_exception import parse_boolean

config = configparser.RawConfigParser()
config.read('config.properties')
details_dict = dict(config.items('WAITRESS_SERVER'))
WAITRESS_PORT = 5000
WAITRESS_HOST = '0.0.0.0'
WAITRESS_THREADS = 4
if 'waitress_threads' in details_dict:
    WAITRESS_THREADS = int(details_dict.get('waitress_threads'))
if 'waitress_host' in details_dict:
    WAITRESS_HOST = str(details_dict.get('waitress_host'))
if 'waitress_port' in details_dict:
    WAITRESS_PORT = int(details_dict.get('waitress_port'))

img_convert_defaults = dict(config.items('IMAGE_CONVERTING_OPTIONS'))
API_IMG_DEFAULT_EXTENSION = str(img_convert_defaults.get('api_img_default_extension'))
API_IMG_BASE_WIDTH = int(img_convert_defaults.get('api_img_base_width'))  # for 2 Mpixels converting
API_IMG_OPTIMIZE_PERCENT = int(img_convert_defaults.get('api_img_optimize_percent'))
API_IMG_OPTIMIZE = parse_boolean(img_convert_defaults.get('api_img_optimize'))
API_IMG_ABSOLUTE_RESIZE = parse_boolean(img_convert_defaults.get('api_img_absolute_resize'))
