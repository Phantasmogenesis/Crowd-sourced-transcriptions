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
                if user_input != "":
                    transcription_functions.create_file(user_input)
                return redirect(url_for("home.home_page"))
        else:
            return redirect(url_for("home.home_page"))
        
    if request.method == "GET":
        transcription_functions.get_random_jpg()
        # mine = str.replace(transcription_functions.jpg_view_link, "/preview", "")
        # mine = str.replace(mine, "https://drive.google.com/file/d/", "")
        # print(mine)

        return render_template("transcribe.html", jpg_link=transcription_functions.jpg_view_link)

