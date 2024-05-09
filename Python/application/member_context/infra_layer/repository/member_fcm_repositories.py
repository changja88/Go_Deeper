from typing import Optional

from applications.common.django.django_model_util import get_obj_or_none
from applications.common.type import MemberID
from applications.member.domain_layer.entity.member_fcm import MemberFCM
from application.member_context.infra_layer.django.models import MemberFCMORM


class MemberFCMReadRepository:
    def find_by(self, member_id: MemberID) -> Optional[MemberFCM]:
        member_fcm_orm: Optional[MemberFCMORM] = get_obj_or_none(MemberFCMORM, member_id=member_id)
        if member_fcm_orm:
            return MemberFCM(
                member_id=MemberID(member_fcm_orm.member.id),
                fcm_token=member_fcm_orm.fcm_token,
                device_info=member_fcm_orm.device,
            )
        return None


class MemberFCMWriteRepository:
    def update_or_create(self, member_fcm: MemberFCM) -> MemberFCM:
        member_fcm_orm, _ = MemberFCMORM.objects.update_or_create(
            member_id=member_fcm.member_id,
            defaults={
                "member_id": member_fcm.member_id,
                "fcm_token": member_fcm.fcm_token,
                "device": member_fcm.device_info,
            },
        )
        return MemberFCM(
            member_id=MemberID(member_fcm_orm.member_id),
            fcm_token=member_fcm_orm.fcm_token,
            device_info=member_fcm_orm.device,
        )


class MemberFCMCompoundRepository(MemberFCMReadRepository, MemberFCMWriteRepository): ...
