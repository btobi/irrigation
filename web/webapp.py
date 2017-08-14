from . import create_app

app = create_app()


def run():
    app.run(host='0.0.0.0', port=5500, debug=True)