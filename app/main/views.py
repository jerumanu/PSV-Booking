
from flask import render_template,request,redirect,url_for,abort
from app.models import *
from . import main
from .. import db,photos
from flask_login import login_required, current_user
import markdown2
from .forms import *



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

def bookings():

    if not current_user.is_authenticated:
        return redirect(url_for('core.home'))
    context = {"user_has_booking":user_has_booking(),"user_bookings":get_user_bookings()}
    return render_template('booking/dashboard.html', title='Booking Dashboard',data=context)


@booking.route('/bookings/new', methods=('GET', 'POST'))
def new_booking():
    if not current_user.is_authenticated:
        return redirect(url_for('core.home'))

    form = BookingForm()
    if form.validate_on_submit():
        print (form.car_id.data)
        booking = Booking(user_id=current_user.id,
                    car_id=form.car_id.data,
                    start_time=form.start_date_time.data,
                    end_time=form.end_date_time.data)
        booking_validation = booking.is_car_avaiable()
        if booking_validation['result'] == False:
            flash(booking_validation['reason'])
            return render_template('booking/new.html', title='New Booking', form=form)
        db.session.add(booking)
        db.session.commit()
        flash('Thanks for making a booking')
        return redirect(url_for('booking_blueprint.bookings'))
    return render_template('booking/new.html', title='New Booking',form=form)

