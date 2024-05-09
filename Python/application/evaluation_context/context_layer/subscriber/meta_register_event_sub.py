from typing import Optional

from pydantic import NonNegativeInt, PositiveInt

from applications.common.enum import Gender
from applications.common.type import MemberID
from application.evaluation_context.infra_layer.service.member_evaluation_register_service import (
    AssetMetaTearDataSet,
    BackgroundMetaTearDataSet,
    MemberEvaluationRegisterService,
    WorkMetaTearDataSet,
)


class MetaRegisterEventSubscriber:

    @classmethod
    def subscribe_income_meta_register_event(cls, member_id: MemberID, income_meta_tear: NonNegativeInt) -> None:
        from application.evaluation_context.context_layer.publisher.member_meta_request_event_pub import (
            MemberMetaRequestEventPublisher,
        )

        gender: Gender = MemberMetaRequestEventPublisher.publish_member_gender_request_event(member_id=member_id)
        MemberEvaluationRegisterService(member_id=member_id, gender=gender).register_income_evaluation_point(
            income_meta_tear=income_meta_tear
        )

    @classmethod
    def subscribe_asset_meta_register_event(
        cls,
        member_id: MemberID,
        asset_meta_tear: Optional[NonNegativeInt],
        car_price_meta_tear: Optional[NonNegativeInt],
    ) -> None:
        from application.evaluation_context.context_layer.publisher.member_meta_request_event_pub import (
            MemberMetaRequestEventPublisher,
        )

        gender: Gender = MemberMetaRequestEventPublisher.publish_member_gender_request_event(member_id=member_id)
        MemberEvaluationRegisterService(member_id=member_id, gender=gender).register_asset_evaluation_point(
            asset_meta_tear_set=AssetMetaTearDataSet(
                asset_meta_tear=asset_meta_tear, car_price_meta_tear=car_price_meta_tear
            ),
        )

    @classmethod
    def subscribe_background_meta_register_event(
        cls,
        member_id: MemberID,
        family_asset_meta_tear: Optional[NonNegativeInt],
        father_job_meta_tear: Optional[NonNegativeInt],
        mother_job_meta_tear: Optional[NonNegativeInt],
    ) -> None:
        from application.evaluation_context.context_layer.publisher.member_meta_request_event_pub import (
            MemberMetaRequestEventPublisher,
        )

        gender: Gender = MemberMetaRequestEventPublisher.publish_member_gender_request_event(member_id=member_id)
        MemberEvaluationRegisterService(member_id=member_id, gender=gender).register_background_evaluation_point(
            background_meta_tear_set=BackgroundMetaTearDataSet(
                family_asset_meta_tear=family_asset_meta_tear,
                father_job_meta_tear=father_job_meta_tear,
                mother_job_meta_tear=mother_job_meta_tear,
            ),
        )

    @classmethod
    def subscribe_work_meta_register_event(
        cls, member_id: MemberID, job_meta_tear: Optional[NonNegativeInt], company_meta_tear: Optional[NonNegativeInt]
    ) -> None:
        from application.evaluation_context.context_layer.publisher.member_meta_request_event_pub import (
            MemberMetaRequestEventPublisher,
        )

        gender: Gender = MemberMetaRequestEventPublisher.publish_member_gender_request_event(member_id=member_id)
        MemberEvaluationRegisterService(member_id=member_id, gender=gender).register_work_evaluation_point(
            work_meta_tear_set=WorkMetaTearDataSet(job_meta_tear=job_meta_tear, company_meta_tear=company_meta_tear),
        )

    @classmethod
    def subscribe_birth_year_register_event(cls, member_id: MemberID, gender: Gender, birth_year: PositiveInt) -> None:
        MemberEvaluationRegisterService(member_id=member_id, gender=gender).register_birth_year_evaluation_point(
            birth_year=birth_year
        )

    @classmethod
    def subscribe_education_meta_register_event(cls, member_id: MemberID, education_meta_tear: NonNegativeInt) -> None:
        from application.evaluation_context.context_layer.publisher.member_meta_request_event_pub import (
            MemberMetaRequestEventPublisher,
        )

        gender: Gender = MemberMetaRequestEventPublisher.publish_member_gender_request_event(member_id=member_id)
        MemberEvaluationRegisterService(member_id=member_id, gender=gender).register_education_meta_tear(
            education_meta_tear=education_meta_tear
        )

    @classmethod
    def subscribe_appearance_meta_register_event(
        cls, member_id: MemberID, appearance_meta_tear: NonNegativeInt
    ) -> None:
        from application.evaluation_context.context_layer.publisher.member_meta_request_event_pub import (
            MemberMetaRequestEventPublisher,
        )

        gender: Gender = MemberMetaRequestEventPublisher.publish_member_gender_request_event(member_id=member_id)
        MemberEvaluationRegisterService(member_id=member_id, gender=gender).register_appearance_meta_tear(
            appearance_meta_tear=appearance_meta_tear
        )
