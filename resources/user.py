from models.user import UserModel
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity


class User(Resource):

    @jwt_required()
    def get(self, id):
        users = UserModel.find_by_id(id)
        if users:
            return {'user': users.json()}, 200
        return {'message': 'User not found!'}, 404

    @jwt_required()
    def delete(self, id):
        user = UserModel.find_by_id(id)
        if user:
            if current_identity.role_id > user.role_id:
                user_to_delete = UserModel.delete_user(id)
                return {'message': 'User {0} was successfully deleted from database!'.format(user.name)}, 200
            return {'message': 'You have do not have permission to delete this user'}, 401
        else:
            return {'message': 'No such user exist'}, 404


class UserList(Resource):

    @jwt_required()
    def get(self):
        users = UserModel.find_all()
        if users:
            return {'users': [user.json() for user in users]}, 200
        return {'message': 'No users found!'}, 404


class UserRegister(Resource):

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('role_id',
                            type=int,
                            required=True,
                            help='Role is required!')

        parser.add_argument('name',
                            type=str,
                            required=True,
                            help='Name is required!')

        parser.add_argument('address',
                            type=str,
                            help='Address')

        parser.add_argument('email',
                            type=str,
                            help='Email')

        parser.add_argument('bio',
                            type=str,
                            help='bio')

        parser.add_argument('username',
                            type=str,
                            required=True,
                            help='Username is required!')

        parser.add_argument('password',
                            type=str,
                            required=True,
                            help='Password is required!')

        data_payload = parser.parse_args()

        if UserModel.find_by_name(data_payload['username']):
            return {'message': 'User with the same name already exists in database!'}, 400
        else:
            address = data_payload.get('address', None)
            email = data_payload.get('email', None)
            bio = data_payload.get('bio', None)

            if(data_payload["role_id"] < current_identity.role_id):
                UserModel.insert_user_into_table(data_payload["role_id"],
                                                 data_payload["name"],
                                                 address,
                                                 email,
                                                 bio,
                                                 data_payload["username"],
                                                 data_payload["password"])
                return {'message': 'User successfully added to the database!'}, 201
            else:
                return {'message': 'You do not have permission to create user with this role'}, 400


class UserUpdate(Resource):

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id',
                            type=int,
                            required=True,
                            help='ID is required!')

        parser.add_argument('role_id',
                            type=int,
                            required=True,
                            help='Role is required!')

        parser.add_argument('name',
                            type=str,
                            required=True,
                            help='Name is required!')

        parser.add_argument('address',
                            type=str,
                            help='Address')

        parser.add_argument('email',
                            type=str,
                            help='Email')

        parser.add_argument('bio',
                            type=str,
                            help='bio')

        # parser.add_argument('password',
        #                     type=str,
        #                     required=True,
        #                     help='Password is required!')

        data_payload = parser.parse_args()

        print(data_payload)
        if UserModel.find_by_id(data_payload['id']):
            address = data_payload.get('address', None)
            email = data_payload.get('email', None)
            bio = data_payload.get('bio', None)

            if(data_payload["role_id"] < current_identity.role_id or data_payload["id"] == current_identity.id):
                if(data_payload["id"] == current_identity.id and data_payload["role_id"] >= current_identity.role_id):
                    return {'message': 'You can not update your role'}, 401
                else:
                    UserModel.update_user_into_table(data_payload["id"],
                                                     data_payload["role_id"],
                                                     data_payload["name"],
                                                     address,
                                                     email,
                                                     bio)
                    return {'message': 'User successfully updated!'}, 202
            else:
                return {'message': 'You do not have permission to update user to this role'}, 400
        else:
            return {'message': 'No such user exist'}, 400
