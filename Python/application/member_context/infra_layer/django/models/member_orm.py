import uuid
from typing import Any, Union

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django_extensions.db.models import TimeStampedModel
from djchoices import ChoiceItem, DjangoChoices

from applications.member.domain_layer.value_object.enum import MemberStatus
from applications.member.domain_layer.value_object.permission import (
    AdminPermission,
)
from applications.member.domain_layer.value_object.unique_info import UniqueInfo


class MemberManager(BaseUserManager):
    use_in_migrations = True

    def create_superuser(self, password: str, nickname: str) -> AbstractBaseUser:
        user = self.model(
            name="관리자",
            nickname=nickname,
            password=password,
            birth_year=2023,
            friend_code=str(uuid.uuid4())[:6],
            status=MemberStatus.INACTIVE,
        )
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class MemberORM(TimeStampedModel, AbstractBaseUser, PermissionsMixin):
    class StatusChoices(DjangoChoices):
        registered = ChoiceItem(MemberStatus.REGISTERED, "가입만 완료")
        under_review = ChoiceItem(MemberStatus.UNDER_REVIEW, "심사중")
        recommend_off = ChoiceItem(MemberStatus.RECOMMEND_OFF, "추천제외 상태")
        active = ChoiceItem(MemberStatus.ACTIVE, "모든 심사 완료")
        inactive = ChoiceItem(MemberStatus.INACTIVE, "탈퇴 상태")

    name = models.CharField("본명", blank=False, null=False)
    phone_number = models.CharField("전화번호", blank=False, null=False)
    nickname = models.CharField("닉네임", blank=False, null=False, unique=True)
    friend_code = models.CharField("친구초대 코드 ", null=False, blank=False, unique=True)
    introduction = models.TextField("소개글", null=False, blank=True)

    status = models.CharField("상태", choices=StatusChoices.choices, blank=False, null=False)
    last_access = models.DateTimeField("마지막 접근 시간", default=timezone.now)
    is_staff = models.BooleanField("스태프 여부", default=False)
    is_superuser = models.BooleanField("슈퍼유저 여부", default=False)

    last_login = None
    email = None

    USERNAME_FIELD = "nickname"
    objects = MemberManager()

    class Meta:
        db_table = "member"
        verbose_name = "[member] 멤버 정보"
        verbose_name_plural = "[member] 정보"
        constraints = [
            models.UniqueConstraint(fields=["name", "phone_number"], name="register_unique"),
        ]

    def __str__(self) -> str:
        return f"[id: {self.id}] [name: {self.name}] [nickname: {self.nickname}] [status: {self.status}]"

    @property
    def permission(self) -> AdminPermission:
        return AdminPermission(is_superuser=self.is_superuser, is_staff=self.is_staff)

    @permission.setter
    def permission(self, value: Union[AdminPermission, dict[str, Any]]) -> None:
        data = value
        if isinstance(value, AdminPermission):
            data = value.model_dump()
        self.is_superuser = data.get("is_superuser")
        self.is_staff = data.get("is_staff")
        # self.save()
        # self.refresh_from_db()

    @property
    def unique_info(self) -> UniqueInfo:
        return UniqueInfo(
            name=self.name,
            nickname=self.nickname,
            phone_number=self.phone_number,
        )

    @unique_info.setter
    def unique_info(self, value: Union[UniqueInfo, dict[str, Any]]) -> None:
        data = value
        if isinstance(value, UniqueInfo):
            data = value.model_dump()
        self.name = data.get("name")
        self.nickname = data.get("nickname")
        self.phone_number = data.get("phone_number")
        # self.save()
        # self.refresh_from_db()
