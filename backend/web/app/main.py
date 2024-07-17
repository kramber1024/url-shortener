from flask import Flask

from app.config import settings
from app.views import blueprint

app: Flask = Flask(__name__)
app.register_blueprint(blueprint)

if __name__ == "__main__":
    app.run(
        host=settings.debug.DEBUG_HOST,
        port=settings.debug.DEBUG_PORT,
    )
