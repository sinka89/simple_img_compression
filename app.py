import logging
import logging.config as log_conf

from flask import Flask, jsonify
from waitress import serve

from api.controller.convert_api_controller import get_convert_api_blueprint
from api.util.converting_exception import ConvertingException
from settings import *

app = Flask(__name__)

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
