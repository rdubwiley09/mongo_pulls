from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SelectMultipleField, SubmitField, FieldList, FormField, TextField, TextAreaField, BooleanField, widgets
from wtforms.validators import DataRequired, InputRequired
from app.forms.forms_selections import advertisers, markets, devices, kpis, kpis_plus, u_variables, uvars_plus, logical

class VariableForm(FlaskForm):
    variable = SelectField(u'Variable', choices=uvars_plus, validators = [InputRequired("Please select a variable")])
    values = TextAreaField(u'Values')
    generateFromFloodlightData = BooleanField('Generate from data?')
    applyToAll = BooleanField('Apply to all?')
    logicalOperator = SelectField(u'Logic', choices = logical, validators = [InputRequired("Please select a logical operator")])
    removeVariable = SubmitField('Remove Variable')

class TrimCorrectionForm(FlaskForm):
    trim = StringField(u'Trim', validators = [InputRequired("Please enter a trim to correct")])
    corrections = TextAreaField(u'Trim Corrections')
    removeCorrection = SubmitField('Remove Correction')

class ActivitySelectionForm(FlaskForm):
    floodlights = SelectMultipleField('Floodlights', choices=[('None','None')], validators = [InputRequired("Please select a logical operator")])
    variables = SelectMultipleField('User Variables',choices=[('None','None')])
    removeActivity = SubmitField('Remove Activity')

class AudienceForm(FlaskForm):
    advertiser = SelectField(u'Advertiser', choices=advertisers, validators = [InputRequired("Please select an advertiser")])
    market = SelectField(u'Market', choices=markets, validators = [DataRequired("Please select a market")])
    variable_form = FieldList(FormField(VariableForm))
    addVariable = SubmitField('Add Variable')
    trim_correction_form = FieldList(FormField(TrimCorrectionForm))
    addTrimCorrection = SubmitField('Add Trim Correction')
    submitAdvertiserData = SubmitField('Submit Advertiser Data')
    activity_selection_form = FieldList(FormField(ActivitySelectionForm))
    addActivitySelection = SubmitField('Add Activity Selection')
    submit = SubmitField('Submit')

class CsvSubmit(FlaskForm):
    save_to_csv = SubmitField('Save to CSV')
    submit_to_dcm = SubmitField('Submit to DCM')
