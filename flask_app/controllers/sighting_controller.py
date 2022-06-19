from flask_app import app
from flask import render_template, request, redirect, url_for, session, flash

from flask_app.models.sighting import Sighting
from flask_app.models.skeptics import Skeptic

# # # # # # # # # # #
#   Routes 
# # # # # # # # # # #

@app.route('/dashboard')
def route_dashboard():

    sightings = Sighting.get_all()

    return render_template("pages/dashboard.html", sightings=sightings)  

@app.route('/show/<int:sighting_id>')
def route_view(sighting_id):

    sighting = Sighting.get_by_id(sighting_id)
    sighting.date_sighted = sighting.date_sighted.date()

    session['sighting_id'] = sighting_id

    if len([x for x in sighting.skeptics if x.user_id == session['logged_in']['id']]) > 0:
        user_is_skeptic = True
    else:
        user_is_skeptic = False
    
    return render_template("pages/show_sighting.html", sighting=sighting, user_is_skeptic=user_is_skeptic) 

@app.route('/new/sighting')
def route_new_sighting():

    return render_template("pages/new_Sighting.html") 

@app.route('/edit/<int:sighting_id>')
def route_edit_sighting(sighting_id):

    session['edit_sighting_id'] = sighting_id

    sighting = Sighting.get_by_id(sighting_id)
    sighting.date_sighted = sighting.date_sighted.date()

    return render_template("pages/edit_sighting.html", sighting=sighting)

# # # # # # # # # # #
#   Posts
# # # # # # # # # # #

@app.route('/report/sighting', methods=['POST'])
def route_report_sighting():

    data = request.form.to_dict()
    data['reported_by'] = session['logged_in']['id']

    if not Sighting.validate_sighting(data):
        return redirect("/new/sighting") 

    if 'logged_in' in session:
        Sighting.save(data)

    return redirect("/dashboard") 

@app.route('/update/sighting', methods=['POST'])
def route_update_sighting():

    sighting = Sighting.get_by_id(session["edit_sighting_id"])
    del session["edit_sighting_id"]

    data = request.form.to_dict()
    data["reported_by"] = sighting.reported_by
    data["id"] = sighting.id

    if not Sighting.validate_sighting(data):
        return redirect(f"/edit/sighting/{sighting.id}")     

    if session['logged_in']['id'] == sighting.reported_by:
        Sighting.update(data)

    return redirect("/dashboard") 

@app.route('/delete/sighting/<int:sighting_id>', methods=['POST'])
def route_delete_sighting(sighting_id):

    sighting = Sighting.get_by_id(sighting_id)

    if session['logged_in']['id'] == sighting.reported_by:
        Sighting.delete_by_id(sighting_id)

    return redirect("/dashboard") 

@app.route('/setskeptical', methods=['POST'])
def route_set_skeptical():

    sighting_id = session["sighting_id"]
    del session["sighting_id"]

    data = {
        "sighting_id": sighting_id,
        "user_id": session['logged_in']['id']
    }

    if request.form['action'] == 'skeptical':
        Skeptic.save(data)
    else:
        Skeptic.delete(data)

    return redirect(f"/show/{sighting_id}") 
