from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

# Create a Flask instance
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
# Add Bootstrap to the Flask app
Bootstrap(app)


class CafeForm(FlaskForm):
    """Create a form object with WTForms."""
    cafe = StringField('Cafe name', validators=[DataRequired()])
    url = StringField('Cafe Location on Google Maps (URL)',
                      validators=[DataRequired(), URL()])
    open = StringField('Opening Time (like 7AM)', validators=[DataRequired()])
    close = StringField('Closing Time (like 8PM)', validators=[DataRequired()])
    coffee = SelectField('Coffee Rating', choices=[
                        ('☕️', '☕️'), ('☕️☕️', '☕️☕️'), ('☕️☕️☕️', '☕️☕️☕️'), ('☕️☕️☕️☕️', '☕️☕️☕️☕️'), ('☕️☕️☕️☕️☕️', '☕️☕️☕️☕️☕️')], validators=[DataRequired()])
    wifi = SelectField('Wifi Strength Rating', choices=[
        ('✘', '✘'), ('💪', '💪'), ('💪💪', '💪💪'), ('💪💪💪', '💪💪💪'), ('💪💪💪💪', '💪💪💪💪'), ('💪💪💪💪💪', '💪💪💪💪💪')], validators=[DataRequired()])
    power = SelectField('Power Socket Availability', choices=[
        ('✘', '✘'), ('🔌', '🔌'), ('🔌🔌', '🔌🔌'), ('🔌🔌🔌', '🔌🔌🔌'), ('🔌🔌🔌🔌', '🔌🔌🔌🔌'), ('🔌🔌🔌🔌🔌', '🔌🔌🔌🔌🔌')], validators=[DataRequired()])
    submit = SubmitField('Submit')


# All Flask routes
@app.route("/", methods=['GET'])
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    # When the form is submitted
    if form.validate_on_submit():
        # Open the CSV database
        with open('cafe-data.csv', mode="a", newline='', encoding="utf8") as csv_file:
            # Write a new row into the CSV file
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow([form.cafe.data, form.url.data, form.open.data,
                            form.close.data, form.coffee.data, form.wifi.data, form.power.data])
            # Show the database
            return redirect(url_for('cafes'))

    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    # Read the data from the CSV file
    with open('cafe-data.csv', newline='', encoding="utf8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
