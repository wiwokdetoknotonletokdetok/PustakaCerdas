from pustakacerdas.resources import UserRecommendations


def initialize_routes(api):
    api.add_resource(UserRecommendations, "/users/me/recommendations")
