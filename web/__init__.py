import logging

print "init webapp"

from flask import Flask, request as req

print "import views"

from web.controller import simple_page_blueprint
print "import views"
from web.controller import views
print "import views"


def create_app():
    print "create app"
    app = Flask(__name__)
    app.register_blueprint(simple_page_blueprint)

    app.logger.setLevel(logging.NOTSET)

    @app.after_request
    def log_response(resp):
        app.logger.info("{} {} {}\n{}".format(
            req.method, req.url, req.data, resp)
        )
        return resp

    return app