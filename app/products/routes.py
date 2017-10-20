try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import csv
import six
from flask import render_template, flash, redirect, url_for, abort, request, current_app, make_response
from flask.ext.login import login_required, current_user
from flask.ext.babel import gettext
from flask.ext.paginate import Pagination
from .. import db, babel, cfg
from ..models import *
from . import products
from .forms import ProductForm, CommentForm, FindProductForm, FindProductsRangeForm, ExportProductsRangeForm, HandScannerSearchForm
from datetime import datetime

@products.route('/')
def index():
    start = datetime.now()
    debug_print=False
    page = request.args.get('page', 1, type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    status = request.args.get('status')
    operation = request.args.get('operation')
    per_page = current_app.config['PRODUCTS_PER_PAGE']
    db.create_all()

    query = Product.query
    if start_date:
        query = query.filter(start_date <= Product.date_added)
    if end_date:
        query = query.filter(end_date >= Product.date_added)
    if status:
        # include in the list in case any of statuses is equal to searched status_id
        query = query.filter(Product.statuses.any(Status.status==status))
    if operation:
        # include in the list in case one of operations is equal to searched operation_id
        query = query.filter(Product.operations.any(Operation.operation_status_id==operation))
    if debug_print:
        print("before query:", datetime.now() - start)
    total = query.count()
    products = query.order_by(Product.date_added.desc()).paginate(page, per_page, False).items
    if debug_print:
        print("after query:", datetime.now() - start)
    pagination = Pagination(page=page, total=total, record_name='products', per_page=per_page)
    if debug_print:
        print("after pagination:", datetime.now() - start)
    t = render_template('products/index.html', products=products, pagination=pagination, Status=Status, Operation=Operation)
    if debug_print:
        print("FINISHED template rendering:", datetime.now() - start)
    return t

@products.route('/download')
def download(start_date=None, end_date=None, status=None, operation=None):
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    status = request.args.get('status')
    operation = request.args.get('operation')
    query = Product.query
    if start_date and start_date!='':
        query = query.filter(start_date <= Product.date_added)
    if end_date and end_date!='':
        query = query.filter(end_date >= Product.date_added)
    if status and status!='':
        # include in the list in case any of statuses is equal to searched status_id
        query = query.filter(Product.statuses.any(Status.status==status))
    if operation and operation!='':
        # include in the list in case one of operations is equal to searched operation_id
        query = query.filter(Product.operations.any(Operation.operation_status_id==operation))

    csv_header = ['Id', 'Type', 'Serial', 'Date Added', 'Success Statuses', 'Failed Statuses', 'Success Operations', 'Failed Operations']
    buffer = StringIO()
    writer = csv.writer(buffer, delimiter=',')
    writer.writerow(csv_header)

    products = query.order_by(Product.date_added.desc()).all()
    for product in products:
        row = ["{id}".format(id=product.id), "{type}".format(type=product.type), "{sn}".format(sn=product.serial), " {date}".format(date=product.date_added)]
        row.append(product.statuses.filter(Status.status==1).count())
        row.append(product.statuses.filter(Status.status==2).count())
        row.append(product.operations.filter(Operation.operation_status_id==1).count())
        row.append(product.operations.filter(Operation.operation_status_id==2).count())
        #row.append(product.id)
        writer.writerow(row)

    output = make_response(buffer.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename={name}.csv".format(name=current_app.config['NAME'])
    output.headers["Content-type"] = "text/csv"
    return output

@products.route('/find_product', methods=['GET', 'POST'])
def find_product():
    type_query = db.session.query(Product.type.distinct().label("type"))
    type_choices = [(six.u(row.type), six.u(row.type)) for row in type_query.all()]
    type_choices.insert(0, ("", "Select Product Type"))
    basic_search_form = FindProductForm(type_choices)
    detailed_search_form = FindProductsRangeForm()
    hand_scanner_search_form = HandScannerSearchForm()

    if basic_search_form.validate_on_submit():
        result = Product.query.filter_by(type=basic_search_form.type.data).filter_by(serial=basic_search_form.serial.data).first()
        if result is not None:
            flash(gettext(u'Product with serial {serial} found.'.format(serial=basic_search_form.serial.data)))
            return redirect(url_for('products.product', id=result.id))
        flash(gettext(u'Product with serial {serial} not found.'.format(serial=basic_search_form.serial.data)))

    if detailed_search_form.validate_on_submit():
        start_date = detailed_search_form.start.data
        end_date = detailed_search_form.end.data
        status = ""
        operation = ""
        query = Product.query
        if start_date:
            query = query.filter(start_date <= Product.date_added)
        if end_date:
            query = query.filter(end_date >= Product.date_added)
        if detailed_search_form.status_failed.data:
            status = 2
            query = query.filter(Product.statuses.any(Status.status==status))
        if detailed_search_form.operation_failed.data:
            operation = 2
            query = query.filter(Product.operations.any(Operation.operation_status_id==operation))
        total = query.count()
        result = query.all()
        if result is not None:
            flash(gettext(u'{number} products found with selected criteria.'.format(number=len(result), start=start_date, end=end_date)))
            return redirect(url_for('products.index', start_date=start_date, end_date=end_date, status=status, operation=operation))
        flash(gettext(u'No products are matching selected criteria.'.format(number=len(result), start=start_date, end=end_date)))

    return render_template('products/find_product.html', basic_search_form=basic_search_form, detailed_search_form=detailed_search_form, hand_scanner_search_form=hand_scanner_search_form)

@products.route('/export_csv', methods=['GET', 'POST'])
def export_csv():
    #type_query = db.session.query(Operation_Type.name.distinct().label("type"))
    type_query = Operation_Type.query
    operation_types = [(six.u(row.id), six.u(row.name)) for row in type_query.all()]
    operation_types.insert(0, ("", "Select Operation Type"))
    search_form = ExportProductsRangeForm(operation_types)

    if search_form.validate_on_submit():
        start_date = search_form.start.data
        end_date = search_form.end.data
        query = Product.query
        if start_date:
            query = query.filter(start_date <= Product.date_added)
        if end_date:
            query = query.filter(end_date >= Product.date_added)
        if search_form.type.data:
            query = query.filter(Product.operations.any(Operation.operation_type_id==search_form.type.data))
        total = query.count()
        result = query.all()
        if result is not None:
            flash(gettext(u'{number} products found with selected criteria.'.format(number=len(result), start=start_date, end=end_date)))
            return redirect(url_for('products.export', start_date=start_date, end_date=end_date, operation_type_id=search_form.type.data))
        flash(gettext(u'No products are matching selected criteria.'.format(number=len(result), start=start_date, end=end_date)))

    return render_template('products/export_csv.html', search_form=search_form)

@products.route('/export')
def export(start_date=None, end_date=None, operation_type_id=None):
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    operation_type_id = request.args.get('operation_type_id')
    query = Product.query
    if start_date and start_date!='':
        query = query.filter(start_date <= Product.date_added)
    if end_date and end_date!='':
        query = query.filter(end_date >= Product.date_added)
    #if operation_type_id and operation_type_id!='':
    #        query = query.filter(Product.operations.any(Operation.operation_type_id==operation_type_id))

    csv_header = ['Id', 'Type', 'Serial', 'Date Added', 'Operation Type Id', 'Operation Name', 'Result 1', 'Result 2']
    buffer = StringIO()
    writer = csv.writer(buffer, delimiter=',')
    writer.writerow(csv_header)

    products = query.order_by(Product.date_added.desc()).all()
    for product in products:
        row = ["{id}".format(id=product.id), "{type}".format(type=product.type), "{sn}".format(sn=product.serial), " {date}".format(date=product.date_added)]
        row.append(operation_type_id)
        row.append((Operation_Type.query.filter_by(id=operation_type_id).first().name).encode("utf-8"))
        if product.operations.filter(Operation.operation_type_id==operation_type_id).count() >0:
            row.append(product.operations.filter(Operation.operation_type_id==operation_type_id).first().result_1)
            row.append(product.operations.filter(Operation.operation_type_id==operation_type_id).first().result_2)
        writer.writerow(row)

    output = make_response(buffer.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename={name}-export-opertation_type_id-{operation_type_id}.csv".format(name=current_app.config['NAME'], operation_type_id=operation_type_id)
    output.headers["Content-type"] = "text/csv"
    return output

@products.route('/product/<id>', methods=['GET', 'POST'])
def product(id):
    product = Product.query.get_or_404(id)
    comment = None
    form = None
    if current_user.is_authenticated:
        form = CommentForm()
        if form.validate_on_submit():
            comment = Comment(body=form.body.data, product=product, author=current_user)
    if comment:
        db.session.add(comment)
        db.session.commit()
        flash(gettext(u'Your comment has been published.'))
        return redirect(url_for('.product', id=product.id) + '#top')

    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['COMMENTS_PER_PAGE']
    total = product.comments.count()
    comments = product.comments.order_by(Comment.timestamp.asc()).paginate(page, per_page, False).items
    pagination = Pagination(page=page, total=total, record_name='comments', per_page=per_page)
    stations = {}
    headers = {}
    if current_user.is_authenticated:
        headers['X-XSS-Protection'] = '0'
        
    return render_template('products/product.html', product=product, form=form, comments=comments, pagination=pagination, Status=Status, Operation=Operation), 200, headers

@products.route('/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    product = Product.query.get_or_404(id)
    if not current_user.is_admin and product.author != current_user:
        abort(403)
    form = ProductForm()
    if form.validate_on_submit():
        form.to_model(product)
        db.session.add(product)
        db.session.commit()
        flash(gettext(u'The product was updated successfully.'))
        return redirect(url_for('.product', id=product.id))
    form.from_model(product)
    return render_template('products/edit_product.html', form=form)
