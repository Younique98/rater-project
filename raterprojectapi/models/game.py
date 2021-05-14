from raterprojectapi.models.gameReview import GameReview
from django.db import models


class Game(models.Model):

    title = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    year_released = models.IntegerField()
    estimated_time_to_play = models.IntegerField()
    number_of_players = models.IntegerField()
    age_recommendation = models.IntegerField()
    designer = models.CharField(max_length=50)
    categories = models.ManyToManyField("Category", through="GameCategory")
    @property
    def average_rating(self):
        """Average rating calculated attribute for each game"""
        ratings = GameReview.objects.filter(game_id=self)

    # Sum all of the ratings for the game
        total_rating = 0
        for rating in ratings:
            total_rating += rating.rating