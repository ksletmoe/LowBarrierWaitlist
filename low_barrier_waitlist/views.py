# -*- coding: utf-8 -*-
import os
import json
import logging

import flask
from werkzeug.utils import secure_filename
from flask_security import login_required

from . import app
from . import forms
from .models import Participant
from .participant_importer import import_participants
from .ranker import Ranker

logger = logging.getLogger(__name__)


@app.route("/", methods=("POST", "GET"))
def root():
    form = forms.CheckIn()
    if form.validate_on_submit():
        participant = Participant.objects(hmis=form.hmis.data).first()
        if participant:
            participant.assigned_bed = False
            participant.check_in()

            if participant.save():
                return flask.redirect("/confirmed/{}".format(participant.hmis))
            else:
                flask.abort(500)
        else:
            return flask.redirect("/registration_required")

    return flask.render_template("index.html", form=form)


@app.route("/confirmed/<hmis_id>")
def confirm(hmis_id):
    return flask.render_template("confirmed.html", hmis_id=hmis_id)


@app.route("/registration_required")
def registration_required():
    return flask.render_template("registration_required.html")


@app.route("/admin")
@login_required
def admin():
    # TODO: pagination
    r = Ranker(Participant.bed_eligable)
    return flask.render_template(
        "admin.html", ranked_participants=r.ranked_participants
    )


@app.route("/admin/logout", methods=["POST"])
def logout():
    # TODO: actually do this
    flask.redirect("/")


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in app.config["ALLOWED_EXTENSIONS"]
    )


@app.route("/admin/import", methods=("GET", "POST"))
@login_required
def admin_import():
    form = forms.Import()
    errors = []

    if form.validate_on_submit():
        f = form.participant_list.data

        if allowed_file(f.filename):
            filename = secure_filename(f.filename)
            local_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            f.save(local_path)

            success, imported_count, errors = import_participants(local_path)
            if success:
                return flask.render_template(
                    "/import_successful.html", participant_count=imported_count
                )
        else:
            flask.abort(422)

    if len(errors) > 0:
        for error in errors:
            logger.error(error)
    return flask.render_template(
        "/admin_import.html", form=form, import_errors=errors
    )


@app.route("/admin/assign_bed/<hmis_id>", methods=["POST"])
@login_required
def assign_bed(hmis_id):
    participant = Participant.objects.get_or_404(hmis=hmis_id)
    participant.assigned_bed = True
    if participant.save():
        return (
            json.dumps({"success": True}),
            200,
            {"Content-Type": "application/json"},
        )
    else:
        flask.abort(500)


@app.route("/about", methods=["GET"])
def about_page():
    return flask.render_template("about.html")


@app.route("/contact", methods=["GET"])
def contact_page():
    return flask.render_template("contact.html")
