from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES, UploadSet, configure_uploads
import os,stripe
from dotenv import load_dotenv

from flask_msearch import Search
from flask_login import LoginManager
from flask_migrate import Migrate
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///myshop.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "u2ifhyiuek12"
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')
app.config['MSEARCH_BACKEND'] = 'whoosh'  # or another supported backend
app.config['MSEARCH_INDEX_NAME'] = 'msearch'
app.config['MSEARCH_ENABLE'] = True

stripe.api_key = os.getenv('STRIPE_SECRET_KEY' )
stripe_public_key = os.getenv('STRIPE_PUBLIC_KEY')


photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
# patch_request_class(app) 
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
search = Search()
# search.init_app(app)


migrate = Migrate(app,db)
with app.app_context():
  if db.engine.url.drivername == "sqlite":
    migrate.init_app(app,db,render_as_batch = True)
  else:
    migrate.init_app(app,db)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='customerLogin'
login_manager.needs_refresh_message_category='danger'
login_manager.login_message=u"Please Login first"


from shop.admin import routes,models as admin_routes
from shop.products import routes ,models as product_routes
from shop.carts import carts
from shop.products.models import *
from shop.customers import routes,model 


 