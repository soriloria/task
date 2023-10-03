from rest_framework import serializers
from .models import User, Restaurant, Menu, Vote


# serializers to use field from model in rest_framework's appearance
class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    name = serializers.CharField()
    password = serializers.CharField(write_only=True)


class Restaurantserializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address']


class Menuserializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['day_of_week', 'first', 'second', 'drinks', 'restaurant']


class Menuserializer2(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['first', 'second', 'drinks']


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'


class Restaurantserializer2(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['name', 'votes']
