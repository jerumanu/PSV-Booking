
from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField
from wtforms.validators import Required


class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')









class BookingForm(ModelForm, FlaskForm):

    cars = Car.query.all()
    car_list = []
    #car.id, car.make + car.model
    for car in cars:
        car_make_model = car.make + " " + car.model
        car_list.append((car.id,car_make_model ))

    car_id = SelectField('Car',choices=car_list,coerce=int, validators=[DataRequired()])


    start_date_time = DateTimeField('Start Date/Time', id="start_date_time",format='%Y-%m-%d %H:%M:%S',validators=[DataRequired()])
    end_date_time = DateTimeField('End Date/Time',id="end_date_time", format='%Y-%m-%d %H:%M:%S',validators=[DataRequired()])
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField,RadioField,SelectField
from wtforms.validators import Required

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Whats about yourself.',validators = [Required()])
    submit = SubmitField('Submit')
    
class PostForm(FlaskForm):
    post_title = StringField('Title')
    description = TextAreaField('Description', validators=[Required()])
    submit = SubmitField('Submit')
    
class CommentForm(FlaskForm):
    comment = TextAreaField('write a comment',validators=[Required()])
    submit = SubmitField('comment')

