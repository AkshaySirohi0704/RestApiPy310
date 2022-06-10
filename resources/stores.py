from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store import StoreModel


class Store(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id',
                        type=int,
                        required=True,
                        help="Store ID is required!"
                        )

    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "A store with name '{}' already exists.".format(name)}

        data=Store.parser.parse_args()
        store = StoreModel(data['id'], name)

        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred inserting the store."}

        return store.json()

    @jwt_required()
    def delete(self, name):
        store=StoreModel.find_by_name(name)
        if store:
            store.delete()

        return {"message":"Item Deleted"}

    def put(self, name):
        data=Store.parser.parse_args()
        store = StoreModel.find_by_name(name)
        if store is None:
            store = StoreModel(data['id'], name)
        else:
            store.id=data['id']
        
        store.save_to_db()

        return store.json()

class StoreList(Resource):

    def get(self):
        return {'Strores': list(map(lambda x: x.json(), StoreModel.query.all()))}