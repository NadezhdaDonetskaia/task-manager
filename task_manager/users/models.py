from django.contrib.auth.models import User


class UserTask(User):

    class Meta:
        proxy = True

    @property
    def full_name(self):
        return self.get_full_name()