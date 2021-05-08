"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from raterprojectapi.models import Game, Category, Gamer, GameReview


class Games(ViewSet):
    """Rater Project Games"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """

        # Uses the token passed in the `Authorization` header
        # gamer = Gamer.objects.get(user=request.auth.user)

        # Create a new Python instance of the Game class
        # and set its properties from what was sent in the
        # body of the request from the client.
        game = Game()
        game.title = request.data["title"]
        game.description = request.data["description"]
        game.number_of_players = request.data["numberOfPlayers"]
        game.year_released = request.data["yearReleased"]
        game.estimated_time_to_play = request.data["estimatedTimeToPlay"]
        game.age_recommendation = request.data["ageRecommendation"]
        game.designer = request.data["designer"]
        game.gamer = gamer

        # Use the Django ORM to get the record from the database
        # whose `id` is what the client passed as the
        # `categoryId` in the body of the request.
        category = Category.objects.get(pk=request.data["categoryId"])
        game.category = category

        game_review = GameReview.objects.get(pk=request.data["gameReviewId"])
        game.game_review = game_review

        # Try to save the new game to the database, then
        # serialize the game instance as JSON, and send the
        # JSON as a response to the client request
        try:
            game.save()
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)



    def retrieve(self, request, pk=None):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/games/2
            #
            # The `2` at the end of the route becomes `pk`
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a game

        Returns:
        Response -- Empty body with 204 status code
        """
        game = Game()
        game.title = request.data["title"]
        game.description = request.data["description"]
        game.number_of_players = request.data["numberOfPlayers"]
        game.year_released = request.data["yearReleased"]
        game.estimated_time_to_play = request.data["estimatedTimeToPlay"]
        game.age_recommendation = request.data["ageRecommendation"]
        game.designer = request.data["designer"]
        game.gamer = gamer

        # Use the Django ORM to get the record from the database
        # whose `id` is what the client passed as the
        # `categoryId` in the body of the request.
        category = Category.objects.get(pk=request.data["categoryId"])
        game.category = category

        game_review = GameReview.objects.get(pk=request.data["gameReviewId"])
        game.game_review = game_review
        game.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            game = Game.objects.get(pk=pk)
            game.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to games resource

        Returns:
            Response -- JSON serialized list of games
        """
        # Get all game records from the database
        games = Game.objects.all()

        # Support filtering games by type
        #    http://localhost:8000/games?type=1
        #
        # That URL will retrieve all tabletop games
        category = self.request.query_params.get('category', None)
        if category is not None:
            games = games.filter(category__id=category)

        serializer = GameSerializer(
            games, many=True, context={'request': request})
        return Response(serializer.data)

class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games

    Arguments:
        serializer type
    """
    class Meta:
        model = Game
        fields = ('id', 'title', 'number_of_players', 'description', 'year_released', 'estimated_time_to_play', 'age_recommendation', 'designer')
        depth = 1