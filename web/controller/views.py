from flask import Blueprint
from flask import render_template

from database.models import Session, SensorLog
from web import simple_page_blueprint


@simple_page_blueprint.route("/")
def index():
    session = Session()
    logs = session.query(SensorLog).all()

    datasets = []
    datasets.append([])
    datasets.append([])
    datasets.append([])
    datasets.append([])
    datasets.append([])

    for log in logs:
        log.date = log.date.replace(microsecond=0)
        datasets[log.entity_id].append(log)

    return render_template("index.html", datasets=datasets)
