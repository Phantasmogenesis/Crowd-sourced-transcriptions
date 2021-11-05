from flask import Blueprint, render_template, request, redirect
from flask.helpers import url_for
import review_functions
# from transc.py import get_random_jpg_id, download_jpg
# import display_img as display_img
# import drive_functions as df

review = Blueprint("review", __name__)

@review.route("/review", methods=['POST', 'GET'])

def review_page():
    if request.method == "POST":
        # print("t")
        if request.form.get("Yes") == "Yes":
            review_functions.increment_review_counter(review_functions.txt_file_id, review_functions.jpg_file_id)
            return redirect(url_for("home.home_page"))
        elif request.form.get("No") == "No":
            review_functions.decrement_review_counter(review_functions.txt_file_id, review_functions.jpg_file_id)
            return redirect(url_for("home.home_page"))

    
    review_functions.get_transcription()

    # review_functions.submit_review("a")

    # review_functions.get_transcription_txt()
    # review_functions.read_txt_file(review_functions.txt_file_id)
    # review_functions.increment_review_counter(review_functions.txt_file_id, review_functions.jpg_file_id)


    return render_template("review.html", jpg_link=review_functions.jpg_view_link, txt_content=review_functions.txt_file_content)
