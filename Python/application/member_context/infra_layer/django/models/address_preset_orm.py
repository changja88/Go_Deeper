from django.db import models


class AddressLevel1ORM(models.Model):
    name = models.CharField("도/광역시", max_length=16, blank=False, null=False)
    order = models.PositiveIntegerField("노출 순위", blank=False, null=True)

    class Meta:
        db_table = "address_level1"
        verbose_name = "[address_level1] 1단계 주소 정보 - 도/광역시/특별시"
        verbose_name_plural = "[address_level1] 1단계 주소 정보 - 도/광역시/특별시"

    def __str__(self) -> str:
        return f"[id: {self.id}] [name: {self.name}]"


class AddressLevel2ORM(models.Model):
    name = models.CharField("시", max_length=16, blank=False, null=False)
    order = models.PositiveIntegerField("노출 순위", blank=False, null=True)
    level1 = models.ForeignKey(AddressLevel1ORM, on_delete=models.CASCADE, related_name="level2")

    class Meta:
        db_table = "address_level2"
        verbose_name = "[address_level2] 2단계 주소 정보 - 일반시/구"
        verbose_name_plural = "[address_level2] 2단계 주소 정보 - 도/광역시/특별시"

    def __str__(self) -> str:
        return f"[id: {self.id}] [name: {self.name}] [level1: {self.level1}]"
