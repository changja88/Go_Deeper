from Python.Repository_Pattern.repositories.user_repository import UserRepository


class UserService:

    def get_user_by_id(self, user_id):
        UserRepository.get_user_by_id(user_id=user_id)
