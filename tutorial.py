from flask import Blueprint, render_template, request, redirect

tutorial = Blueprint("tutorial", __name__)

@tutorial.route("/tutorial", methods=['POST', 'GET'])

def tutorial_page():
    return render_template("tutorial.html")

