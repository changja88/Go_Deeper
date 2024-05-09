from ninja import Router

from application.member_context.presentation_layer.apis.api_lookup_address import (
    address_lookup_router,
)
from application.member_context.presentation_layer.apis.api_member import member_router
from application.member_context.presentation_layer.apis.api_member_address import (
    member_address_router,
)
from application.member_context.presentation_layer.apis.api_member_fcm import (
    member_fcm_router,
)
from application.member_context.presentation_layer.apis.api_nickname import (
    nick_name_router,
)
from application.member_context.presentation_layer.apis.api_register import (
    register_router,
)

member_api_router = Router(tags=["member"])  # merry-marry.me/api/member

member_api_router.add_router("", member_router, tags=["member"])
member_api_router.add_router("nickname", nick_name_router, tags=["member"])
member_api_router.add_router("register", register_router, tags=["member"])
member_api_router.add_router("address-lookup", address_lookup_router, tags=["member"])
member_api_router.add_router("address", member_address_router, tags=["member"])
member_api_router.add_router("fcm", member_fcm_router, tags=["member"])
