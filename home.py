from flask import Blueprint, render_template, request, redirect
# from transc.py import get_random_jpg_id, download_jpg
import transcription_functions
# import drive_functions as df

home = Blueprint("home", __name__)

@home.route("/home", methods=['POST', 'GET'])
@home.route("/", methods=['POST', 'GET'])

def home_page():
    if request.method == "POST":
        user_input = request.form['user_input']
        # # print(user_input)
        transcription_functions.create_file(user_input)
        # print(transcription_functions.jpg_file_id)
        # print(transcription_functions.text_file_id)
        # transcription_functions.write_to_file(user_input)
        return redirect("/home")
        

    
    # f = open("static/images/document.jpg", "r+b")
    transcription_functions.get_random_jpg()
    # print(transcription_functions.jpg_view_link)
    # transcription_functions.download_jpg(transcription_functions.service, transcription_functions.jpg_file_id)
    # transcription_functions.convert_img()

    return render_template("home.html", jpg_link=transcription_functions.jpg_view_link)

