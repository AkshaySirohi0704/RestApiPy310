import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    TABLE_NAME = 'users'

    parser = reqparse.RequestParser()
    parser.add_argument('_id',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!")
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "User with that username already exists."}, 400

        item = UserModel(data['_id'],data['username'],data['password'])
        item.save_to_db()

        return {"message": "User created successfully."}, 201

class UserList(Resource):

    def get(self):
        return {'Users': list(map(lambda x: x.json(), UserModel.query.all()))}

