from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email,Length

class SignUpForm(Form):
	first_name = StringField('First Name',validators=[DataRequired("Please enter a first name.")])
	last_name = StringField('Last Name',validators=[DataRequired("Please enter a last name.")])
	email = StringField('Email',validators=[DataRequired("Please enter an email"), Email("Please enter a valid email addresss.")])
	password = PasswordField('Password',validators=[DataRequired("Please enter a password."), Length(min=6,message="Password must be 6 characters or more.")])

	# first_name = StringField('First Name')
	# last_name = StringField('Last Name')
	# email = StringField('Email')
	# password = PasswordField('Password')

	submit = SubmitField('Sign up')

class LoginForm(Form):
	email = StringField('Email',validators=[DataRequired("Please enter your email addresss.."),Email("Please enter a valid email address.")])
	password = PasswordField('Password',validators=[DataRequired("Please enter a password.")])
	submit = SubmitField("Sign in")

class AddressForm(Form):
	address = StringField('Address',validators=[DataRequired("Please enter an address.")])
	submit = SubmitField("Search")