from ninja import Router

from application.wanted_context.presentation_layer.apis.api_member_wanted import (
    member_wanted_router,
)

wanted_api_router = Router()  # merry-marry.me/api/wanted/
wanted_api_router.add_router("", member_wanted_router, tags=["wanted"])
