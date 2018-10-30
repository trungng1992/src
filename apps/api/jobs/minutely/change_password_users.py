from django_extensions.management.jobs import MinutelyJob

class Job(MinutelyJob):
    help = "Change password user"

    def execute(self):
        from apps.api.models import  Users
        import numpy as np
        import sys
        try:
            _obUsers = Users.objects.all()
            for index in _obUsers:
                if _obUsers[index].username == "guacadmin":
                    continue

                _obUsers[index].password_hash = _passSalt = np.random.bytes(32)
                _obUsers[index].save()
        except Users.DoesNotExist:
            sys.stderr.write("There is not any user in db.")
