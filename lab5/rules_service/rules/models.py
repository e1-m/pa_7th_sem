from django.db import models


class Rule(models.Model):
    class Trigger(models.TextChoices):
        ON_MESSAGE = "on_message", "On Message"
        ON_CONFIRMATION = "on_confirmation", "On Confirmation"

    class Action(models.TextChoices):
        ESCALATE = "escalate", "Escalate"
        REJECT = "reject", "Reject"

    name = models.CharField(max_length=120)
    trigger = models.CharField(
        max_length=20,
        choices=Trigger.choices,
        default=Trigger.ON_MESSAGE
    )
    condition = models.TextField()
    action = models.CharField(
        max_length=20,
        choices=Action.choices,
        default=Action.REJECT
    )
    priority = models.PositiveSmallIntegerField(default=1)
    is_enabled = models.BooleanField(default=True)
    response = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
