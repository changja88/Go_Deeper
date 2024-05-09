from typing import Any, Union

from django.db import models
from model_utils.models import TimeStampedModel

from applications.member.domain_layer.value_object.address import (
    Address,
    AddressUnit,
)
from application.member_context.infra_layer.django.models import (
    AddressLevel1ORM,
    AddressLevel2ORM,
)
from application.meta_context.infra_layer.django_meta.models.certification_orm import (
    CertificationORM,
)


class MemberLivingAddressORM(CertificationORM):
    member = models.OneToOneField("MemberORM", on_delete=models.CASCADE, related_name="living_address", db_index=True)
    level1 = models.ForeignKey(AddressLevel1ORM, on_delete=models.CASCADE, related_name="living_level1_address")
    level2 = models.ForeignKey(AddressLevel2ORM, on_delete=models.CASCADE, related_name="living_level2_address")

    class Meta:
        db_table = "member_living_address"
        verbose_name = "[living_address] 사용자 계정"
        verbose_name_plural = "[living_address] 사용자 계정"
        index_together = ("level1", "level2")

    def __str__(self) -> str:
        return f"[id: {self.id}] [level1_address: {self.level1}] [level2_address: {self.level2}]"

    @property
    def address(self) -> Address:
        return Address(
            level1=AddressUnit(id=self.level1.id, name=self.level1.name),
            level2=AddressUnit(id=self.level2.id, name=self.level2.name),
        )

    @address.setter
    def address(self, value: Union[Address, dict[str, Any]]) -> None:
        data = value
        if isinstance(value, Address):
            data = value.model_dump()
        if level1_id := data.get("level1", "").get("id"):
            self.level1_id = level1_id
        if level2_id := data.get("level2", "").get("id"):
            self.level2_id = level2_id


class MemberPlayingAddressORM(TimeStampedModel):
    member = models.OneToOneField("MemberORM", on_delete=models.CASCADE, related_name="playing_address", db_index=True)
    level1 = models.ForeignKey(AddressLevel1ORM, on_delete=models.CASCADE, related_name="playing_level1_address")
    level2 = models.ForeignKey(AddressLevel2ORM, on_delete=models.CASCADE, related_name="playing_level2_address")

    class Meta:
        db_table = "member_playing_address"
        verbose_name = "[playing_address] 사용자 활동 지역"
        verbose_name_plural = "[playing_address] 사용자 활동 지역"
        index_together = ("level1", "level2")

    def __str__(self) -> str:
        return f"[id: {self.id}] [level1_address: {self.level1}] [level2_address: {self.level2}]"

    @property
    def address(self) -> Address:
        return Address(
            level1=AddressUnit(id=self.level1.id, name=self.level1.name),
            level2=AddressUnit(id=self.level2.id, name=self.level2.name),
        )

    @address.setter
    def address(self, value: Union[Address, dict[str, Any]]) -> None:
        data = value
        if isinstance(value, Address):
            data = value.model_dump()

        if level1_id := data.get("level1", "").get("id"):
            self.level1_id = level1_id
        if level2_id := data.get("level2", "").get("id"):
            self.level2_id = level2_id
