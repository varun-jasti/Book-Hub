from wtforms import Form, StringField,TextAreaField,PasswordField,SubmitField,validators,ValidationError
from flask_wtf.file import FileRequired,FileAllowed,FileField
from flask_wtf import FlaskForm
from .model import Register


class CustomerRegistration(FlaskForm):
  name = StringField('Name:')
  username = StringField('Username:',[validators.DataRequired()])
  email = StringField('Email:',[validators.Email(),validators.DataRequired()])
  password = PasswordField('Password:',[validators.DataRequired(),validators.EqualTo('confirm',message = 'Both Password must match')])
  confirm = PasswordField('Repeat Password',[validators.DataRequired()])
  country = StringField('Country:',[validators.DataRequired()])
  state = StringField('State:',[validators.DataRequired()])
  city = StringField('City:',[validators.DataRequired()])
  contact = StringField('Conatact:',[validators.DataRequired()])
  address = StringField('Address:',[validators.DataRequired()])
  zipcode = StringField('Zip Code:',[validators.DataRequired()])

  profile = FileField('Profile',validators=[FileAllowed(['jpg','png','jpg','gif'],'Image Only please')])

  submit =SubmitField('Register')


  def validate_username(self,username):
    if Register.query.filter_by(username=username.data).first():
      raise ValidationError("This username already in use!")
     
  def validate_email(self,email):
    if Register.query.filter_by(email=email.data).first():
      raise ValidationError("This email address is already in use!")
    
  


class CustomerLoginFrom(FlaskForm):
    email = StringField('Email: ', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password: ', [validators.DataRequired()])


   
