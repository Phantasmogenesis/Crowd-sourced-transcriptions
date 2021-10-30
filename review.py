from flask import Blueprint, render_template, request
import review_functions
# from transc.py import get_random_jpg_id, download_jpg
# import display_img as display_img
# import drive_functions as df

review = Blueprint("review", __name__)

@review.route("/review", methods=['POST', 'GET'])

def review_page():
    # if request.method == "POST":
    #     user_input = request.form['user_input']
    #     # print(user_input)
    #     display_img.create_file(user_input)
    #     print(display_img.jpg_file_id)
    #     print(display_img.text_file_id)
    #     # display_img.write_to_file(user_input)

    
    review_functions.get_transcription_jpg()
    review_functions.get_transcription_txt()
    review_functions.read_txt_file(review_functions.txt_file_id)
    review_functions.increment_review_counter(review_functions.txt_file_id, review_functions.jpg_file_id)


    return render_template("review.html", jpg_link=review_functions.jpg_view_link, txt_content=review_functions.txt_file_content)
