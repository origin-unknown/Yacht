from flask_wtf import FlaskForm
from wtforms import ValidationError, Form
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields import (
    PasswordField,
    StringField,
    SubmitField,
    TextAreaField,
    FieldList,
    FormField
)
from wtforms.fields.html5 import (
    EmailField,
    URLField
)
from wtforms.validators import (
    Email,
    EqualTo,
    InputRequired,
    Length,
    URL
)
from app import db
from app.models import Template, Compose

import os, sys #used for getting file type
from urllib.parse import urlparse
import urllib.request, json

def validate_json(form, field): ### Make sure they're trying to download a json file
    template_path = field.data
    ext = os.path.splitext(template_path)[1]
    if ext not in ('.json'):
        raise ValidationError('Invalid File Type')

def validate_json_content(form, field): ### Verify that the file is a valid json file
    with urllib.request.urlopen(field.data) as file:
        try:
            print(file)
            return json.load(file)
        except:
            raise ValidationError('Invalid JSON')

def validate_yaml(form, field): ### Validate that the file is a yaml file (Not in use yet)
    template_path = field.data
    ext = os.path.splitext(template_path)[1]
    if ext not in ('.yml', '.yaml'):
        raise ValidationError('Invalid File Type')

def reject_template_duplicates(form, field): ### Don't allow duplicates for the name or URL fields (queries db for this info)
    print(field.data)
    if Template.query.filter_by(name=field.data).first():
        raise ValidationError('Template name already exists')
    elif Template.query.filter_by(url=field.data).first():
        raise ValidationError('Template url already exists')

def reject_compose_duplicates(form, field): ### Same as above but for compose (not in use yet)
    print(field.data)
    if Compose.query.filter_by(name=field.data).first():
        raise ValidationError('Template name already exists')
    elif Compose.query.filter_by(url=field.data).first():
        raise ValidationError('Template url already exists')

### Form for adding a new template
class TemplateForm(FlaskForm):
    template_name = StringField('Template Name', validators=[InputRequired(), reject_template_duplicates])
    template_url = URLField( 'Template URL', validators=[InputRequired(), URL(message='error'), reject_template_duplicates, validate_json, validate_json_content])
    submit = SubmitField('Add Template')

### Form for adding a compose temmplate (Not in use yet)
class ComposeForm(FlaskForm):
    template_name = StringField('Template Name', validators=[InputRequired(), reject_compose_duplicates])
    template_url = URLField( 'Template URL', validators=[InputRequired(), URL(message='error'), reject_compose_duplicates, validate_yaml])
    description = TextAreaField( 'Template Description', validators=[InputRequired()])
    submit = SubmitField('Add Compose Template')
