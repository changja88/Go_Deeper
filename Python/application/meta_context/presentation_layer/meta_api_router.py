from ninja import Router

from application.meta_context.presentation_layer.apis.api_certification import (
    certification_register_router,
)
from application.meta_context.presentation_layer.apis.api_lookup_date_test_meta import (
    date_test_meta_lookup_router,
)
from application.meta_context.presentation_layer.apis.api_lookup_education_meta import (
    education_meta_lookup_router,
)
from application.meta_context.presentation_layer.apis.api_lookup_finance_meta import (
    finance_meta_lookup_router,
)
from application.meta_context.presentation_layer.apis.api_lookup_physical_meta import (
    physical_meta_lookup_router,
)
from application.meta_context.presentation_layer.apis.api_lookup_preference_meta import (
    preference_meta_lookup_router,
)
from application.meta_context.presentation_layer.apis.api_member_date_test_meta import (
    member_date_test_meta_lookup_router,
)
from application.meta_context.presentation_layer.apis.api_member_education_meta import (
    member_education_meta_router,
)
from application.meta_context.presentation_layer.apis.api_member_finance_meta import (
    member_finance_meta_router,
)
from application.meta_context.presentation_layer.apis.api_member_photo import (
    member_photo_router,
)
from application.meta_context.presentation_layer.apis.api_member_physical_meta import (
    member_physical_meta_router,
)
from application.meta_context.presentation_layer.apis.api_member_preference_meta import (
    member_preference_meta_router,
)

meta_api_router = Router()  # merry-marry.me/api/meta/

# Member
meta_api_router.add_router("member/photo", member_photo_router, tags=["meta"])
meta_api_router.add_router("member/physical-meta", member_physical_meta_router, tags=["meta"])
meta_api_router.add_router("member/finance-meta", member_finance_meta_router, tags=["meta"])
meta_api_router.add_router("member/education-meta", member_education_meta_router, tags=["meta"])
meta_api_router.add_router("member/preference-meta", member_preference_meta_router, tags=["meta"])
meta_api_router.add_router("member/date-test-meta", member_date_test_meta_lookup_router, tags=["meta"])

# Lookup
meta_api_router.add_router("lookup/physical-meta", physical_meta_lookup_router, tags=["meta"])
meta_api_router.add_router("lookup/finance-meta", finance_meta_lookup_router, tags=["meta"])
meta_api_router.add_router("lookup/education-meta", education_meta_lookup_router, tags=["meta"])
meta_api_router.add_router("lookup/preference-meta", preference_meta_lookup_router, tags=["meta"])
meta_api_router.add_router("lookup/date-test-meta", date_test_meta_lookup_router, tags=["meta"])

# Certification
meta_api_router.add_router("certification", certification_register_router, tags=["meta"])
