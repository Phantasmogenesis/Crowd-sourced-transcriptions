from flask import Blueprint, render_template, request, redirect

citations = Blueprint("citations", __name__)

@citations.route("/citations", methods=['POST', 'GET'])

def citations_page():
    if request.method == "GET":
        render_template("citations.html")

