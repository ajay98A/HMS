from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,IntegerField,SelectField,TextField,DateField,FloatField
from wtforms.validators import DataRequired,Email,EqualTo,Optional
from wtforms import ValidationError
from project.models import User,Patient

class LoginForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired(),EqualTo('confirm_pass',message="Passwords Donot match!")])
    confirm_pass = PasswordField('Confirm Password',validators=[DataRequired()])
    role = SelectField('Role',choices=[('staff', 'Registration/Admision Desk'), ('pharma', 'Pharmacist'), ('diag', 'Diagnostic services executive')],validators=[DataRequired()])
    submit = SubmitField('Register')

    def check_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username exists!')
class AddPatient(FlaskForm):
    ssn_id = IntegerField('ssn id',validators=[DataRequired()])
    name = StringField('Patient Name',validators=[DataRequired()])
    age = StringField('Age',validators=[DataRequired()])
    Address = TextField('Address',validators=[DataRequired()])
    bed_type = SelectField('Bed Types', choices=[('General ward', 'General ward'), ('semi sharing', 'semi sharing'),('single room','single room') ])
    date = DateField('Date(yyyy-mm-dd)',validators=[DataRequired()])
    city = StringField('City',validators=[DataRequired()])
    state = StringField('State',validators=[DataRequired()])
    status = SelectField('Status', choices=[('Active','Active'), ('Discharged','Discharged') ])
    submit = SubmitField('Add Patient')

    def check_patient(self,field):
        if Patient.query.filter_by(ssn_id=field.data).first():
            raise ValidationError('Patient exists!')
class SearchForm(FlaskForm):
    pid = IntegerField('Patient Id',validators=[DataRequired()])
    name = StringField('Patient Name',validators=[Optional()])
    age = IntegerField('Age',validators=[Optional()])
    submit = SubmitField('Search',validators=[Optional()])

class DeletePatient(FlaskForm):
    pid = IntegerField('Patient Id',validators=[DataRequired()])
    name = StringField('Patient Name',validators=[Optional()])
    age = IntegerField('Age',validators=[Optional()])
    submit = SubmitField('Search',validators=[Optional()])

class UpdateForm(FlaskForm):
    pid = IntegerField('Patient Id',validators=[DataRequired()])
    name = StringField('Patient Name',validators=[Optional()])
    age = StringField('Age',validators=[Optional()])
    Address = TextField('Address',validators=[Optional()])
    city = StringField('City',validators=[Optional()])
    state = StringField('State',validators=[Optional()])
    submit = SubmitField('Update Patient')

class MedicineForm(FlaskForm):
    mid = IntegerField('Medicine Id',validators=[DataRequired()])
    mname = StringField('Medicine Name',validators=[DataRequired()])
    qavailable = IntegerField('Quantity',validators=[DataRequired()])
    rate = FloatField('Price',validators=[DataRequired()])
    submit = SubmitField('Register')

class medicineissue(FlaskForm):
    name = StringField("Medicine Name",validators=[Optional()])
    qissued = StringField("Quantity",validators=[Optional()])
    submit = SubmitField('Issue')

class billingForm(FlaskForm):
    id = IntegerField("patient Id",validators=[DataRequired()])
    submit = SubmitField('Get Bill')
class AddDiagForm(FlaskForm):
    tid = IntegerField("Diagnostic Id",validators=[DataRequired()])
    tname = StringField("Diagnostic Service Name",validators=[DataRequired()])
    rate = FloatField("Charge ",validators=[DataRequired()])
    submit = SubmitField('Get Bill')
class DiagnosticIssue(FlaskForm):
    name = StringField("Diagnostic Name",validators=[Optional()])
    submit = SubmitField('Issue')
class diag_bill(FlaskForm):
    pid = IntegerField("Patient Id",validators=[DataRequired()])
    submit = SubmitField('Get Bill')
class pharma_bill(FlaskForm):
    pid = IntegerField("Patient Id",validators=[DataRequired()])
    submit = SubmitField('Get Bill')
