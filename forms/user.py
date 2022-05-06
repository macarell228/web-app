from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, \
    RadioField, TextAreaField, IntegerRangeField, SelectMultipleField
from wtforms import widgets
from wtforms.validators import DataRequired, Optional


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


def init_register_form(_roles):
    class RegisterForm(FlaskForm):
        email = EmailField('Почта', validators=[DataRequired()])
        password = PasswordField('Пароль', validators=[DataRequired()])
        password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
        surname = StringField('Фамилия', validators=[DataRequired()])
        name = StringField('Имя', validators=[DataRequired()])
        patronymic = StringField('Отчество', validators=[Optional()], default='')
        status = RadioField("Ваша роль в школе:", choices=_roles)

        submit = SubmitField('Завершить/Далее ->')

    return RegisterForm()


def init_optional_register_form(_classes=None, _choices=None):
    class OptionalRegisterForm(FlaskForm):
        if _choices:
            work_exp = IntegerRangeField("Опыт работы", validators=[DataRequired()])
            academics = TextAreaField("Место обучения", validators=[DataRequired()])
            dir_of_preparation = TextAreaField("Направление обучения", validators=[DataRequired()])
            subjects = MultiCheckboxField("Предметы, которые вы преподаете:", validators=[DataRequired()],
                                          choices=_choices)
        elif _classes:
            education_class = RadioField("Ваш класс обучения:", choices=_classes)

        submit = SubmitField('Завершить регистрацию')

    return OptionalRegisterForm()
