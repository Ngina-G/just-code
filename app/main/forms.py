from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, ValidationError
from wtforms.validators import InputRequired, Email
from ..models import User

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [InputRequired()])
    submit = SubmitField('Submit')

class PostForm(FlaskForm):
    title = TextAreaField('Title')
    content = TextAreaField('Write Something')
    submit = SubmitField('SUBMIT')

class CommentForm(FlaskForm):
    opinion = TextAreaField('Comment')
    submit = SubmitField('SUBMIT')

class CategoryForm(FlaskForm):
    name =  StringField('Category Name', validators=[InputRequired()])
    submit = SubmitField('Create')