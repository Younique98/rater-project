"""View module for handling requests about park areas"""
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from raterprojectapi.models import Gamer, Game


class Profile(ViewSet):
    """Gamer can see profile information"""

    def list(self, request):
        """Handle GET requests to profile resource

        Returns:
            Response -- JSON representation of user info and events
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        game = Game.objects.filter(maker=gamer)

        gamer = GamerSerializer(
            gamer, many=False, context={'request': request})
        game = GameSerializer(
            game, many=False, context={'request': request})

        # Manually construct the JSON structure you want in the response
        profile = {}
        profile["gamer"] = gamer.data
        profile["game"] = game.data

        return Response(profile)
# Serializers allow complex data such as querysets and model instances to be converted to native Python datatypes that can then be easily rendered into JSON, XML or other content types.
class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for gamer's related Django user"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')


class GamerSerializer(serializers.ModelSerializer):
    """JSON serializer for gamers"""
    user = UserSerializer(many=False)

    class Meta:
        model = Gamer
        fields = ('user', 'bio', 'currently_playing_image')


class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games"""
    class Meta:
        model = Game
        fields = ('id', 'title', 'number_of_players', 'description', 'year_released',  'estimated_time_to_play', 'age_recommendation', 'designer')
