from flask_app import app
from flask import render_template, request, redirect, url_for, session, flash

from flask_app.models.user import User

# # # # # # # # # # #
#   Routes 
# # # # # # # # # # #

@app.route('/')
def route_landing():

    return redirect("/login")  

# # # # # # # # # # #
#   Posts
# # # # # # # # # # #


# # # # # # # # # # #
#   !! Test Routes !!
# # # # # # # # # # #   

@app.route('/clear')
def route_clear():
    session.clear()
    return redirect("/")      

# # # # # # # # # # #
#   Error 
# # # # # # # # # # # 

@app.errorhandler(404)
def handle_404(ex):
    return render_template("pages/error_pages/404_error.html")  

@app.errorhandler(500)
def handle_500(ex):
    return render_template("pages/error_pages/500_error.html")  