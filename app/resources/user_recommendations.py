from flask_restful import Resource


class UserRecommendations(Resource):
    def get(self, user_id):
        return {"data": user_id}, 200
