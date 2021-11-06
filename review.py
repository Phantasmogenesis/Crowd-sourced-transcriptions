from flask import Blueprint, render_template, request, redirect
from flask.helpers import url_for
import review_functions

review = Blueprint("review", __name__)

@review.route("/review", methods=['POST', 'GET'])

def review_page():
    if request.method == "POST":
        if request.form.get("Yes") == "Yes":
            review_functions.increment_review_counter(review_functions.txt_file_id, review_functions.jpg_file_id)
            return redirect(url_for("home.home_page"))
        elif request.form.get("No") == "No":
            review_functions.decrement_review_counter(review_functions.txt_file_id, review_functions.jpg_file_id)
            return redirect(url_for("home.home_page"))

    
    review_functions.get_transcription()

    return render_template("review.html", jpg_link=review_functions.jpg_view_link, txt_content=review_functions.txt_file_content)
