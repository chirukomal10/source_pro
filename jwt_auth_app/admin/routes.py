from flask import Blueprint
from admin.views import create_admin

admin_blueprint = Blueprint('admin', __name__)


@admin_blueprint.route('/admin/create', methods=['POST'])
def admin_create():
    return create_admin()