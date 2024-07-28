from flask_wtf.file import FileAllowed,FileField,FileRequired
from wtforms import IntegerField,StringField,BooleanField,TextAreaField,validators,SubmitField,DecimalField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

class AddproductForm(FlaskForm):
  name = StringField('Name',[validators.DataRequired()])
  price = DecimalField('Price',[validators.DataRequired()])
  discount = IntegerField('Discount',default=0)
  stock = IntegerField('Stock',[validators.DataRequired()]) 
  desc = TextAreaField('Description',[validators.DataRequired()])
  colors = TextAreaField('Type',[validators.DataRequired()])

  image_1 = FileField('Image 1',validators=[FileAllowed(['jpg','png','gif','jpeg'],'images only please')])
  image_2 = FileField('Image 2',validators=[FileAllowed(['jpg','png','gif','jpeg'],'images only please')])
  image_3 = FileField('Image 3',validators=[FileAllowed(['jpg','png','gif','jpeg'],'images only please')])
  

  submit = SubmitField('Add Product')



