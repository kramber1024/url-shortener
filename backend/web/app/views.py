from flask import Blueprint, render_template

from app.config import settings

blueprint: Blueprint = Blueprint(
    "app",
    __name__,
    url_prefix=None,
    static_folder="/static",
    static_url_path="/static",
    template_folder="/templates",
)


@blueprint.route("/", methods=["GET"])
def index() -> tuple[str, int]:
    return "ushort", 200


@blueprint.route("/login", methods=["GET"])
def login() -> tuple[str, int]:
    return render_template(
        "signin.html",
        brand_name=settings.app.NAME,
    ), 200
