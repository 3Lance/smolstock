from rest_framework.generics import CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, ListAPIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.db.models.functions import Greatest
from django.contrib.postgres.search import TrigramSimilarity


class BuyCoinView(CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = BuyCoinSerializer(data = request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        data = serializer.create(serializer.validated_data)
        return Response(data, status=status.HTTP_202_ACCEPTED)


class SellCoinView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        serializer = SellCoinSerializer(data = request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        data = serializer.update(serializer.validated_data)
        return Response(data, status=status.HTTP_202_ACCEPTED)


class GETMyHoldingsView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MyHoldingsSerializer
    
    def get_object(self):
        try : 
            return MyHoldings.objects.get(user = self.request.user)
        except : 
            raise CustomError("Verify yourself with PAN to trade", code=status.HTTP_406_NOT_ACCEPTABLE)


class MyWatchlistView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MyWatchlistSerializer

    def get_object(self):
        obj, created = MyWatchlist.objects.get_or_create(user = self.request.user)
        if created:
            obj.watchlist = []
            obj.save()
        return obj


class NEWSView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NEWSSerializer
    queryset = News.objects.all()


class CoinDetailsView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CoinSerializer

    def get_object(self):
        coin = self.request.GET.get("coin")
        try:
            return Coin.objects.get(Name = coin)
        except:
            raise CustomError("Invalid Coin Requested")


class TransactionsView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionsSerializer

    def get_object(self):
        try:
            return TransactionHistory.objects.get(user = self.request.user)
        except:
            return []


class InWatchlistView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        coin = request.GET.get("coin")
        try:
            coin = Coin.objects.get(Name = coin)
        except:
            raise CustomError("Invalid Coin Requested")
        boool = False
        obj = MyWatchlist.objects.get_or_create(user = request.user)
        if coin.Name in obj[0].watchlist:
            boool = True
        return Response({'present' : boool})


class SearchView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        search = request.GET.get("search")
        coins = Coin.objects.annotate( similarity=Greatest(
                TrigramSimilarity('Name', search), TrigramSimilarity('FullName', search)
            )).filter(similarity__gte=0.3).order_by('-similarity')
        result = {}
        for coin in coins:
            result.update({ coin.Name : coin.FullName})
        return Response(result)