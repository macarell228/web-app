from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, RadioField, TextAreaField, IntegerRangeField
from wtforms.validators import DataRequired


def init_register_form(_roles, _classes):
    class RegisterForm(FlaskForm):
        email = EmailField('Почта', validators=[DataRequired()])
        password = PasswordField('Пароль', validators=[DataRequired()])
        password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
        surname = StringField('Фамилия', validators=[DataRequired()])
        name = StringField('Имя', validators=[DataRequired()])
        patronymic = StringField('Отчество')
        status = RadioField("Ваша роль в школе:", choices=_roles)

        # for students
        education_class = RadioField("Ваш класс обучения:", choices=_classes)

        # for teachers
        work_exp = IntegerRangeField("Опыт работы", validators=[DataRequired()])
        academics = TextAreaField("Место обучения", validators=[DataRequired()])
        dir_of_preparation = TextAreaField("Направление обучения", validators=[DataRequired()])

        submit = SubmitField('Далее ->')

    return RegisterForm()
