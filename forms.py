from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    ful_name = StringField('Ф.И.О.', validators=[DataRequired()], render_kw={"class": "form-control"})
    age = IntegerField('Возраст', validators=[DataRequired()], render_kw={"class": "form-control"})
    number = IntegerField('Номер больничного листа', validators=[DataRequired()], render_kw={"class": "form-control"})
    # 'srAD': '4',
    # 'creatinine': '150',
    # 'bilirubin': '16',
    # 'platelets': '25',
    # 'PaO2/FiO2': '150',
    # 'gsc': '3',

    submit = SubmitField('Отправить', render_kw={"class": "btn btn-primary"})
