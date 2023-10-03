from django.urls import path
from . import views

# urls to access to functionality
urlpatterns = [
    path('register/', views.Register.as_view(), name='register'),
    path('login/', views.Login.as_view(), name='login'),
    path('user/', views.UserView.as_view(), name='user'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('create_restaurant/', views.CreateRestaurant.as_view(), name='restaurants'),
    path('create_menu/', views.CreateMenuForEachDay.as_view(), name='menu'),
    path('menu/<int:restaurant_id>/edit/<int:day_of_week>/', views.EditMenu.as_view(), name='edit'),
    path('show_restaurants/', views.ShowRestaurants.as_view(), name='show'),
    path('restaurant/menus/', views.MenuByRestaurantView.as_view(), name='menu'),
    path('vote/restaurant/<int:restaurant_id>/', views.VoteForRestaurantView.as_view(), name='vote_for_restaurant'),
    path('get_votes/', views.RestaurantVotesView.as_view(), name='votes'),
    path('reset_votes/', views.ResetVotesView.as_view(), name='reset'),
]
