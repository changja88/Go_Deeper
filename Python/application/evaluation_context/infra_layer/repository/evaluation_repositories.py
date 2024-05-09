from typing import Optional

from applications.common.django.django_model_util import get_obj_or_none
from applications.common.enum import Gender
from applications.common.type import MemberID
from application.evaluation_context.domain_layer.value_object.evaluation_point import (
    EvaluationPoint,
)
from application.evaluation_context.domain_layer.value_object.evaluation_point_set import (
    EvaluationPointSet,
)
from application.evaluation_context.infra_layer.django_evaluation.models import (
    MemberEvaluationORM,
)
from applications.member.domain_layer.value_object.enum import MemberStatus


class EvaluationReadRepository:

    def find_all_by(
        self, min_evaluation_point_set: EvaluationPointSet, max_evaluation_point_set: EvaluationPointSet, gender: Gender
    ) -> list[MemberID]:
        member_ids: list[MemberID] = list(
            MemberEvaluationORM.objects.filter(
                member__status=MemberStatus.ACTIVE,
                member__birth_meta__gender=gender,
                work_point__range=[
                    min_evaluation_point_set.work_point.point,
                    max_evaluation_point_set.work_point.point,
                ],
                income_point__range=[
                    min_evaluation_point_set.income_point.point,
                    max_evaluation_point_set.income_point.point,
                ],
                asset_point__range=[
                    min_evaluation_point_set.asset_point.point,
                    max_evaluation_point_set.asset_point.point,
                ],
                background_point__range=[
                    min_evaluation_point_set.background_point.point,
                    max_evaluation_point_set.background_point.point,
                ],
                education_point__range=[
                    min_evaluation_point_set.education_point.point,
                    max_evaluation_point_set.education_point.point,
                ],
                appearance_point__range=[
                    min_evaluation_point_set.appearance_point.point,
                    max_evaluation_point_set.appearance_point.point,
                ],
                birth_year_point__range=[
                    min_evaluation_point_set.birth_year_point.point,
                    max_evaluation_point_set.birth_year_point.point,
                ],
            ).values_list("member_id", flat=True)
        )
        return member_ids

    def find_by_member_id(self, member_id: MemberID) -> EvaluationPointSet:
        evaluation_data: EvaluationPointSet = EvaluationPointSet(
            work_point=EvaluationPoint(0),
            income_point=EvaluationPoint(0),
            asset_point=EvaluationPoint(0),
            background_point=EvaluationPoint(0),
            education_point=EvaluationPoint(0),
            appearance_point=EvaluationPoint(0),
            birth_year_point=EvaluationPoint(0),
        )
        evaluation_orm: Optional[MemberEvaluationORM] = get_obj_or_none(MemberEvaluationORM, member_id=member_id)
        if evaluation_orm:
            evaluation_data = EvaluationPointSet(
                work_point=EvaluationPoint(evaluation_orm.work_point),
                income_point=EvaluationPoint(evaluation_orm.income_point),
                asset_point=EvaluationPoint(evaluation_orm.asset_point),
                background_point=EvaluationPoint(evaluation_orm.background_point),
                education_point=EvaluationPoint(evaluation_orm.education_point),
                appearance_point=EvaluationPoint(evaluation_orm.appearance_point),
                birth_year_point=EvaluationPoint(evaluation_orm.birth_year_point),
            )
        return evaluation_data


class EvaluationWriteRepository:

    def update_or_create_work_evaluation_point(
        self, member_id: MemberID, evaluation_point: EvaluationPoint
    ) -> EvaluationPoint:
        evaluation_orm: MemberEvaluationORM
        evaluation_orm, _ = MemberEvaluationORM.objects.update_or_create(
            member_id=member_id, defaults={"member_id": member_id, "work_point": evaluation_point.point}
        )
        return EvaluationPoint(point=evaluation_orm.work_point)

    def update_or_create_asset_evaluation_point(
        self, member_id: MemberID, evaluation_point: EvaluationPoint
    ) -> EvaluationPoint:
        evaluation_orm: MemberEvaluationORM
        evaluation_orm, _ = MemberEvaluationORM.objects.update_or_create(
            member_id=member_id, defaults={"member_id": member_id, "asset_point": evaluation_point.point}
        )
        return EvaluationPoint(point=evaluation_orm.asset_point)

    def update_or_create_background_evaluation_point(
        self, member_id: MemberID, evaluation_point: EvaluationPoint
    ) -> EvaluationPoint:
        evaluation_orm: MemberEvaluationORM
        evaluation_orm, _ = MemberEvaluationORM.objects.update_or_create(
            member_id=member_id, defaults={"member_id": member_id, "background_point": evaluation_point.point}
        )
        return EvaluationPoint(point=evaluation_orm.background_point)

    def update_or_create_income_evaluation_point(
        self, member_id: MemberID, evaluation_point: EvaluationPoint
    ) -> EvaluationPoint:
        evaluation_orm: MemberEvaluationORM
        evaluation_orm, _ = MemberEvaluationORM.objects.update_or_create(
            member_id=member_id, defaults={"member_id": member_id, "income_point": evaluation_point.point}
        )
        return EvaluationPoint(point=evaluation_orm.income_point)

    def update_or_create_education_evaluation_point(
        self, member_id: MemberID, evaluation_point: EvaluationPoint
    ) -> EvaluationPoint:
        evaluation_orm: MemberEvaluationORM
        evaluation_orm, _ = MemberEvaluationORM.objects.update_or_create(
            member_id=member_id, defaults={"member_id": member_id, "education_point": evaluation_point.point}
        )
        return EvaluationPoint(point=evaluation_orm.education_point)

    def update_or_create_appearance_evaluation_point(
        self, member_id: MemberID, evaluation_point: EvaluationPoint
    ) -> EvaluationPoint:
        evaluation_orm: MemberEvaluationORM
        evaluation_orm, _ = MemberEvaluationORM.objects.update_or_create(
            member_id=member_id, defaults={"member_id": member_id, "appearance_point": evaluation_point.point}
        )
        return EvaluationPoint(point=evaluation_orm.appearance_point)

    def update_or_create_birth_year_evaluation_point(
        self, member_id: MemberID, evaluation_point: EvaluationPoint
    ) -> EvaluationPoint:
        evaluation_orm: MemberEvaluationORM
        evaluation_orm, _ = MemberEvaluationORM.objects.update_or_create(
            member_id=member_id, defaults={"member_id": member_id, "birth_year_point": evaluation_point.point}
        )
        return EvaluationPoint(point=evaluation_orm.birth_year_point)


class EvaluationCompoundRepository(EvaluationReadRepository, EvaluationWriteRepository): ...
