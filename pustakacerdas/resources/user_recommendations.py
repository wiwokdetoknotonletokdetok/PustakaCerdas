import uuid

from flask_restful import Resource

from pustakacerdas.dto import WebResponse
from pustakacerdas.models import User
from pustakacerdas.security import allowed_roles


class UserRecommendations(Resource):

    @allowed_roles(["USER"])
    def get(self, payload):
        user_id = payload.get("sub")

        user = get_user(user_id)

        response = WebResponse.builder().data(user.name).build()
        return response.dict(), 200


def get_user(user_id):
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        response = WebResponse.builder().errors("User tidak ditemukan").build()
        return response.dict(), 404

    user = User.query.get(user_uuid)

    if not user:
        response = WebResponse.builder().errors("User tidak ditemukan").build()
        return response.dict(), 404

    return user
