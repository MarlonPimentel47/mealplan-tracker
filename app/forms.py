from wtforms.validators import DataRequired, NumberRange, Email, EqualTo, ValidationError
from wtforms import StringField, PasswordField, SubmitField, FloatField
from flask_wtf import FlaskForm
from app.models import User


class DefaultForm(FlaskForm):

    current_money = FloatField('Current Amount:',
                               validators=[DataRequired(), NumberRange(min=1, max=5000)], default=600.47)
    avg_spent = FloatField('Avg Amount Spent:',
                           validators=[DataRequired(), NumberRange(min=1, max=500)], default=7.50)
    submit = SubmitField('Click to Submit')


class LoginForm(FlaskForm):

    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):

    username = StringField('Username:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired(), Email()])
    password = PasswordField('Password:', validators=[DataRequired()])
    password2 = PasswordField('Repeat password:',
                              validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Username already exists.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Please use a different email.")


#  a user can have many daily forms (mp records) so one to many relationship in models
class DailyForm(FlaskForm):

    mealplan_amount = FloatField('MP Amount:',
                                 validators=[DataRequired(), NumberRange(min=1, max=5000)], default=600.47)
    amount_spent = FloatField('Amount Spent Today:',
                              validators=[DataRequired(), NumberRange(min=1, max=500)], default=7.50)
    submit = SubmitField('Click to Submit')


class ResetPasswordRequestForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Email()])

    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')
