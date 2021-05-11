"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from raterprojectapi.models import Gamer, Game, GameReview
from django.contrib.auth.models import User


class GameReviews(ViewSet):
    """Rater Project Game Reviews"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        try:
            game_review = GameReview.objects.get(pk=pk)
            serializer = GameReviewSerializer(game_review, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        
        game_reviews = GameReview.objects.all()
        game = self.request.query_params.get("game", None)
        
        # Set the `joined` property on every event
       
        if game is not None:
            game_reviews = game_reviews.filter(game_id__id= game)
        # game = self.request.query_params.get('gameId', None)
        # gamer = Gamer.objects.get(user=request.auth.user)
        # reviewed_game = Game.objects.get(pk="game_id")
        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = GameReviewSerializer(
            game_reviews, many=True, context={'request': request})
        return Response(serializer.data)

class GameReviewSerializer(serializers.ModelSerializer):
    """JSON serializer for game types

    Arguments:
        serializers
    """
    class Meta:
        model = GameReview
        fields = ('id', 'review_descrip', 'gamer_id', 'game_id', 'rating')
        depth = 1

class Reviewer(serializers.ModelSerializer):
    """JSON serializer for event organizer"""
    user = GameReviewSerializer(many=False)

    class Meta:
        model = Gamer
        fields = ['user']

class GamerReviewerUser(serializers.ModelSerializer):
    """JSON serializer for event organizer"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')

class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for event organizer"""
    class Meta:
        model = Game
        fields = ('id', 'title', 'number_of_players',  'description', 'year_released', 'estimated_time_to_play', 'age_recommendation', 'designer', 'category_id')
        depth = 1