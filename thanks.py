from flask import Blueprint, render_template, request, redirect

thanks = Blueprint("thanks", __name__)

@thanks.route("/thanks", methods=['POST', 'GET'])

def thanks_page():
    if request.method == "GET":
        return render_template("thanks.html")
