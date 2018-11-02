from django.db import models
from django.db.models import Q
from django.utils import timezone


class ActivityManager(models.Manager):
    use_for_related_fields = True

    def __init__(self, default_form=None):
        super(ActivityManager, self).__init__()
        if default_form is not None:
            self.base_query = Q(form=default_form)
        else:
            self.base_query = Q(id__isnull=False)

    def get_queryset(self):
        return super(ActivityManager, self).get_queryset().filter(self.base_query)

    def join(self, **kwargs):
        return self.filter(
                self.base_query &
                Q(status='open') &
                Q(start__lte=timezone.now()) &
                Q(end__gte=timezone.now()), **kwargs)

    def history(self, **kwargs):
        return self.filter(self.base_query & Q(status='close'), **kwargs)


class TeamManager(models.Manager):
    use_for_related_fields = True

    def active(self, **kwargs):
        return self.filter(is_active=True, **kwargs)

    def calc(self, **kwargs):
        return self.active(group__activity__status='calc', **kwargs)

    def owner(self, user, **kwargs):
        return self.active().filter(owner=user, **kwargs)

    def history(self, **kwargs):
        return self.active().filter(group__activity__status='close', group__activity__is_show_form=True, **kwargs)

    def review(self, user, **kwargs):
        return self.calc().filter(group__jury=user, **kwargs)

    def review_group(self, group, user):
        return self.calc(group__id=group).filter(Q(review__jury=user) | Q(review__isnull=True)).order_by('review__id')\
            .values('id',
                    'title',
                    'owner__first_name',
                    'group__activity__is_copy',
                    'group__activity__is_suggest',
                    'review',
                    'review__is_copy',
                    'review__is_suggest',
                    'review__score',
                    'review__comment'
                )


class GroupSettingManager(models.Manager):
    use_for_related_fields = True

    def jury(self, user, **kwargs):
        return self.filter(jury=user, activity__status='calc', **kwargs)
