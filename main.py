from flask import Flask, render_template
from controller.database import db
from controller.config import Config
from controller.models import *

app = Flask(__name__, template_folder='templates',static_folder='static')
app.config.from_object(Config)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
# app.config['secret_key'] = 'secret_key'
db.init_app(app)

with app.app_context():
    db.create_all()
    
    admin_role = Role.query.filter_by(name='admin').first()
    if not admin_role:
        admin_role = Role(name='admin')
        db.session.add(admin_role)
    
    cust_role = Role.query.filter_by(name='customer').first()
    if not cust_role:
        cust_role = Role(name='customer')
        db.session.add(cust_role)

    manager_role = Role.query.filter_by(name='store_manager').first()
    if not manager_role:
        manager_role = Role(name='store_manager')
        db.session.add(manager_role)
    
    # admin_user = User.query.filter_by(email_id = 'admin@gmail.com').first()
    # if not admin_user:
    #     admin_user 

    db.session.commit()

@app.route('/')
def index():
    return render_template('hello.html')

@app.route('/about')
def about():
    return 'About page'


if __name__ == '__main__':
    app.run()


# '/'
# '/about'