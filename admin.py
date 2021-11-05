from flask import Blueprint, render_template, request, redirect
from flask.helpers import url_for
import admin_functions
# from transc.py import get_random_jpg_id, download_jpg
# import display_img as display_img
# import drive_functions as df

admin = Blueprint("admin", __name__)

@admin.route("/admin", methods=['POST', 'GET'])

def admin_page():
    if request.method == "POST":
        # print("t")
        if request.form.get("Yes") == "Yes":
            admin_functions.approve_transcription(admin_functions.txt_file_id, admin_functions.jpg_file_id)
            return redirect(url_for("home.home_page"))
        elif request.form.get("No") == "No":
            admin_functions.disapprove_transcription(admin_functions.txt_file_id, admin_functions.jpg_file_id)
            return redirect(url_for("home.home_page"))

    
    admin_functions.get_transcription()

    # review_functions.submit_review("a")

    # review_functions.get_transcription_txt()
    # review_functions.read_txt_file(review_functions.txt_file_id)
    # review_functions.increment_review_counter(review_functions.txt_file_id, review_functions.jpg_file_id)


    return render_template("admin.html", jpg_link=admin_functions.jpg_view_link, txt_content=admin_functions.txt_file_content)
