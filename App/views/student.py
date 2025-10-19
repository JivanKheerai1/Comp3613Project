from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from App.models import Student
from.index import index_views
from App.controllers.student_controller import get_all_students_json,fetch_accolades

student_views = Blueprint('student_views', __name__, template_folder='../templates')

@student_views.route('/api/accolades', methods=['GET'])
@jwt_required()
def accolades_report_action():
    user = jwt_current_user
    if user.role != 'student':
        return jsonify(message='Access forbidden: Not a student'), 403
    report = fetch_accolades(user.student_id)
    if not report:
        return jsonify(message='No accolades for this student'), 404
    return jsonify(report)

