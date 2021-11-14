from flask import Blueprint, render_template, request, redirect
from flask.helpers import url_for
from transcription_functions import *
from ast import literal_eval


transcribe = Blueprint("transcribe", __name__)

@transcribe.route("/transcribe", methods=['POST', 'GET'])

def transcribe_page():
    if request.method == "POST":
        jpg_info = request.form["fileData"]
        # print(jpg_info)
        if jpg_info != "None" and jpg_info != None:
            jpg_info = literal_eval(jpg_info)
            jpg_id = jpg_info["id"]
            jpg_name = jpg_info["name"]
            # txt_id = get_transcription_txt(jpg_name)
            if checkFile(jpg_id) == True:
                if request.form.get("Submit") == "Submit":
                    user_input = request.form['transcription-input']
                    if user_input != "" and checkFile(jpg_id) == True:
                        create_file(jpg_id, jpg_name, user_input)
                        return redirect(url_for("home.home_page"))
                    else:
                        return redirect(url_for("home.home_page"))
                else:
                    return redirect(url_for("home.home_page"))
        else:
            return redirect(url_for("home.home_page"))
        
    if request.method == "GET":
        jpg_info = get_random_jpg()
        if jpg_info != None:
            jpg_name = get_jpg_name(jpg_info)
            jpg_link = get_jpg_link(jpg_info)
            return render_template("transcribe.html", jpg_data=jpg_info, jpg_link=jpg_link)
        else:
            return render_template("transcribe.html", jpg_data=None, jpg_link=None)

