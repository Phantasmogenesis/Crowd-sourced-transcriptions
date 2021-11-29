from flask import Blueprint, render_template, request, redirect
from flask.helpers import url_for
from librarian_functions import *
from ast import literal_eval
import flask_login


librarian = Blueprint("librarian", __name__)

@librarian.route("/librarian", methods=['POST', 'GET'])
@flask_login.login_required
def librarian_page():
    if request.method == "POST":
        jpg_info = request.form["fileData"]
        if jpg_info != "None" and jpg_info != None:
            jpg_info = literal_eval(jpg_info)
            jpg_id = jpg_info["id"]
            jpg_name = jpg_info["name"]
            txt_id = get_transcription_txt(jpg_name)
            if request.form.get("Yes") == "Yes":
                if checkFile(jpg_id):
                    approve_transcription(txt_id, jpg_id)
                    return redirect(url_for("home.home_page"))
            elif request.form.get("No") == "No":
                if checkFile(jpg_id):
                    disapprove_transcription(txt_id, jpg_id)
                    return redirect(url_for("home.home_page"))
                else:
                    return redirect(url_for("home.home_page"))
            elif request.form.get("Submit") == "Submit":
                if checkFile(jpg_id):
                    user_input = request.form['transcription-input']
                    if user_input != "":
                        submit_edit(txt_id, jpg_id, jpg_name, user_input)
                    return redirect(url_for("home.home_page"))
                else:
                    return redirect(url_for("home.home_page"))
            else:
                return redirect(url_for("home.home_page"))
        return redirect(url_for("home.home_page"))

    if request.method == "GET":
        jpg_data = get_transcription()
        if jpg_data != None:
            jpg_view_link = get_jpg_link(jpg_data)
            jpg_name = get_jpg_name(jpg_data)
            txt_content = read_txt_file(get_transcription_txt(jpg_name))
            return render_template("librarian.html", jpg_link=jpg_view_link, jpg_data= jpg_data, txt_content=txt_content)
        else:
            txt_content = "There was nothing available to be reviewed. Please try again at another time or inform an administrator if the problem persists."
            return render_template("librarian.html", jpg_link=url_for('static', filename='images/imageonline-co-textimage.jpg'), jpg_data=None, txt_content=None)
