from ninja import Router

from application.matching_context.presentation_layer.apis.api_match import (
    matching_router,
)
from application.matching_context.presentation_layer.apis.api_matching_exclude_friend import (
    matching_exclude_friend_router,
)

matching_api_router = Router()  # merry-marry.me/api/matching/
matching_api_router.add_router("exclude/", matching_exclude_friend_router, tags=["matching"])
matching_api_router.add_router("request/", matching_router, tags=["matching"])
