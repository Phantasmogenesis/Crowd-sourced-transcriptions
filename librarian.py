from flask import Blueprint, render_template, request, redirect
from flask.helpers import url_for
import librarian_functions
import flask_login


librarian = Blueprint("librarian", __name__)

@librarian.route("/librarian", methods=['POST', 'GET'])
@flask_login.login_required
def librarian_page():
    if request.method == "POST":
        if librarian_functions.checkFile:
            if request.form.get("Yes") == "Yes":
                librarian_functions.approve_transcription(librarian_functions.txt_file_id, librarian_functions.jpg_file_id)
                return redirect(url_for("home.home_page"))
            elif request.form.get("No") == "No":
                librarian_functions.disapprove_transcription(librarian_functions.txt_file_id, librarian_functions.jpg_file_id)
                return redirect(url_for("home.home_page"))
            elif request.form.get("Submit") == "Submit":
                user_input = request.form['transcription-input']
                if user_input != "":
                    librarian_functions.submit_edit(user_input)
                return redirect(url_for("home.home_page"))
        else:
            return redirect(url_for("home.home_page"))

    if request.method == "GET":
        librarian_functions.get_transcription()

        return render_template("librarian.html", jpg_link=librarian_functions.jpg_view_link, txt_content=librarian_functions.txt_file_content)
