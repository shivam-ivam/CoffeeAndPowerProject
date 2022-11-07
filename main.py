from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import pandas

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Cafe Location on Google map', validators=[DataRequired(), URL()])
    open = StringField('Opening Time eg.8AM', validators=[DataRequired()])
    close = StringField('Closing Time eg.10pM', validators=[DataRequired()])
    wifi = SelectField(label='Wifi Strength Rating', choices=('✘', '💪', '💪💪', '💪💪💪', '💪💪💪💪', '💪💪💪💪💪'), validators=[DataRequired()])
    rating = SelectField(label='Coffee Rating', choices=('✘', '☕', '☕☕', '☕☕☕', '☕☕☕☕', '☕☕☕☕☕'), validators=[DataRequired()])
    power = SelectField(label='Power Socket Availability', choices=('✘', '🔌', '🔌🔌', '🔌🔌🔌', '🔌🔌🔌🔌', '🔌🔌🔌🔌🔌'), validators=[DataRequired()])
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("True")
        cafe = form.cafe.data
        location = form.location.data
        open_time = form.open.data
        close_time = form.close.data
        wifi = form.wifi.data
        power = form.power.data
        coffee_rating = form.rating.data
        new_row_data = f'{cafe},{location},{open_time},{close_time},{coffee_rating},{wifi},{power}'
        print(new_row_data)
        with open('cafe-data.csv', mode='a', encoding="utf-8") as file:
            file.write(f'\n{new_row_data}')

    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    csv_data = pandas.read_csv('cafe-data.csv')
    length = len(csv_data)
    return render_template('cafes.html', cafes=csv_data, length=length)


if __name__ == '__main__':
    app.run(debug=True)

