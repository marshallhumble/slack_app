from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, FormField
from wtforms.validators import Required, Length

app = Flask(__name__)
app.config['SECRET_KEY'] = 'top secret!'
bootstrap = Bootstrap(app)


class NameForm(Form):
    user = StringField('What is your username?', validators=[Required(), Length(1, 32)])
    domain = StringField('What is your team name?', validators=[Required(), Length(1, 16)])
    token = StringField('What is you API token?', validators=[Required(), Length(1, 40)])
    time = FormField('Enter in the # of days to limit (not required)', widget=NumberInput())

    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    token = None
    domain = None
    user = None
    time = None

    form = NameForm()
    if form.validate_on_submit():
        token = form.token.data
        form.token.data = ''
        domain = form.domain.data
        form.domain.data = ''
        user = form.user.data
        form.user.data = ''
        time = form.time.data
        form.time.data = ''
    return render_template('index.html', form=form, token=token, domain=domain, user=user, time=time)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
