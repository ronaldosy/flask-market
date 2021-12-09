from market import app, db, server_session
from market.models import Item, User
from flask import render_template, redirect, url_for, flash, request, session
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm, NewItemForm
from functools import wraps
#from flask_login import login_user, logout_user, current_user


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'loggedin' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first')
            return redirect(url_for('login_page'))
    return wrap

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    sell_form = SellItemForm()
    new_item_form = NewItemForm()
    if request.method == "POST":
        # Purchase new item and put in user invetory
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        current_user = User.query.filter_by(id=session['user_id']).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"Congrats! you purchased {p_item_object.name}", category='success')
            else:
                flash("Budget overlimit", category='danger')
        
        #Sold item from inventory and put back to market
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f"Congrats! you sold {s_item_object.name}", category='success')
            else:
                flash("Something went wrong with selling {s_item_object.name}", category='danger')

        # Create new item in user inventory
        if new_item_form.validate_on_submit():
            new_item = Item(name=new_item_form.name.data,
                            price=new_item_form.price.data, 
                            barcode=new_item_form.barcode.data,
                            description=new_item_form.description.data,
                            owner=current_user.id)
            db.session.add(new_item)
            db.session.commit()
        return redirect(url_for('market_page'))

    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=session['user_id'])
        curr_user = User.query.filter_by(id=session['user_id']).first()
        return render_template('market.html', items=items, purchase_form=purchase_form, owned_items = owned_items, sell_form=sell_form, new_item_form=new_item_form, curr_user=curr_user)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        flash(f'Account created successfully', category="success")
        return redirect(url_for('login_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating the user: {err_msg}', category='danger')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        attempted_user = User.query.filter_by(username=login_form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=login_form.password.data):
            session['username'] = attempted_user.username
            session['user_id'] = attempted_user.id
            session['loggedin'] = True
            flash(f'Success! you are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and password not match, please try again', category='danger')

    return render_template('login.html', form=login_form)


@app.route('/logout')
def logout_page():
    session.pop('username', default=None)
    session.pop('user_id', default=None)
    session.pop('loggedin', default=None)
    flash("You have been logged out", category='info')
    return redirect(url_for('home_page'))
