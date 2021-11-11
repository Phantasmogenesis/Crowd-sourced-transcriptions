from flask import Blueprint, render_template, request, redirect
import transcription_functions

home = Blueprint("home", __name__)

@home.route("/home", methods=['POST', 'GET'])
@home.route("/", methods=['POST', 'GET'])

def home_page():
    if request.method == "GET":
        transcription_functions.get_random_jpg()

        return render_template("home.html", jpg_link=transcription_functions.jpg_view_link)

