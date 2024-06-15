from flask import Blueprint, render_template, jsonify, send_from_directory
from flask_login import login_required, current_user

pages = Blueprint('pages', __name__)

# @pages.route("/react/<path:path>")
# @login_required
# def react_app(path):
#     return render_template("react_app.html", flask_token="Hello there!", user=current_user)

@pages.route("/")
def home():
    print('home path')
    return render_template("home.html", user=current_user)

@pages.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@pages.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory('./images/', filename, as_attachment=True)



