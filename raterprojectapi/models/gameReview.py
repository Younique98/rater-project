from django.db import models

class GameReview(models.Model):

    review_descrip = models.CharField(max_length=50)
    gamer_id = models.ForeignKey("Gamer", on_delete=models.CASCADE, related_name="game_review_gamer")
    game_id = models.ForeignKey("Game", on_delete=models.CASCADE)
    rating = models.IntegerField()
    
    @property
    def joined(self):
        return self.__joined

    @joined.setter
    def joined(self, value):
        self.__joined = value