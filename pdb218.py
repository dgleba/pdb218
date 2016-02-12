# prodigy trakberry wee little flasky app..
# orginally from flask-admin auth example.

from flask import Flask, url_for, redirect, render_template, request, abort
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
from flask_admin import helpers as admin_helpers
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import ModelView
from flask_security.utils import encrypt_password
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import column_property
from sqlalchemy.ext.hybrid import hybrid_property
import flask_admin
import flask_admin as admin
import os, time

from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Create Flask application

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Define models - reflect

# reflect models from the database...
connection = db.engine.connect()
db.metadata.reflect(db.engine, only=['tkb_prodtrak', 'pr_who_list'])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#reflect table...   
class tkb_prodtrak(db.Model):
    __table__ = db.Table(
        'tkb_prodtrak', db.metadata,
        #db.Column('id', db.Integer, primary_key=True),
        autoload=True,
        autoload_with=db.engine
    )
     
    @hybrid_property
    def tmstamp(self):
        return time.ctime(int(self.part_timestamp))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
				
		
roles_users = db.Table(
    'roles_users',
	db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __str__(self):
        return self.email

		
# Setup Flask-Security

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


# Create customized model view class

class SecuredView(sqla.ModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('superuser'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


# Flask views

# flask admin cuts off my url  --- this noworky.. #  http://stackoverflow.com/questions/26585050/flask-admin-pages-inaccessible-in-production
@app.route('/')

def index():
    return render_template('index.html')


# Create admin

admin = flask_admin.Admin(
    app,  'Prodigy (Flask, pdb218)',
    base_template='my_master.html',  template_mode='bootstrap3', )

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# customize trakberry


class prodtrack_admview(SecuredView):

    column_display_pk = True
    can_delete = False
    page_size = 30
    # sort: ('timestamp', True) true means decending sort.
    column_default_sort = ('part_timestamp', True)
    can_export = True
    #column_exclude_list = [ 'comments' ]
    column_list = [ 'machine', 'cycletime', 'part_number', 'tmstamp' ]
    column_searchable_list = ['machine', 'part_number',  ]
    column_filters = ['machine', 'cycletime', 'part_number',]

    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Add model views

admin.add_view(prodtrack_admview(tkb_prodtrak, db.session))

admin.add_view(SecuredView(Role, db.session))
admin.add_view(SecuredView(User, db.session))


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# define a context processor for merging flask-admin's template context into the
# flask-security views.
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
    )


if __name__ == '__main__':

    # run user's sql manually to create user/role tables...

    # Start app
    app.run(host='0.0.0.0', debug=True)
