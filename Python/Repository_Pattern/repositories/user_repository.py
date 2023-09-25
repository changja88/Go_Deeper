from Python.Repository_Pattern.models.user import UserModel


class UserRepository:
    def get_user_by_id(self, user_id):
        return UserModel.objects.get(id=user_id)

    def create_a_user(self, name, email):
        return UserModel.objects.create(name=name, email=email)
