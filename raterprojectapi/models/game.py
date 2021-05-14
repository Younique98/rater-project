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
    average_rating = models.IntegerField()
    @property
    def joined(self):
        return self.__joined

    @joined.setter
    def joined(self, value):
        self.__joined = value