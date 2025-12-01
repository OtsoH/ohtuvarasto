from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class WarehouseForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    capacity = FloatField(
        "Capacity",
        validators=[DataRequired(), NumberRange(min=0.01)]
    )
    submit = SubmitField("Save")


class ItemForm(FlaskForm):
    amount = FloatField(
        "Amount",
        validators=[DataRequired(), NumberRange(min=0.01)]
    )
    submit = SubmitField("Submit")
