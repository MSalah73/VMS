from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    pass
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class Vessel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, null=False, blank=False,)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    # From https://bbs.naccscenter.com/naccs/dfw/web/data/code/scac-code/senpaku_n.pdf and a quick google seach
    # it seems the char limit is 8 but just to be safe I will leave it as 10.
    # in a real world project these codes have a specification for formatting and character limit.
    naccs_code = models.CharField(
        max_length=10, unique=True, null=False, blank=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        self.naccs_code = self.naccs_code.upper()
        super().save(*args, **kwargs)  # Call the "real" save() method.
