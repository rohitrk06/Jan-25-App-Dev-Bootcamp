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
    
    # admin_user = User.query.filter_by(user_email = 'admin@gmail.com').first()
    # if not admin_user:
    #     admin_user = User(
    #         user_email = "admin@gmail.com",
    #         password = "1234567890",
    #         user_name = "Super Admin"
    #     )
    #     db.session.add(admin_user)
    #     # print(admin_user.id)
    #     admin_user_details = User.query.filter_by(user_email = "admin@gmail.com").first()
    #     admin_role = Role.query.filter_by(name='admin').first()

    #     user_id = admin_user_details.user_id
    #     role_id = admin_role.id

    #     user_role = UserRole(user_id = user_id, role_id = role_id)
    #     db.session.add(user_role)

    admin_user = User.query.filter_by(user_email = 'admin@gmail.com').first()
    if not admin_user:
        admin_role = Role.query.filter_by(name='admin').first()
        store_manager_role = Role.query.filter_by(name='store_manager').first()
        admin_user = User(
            user_email = "admin@gmail.com",
            password = "1234567890",
            user_name = "Super Admin",
            roles = [admin_role,store_manager_role]
        )
        db.session.add(admin_user)

    db.session.commit()


from controller.auth_routes import *
from controller.routes import *


if __name__ == '__main__':
    app.run()
