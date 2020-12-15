






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
