from app.forms import DefaultForm, LoginForm, RegistrationForm, DailyForm, ResetPasswordRequestForm, ResetPasswordForm
from flask_login import current_user, login_user, logout_user, login_required
from flask import render_template, flash, redirect, url_for, request, Markup
from app.money_logic import main_func, money_will_last
from app.models import User, MealPlanRecord
from app.email import send_password_reset_email
from app.graph_data import test_graph
from werkzeug.urls import url_parse
from app import app, db


@app.route('/', methods=['POST', 'GET'])
@app.route('/home', methods=['POST', 'GET'])
def home():
    form = DefaultForm()
    if form.validate_on_submit():
        output = main_func(form.current_money.data, form.avg_spent.data)
        return render_template('home.html', form=form, output=output)

    return render_template('home.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You have been registered!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        #  otherwise, the user is valid as user is in db and password matches
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('user', username=user.username)
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('Logged out successfully')
    return redirect(url_for('home'))


#  flash displayed even if the email provided by the user is unknown.
#  Thus, clients cannot use this form to figure out if a given user is a member or not.
@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password. Check spam/junk if not found.')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('home'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


#  need to allow users to delete a record (if today's record is deleted, the form is enabled)
@app.route('/user/<username>', methods=['POST', 'GET'])
@login_required
def user(username):
    form = DailyForm()
    if form.validate_on_submit():
        mp_record = MealPlanRecord(mp_amount=form.mealplan_amount.data,
                                   money_spent=form.amount_spent.data,
                                   student=current_user)
        db.session.add(mp_record)
        net_money = money_will_last(form.mealplan_amount.data, form.amount_spent.data)[1]
        mp_record.net_cash = net_money
        db.session.commit()
        flash('New meal plan record added')
        return redirect(url_for('user', username=current_user.username))

    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    records = user.past_records.order_by(MealPlanRecord.date.desc()).all()

    #  last 4 records to populate graph
    records_to_graph = user.past_records.order_by(MealPlanRecord.date.desc()).limit(5)
    some_graph = test_graph(records_to_graph)
    if records:
        meal_records = user.past_records.order_by(MealPlanRecord.date.desc()).paginate(
            page, app.config['RECORDS_PER_PAGE'], False)
        next_url = url_for('user', username=user.username, page=meal_records.next_num) \
            if meal_records.has_next else None
        prev_url = url_for('user', username=user.username, page=meal_records.prev_num) \
            if meal_records.has_prev else None

        #  if past records exist of course, will display on top
        recent_record = user.past_records.order_by(MealPlanRecord.date.desc()).first()
        estimated_end = money_will_last(recent_record.mp_amount, recent_record.money_spent)[0]

    else:
        return render_template('user.html', user=user, form=form)

    return render_template('user.html', user=user, meal_records=meal_records.items,
                           form=form, recent_mp_amount=recent_record.mp_amount,
                           estimated_end=estimated_end, next_url=next_url, prev_url=prev_url,
                           div_graph=Markup(some_graph))
