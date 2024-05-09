from typing import Optional

from pydantic import NonNegativeInt

from applications.common.type import MemberID
from application.evaluation_context.context_layer.subscriber.meta_register_event_sub import (
    MetaRegisterEventSubscriber,
)


class MetaRegisterEventPublisher:

    @classmethod
    def publish_income_meta_register_event(
        cls, member_id: MemberID, income_meta_tear: Optional[NonNegativeInt]
    ) -> None:
        MetaRegisterEventSubscriber.subscribe_income_meta_register_event(
            member_id=member_id, income_meta_tear=income_meta_tear
        )

    @classmethod
    def publish_work_meta_register_event(
        cls, member_id: MemberID, job_meta_tear: Optional[NonNegativeInt], company_meta_tear: Optional[NonNegativeInt]
    ) -> None:
        MetaRegisterEventSubscriber.subscribe_work_meta_register_event(
            member_id=member_id,
            job_meta_tear=job_meta_tear,
            company_meta_tear=company_meta_tear,
        )

    @classmethod
    def publish_background_meta_register_event(
        cls,
        member_id: MemberID,
        family_asset_meta_tear: Optional[NonNegativeInt],
        father_job_meta_tear: Optional[NonNegativeInt],
        mother_job_meta_tear: Optional[NonNegativeInt],
    ) -> None:
        MetaRegisterEventSubscriber.subscribe_background_meta_register_event(
            member_id=member_id,
            family_asset_meta_tear=family_asset_meta_tear,
            father_job_meta_tear=father_job_meta_tear,
            mother_job_meta_tear=mother_job_meta_tear,
        )

    @classmethod
    def publish_asset_meta_register_event(
        cls,
        member_id: MemberID,
        asset_meta_tear: Optional[NonNegativeInt],
        car_price_meta_tear: Optional[NonNegativeInt],
    ) -> None:
        MetaRegisterEventSubscriber.subscribe_asset_meta_register_event(
            member_id=member_id,
            asset_meta_tear=asset_meta_tear,
            car_price_meta_tear=car_price_meta_tear,
        )

    @classmethod
    def publish_education_meta_register_event(cls, member_id: MemberID, education_meta_tear: NonNegativeInt) -> None:
        MetaRegisterEventSubscriber.subscribe_education_meta_register_event(
            member_id=member_id, education_meta_tear=education_meta_tear
        )

    @classmethod
    def publish_application_meta_register_event(cls, member_id: MemberID, appearance_meta_tear: NonNegativeInt) -> None:
        MetaRegisterEventSubscriber.subscribe_appearance_meta_register_event(
            member_id=member_id, appearance_meta_tear=appearance_meta_tear
        )
