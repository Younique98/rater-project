from django.db import models

class GameCategory(models.Model):
    category_id = models.ForeignKey("Category", on_delete=models.CASCADE )
    game_id = models.ForeignKey("Game", on_delete=models.CASCADE)