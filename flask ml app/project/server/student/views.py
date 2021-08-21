# project/server/auth/views.py


from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from project.server.app import db
from project.server.auth.views import auth_required
from project.server.dbmodel.studentModel import Student

stu_blueprint = Blueprint('student', __name__)

class StudentAPI(MethodView):
    @auth_required
    def post(self):
        post_data = request.get_json()
        student = Student(
                name=post_data.get('name')
            )
        db.session.add(student)
        db.session.commit()

        responseObject = {
            'status': 'success',
            'message': 'Successfully added.',
            'studentId': student.id
        }
        return make_response(jsonify(responseObject)), 201

# define the API resources
stu_view = StudentAPI.as_view('student_api')

stu_blueprint.add_url_rule(
    '/student/add',
    view_func=stu_view,
    methods=['POST']
)
