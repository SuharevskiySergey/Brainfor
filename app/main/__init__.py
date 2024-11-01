from flask import Blueprint

bp = Blueprint('main', __name__)


from app.main import routes
from app.main.admin_panel import admin_routes
from app.main.teacher_panel import teacher_routes



