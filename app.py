import logging
import logging.config as log_conf

from flasgger import Swagger, LazyJSONEncoder, LazyString
from flask import Flask, jsonify, request
from waitress import serve

from api.controller.convert_api_controller import get_convert_api_blueprint
from api.util.converting_exception import ConvertingException
from settings import *

app = Flask(__name__)
app.config["SWAGGER"] = {"title": "Swagger-UI", "uiversion": 3}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec_1",
            "route": "/apispec_1.json",
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    # "static_folder": "static",  # must be set by user
    "swagger_ui": True,
    "specs_route": "/apidocs/",
}

template = dict(
    swaggerUiPrefix=LazyString(lambda: request.environ.get("HTTP_X_SCRIPT_NAME", ""))
)

app.json_encoder = LazyJSONEncoder
swagger = Swagger(app, config=swagger_config, template=template)


@app.errorhandler(404)
def uri_not_found(e):
    return jsonify(error=str(e)), 404


@app.errorhandler(500)
def internal_server_error(e):
    return jsonify(error=str(e)), 500


@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400


@app.errorhandler(ConvertingException)
def convert_exception(e):
    return jsonify(error=str(e)), 500


def main():
    create_log_dir_if_necessary()
    log_conf.fileConfig(fname='logging.cfg', disable_existing_loggers=False)
    app.register_blueprint(get_convert_api_blueprint())
    logging.info(">>>> Starting api host on {0} with nr. of threads {1}...".format(
        (WAITRESS_HOST + ':' + str(WAITRESS_PORT)), WAITRESS_THREADS))


if __name__ == '__main__':
    main()
    serve(app, host=WAITRESS_HOST, port=WAITRESS_PORT, threads=WAITRESS_THREADS)
