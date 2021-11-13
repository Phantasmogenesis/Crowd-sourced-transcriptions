from flask import Blueprint, render_template, request, redirect
from transcription_functions import *

home = Blueprint("home", __name__)

@home.route("/home", methods=['POST', 'GET'])
@home.route("/", methods=['POST', 'GET'])

def home_page():
    if request.method == "GET":
        jpg_info = get_random_jpg()
        if jpg_info != None:
            jpg_link = get_jpg_link(jpg_info)
            return render_template("home.html", jpg_link=jpg_link)
        else:
            return render_template("home.html", jpg_link=None)


