from flask import Flask, request, redirect, url_for, render_template, session, jsonify
# Use `render_template` to send user to a different page; Redirect 301
# Use `request` to GET or POST from HTML form.
# Use `session` to pass server-side information/request

from flask_assets import Environment, Bundle
# Initialize the app by creating an Environment instance, and registering your assets with it in the form of so called bundles.


app = Flask(__name__)

bundles = {

    'all_js': Bundle(
        'scripts.js',
        output='gen/all.js'),

    'all_css': Bundle(
        'css/style.css',
        output='gen/all.css'),
}
assets = Environment(app)
assets.register(bundles)


@app.route("/")
@app.route("/index/")
# Define the website pages
def home():
    return render_template("index.html")

@app.route("/sqrt/<input>")
# Define the website pages
def sqrt(input):
    print('input',input**2)
    return render_template("sqrt.html", output=input)

@app.route("/user/<username>")
# Define the website pages
def user(username):
    print('username',username)
    return render_template("user.html", usr=username)

@app.errorhandler(404)
def page_not_found(e):
    # set the 404 status explicitly
    return render_template('404.html'), 404

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000, debug=True)
