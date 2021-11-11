from flask import Blueprint, render_template, request, redirect
from flask.helpers import url_for
import transcription_functions


transcribe = Blueprint("transcribe", __name__)

@transcribe.route("/transcribe", methods=['POST', 'GET'])

def transcribe_page():
    if request.method == "POST":
        if transcription_functions.checkFile:
            if request.form.get("Submit") == "Submit":
                user_input = request.form['transcription-input']
                transcription_functions.create_file(user_input)
                return redirect(url_for("home.home_page"))
        else:
            return redirect(url_for("home.home_page"))
        
    if request.method == "GET":
        transcription_functions.get_random_jpg()

        return render_template("transcribe.html", jpg_link=transcription_functions.jpg_view_link)

