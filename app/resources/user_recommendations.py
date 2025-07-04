from flask_restful import Resource

from app.dto import WebResponse
from app.security import allowed_roles


class UserRecommendations(Resource):

    @allowed_roles(["USER"])
    def get(self, payload):
        user_id = payload.get("sub")

        response = WebResponse.builder().data(user_id).build()
        return response.dict(), 200
