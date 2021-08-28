from project.server.app import db, ma
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class Category(db.Model):
    """ Category Model for storing document category details """
    __tablename__ = "Category"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description= db.Column(db.Text, unique=False, nullable=True)




class Dcoument(db.Model):
    """ Document Model for storing document related details """
    __tablename__ = "Dcoument"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    display_file_name = db.Column(db.String(255), unique=False, nullable=False)
    file_name = db.Column(db.String(255), unique=False, nullable=False) 
    category = db.Column(db.String(255), unique=False, nullable=False)


class DocumentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Dcoument

    # id = ma.auto_field()



class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        # include_fk = True