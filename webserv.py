from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, PasswordField
from collections import OrderedDict
import json

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

with open('json/config.json') as json_data_file:
    data = json.load(json_data_file)
    json_data_file.close()
with open('json/restart.json') as json_data_file:
    restart = json.load(json_data_file)
    json_data_file.close()

class settings(Form):
    ID = {}
    ID['serial'] = TextField("data['id']['serial']", validators=[validators.required()])
    ID['name'] = TextField("data['id']['name']", validators=[validators.required()])
    ID['wint'] = TextField("data['id']['wint']", validators=[validators.required()])
    ID['wssid'] = PasswordField("data['id']['wssid']", validators=[validators.required()])
    ID['wpass'] = TextField("data['id']['wpass']", validators=[validators.required()])
    ID['pollRate'] = TextField("data['id']['pollRate']", validators=[validators.required()])
    ID['user'] = TextField("data['influx']['user']", validators=[validators.required()])
    ID['passwd'] = PasswordField("data['influx']['passwd']", validators=[validators.required()])
    ID['host'] = TextField("data['influx']['host']", validators=[validators.required()])
    influx = {}
    influx['port'] = TextField("data['influx']['port']", validators=[validators.required()])
    influx['db'] = TextField("data['influx']['db']", validators=[validators.required()])
    influx['retentionActive'] = TextField("data['influx']['retentionActive']", validators=[validators.required()])
    influx['retentionName'] = TextField("data['influx']['retentionName']", validators=[validators.required()])
    influx['retentionDuration'] = TextField("data['influx']['retentionDuration']", validators=[validators.required()])
    influx['retentionReplication'] = TextField("data['influx']['retentionReplication']", validators=[validators.required()])

#Rewrite old conf
def writeConf():
    sortedID = OrderedDict([('serial',data['id']['serial']),
                            ('name',data['id']['name']),
                            ('wint',data['id']['wint']),
                            ('wssid',data['id']['wssid']),
                            ('wpass',data['id']['wpass']),
                            ('pollRate',data['id']['pollRate'])])
    sortedInflux = OrderedDict([('user',data['influx']['user']),
                                ('passwd',data['influx']['passwd']),
                                ('host',data['influx']['host']),
                                ('port',data['influx']['port']),
                                ('db',data['influx']['db']),
                                ('retentionActive',data['influx']['retentionActive']),
                                ('retentionName',data['influx']['retentionName']),
                                ('retentionDuration',data['influx']['retentionDuration']),
                                ('retentionReplication',data['influx']['retentionReplication'])])
    data['id'] = sortedID
    data['influx'] = sortedInflux
    outfile = open('json/config.json', "w")
    outfile.write(json.dumps(data, indent=4, sort_keys=False))
    outfile.close()
    restart['isRestart'] = "True"
    outrst = open('json/restart.json', "w")
    outrst.write(json.dumps(restart))
    outrst.close()

@app.route("/", methods=['GET', 'POST'])
def index():
    form = settings(request.form)
    print form.errors
    if request.method == 'POST':
        data['id']['serial'] = request.form["data['id']['serial']"]
        data['id']['name'] = request.form["data['id']['name']"]
        data['id']['wint'] = request.form["data['id']['wint']"]
        data['id']['wssid'] = request.form["data['id']['wssid']"]
        data['id']['wpass'] = request.form["data['id']['wpass']"]
        data['id']['pollRate'] = request.form["data['id']['pollRate']"]
        data['influx']['user'] = request.form["data['influx']['user']"]
        data['influx']['passwd'] = request.form["data['influx']['passwd']"]
        data['influx']['host'] = request.form["data['influx']['host']"]
        data['influx']['port'] = request.form["data['influx']['port']"]
        data['influx']['db'] = request.form["data['influx']['db']"]
        data['influx']['retentionActive'] = request.form["data['influx']['retentionActive']"]
        data['influx']['retentionName'] = request.form["data['influx']['retentionName']"]
        data['influx']['retentionDuration'] = request.form["data['influx']['retentionDuration']"]
        data['influx']['retentionReplication'] = request.form["data['influx']['retentionReplication']"]
        if form.validate():
            flash(' Configuration Saved')
            writeConf()
        else:
            flash(' Error: All Fields are Required to be Filled')
    return render_template('index.html', form=form, data=data)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=2048, debug=True)
