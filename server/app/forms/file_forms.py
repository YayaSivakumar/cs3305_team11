
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, SelectField
from wtforms.validators import DataRequired

class UploadForm(FlaskForm):
    """
    File upload form
    """
    message = TextAreaField("Enter message: ")
    upload_name = StringField("Enter upload name: ")
    expiration_hours = SelectField("Enter expiration hours: ",
                                   choices=[('24', '24 Hours'), ('72', '3 Days'), ('168', '7 Days')],
                                   default=(),
                                   validators=[DataRequired()])
    password = PasswordField("Enter password: ")
    submit = SubmitField("Submit")


class UpdateForm(FlaskForm):
    """
    File update form
    """
    upload_name = StringField("Enter upload name: ")
    message = StringField("Enter message: ")
    expiration_hours = StringField("Enter expiration hours: ",
                                   validators=[DataRequired()])
    submit = SubmitField("Submit")


class DownloadForm(FlaskForm):
    """
    File download form
    """
    password = PasswordField("Enter password: ")
    submit = SubmitField("Download")
