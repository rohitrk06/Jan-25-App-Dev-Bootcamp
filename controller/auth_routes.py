from main import app
from flask import render_template, request, session, flash, redirect, url_for
from controller.models import *

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method =='GET':
        # Check if user is login already then redirect to dashboard
        if 'user_email' in session:
            ## Revist later
            return redirect('/')
        
        return render_template('login.html')
    
    if request.method == 'POST':

        email = request.form.get('email',None)
        password = request.form.get('password',None)

        #data validation
        if not email or not password:
            flash('Email and Password are required')
            return render_template('login.html')
        
        if '@' not in email:
            flash('Invalid Email')
            return render_template('login.html')
        
        # Add your data vaildation here

        # Query Database to check if user exists

        user = User.query.filter_by(user_email = email).first()
        if not user:
            flash('User does not exists.. Please register......')
            return render_template('login.html')
        
        if user.password != password:
            flash('Invalid Password')
            return render_template('login.html')
        

        session['user_email'] = user.user_email
        session['user_role'] = [role.name for role in user.roles]

        flash("User successfully logged in....")

        # Redirect to home page
        return redirect(url_for('home'))


@app.route('/logout')
def logout():
    if 'user_email' not in session:
        flash('You are not logged in')
        return redirect(url_for('login'))
    
    session.pop('user_email')
    session.pop('user_role') 

    flash('You are successfully logged out')
    return redirect(url_for('login'))

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        ## Check if user is login already then redirect to dashboard
        return render_template('register.html')
    
    if request.method == 'POST':
        email = request.form.get('email',None)
        password = request.form.get('password',None)
        confirm_password = request.form.get('confirm_password',None)
        user_name = request.form.get('user_name',None)

        role = request.form.get('role',None)
    
        #data validation
        if not email or not password or not confirm_password or not user_name or not role:
            flash('All fields are required')
            return render_template('register.html')
        
        if '@' not in email:
            flash('Invalid Email')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Password and Confirm Password does not match')
            return render_template('register.html')
        
        if len(password) < 8:
            flash('Password should be minimum of 8 characters')
            return render_template('register.html')
        
        user = User.query.filter_by(user_email = email).first()
        if user:
            flash('User already exists.. Please Login or user another email')
            return render_template('register.html')
        
        role = Role.query.filter_by(name = role).first()
        if not role:
            flash('Invalid Role')
            return render_template('register.html')
        
        user = User(
            user_email = email,
            password = password,
            user_name = user_name,
            roles = [role]
        )

        db.session.add(user)
        db.session.commit()

        flash('User successfully registered')

        return redirect(url_for('login'))

        


    