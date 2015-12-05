from flask import Flask, render_template, request

# App Specific
import requests
import calendar
from datetime import datetime, timedelta


app = Flask(__name__)
app.config['SECRET_KEY'] = 'top secret!'


def delete_my_files(token, domain, user, time):
    deleted_list = []
    while 1:
        files_list_url = 'https://slack.com/api/files.list'
        date = str(calendar.timegm((datetime.now() + timedelta(-time)).utctimetuple()))
        data = {"token": token, "ts_to": date, "user": user}
        response = requests.post(files_list_url, data=data)
        if len(response.json()["files"]) == 0:
            break
        for f in response.json()["files"]:
            deleted_list.append( f["name"])
            timestamp = str(calendar.timegm(datetime.now().utctimetuple()))
            delete_url = "https://" + domain + ".slack.com/api/files.delete?t=" + timestamp
            requests.post(delete_url, data={
                "token": token,
                "file": f["id"],
                "set_active": "true",
                "_attempts": "1"})
    return deleted_list

"""
class NameForm(Form):
    user = StringField('What is your username?', validators=[Required(), Length(1, 32)])
    domain = StringField('What is your team name?', validators=[Required(), Length(1, 16)])
    token = StringField('What is you API token?', validators=[Required(), Length(1, 40)])
    time = StringField('Enter in the # of days to limit (not required)', validators=[Length(1, 3)])
    submit = SubmitField('Submit')
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    token = request.values.get('token')
    domain = request.values.get('domain')
    user = request.values.get('user')
    time = request.values.get('time')
    if delete_my_files(token, domain, user, time):
        return render_template('result.html', token=token, domain=domain, user=user, time=time)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
