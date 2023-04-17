__version__ = '1.0.0'
from flask import (Flask, request, render_template)
from werkzeug.middleware.proxy_fix import ProxyFix
from .get_gds_area import get_gds_area


def create_app():
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1,
                            x_proto=1, x_host=1, x_prefix=1)
    # max file size is 16MB
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    @app.route("/", methods=("POST", "GET"))
    def index():
        if request.method == "GET":
            return render_template("index.html", areas=None)

        if request.files["gds_file"].filename == "":
            return "No file selected"
        if not request.files["gds_file"].filename.endswith(".gds"):
            return "File extension must be .gds"

        if request.form["top_cell_name"] == "":
            top_cell_name = None
        else:
            top_cell_name = request.form["top_cell_name"]

        areas, err = get_gds_area(request.files["gds_file"], top_cell_name)

        return render_template("index.html", areas=areas)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(port=8000, debug=True)
