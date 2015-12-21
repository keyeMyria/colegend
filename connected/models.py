from django.db import models
from django.utils.translation import ugettext as _
from core.models import AutoOwnedBase, TimeStampedBase


class Connected(AutoOwnedBase, TimeStampedBase):
    """
    A django model representing the 'connected' path of the user.
    """
    legend_introduction = models.BooleanField(default=False)
    legend = models.BooleanField(default=False)

    guidelines_introduction = models.BooleanField(default=False)
    guidelines = models.BooleanField(default=False)

    chat_introduction = models.BooleanField(default=False)
    chat = models.BooleanField(default=False)

    guide_introduction = models.BooleanField(default=False)
    guide = models.BooleanField(default=False)

    virtual_room_introduction = models.BooleanField(default=False)
    virtual_room = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('connected path')
        verbose_name_plural = _('connected path')

    def __str__(self):
        return _("Connected path of {}").format(self.owner)
