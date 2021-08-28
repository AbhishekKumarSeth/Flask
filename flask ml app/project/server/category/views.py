
from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from project.server.app import db
from project.server.auth.views import auth_required
from project.server.dbmodel.documentmodel import Category,CategorySchema

category_blueprint = Blueprint('category', __name__)


def get_all():
    try:
        categories = Category.query.all()
        categories_schema = CategorySchema(many=True)
        
        results = categories_schema.dump(categories)
        
        return {"count": len(results), "data": results}

    except Exception as ex:
        print(ex)
        return ex


def get_by_id(cat_id):
    try:
        category_obj =  Category.query.get(cat_id)
        categories_schema = CategorySchema(many=False)
        results = categories_schema.dump(category_obj)
        
        return {"data": results}
        
    except Exception as ex:
        print(ex)
        return ex


def save():
    
    try:
        post_data = request.get_json()

        category = Category(
            name=post_data.get("name"),
            description=post_data.get("description")
        )
        db.session.add(category)
        db.session.commit()


        categories_schema = CategorySchema(many=False)
        results = categories_schema.dump(category)

        return {"data": results}
        
    except Exception as ex:
        print(ex)
        return ex



def update(id):
    try:
        post_data = request.get_json()

        # new_name=post_data.get('name'),
        # new_description=post_data.get('description')

        category_obj = Category.query.filter_by(id=id).first()
        
        category_obj.name = post_data.get('name')
        category_obj.description = post_data.get('description')

        
        db.session.commit()
        
        categories_schema = CategorySchema(many=False)
        results = categories_schema.dump(category_obj)
        
        return {"data": results}
    except Exception as ex:
        print(ex)
        return ex


def delete(id):
    try:
        category_obj = Category.query.filter_by(id=id).first()
        db.session.delete(category_obj)
        db.session.commit()

        categories_schema = CategorySchema(many=False)
        results = categories_schema.dump(category_obj)
        
        return {"data": results}
    except Exception as ex:
        print(ex)
        return ex


category_blueprint.add_url_rule('/category', view_func=get_all, methods=['GET'])
category_blueprint.add_url_rule('/category/<cat_id>', view_func=get_by_id, methods=['GET'])
category_blueprint.add_url_rule('/save', view_func=save, methods=['POST'])
category_blueprint.add_url_rule('/category/<id>', view_func=update, methods=['PUT'])
category_blueprint.add_url_rule('/category/<id>', view_func=delete, methods=['DELETE'])
