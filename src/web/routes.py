from flask import Blueprint, render_template, redirect, url_for, flash
from .storage import warehouse_storage
from .forms import WarehouseForm, ItemForm

main_bp = Blueprint("main", __name__)


def _get_warehouse_or_redirect(warehouse_id):
    warehouse = warehouse_storage.get(warehouse_id)
    if not warehouse:
        flash("Warehouse not found", "error")
    return warehouse


@main_bp.route("/")
def index():
    warehouses = warehouse_storage.get_all()
    return render_template("index.html", warehouses=warehouses)


@main_bp.route("/warehouse/create", methods=["GET", "POST"])
def create_warehouse():
    form = WarehouseForm()
    if form.validate_on_submit():
        warehouse_storage.create(form.name.data, form.capacity.data)
        flash("Warehouse created successfully!", "success")
        return redirect(url_for("main.index"))
    return render_template("create_warehouse.html", form=form)


@main_bp.route("/warehouse/<int:warehouse_id>")
def view_warehouse(warehouse_id):
    warehouse = _get_warehouse_or_redirect(warehouse_id)
    if not warehouse:
        return redirect(url_for("main.index"))
    available = warehouse["capacity"] - warehouse["balance"]
    return render_template("view_warehouse.html",
                           warehouse=warehouse, available=available)


@main_bp.route("/warehouse/<int:warehouse_id>/edit", methods=["GET", "POST"])
def edit_warehouse(warehouse_id):
    warehouse = _get_warehouse_or_redirect(warehouse_id)
    if not warehouse:
        return redirect(url_for("main.index"))
    form = WarehouseForm()
    if form.validate_on_submit():
        warehouse_storage.update(warehouse_id, name=form.name.data,
                                 capacity=form.capacity.data)
        flash("Warehouse updated successfully!", "success")
        return redirect(url_for("main.view_warehouse",
                                warehouse_id=warehouse_id))
    form.name.data = warehouse["name"]
    form.capacity.data = warehouse["capacity"]
    return render_template("edit_warehouse.html",
                           form=form, warehouse=warehouse)


@main_bp.route("/warehouse/<int:warehouse_id>/add", methods=["GET", "POST"])
def add_items(warehouse_id):
    warehouse = _get_warehouse_or_redirect(warehouse_id)
    if not warehouse:
        return redirect(url_for("main.index"))
    form = ItemForm()
    if form.validate_on_submit():
        success, error = warehouse_storage.add_items(warehouse_id,
                                                     form.amount.data)
        if success:
            flash("Items added successfully!", "success")
            return redirect(url_for("main.view_warehouse",
                                    warehouse_id=warehouse_id))
        flash(error, "error")
    available = warehouse["capacity"] - warehouse["balance"]
    return render_template("add_items.html", form=form,
                           warehouse=warehouse, available=available)


@main_bp.route("/warehouse/<int:warehouse_id>/remove", methods=["GET", "POST"])
def remove_items(warehouse_id):
    warehouse = _get_warehouse_or_redirect(warehouse_id)
    if not warehouse:
        return redirect(url_for("main.index"))
    form = ItemForm()
    if form.validate_on_submit():
        success, error = warehouse_storage.remove_items(warehouse_id,
                                                        form.amount.data)
        if success:
            flash("Items removed successfully!", "success")
            return redirect(url_for("main.view_warehouse",
                                    warehouse_id=warehouse_id))
        flash(error, "error")
    return render_template("remove_items.html", form=form, warehouse=warehouse)


@main_bp.route("/warehouse/<int:warehouse_id>/delete", methods=["POST"])
def delete_warehouse(warehouse_id):
    if warehouse_storage.delete(warehouse_id):
        flash("Warehouse deleted successfully!", "success")
    else:
        flash("Warehouse not found", "error")
    return redirect(url_for("main.index"))
