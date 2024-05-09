from applications.common.type import MemberID
from application.member_context.infra_layer.django.models import BearerTokenORM


class TokenService:
    def find_token_by(self, member_id: MemberID) -> BearerTokenORM:
        token: BearerTokenORM = BearerTokenORM.objects.get(member_id=member_id)
        return token

    def register_by(self, member_id: MemberID) -> BearerTokenORM:
        token: BearerTokenORM = BearerTokenORM.objects.create(member_id=member_id)
        return token
