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