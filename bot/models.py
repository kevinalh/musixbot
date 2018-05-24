from django.db import models


class BotUser(models.Model):
    psid = models.TextField(unique=True)

    def __str__(self):
        return self.psid
