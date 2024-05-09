from typing import List

from pydantic import Field, PositiveInt

from applications.common.ninja.custom_entity_model import ValueObject


class WantedPreference(ValueObject):
    alcohol_preference_meta_ids: list[PositiveInt] = Field(default_factory=list)
    smoke_preference_meta_ids: list[PositiveInt] = Field(default_factory=list)
    religion_preference_meta_ids: list[PositiveInt] = Field(default_factory=list)
    hobby_preference_meta_ids: list[PositiveInt] = Field(default_factory=list)

    def set_alcohol_preference_meta_ids(self, meta_ids: list[PositiveInt]) -> None:
        self.alcohol_preference_meta_ids.clear()
        self.alcohol_preference_meta_ids.extend(meta_ids)

    def set_smoke_preference_meta_ids(self, meta_ids: list[int]) -> None:
        self.smoke_preference_meta_ids.clear()
        self.smoke_preference_meta_ids.extend(meta_ids)

    def set_religion_preference_meta_ids(self, meta_ids: List[int]) -> None:
        self.religion_preference_meta_ids.clear()
        self.religion_preference_meta_ids.extend(meta_ids)

    def set_hobby_preference_meta_ids(self, meta_ids: List[int]) -> None:
        self.hobby_preference_meta_ids.clear()
        self.hobby_preference_meta_ids.extend(meta_ids)

    def get_all_meta_ids(self) -> set[PositiveInt]:
        all_meta_ids: set[PositiveInt] = set()
        all_meta_ids.update(set(self.alcohol_preference_meta_ids))
        all_meta_ids.update(set(self.smoke_preference_meta_ids))
        all_meta_ids.update(set(self.religion_preference_meta_ids))
        all_meta_ids.update(set(self.hobby_preference_meta_ids))
        return all_meta_ids
