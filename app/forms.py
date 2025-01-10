from flask_wtf import FlaskForm,RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    TextAreaField, SelectField, RadioField,FileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, \
    Length, InputRequired
from flask_babel import _, lazy_gettext as _
from app.models import User
from app.config import Config
from flask_wtf.file import FileField, FileRequired

class LoginForm(FlaskForm):
    username = StringField(_('Username'), validators=[DataRequired()])
    password = PasswordField(_('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_('Keep me logged in (for up to one year)'))
    submit = SubmitField(_('Log in'))


class RegistrationForm(FlaskForm):
    username = StringField(_('Username'), validators=[DataRequired()])
    password = PasswordField(_('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _('Confirm password'), validators=[DataRequired(),
                                           EqualTo('password')])
    email = StringField(_('Email address (recommended)'), validators=[DataRequired(), Email()])
    # 要有domain name先用到
    # recaptcha=RecaptchaField(_('CAPTCHA Security check'))
    submit = SubmitField(_('Sign up'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_('Please use a different username.'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_('Please use a different email address.'))


class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_('Request Password Reset'))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(_('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _('Repeat Password'), validators=[DataRequired(),
                                           EqualTo('password')])
    submit = SubmitField(_('Request Password Reset'))


class EditForm(FlaskForm):
    edit_post = TextAreaField(_(''),validators=[Length(min=0, max=2000)])
    submit = SubmitField(_('Publish change'))
    cancel = SubmitField(_('Cancel'))


class PostForm(FlaskForm):
    title = StringField(_('Title'), validators=[DataRequired()])
    body = TextAreaField(_('Body'), validators=[DataRequired()])
    image = FileField(_('Photo'))
    submit = SubmitField(_('Publish page'))


class DonationForm(FlaskForm):
    once_or_monthly = RadioField('', choices=[('once', 'Just Once'), ('monthly', 'Give Monthly')], validators=[InputRequired()])
    amount = RadioField('', choices=[('20', '$20'), ('50', '$50'), ('100', '$100'), ('200', '$200')], validators=[InputRequired()])
    transaction_fee = BooleanField(_("I'll generously add 4% to cover the transaction fees so you can keep 100% of my donation."))
    card = SubmitField(_('Donate by credit/debit card'))
    paypal = SubmitField(_('Paypal'))
    payme = SubmitField(_('Payme'))

class PaymentForm(FlaskForm):
    firstname = StringField(_('First name'), validators=[DataRequired()])
    lastname = StringField(_('Last name'), validators=[DataRequired()])
    email = StringField(_('Email address'), validators=[DataRequired(), Email()])
    pay_acc=StringField(_('Account'), validators=[DataRequired()])
    submit = SubmitField(label=_('Submit'))


class LeaveMessageForm(FlaskForm):
    name=StringField(_('Guest name'), validators=[DataRequired()])
    message=StringField(_('Message'), validators=[DataRequired()])
    submit = SubmitField(_('Send'))