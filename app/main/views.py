
from flask import render_template,request,redirect,url_for,abort
from app.models import *
from . import main
from .. import db,photos
from flask_login import login_required, current_user
import markdown2
from .forms import *
from ..request import getquote


@main.route('/')
def index():
    '''
    Index page
    return
    '''
    
    message= "Welc"
    title= 'BLOG-app!'
    
    quote =getquote()
    
        

    return render_template('index.html', message=message,title=title,quote = quote ) 

   
@main.route('/user/<uname>')
@login_required
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)


  

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):

    user = User.query.filter_by(username = uname).first()
    
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))


@main.route('/booking/new_booking', methods = ['GET','POST'])
@login_required
def new_booking():
    
    form = BookingForm()

    if form.validate_on_submit():
        car_type = form.car_type.data
        start_date_time = form.start_date_time.data
        end_date_time = form.end_date_time.data
        mobile = form.mobile.data
        ID_numper = form.ID_numper.data
        payment = form.payment.data

        
        new_booking = Booking(car_type=car_type,start_date_time= start_date_time,end_date_time= end_date_time,mobile = mobile,ID_numper = ID_numper, payment = payment,user_id=current_user.id)

        title='New booking'

        new_booking.save_booking()
        

        return redirect(url_for('main.new_booking'))

    return render_template('booking.html',form= form)



@main.route('/booking/all', methods=['GET', 'POST'])
@login_required
def all():
    opinion = Booking.query.all()
    return render_template( 'opinion.html',opinion=opinion)


@main.route('/comments/<id>')
@login_required
def comment(id):
    '''
    function to return the comments
    '''
    comm =Comments.get_comment(id)
    title = 'comments'
    return render_template('comment.html',comment = comm,title = title)



@main.route('/new_comment/', methods = ['GET','POST'])
@login_required
def new_comment():
    # bookings = Book.query.filter_by(id = booking_id).first()
    form = CommentForm()
    comments = Comments.query.all()
    if form.validate_on_submit():
        username = form.username.data
        # new_username = Comments(username=username,user_id=current_user.id)
        # new_username.save_username() 

        comment = form.comment.data
        new_comment = Comments(comment=comment, username = username ,user_id=current_user.id)
        new_comment.save_comment()
        return redirect(url_for('main.new_comment'))
    title='New comment'
    return render_template('new_comment.html',title=title,comment_form = form ,comments=comments)


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





