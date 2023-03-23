from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import URL


class UrlForm(FlaskForm):
    url = StringField('url', validators=[URL()])
    submit = SubmitField('Sent')
