from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.fields.html5 import URLField
from wtforms.validators import InputRequired, DataRequired


class UrlForm(FlaskForm):

    url = URLField('Url', validators=[InputRequired('This field is required!')])
    submit = SubmitField('Short it!')


class ExtendedUrlForm(UrlForm):

    validity = SelectField(
        'Validity',
        validators=[DataRequired()],
        choices=[
            ('1', '1 Day'),
            ('7', '1 Week'),
            ('30', '30 Days'),
            ('365', '1 Year'),
            ('-1', 'Endless'),
        ],
        default='-1'
    )
