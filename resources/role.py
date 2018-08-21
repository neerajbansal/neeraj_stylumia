from models.role import RoleModel
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class RoleList(Resource):

    @jwt_required()
    def get(self):
        roles = RoleModel.find_all_roles()
        if roles:
            return {'roles': [role.json() for role in roles]}, 200
        return {'message': 'No roles found!'}, 404
