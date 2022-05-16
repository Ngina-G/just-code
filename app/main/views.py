from flask import render_template, redirect,url_for, abort
from flask_login import login_required, current_user
from . import main
from .. import db,photos
from ..models import User, PhotoProfile