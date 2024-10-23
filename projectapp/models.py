from django.db import models
import json

class Rule(models.Model):
    rule_string = models.TextField()
    ast = models.JSONField(default=dict)

    def __str__(self):
        return self.rule_string
