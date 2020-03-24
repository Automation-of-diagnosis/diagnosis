from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired

choices_srad = [
    ('0', ''),
    ('1', 'АД среднее <70 мм рт.ст.'),
    ('2', 'Допамин <= 5 или любая доза добутамина'),
    ('3', 'Допамин > 5 или адреналин <= 0,1, или норадреналин <= 0,1'),
    ('4', 'Допамин > 15 или адреналин > 0,1, или норадреналин > 0,1'),
]


class LoginForm(FlaskForm):
    ful_name = StringField('Ф.И.О.', render_kw={"class": "form-control"})
    age = IntegerField('Возраст',  render_kw={"class": "form-control"})
    number = IntegerField('Номер больничного листа',  render_kw={"class": "form-control"})
    srad = SelectField('срАД (мм рт.ст.)', choices=choices_srad)
    creatinine = IntegerField('Креатинин (ммоль/л)',  render_kw={"class": "form-control"})
    platelets = IntegerField('Тромбоциты (10*9/л)',  render_kw={"class": "form-control"})
    bilirubin = IntegerField('Билирубин (ммоль/л)', render_kw={"class": "form-control"})
    pao2_fio2 = IntegerField('PaO2/FiO2 (мм рт.ст.)',  render_kw={"class": "form-control"})
    gsc = IntegerField('GSC', render_kw={"class": "form-control"})
    submit = SubmitField('Отправить', render_kw={"class": "btn btn-primary"})
# validators=[DataRequired()],