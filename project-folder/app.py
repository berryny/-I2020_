from flask import Flask, request, redirect, url_for, render_template, session, jsonify
# Use `render_template` to send user to a different page; Redirect 301
# Use `request` to GET or POST from HTML form.
# Use `session` to pass server-side information/request

from flask_assets import Environment, Bundle
# Initialize the app by creating an Environment instance, and registering your assets with it in the form of so called bundles.

# Quickstart Flask-SQLAlchemy https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/
from flask_sqlalchemy import SQLAlchemy

from bs4 import BeautifulSoup
import requests, json, urllib3, os, random, sys, uuid
from urllib.parse import urlparse, urljoin, urlunparse

# UUIDType from the SQLAlchemy-Utils package:
from sqlalchemy.dialects.postgresql import UUID

# Install  Pillow 8.0.1 [https://pypi.org/project/Pillow/] to find time image size (h,w)
# pip install Pillow / py -m pip install Pillow
from PIL import Image
from urllib.request import urlopen


app = Flask(__name__)
app.config.from_object('config.Config')

#
# DB SETUP
# this set's up our db connection to our flask application
#
db = SQLAlchemy(app)

# this is our model (aka table)
class PreviewDB(db.Model):
    # __tablename__ = 'example'
    # make a random UUID
    print('db')
    id = db.Column('id', db.Text(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    category = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.Text, nullable=False)

    def __init__(self, category, title, description, image):
        self.category = category
        self.title = title
        self.description = description
        self.image = image

    def __repr__(self):
        return '<PreviewDB %r>' % self.category

bundles = {

    'all_js': Bundle(
        'scripts.js',
        output='gen/all.js'),

    'all_css': Bundle(
        'css/normalize.css',
        'css/style.css',
        output='gen/all_styles.css'),
}
assets = Environment(app)
assets.register(bundles)

@app.route("/", methods=["GET", "POST"])
@app.route("/index/", methods=["GET", "POST"])
# Define the website pages
def home():
    catgFilter = PreviewDB.query.filter()
    wpp = set([cf.category for cf in catgFilter])
    return render_template("index.html", catgData = wpp)

@app.route("/about/")
# Define the category page
def about():
    return render_template("about.html")
    
@app.route("/category/<string:categoryItem>")
# Define the category page
def categoryLayout(categoryItem):
    # catgpreviews = PreviewDB.query.all()
    catgpreviews = PreviewDB.query.filter(PreviewDB.category == categoryItem.lower()).all()
    if catgpreviews:
        results = [
            {
                "category": catgpreview.category,
                "title": catgpreview.title,
                "description": catgpreview.description,
                "image": catgpreview.image
            } for catgpreview in catgpreviews]

        return render_template("category.html", title=categoryItem, sitepreview=results)
    else:
        return render_template("404.html")

@app.errorhandler(404)
def page_not_found(e):
    # set the 404 status explicitly
    return render_template("404.html"), 404

# GET requests to return / select all the data from PreviewDB
@app.route('/api', methods=['GET'])
def get_data():
    table = PreviewDB.query.all()
    d = [{'category':row.category, 'title':row.title, 'description':row.description, 'image':row.image} for row in table]
    return jsonify(d)

if __name__ == '__main__':

    # Threaded option to enable multiple instances for multiple user access support
    app.run( port=5000, debug=True)
