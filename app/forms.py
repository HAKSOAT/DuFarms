from flask_wtf import FlaskForm
from wtforms import HiddenField, IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired


class AddForm(FlaskForm):
    form_name = HiddenField("Form Name")
    name = StringField("Name", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    submit = SubmitField("Add")


class ProductMovementForm(FlaskForm):
    form_name = HiddenField('Form Name')
    product = SelectField('Product:', coerce=int, validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    from_location = SelectField('From:', coerce=int, validators=[DataRequired()])
    to_location = SelectField('To:', coerce=int, validators=[DataRequired()])
    qty = IntegerField("Quantity", validators=[DataRequired()])
    submit = SubmitField('Move Product')
