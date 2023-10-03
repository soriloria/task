# imports of packages to use
from rest_framework.views import APIView
from .serializers import (Userserializer, Restaurantserializer, Menuserializer, LoginSerializer, Restaurantserializer2,
                          Menuserializer2)
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import User, Restaurant, Menu, Vote
import jwt
import datetime
from django.contrib.auth import authenticate
from rest_framework.generics import CreateAPIView


# register user
class Register(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = Userserializer

    def get(self, request, *args, **kwargs):
        return Response('Registration')


# log in if data is valid and making token for 24 hours
class Login(CreateAPIView):
    serializer_class = LoginSerializer

    def get(self, request, *args, **kwargs):
        return Response('Login')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        name = serializer.validated_data['name']
        password = serializer.validated_data['password']

        user = authenticate(request, username=name, password=password)

        if user is None:
            raise AuthenticationFailed('user not found')

        if not user.check_password(password):
            raise AuthenticationFailed('incorrect password')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }

        return response


# this class to check current user and check is he authenticated
class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('unauthenticated')

        user = User.objects.filter(id=payload['id']).first()

        serializer = Userserializer(user)

        return Response(serializer.data)


# log out for current logged user
class Logout(APIView):
    def get(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            "Logged out"
        }
        return response


# class for restaurant to create
class CreateRestaurant(generics.CreateAPIView):
    def get(self, request, *args, **kwargs):
        return Response('Create Restaurant')

    queryset = Restaurant.objects.all()
    serializer_class = Restaurantserializer


# class to show available restaurants
class ShowRestaurants(generics.ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = Restaurantserializer


# class for menu to create for each day of weak (from 1 to 7)
class CreateMenuForEachDay(generics.CreateAPIView):
    def get(self, request, *args, **kwargs):
        return Response('Create Menu')

    queryset = Menu.objects.all()
    serializer_class = Menuserializer


# class to pick restaurants for specific day-menu change
class EditMenu(generics.RetrieveUpdateAPIView):
    serializer_class = Menuserializer

    def get_object(self):
        restaurant_id = self.kwargs.get('restaurant_id')
        day_of_week = self.kwargs.get('day_of_week')
        try:
            menu = Menu.objects.get(restaurant_id=restaurant_id, day_of_week=day_of_week)
            return menu
        except Menu.DoesNotExist:
            return None

    def put(self, request, restaurant_id, day_of_week):
        menu = self.get_object()
        if menu is None:
            return Response({'message': 'Menu not found for the specified restaurant and day.'}, status=404)

        serializer = self.get_serializer(menu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)


# class to show menus from all restaurants for today
class MenuByRestaurantView(APIView):
    def get(self, request):
        current_day_of_week = (datetime.datetime.now().weekday() + 1) % 7

        restaurants = Restaurant.objects.all()

        response_data = {}

        for restaurant in restaurants:
            try:
                menu_today = Menu.objects.filter(restaurant=restaurant, day_of_week=current_day_of_week).first()
                menu_serializer = Menuserializer2(menu_today)

                response_data[restaurant.name] = {
                    'menu_today': menu_serializer.data
                }

            except Menu.DoesNotExist:
                pass

        return Response(response_data)


# class to vote for coming to a particular restaurant
class VoteForRestaurantView(APIView):
    def get(self, request, restaurant_id):
        return Response('Vote for restaurant')

    def post(self, request, restaurant_id):
        try:
            restaurant = Restaurant.objects.get(pk=restaurant_id)
        except Restaurant.DoesNotExist:
            return Response({'error': 'Restaurant not found'})

        if request.user.is_authenticated:
            user = request.user
            if Vote.objects.filter(user=user, restaurant=restaurant).exists():
                return Response({'error': 'You have already voted for this restaurant'})

            vote = Vote(user=user, restaurant=restaurant)
            vote.save()

            restaurant.votes += 1
            restaurant.save()

            serializer = Restaurantserializer(restaurant)
            return Response(serializer.data)
        else:
            return Response({'error': 'You need to be authenticated to vote for a restaurant'})


# check all votes
class RestaurantVotesView(generics.ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = Restaurantserializer2


# reset votes
class ResetVotesView(APIView):
    def get(self, request, *args, **kwargs):
        Vote.objects.all().delete()

        Restaurant.objects.update(votes=0)

        return Response("votes reset successful")
