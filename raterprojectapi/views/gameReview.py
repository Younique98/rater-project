"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from raterprojectapi.models import GameReview, Gamer, GameCategory, Game
from django.contrib.auth.models import User


class GameReviews(ViewSet):
    """Rater Project Game Reviews"""
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        # Uses the token passed in the `Authorization` header
        # gamer = Gamer.objects.get(user=request.auth.user)

        # Create a new Python instance of the Game class
        # and set its properties from what was sent in the
        # body of the request from the client.
        game_review = GameReview()
        game_review.review_descrip = request.data["reviewDescrip"]
        game_review.gamer_id = request.data["gamerId"]
        game_review.game_id = request.data["gameId"]
        game_review.rating = request.data["rating"]
        game_review.gamer = gamer

        # Use the Django ORM to get the record from the database
        # whose `id` is what the client passed as the
        category = GameCategory.objects.get(pk=request.data["categoryId"])
        game_review.category = category

        # game_review = GameReview.objects.get(pk=request.data["gameReviewId"])
        # game.game_review = game_review

        # Try to save the new game to the database, then
        # serialize the game instance as JSON, and send the
        # JSON as a response to the client request
        try:
            game_review.save()
            serializer = GameReviewSerializer(game_review, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)



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

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = GameReviewSerializer(
            game_reviews, many=True, context={'request': request})
        return Response(serializer.data)

class UserReviewSerializer(serializers.ModelSerializer):
    """JSON serializer for game types

    Arguments:
        serializers
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class GamerReviewSerializer(serializers.ModelSerializer):
    """JSON serializer for game types

    Arguments:
        serializers
    """
    user = UserReviewSerializer(many=False)
    class Meta:
        model = Gamer
        fields = ('id', 'currently_playing_image', 'user')

class GameReviewSerializer(serializers.ModelSerializer):
    """JSON serializer for game types

    Arguments:
        serializers
    """
    gamer_id = GamerReviewSerializer(many=False)
    class Meta:
        model = GameReview
        fields = ('id', 'review_descrip', 'gamer_id', 'game_id', 'rating')


class GameReviewCategory(serializers.ModelSerializer):
    """JSON serializer for game types

    Arguments:
        serializers
    """
    game_id = GameReviewSerializer(many=False)
    class Meta:
        model = GameCategory
        fields = ('id', 'category')


