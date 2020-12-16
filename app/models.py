
class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vin = db.Column(db.String(80), unique=True, nullable=False)
    registration = db.Column(db.String(80), unique=True, nullable=False)
    make = db.Column(db.String(80), unique=True, nullable=False)
    model = db.Column(db.String(80), unique=True, nullable=False)
    bookings = db.relationship('Booking', backref='car')
    def __repr__(self):
        return '<Subject %r>' % self.vin


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)

    def __repr__(self):
        return '<Lesson %r>' % self.id
    def is_car_avaiable(self):
        within_another_bookings_timeslot = db.session.query(Booking).filter(Booking.car_id == self.car_id,
            Booking.start_time <= self.start_time,Booking.end_time >= self.end_time).count()

        user_same_time_slot = db.session.query(Booking).filter(Booking.user_id == self.user_id,
                                                                            Booking.start_time <= self.start_time,
                                                                            Booking.end_time >= self.end_time).count()


        booking_within_this_range = db.session.query(Booking).filter(Booking.car_id == self.car_id,
            Booking.start_time >= self.start_time,Booking.end_time <= self.end_time).count()


        starts_two_hours_before_end_start = db.session.query(Booking).filter(Booking.car_id == self.car_id,
             Booking.end_time >= self.start_time - timedelta(hours=2),Booking.end_time <= self.start_time).count()

        user_booking_count = db.session.query(Booking).filter(Booking.user_id == self.user_id).count()

        if user_booking_count > 5:
            return {"result": False,"reason":"You can not have more than 5 bookings"}
        if user_same_time_slot > 0:
            return {"result": False,"reason":" You already have a car already booked for these times."}
        if booking_within_this_range > 0:
            return {"result": False, "reason": " This car has already been booked between these times"}
        if within_another_bookings_timeslot > 0:
            return {"result": False, "reason": "This car has already been booked between these times"}
        if starts_two_hours_before_end_start > 0:
            return {"result": False, "reason": "Atleast 2 hours needed between bookings"}
        return {"result": True, "reason": ""}