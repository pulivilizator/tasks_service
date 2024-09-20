from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, tg_id, username, first_name, password=None):
        user = self.model(
            tg_id=tg_id,
            username=username,
            first_name=first_name,
        )

        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, tg_id, username, first_name, password):
        user = self.create_user(
            tg_id=tg_id,
            username=username,
            first_name=first_name,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user