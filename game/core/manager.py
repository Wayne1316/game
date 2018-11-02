from django.db import models


class VisitManager(models.Manager):
    use_for_related_fields = True

    def newest(self):
        return self.all().order_by('-id')[0]
