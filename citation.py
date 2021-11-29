from flask import Blueprint, render_template, request, redirect

citation = Blueprint("citation", __name__)

@citation.route("/citation", methods=['POST', 'GET'])

def citation_page():
    if request.method == "GET":
        return render_template("citation.html")

