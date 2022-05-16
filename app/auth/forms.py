from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField, BooleanField
from wtforms.validators import InputRequired,Email,EqualTo,Length
from ..models import User
from wtforms import ValidationError