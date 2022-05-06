from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, DateField
from wtforms.validators import DataRequired


class ProfessionalDevForm(FlaskForm):
    date = DateField('Дата прохождения дполнительной подготовки', validators=[DataRequired()])
    description = TextAreaField('Описание дополнительной подготовки', validators=[DataRequired()])
    submit = SubmitField('Далее ->')
