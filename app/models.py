from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




class User(UserMixin,db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    password_secure = db.Column(db.String(255))
    pass_secure  = db.Column(db.String(255))



    comments = db.relationship('Comments', backref='title', lazy='dynamic')
    booking = db.relationship('Booking', backref='username', lazy='dynamic')
   
    

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')


    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)


    def __repr__(self):
        return f'User{self.username}'   


class Role(db.Model):

    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User',backref = 'role',lazy="dynamic")

    def __repr__(self):
        return f'User {self.name}'
# class Car(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     vin = db.Column(db.String(80), unique=True, nullable=False)
#     registration = db.Column(db.String(80), unique=True, nullable=False)
#     make = db.Column(db.String(80), unique=True, nullable=False)
#     model = db.Column(db.String(80), unique=True, nullable=False)
#     bookings = db.relationship('Booking', backref='car')


#     def __repr__(self):
#      return f'Car {self._title}'
       
class Booking(db.Model):
    __tablename__ = 'booking'

    id = db.Column(db.Integer, primary_key=True)
    car_type = db.Column(db.String(255), index=True)
    start_date_time = db.Column(db.String(255), index=True)
    description = db.Column(db.String(255), index=True)
    end_date_time = db.Column(db.String(255), index=True)
    ID_numper= db.Column(db.Integer(), index=True)
    payment = db.Column(db.String(255), index=True)
    mobile = db.Column(db.Integer(), index=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    

    def save_booking(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_bookings(cls, id):
        booking = Booking.query.filter_by(id=id).all()
        return booking

    @classmethod
    def get_all_bookings(cls):
        booking = Booking.query.order_by('-id').all()
        return booking

    def __repr__(self):
        return f'Bookings {self.payment}'

class Comments(db.Model):

    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    comment = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime(250), default=datetime.utcnow)
    booking_id = db.Column(db.Integer, db.ForeignKey("booking.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    # def save_username(self):
    #     db.session.commit()
    @classmethod

    def get_comment(cls,id):
        comments = Comments.query.filter_by(booking_id=id).all()
        return comments

    
    def __repr__(self):
        return f"Comments('{self.comment}','{self.date_posted}')"
