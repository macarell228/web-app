from flask_wtf import FlaskForm

from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Optional

from .checkbox import MultiCheckboxField


def init_news_form(_choices):
    class NewsForm(FlaskForm):
        title = StringField('Заголовок', validators=[DataRequired()])
        content = TextAreaField("Содержание")
        seem_for = MultiCheckboxField("Кому будет видна эта новость:", validators=[Optional()],
                                      choices=_choices)
        submit = SubmitField('Применить')

    return NewsForm()
