from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField,RadioField,SelectField,DateTimeField,IntegerField
from wtforms.validators import Required

class BookingForm(FlaskForm):

    car_type = StringField('Enter preference type car')
    start_date_time = DateTimeField(format='%Y-%m-%d %H:%M:%S')
    end_date_time = DateTimeField(format='%Y-%m-%d %H:%M:%S')
    mobile = IntegerField('Enter your Mobile number')
    ID_numper = IntegerField('Enter your ID Numper')
    payment = SelectField(u'Payment Method', choices=[('Cash', 'Cash'), ('Mpesa', 'Mpesa'),('Bank', 'Bank')])
    submit = SubmitField('Submit')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Whats about yourself.',validators = [Required()])
    submit = SubmitField('Submit')
    
class PostForm(FlaskForm):
    post_title = StringField('Title')
    description = TextAreaField('Description', validators=[Required()])
    submit = SubmitField('Submit')
    
class CommentForm(FlaskForm):
    username = StringField('Insert your name:',validators=[Required()])
    comment = TextAreaField('write a comment',validators=[Required()])
    submit = SubmitField('comment')

