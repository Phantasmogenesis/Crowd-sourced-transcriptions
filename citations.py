from flask import Blueprint, render_template, request, redirect

citation = Blueprint("citation", __name__)

@citation.route("/citations", methods=['POST', 'GET'])

def citation_page():
    if request.method == "GET":
        render_template("citation.html")

