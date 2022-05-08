from flask_wtf import FlaskForm, Form
from wtforms import PasswordField, StringField, SubmitField, EmailField, \
    RadioField, TextAreaField, IntegerRangeField, SelectMultipleField, \
    FieldList, DateField, FormField
from wtforms import widgets
from wtforms.validators import DataRequired, Optional


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class ProfessionalDevelopmentForm(Form):
    date = DateField('Дата начала подготовки', validators=[Optional()])
    description = StringField('Описание подготовки', validators=[Optional()])
    during = IntegerRangeField('Продолжительность', validators=[Optional()])


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


def init_optional_register_form(_classes=None, _choices=None, state=None):
    class OptionalRegisterForm(FlaskForm):
        if not state:
            work_exp = IntegerRangeField("Опыт работы", validators=[DataRequired()])
            academics = TextAreaField("Место обучения", validators=[DataRequired()])
            dir_of_preparation = TextAreaField("Направление обучения", validators=[DataRequired()])
            subjects = MultiCheckboxField("Предметы, которые вы преподаете:", validators=[Optional()],
                                          choices=_choices)
            prof_devop_list = FieldList(FormField(ProfessionalDevelopmentForm), min_entries=5, max_entries=5,
                                        validators=[Optional()])
        else:
            education_class = RadioField("Ваш класс обучения:", choices=_classes, validators=[DataRequired()])

        submit = SubmitField('Завершить регистрацию')

    return OptionalRegisterForm()
