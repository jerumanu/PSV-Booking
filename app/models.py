from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from flask_login import UserMixin
from . import login_manager
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



#...
class User(UserMixin,db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    password_secure = db.Column(db.String(255))
    pitch = db.relationship('Comments', backref='author', lazy='dynamic')


    def __repr__(self):
        return f'User {self.username}'
    pass_secure  = db.Column(db.String(255))

    @property
    def password(self):
            raise AttributeError('You cannot read the password attribute')


    @password.setter
    def password(self, password):
            self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
            return check_password_hash(self.pass_secure,password)


    def __repr__(self):
        return f'User {self.username}'


       
class Booking(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    first_point = db.Column(db.String(255), index=True)
    second_point = db.Column(db.String(255), index=True)
    payment = db.Column(db.String(255), index=True)
    mobile = db.Column(db.Integer(), index=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    

    def save_booking(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_bookings(cls, id):
        bookings = Booking.query.filter_by(id=id).all()
        return bookings

    @classmethod
    def get_all_bookings(cls):
        bookings = Booking.query.order_by('-id').all()
        return bookings

    def __repr__(self):
        return f'Bookings {self._title}'

class Comments(db.Model):

    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime(250), default=datetime.utcnow)
    pitches_id = db.Column(db.Integer, db.ForeignKey("pitches.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod

    def get_comment(cls,id):
        comments = Comments.query.filter_by(pitches_id=id).all()
        return comments
    def __repr__(self):
        return f"Comments('{self.comment}', '{self.date_posted}')"
