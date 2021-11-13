from flask import Blueprint, render_template, request, redirect
from flask.helpers import url_for
from librarian_functions import *
from ast import literal_eval
import flask_login


librarian = Blueprint("librarian", __name__)

@librarian.route("/librarian", methods=['POST', 'GET'])
@flask_login.login_required
def librarian_page():
    # if request.method == "POST":
    #     if librarian_functions.checkFile:
    #         if request.form.get("Yes") == "Yes":
    #             librarian_functions.approve_transcription(librarian_functions.txt_file_id, librarian_functions.jpg_file_id)
    #             return redirect(url_for("home.home_page"))
    #         elif request.form.get("No") == "No":
    #             librarian_functions.disapprove_transcription(librarian_functions.txt_file_id, librarian_functions.jpg_file_id)
    #             return redirect(url_for("home.home_page"))
    #         elif request.form.get("Submit") == "Submit":
    #             user_input = request.form['transcription-input']
    #             if user_input != "":
    #                 librarian_functions.submit_edit(user_input)
    #             return redirect(url_for("home.home_page"))
    #     else:
    #         return redirect(url_for("home.home_page"))

    # if request.method == "GET":
    #     librarian_functions.get_transcription()

    #     return render_template("librarian.html", jpg_link=librarian_functions.jpg_view_link, txt_content=librarian_functions.txt_file_content)


    if request.method == "POST":
        jpg_info = request.form["fileData"]
        print(jpg_info + "yes")
        if jpg_info != None:
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
            elif request.form.get("Submit") == "Submit":
                if checkFile(jpg_id):
                    user_input = request.form['transcription-input']
                    if user_input != "":
                        submit_edit(txt_id, jpg_id, jpg_name, user_input)
                    return redirect(url_for("home.home_page"))
            else:
                return redirect(url_for("home.home_page"))
        return "The page you were reviewing was already completed by someone else."

    if request.method == "GET":
        jpg_data = get_transcription()
        if jpg_data != None:
            jpg_view_link = get_jpg_link(jpg_data)
            jpg_name = get_jpg_name(jpg_data)
            txt_content = read_txt_file(get_transcription_txt(jpg_name))
            return render_template("librarian.html", jpg_link=jpg_view_link, jpg_data= jpg_data, txt_content=txt_content)
        else:
            jpg_view_link = None
            jpg_name = None
            txt_content = "There was nothing available to be reviewed. Please try again at another time or inform an administrator if the problem persists."
            return render_template("librarian.html", jpg_link=url_for('static', filename='images/imageonline-co-textimage.jpg'), jpg_data= jpg_data, txt_content=txt_content)
