from django.db import models




class Follower(models.Model):

    gamer = models.ForeignKey(
        "Gamer", on_delete=models.CASCADE
    )
    game = models.ForeignKey(
        "Game", on_delete=models.CASCADE
    )
    