from flask import render_template, redirect, request, jsonify, flash, session, url_for, Response
from app.app import app
from app.forms.forms import AudienceForm, CsvSubmit
from app.modules.view_functions import *
import requests
import json
import os
import datetime
import sys

@app.template_filter('autoversion')
def autoversion_filter(filename):
  # determining fullpath might be project specific
  fullpath = os.path.join('some_app/', filename[1:])
  timestamp = datetime.datetime.now()
  newfilename = "{0}?v={1}".format(filename, timestamp)
  return newfilename

@app.route('/audiences', methods=['GET','POST'])
def audiences():
    form = AudienceForm()
    validate = True
    scroll = "title"
    if form.addVariable.data:
        scroll = "variable_form-%s" %(str(len(form.variable_form.entries)))
        form.variable_form.append_entry()
        validate = False
    for i,variable in enumerate(form.variable_form.entries):
        if variable.removeVariable.data:
            form.variable_form.entries.pop(i)
            if i > 0:
                scroll = "variable_form-%s" %(str(i-1))
            else:
                scroll = "market"
            validate = False
    if form.addTrimCorrection.data:
        scroll = "trim_correction_form-%s" %(str(len(form.trim_correction_form.entries)))
        form.trim_correction_form.append_entry()
        validate = False
    for i,variable in enumerate(form.trim_correction_form.entries):
        if variable.removeCorrection.data:
            form.trim_correction_form.entries.pop(i)
            if i > 0:
                scroll = "trim_correction_form-%s" %(str(i-1))
            else:
                scroll = "market"
            validate = False
    if form.submitAdvertiserData.data:
        validate = False
    if form.addActivitySelection.data:
        scroll = "activity_selection_form-%s" %(str(len(form.activity_selection_form.entries)))
        form.activity_selection_form.append_entry()
        validate = False
    for i,activity in enumerate(form.activity_selection_form.entries):
        if activity.removeActivity.data:
            form.activity_selection_form.entries.pop(i)
            if i > 0:
                scroll = "activity_selection_form-%s" %(str(i-1))
            else:
                scroll = "submitAdvertiserData"
            validate=False
    floodlights = get_floodlights(form)
    variableSelections = get_variables(form)
    floodlightSelections = get_selections(floodlights)
    if len(form.variable_form.entries) > 0:
        for item in form.activity_selection_form.entries:
            item.floodlights.choices = floodlightSelections
            item.variables.choices = variableSelections
    if validate:
        scroll = "activity_selection_form"
        if form.validate_on_submit():
            try:
                flDf = pd.DataFrame.from_dict(json.loads(floodlights))
                df = generate_audiences(form, flDf)
                name = "%s_%s_audiences.csv" %(form.advertiser.data,form.market.data)
                data = df.to_json(orient='records')
                profileId = lookup_market_profile(form.market.data, form.advertiser.data)
                audiences = {
                    "name": name,
                    "data": data,
                    "profileId": profileId
                }
                session['audiences'] = audiences
                return redirect(url_for('finish'))

            except Exception as e:
                print(e)
                print(sys.exc_info()[0])
                flash("Something went wrong. Try again")
        else:
            flash_errors(form)
    return render_template('create.jade', form=form, scroll=scroll)

@app.route('/audiences/finish', methods=['GET','POST'])
def finish():
    form = CsvSubmit()
    tableData = session.get('audiences',None)
    data = json.loads(tableData['data'])
    table = []
    status = []
    for item in data:
        table.append({'name': item['name'], 'rules': item['Rules']})
    if form.save_to_csv.data:
        df = pd.DataFrame.from_dict(data)
        df = df[['id','advertiserId','name','floodlightActivityId','Rules']]
        return Response(
            df.to_csv(index=False),
            mimetype="text/csv",
            headers={"Content-disposition":
                     "attachment; filename=%s" %(tableData['name'])})
    elif form.submit_to_dcm.data:
        for item in data:
            response = create_audience(item,tableData['profileId'])
            status.append({'name': item['name'], 'rules': item['Rules'], 'status': response})
        session['dcmStatus'] = status
        return redirect(url_for('dcm'))
    return render_template('finish.jade',
                           title="Finish Test",
                           table= table,
                           form = form)

@app.route('/audiences/finish/dcm', methods=['GET'])
def dcm():
    table = session.get('dcmStatus', None)
    return render_template('dcm.jade', table=table)
