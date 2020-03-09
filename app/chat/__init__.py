from flask import Blueprint

chat = Blueprint('chat', __name__)

from app.chat import routes, models, events
