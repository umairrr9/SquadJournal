from flask import render_template, flash, redirect, request, make_response
from app import app, db, models, bcrypt
from .forms import LogInForm, SignUpForm, CreateGroupForm, JoinGroupForm, EntryForm
import datetime
from flask_login import current_user, login_user, logout_user
from app.models import Account, Group, Journal, link
import logging

logging.basicConfig(filename='sjlog', level=logging.INFO, format='%(asctime)s : %(levelname)s : %(message)s')

@app.route('/')
def index():
    return render_template('index.html', title='Squad Journal')



@app.route('/groups')
def groups():
    return render_template('groups.html', title='Squad Journal - Groups')



@app.route('/creategroup', methods=['GET', 'POST'])
def creategroup():
    form = CreateGroupForm()
    if form.validate_on_submit():
        group_hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        flash('The group %s has been created.'%(form.groupName.data))
        g = models.Group(groupName=form.groupName.data, password=group_hashed_password, date_created=datetime.datetime.utcnow())
        db.session.add(g)
        g.accs.append(current_user)
        db.session.commit()
        logging.info('{} created and joined the {} group.'.format(current_user.username, g.groupName))
        return redirect('/groups')
    return render_template('creategroup.html', title='Squad Journal - Create Group', form=form)



@app.route('/joingroup', methods=['GET', 'POST'])
def joingroup():
    form = JoinGroupForm()
    if form.validate_on_submit():
        grp = models.Group.query.filter_by(groupName=form.groupName.data).first()
        a = current_user
        if grp and bcrypt.check_password_hash(grp.password, form.password.data):
            grp.accs.append(a)
            db.session.commit()
            logging.info('{} joined the {} group.'.format(a.username, grp.groupName))
            return redirect('/groups')
        else:
            flash('Wrong group name or password')
            return redirect('/joingroup')
    return render_template('joingroup.html', title='Squad Journal - Join Group', form=form)


@app.route('/addingentry', methods=['GET', 'POST'])
def addingentry():
    form = EntryForm()
    if form.validate_on_submit():
        check1 = models.Group.query.filter_by(groupName=form.grpName.data).first()
        if not check1:
            flash('Wrong group name or password.')
            logging.warning('{} tried adding to an entry to a group which does not exist.'.format(current_user.username))
            return redirect('/addingentry')
        check2 = bcrypt.check_password_hash(check1.password, form.grpPswrd.data)
        if check1 and check2:
            x = models.Journal(entryJ=form.entry.data, locJ=form.loc.data, entry_date=datetime.datetime.utcnow(), idGrp=check1.id, member=current_user.username)
            db.session.add(x)
            db.session.commit()
            logging.info('{} added an entry to the {} group.'.format(current_user.username, check1.groupName))
            return redirect('/groups')
        else:
            flash('Wrong group name or password.')
            logging.warning('{} tried adding to an entry to a group which does not exist.'.format(current_user.username))
            return redirect('/addingentry')
    return render_template('addingentry.html', title='Squad Journal - My Group', form=form)


@app.route('/journal')
def generategroup():
    if request.args.get('id'):
        x = request.args.get('id')
        jrnl = models.Journal.query.filter_by(idGrp=x)
    else:
        flash('Group does not exist.')
        logging.critical('Program not working - a journal page which should not exist has been accessed by {}.'.format(current_user.username))
        return redirect('/groups')
    return render_template('journal.html', title='Squad Journal - My Group', jrnl=jrnl, x=x)


@app.route('/more')
def more():
    return render_template('more.html', title='Squad Journal - More')



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        logging.error('{} some how managed to access a link to the signup page whilst already logged in.'.format(current_user.username))
        return redirect('/')
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        flash('Welcome to Squad Journal, %s'%(form.username.data), 'st')
        a = models.Account(username=form.username.data, email=form.email.data, password=hashed_password, date_created=datetime.datetime.utcnow())
        db.session.add(a)
        db.session.commit()
        return redirect('/login')
    return render_template('signup.html', title='Squad Journal - Sign-Up', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        logging.error('{} some how managed to access a link to the login page whilst already logged in.'.format(current_user.username))
        return redirect('/')
    form = LogInForm()
    if form.validate_on_submit():
        user = models.Account.query.filter_by(email=form.email.data).first()
        if not user:
            flash('Wrong Username or Password')
            logging.warning('Login attempt from unrecognised email.')
            return redirect('/login')
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            logging.info('{} logged in successfully.'.format(user.username))
            return redirect('/groups')
        else:
            logging.info('{} failed to log in.'.format(user.username))
            flash('Wrong Username or Password')
            return redirect('/login')
    return render_template('login.html', title='Squad Journal - Log-In', form=form)



@app.route('/logout')
def logout():
    logging.info('{} logged out.'.format(current_user.username))
    logout_user()
    return redirect('/')