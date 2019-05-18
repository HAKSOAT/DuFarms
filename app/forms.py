from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired


class AddForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    submit = SubmitField("Save")


class EditForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    submit = SubmitField("Save")


class ProductMovementForm(FlaskForm):
    product = SelectField('Product:', coerce=int, validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    from_location = SelectField('From:', coerce=int, validators=[DataRequired()])
    to_location = SelectField('To:', coerce=int, validators=[DataRequired()])
    qty = IntegerField("Quantity", validators=[DataRequired()])
    submit = SubmitField('Move Product')


