from main import app
from flask import render_template, request, session, flash, redirect, url_for
from controller.models import *
import os


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add_category', methods = ['GET', 'POST'])
def add_category():
    if 'admin' in session.get('user_role',None):
        if request.method == 'GET':
            return render_template('add_category.html')
        
        if request.method == 'POST':
            name = request.form.get('name',None)
            description = request.form.get('description',None)


            #data validation
            if not name:
                flash('Category name is required')
                return render_template('add_category.html')

            category = Category.query.filter_by(name = name).first()
            if category:
                flash('Category already exists')
                return render_template('add_category.html')
            
            new_category = Category(name = name, description = description)
            db.session.add(new_category)
            db.session.commit()

            flash('Category added successfully')

        return redirect(url_for('home'))


    else:
        flash('You are not authorized to access this page')
        return redirect('/')


@app.route('/add_product', methods = ['GET', 'POST'])
def add_product():
    if 'store_manager' not in session.get('user_role',None):
        flash('You are not authorized to access this page')
        return redirect('/')
    
    if request.method == 'GET':
        categories = Category.query.all()
        return render_template('add_products.html',all_categories = categories)
    
    if request.method == 'POST':
        name = request.form.get('name',None)
        description = request.form.get('description',None)
        price = request.form.get('price',None)
        cost_price = request.form.get('cost_price',None)
        product_bochure = request.files.get('product_file',None)  # Here while accepting the files, we have used request.files.get instead of request.form.get
        category_id = request.form.get('category_id',None)

        # data validation
        if not name or not price or not cost_price or not category_id:
            flash('All fields are required')
            return redirect(url_for('add_product'))
        
        if product_bochure:
            folder = os.path.join(app.config['UPLOAD_FOLDER'],'product_details')
            file_name = product_bochure.filename
            product_bochure.save(os.path.join(folder,file_name))
            product_details_url = os.path.join('product_details/',file_name)

            #url_for('static',filename = product_details_url) --> 127.0.0.1:5000/static/product_details/file_name

        category = Category.query.get(category_id)
        if not category:
            flash('Invalid Category')
            return redirect(url_for('add_product'))

        new_product = Product(
            name = name,
            description = description,
            price = price,
            cost_price = cost_price,
            product_details_url = product_details_url,
            category_id = category_id
        )

        db.session.add(new_product)
        db.session.commit()

        flash('Product added successfully')
        return redirect(url_for('home'))

        