from django.db import models

class GameCategory(models.Model):
    category_id = models.IntegerField()
    game_id = models.IntegerField()