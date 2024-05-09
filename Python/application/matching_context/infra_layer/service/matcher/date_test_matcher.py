from pydantic import PositiveInt

from applications.common.type import MemberID
from application.matching_context.context_layer.member_date_test_request_event_pub import (
    DateTestMetaRequestEventPublisher,
)
from application.matching_context.infra_layer.service.helper.date_test_similarity_calculator import (
    DateTestSimilarityCalculator,
)
from application.meta_context.domain_layer.entity.member_date_test_meta import (
    MemberDateTestMeta,
)


class DateTestMatcher:

    SIMILARITY_THRESHOLD: PositiveInt
    date_test_similarity_calculator: DateTestSimilarityCalculator = DateTestSimilarityCalculator()

    def __init__(self, similarity_threshold: PositiveInt):
        self.SIMILARITY_THRESHOLD = similarity_threshold

    def find_matched_member_list(self, target_member_id: MemberID, other_member_ids: list[MemberID]) -> list[MemberID]:
        member_id_with_similarity: dict[MemberID, PositiveInt] = self._calculate_all_similarities(
            target_member_id=target_member_id,
            other_member_ids=other_member_ids,
        )
        matched_member_ids: list[MemberID] = self._apply_threshold(member_id_with_similarity=member_id_with_similarity)
        return matched_member_ids

    def _calculate_all_similarities(
        self, target_member_id: MemberID, other_member_ids: list[MemberID]
    ) -> dict[MemberID, PositiveInt]:
        similarity_list: list[PositiveInt] = list()
        target_member_date_test: MemberDateTestMeta = (
            DateTestMetaRequestEventPublisher.publish_member_date_test_meta_request_event(member_id=target_member_id)
        )
        for other_member_id in other_member_ids:
            other_member_date_test: MemberDateTestMeta = (
                DateTestMetaRequestEventPublisher.publish_member_date_test_meta_request_event(member_id=other_member_id)
            )
            similarity_list.append(
                self.date_test_similarity_calculator.calculate_similarity(
                    a_member_date_test=target_member_date_test,
                    b_member_date_test=other_member_date_test,
                )
            )
        member_id_with_similarity = dict(zip(other_member_ids, similarity_list))
        return member_id_with_similarity

    def _apply_threshold(self, member_id_with_similarity: dict[MemberID, PositiveInt]) -> list[MemberID]:
        matched_member_ids: list[MemberID] = list()
        for member_id, similarity in member_id_with_similarity.items():
            if similarity >= self.SIMILARITY_THRESHOLD:
                matched_member_ids.append(member_id)
        return matched_member_ids
