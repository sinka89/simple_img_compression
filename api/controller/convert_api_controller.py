import logging

from flasgger import swag_from
from flask import json, Response, request, make_response, Blueprint, abort

from api.service.convert_service import ConvertService
from api.util.allowed_extension_and_mime_enum import AllowedExtension, get_enum_by_extension
from api.util.boolean_parse_exception import parse_boolean, BooleanParseException
from settings import API_IMG_ABSOLUTE_RESIZE, API_IMG_OPTIMIZE, API_IMG_OPTIMIZE_PERCENT, API_IMG_BASE_WIDTH, \
    API_IMG_DEFAULT_EXTENSION

ALLOWED_EXTENSIONS = AllowedExtension.get_supported_extension()

log = logging.getLogger(__name__)

CONVERT_API = Blueprint('blueprint', __name__, url_prefix='/api')


@CONVERT_API.route("/allowed_extensions", methods=['GET'])
@swag_from('/swagger_templates/converter/allowed_extension.yml')
def get_allowed_extension():
    return Response(json.dumps(ALLOWED_EXTENSIONS), mimetype="application/json", status=200)


@CONVERT_API.route('/convert', methods=['POST'])
@swag_from('/swagger_templates/converter/converter.yml')
def convert_img():
    file = None
    if 'file' in request.files:
        file = request.files.get('file')
    extension = API_IMG_DEFAULT_EXTENSION
    base_width = API_IMG_BASE_WIDTH  # for 2 Mpixels converting
    img_opt_percent = API_IMG_OPTIMIZE_PERCENT
    img_optimize = API_IMG_OPTIMIZE
    img_height = None
    img_absolute_resize = API_IMG_ABSOLUTE_RESIZE
    if request.form.__len__() > 0:
        if request.form.get('extension') is not None:
            extension = str(request.form.get('extension'))
        if extension is None or extension not in ALLOWED_EXTENSIONS:
            abort(400, "Extension not supported")
        if request.form.get('base_width') is not None:
            base_width = int(request.form.get('base_width'))
        if request.form.get('opt_percent') is not None:
            img_opt_percent = int(request.form.get('opt_percent'))
            if img_opt_percent not in range(1, 96):
                abort(400, "Image optimization range is between 1 - 95")
        if request.form.get('img_optimize') is not None:
            try:
                img_optimize = parse_boolean(request.form.get('img_optimize'))
            except BooleanParseException as err:
                abort(400, err)
        if request.form.get('img_height') is not None:
            img_height = int(request.form.get('img_height'))
        if request.form.get('abs_resize') is not None:
            try:
                img_absolute_resize = parse_boolean(request.form.get('abs_resize'))
            except BooleanParseException as err:
                abort(400, err)

    if file is not None and extension is not None:
        converted = ConvertService.convert_to_extension(file, ext=extension, bW=base_width, height=img_height,
                                                        opt_percent=img_opt_percent,
                                                        img_opt=img_optimize, absolute_resize=img_absolute_resize)
        response = make_response(converted, 200)
        response.headers['Content-Type'] = get_enum_by_extension(extension).value[1]
        response.headers['Content-Disposition'] = 'attachment; filename=' + str(file.filename).rsplit('.', 1)[
            0] + '.' + extension
        return response
    else:
        abort(400, 'File not present. Please upload a valid file with "file" key')


def get_convert_api_blueprint():
    return CONVERT_API
