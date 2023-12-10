from django.urls import path
from .views import *


urlpatterns = [
    path('buy/', BuyCoinView.as_view()),
    path('sell/', SellCoinView.as_view()),
    path('myholdings/', GETMyHoldingsView.as_view()),
    path('mywatchlist/', MyWatchlistView.as_view()),
    path('news/', NEWSView.as_view()),
    path('coindetails/', CoinDetailsView.as_view()),
    path('transactions/', TransactionsView.as_view()),
    path('inwatchlist/', InWatchlistView.as_view()),
    path('search/', SearchView.as_view())
]
