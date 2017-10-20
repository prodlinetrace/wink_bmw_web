from flask import render_template, flash, redirect, url_for, abort, request, current_app
from flask_babel import gettext
from .. import db
from ..models import Product, Status, Operation, Operation_Type, Operation_Status, Station, Unit, Comment, User
from . import statistics


@statistics.route('/')
def index():
    products = Product.query.order_by(Product.id.desc())
    statuses = Status.query.order_by(Status.id.desc())
    operations = Operation.query.order_by(Operation.id.desc())
    operation_types = Operation_Type.query.order_by(Operation_Type.id.desc())
    operation_statuses= Operation_Status.query.order_by(Operation_Status.id.desc())
    stations = Station.query.order_by(Station.id.desc())
    units = Unit.query.order_by(Unit.id.desc())
    comments = Comment.query.order_by(Comment.id.desc())
    users = User.query.order_by(User.id.desc())

    return render_template('statistics/index.html', products=products, statuses=statuses, operations=operations, operation_types=operation_types, operation_statuses=operation_statuses, stations=stations, units=units, comments=comments, users=users)
