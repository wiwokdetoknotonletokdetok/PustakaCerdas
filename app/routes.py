from app.resources.user_recommendations import UserRecommendations


def initialize_routes(api):
    api.add_resource(UserRecommendations, "/users/<string:user_id>/recommendations")
