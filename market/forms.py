from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField, IntegerField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError, NumberRange
from market.models import User


class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists')

    def validate_email_address(self, email_address_to_check):
        email_addr = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_addr:
            raise ValidationError('Email address already exists')

    username = StringField(label='Username', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Signup')

class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Signin')

class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase Item')

class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell Item')

class NewItemForm(FlaskForm):
    name = StringField(label='Item Name', validators=[DataRequired()])
    price = IntegerField(label='Price', validators=[DataRequired()])
    barcode = IntegerField(label='Barcode', validators=[NumberRange(max=999999999999), DataRequired()])
    description = StringField(label='Description')
    submit = SubmitField(label='Add New Item')