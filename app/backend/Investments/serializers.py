from .models import *
from rest_framework.serializers import Serializer, ModelSerializer, CharField, FloatField, BooleanField
from .utils import *
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from datetime import date

datee = lambda : date.today().strftime("%B %d; %Y")


class BuyCoinSerializer(Serializer):
    coin_name = CharField(write_only = True)
    buy_amount = FloatField(write_only = True)

    def validate(self, data):
        user = self.context['request'].user

        try: 
            user.pan_details
        except ObjectDoesNotExist:
            raise CustomError("Verify yourself with PAN to trade", code=status.HTTP_406_NOT_ACCEPTABLE)

        coin = Coin.objects.filter(Name = data['coin_name'])
        if not coin.exists():
            raise CustomError("Coin not available to trade", code=status.HTTP_404_NOT_FOUND)

        wallet = user.wallet
        if wallet.amount < data['buy_amount']:
            raise CustomError("Insufficient wallet balance", code=status.HTTP_403_FORBIDDEN)

        if data['buy_amount'] < 1:
            raise CustomError("Invalid amount, you need to spend atleast INR 1")

        data['coin'] = coin[0]
        data['user'] = user
        data['wallet'] = wallet
        return data

    def create(self, validated_data):
        price = validated_data['coin'].Price
        coinname = validated_data['coin_name']
        amount = round(validated_data['buy_amount'], 8)

        validated_data['wallet'].amount -= amount
        validated_data['wallet'].save()

        number_of_coins = round( amount / price , 8)

        obj = validated_data['user'].transactions
        obj.transactions.append(
            f'Bought_{number_of_coins}_{coinname}_on_{datee()}_at_price_{price}')
        obj.save()

        obj = validated_data['user'].my_holdings
        update_my_holdings(obj, coinname, number_of_coins)

        return {'message' : [f'{number_of_coins} {coinname} added to your holdings']}


class SellCoinSerializer(Serializer):
    coin_name = CharField(write_only = True)
    sell_quantity = FloatField(write_only = True)

    def validate(self, data):
        user = self.context['request'].user

        try: 
            user.pan_details
        except ObjectDoesNotExist:
            raise CustomError("Verify yourself with PAN to trade", code=status.HTTP_406_NOT_ACCEPTABLE)

        coin = Coin.objects.filter(Name = data['coin_name'])
        if not coin.exists():
            raise CustomError("Coin not available to trade", code=status.HTTP_404_NOT_FOUND)

        holdings = user.my_holdings
        for holding in holdings.MyHoldings:
            if holding[0] == data['coin_name']:
                quantity = holding[1]
                break
        else:
            raise CustomError("Buy this coin first", code=status.HTTP_403_FORBIDDEN)

        if float(quantity) < data['sell_quantity']:
            raise CustomError("Not enough coins", code=status.HTTP_403_FORBIDDEN)

        data['coin'] = coin[0]
        data['user'] = user
        data['holdings'] = holdings
        return data

    def update(self, validated_data):
        number_of_coins = round(validated_data['sell_quantity'], 8)
        price = validated_data['coin'].Price
        sell_amount = round(number_of_coins * price, 8)
        coinname = validated_data['coin_name']

        obj = validated_data['user'].wallet
        obj.amount += sell_amount
        obj.save()

        obj = validated_data['user'].transactions
        obj.transactions.append(
            f'Sold_{number_of_coins}_{coinname}_on_{datee()}_at_price_{price}')
        obj.save()

        obj = validated_data['holdings']
        update_my_holdings(obj, coinname, -number_of_coins)

        return {'message' : [f'INR {sell_amount} added to your wallet']}


class MyHoldingsSerializer(ModelSerializer):
    class Meta:
        model = MyHoldings
        fields = ['MyHoldings']

    def to_representation(self, instance):
        response = []
        for holding in instance.MyHoldings:
            coin = Coin.objects.get(Name = holding[0])
            response.append([coin.Name, coin.Image, holding[1]])
        return {"MyHoldings" : response}


class MyWatchlistSerializer(ModelSerializer):
    add = BooleanField(write_only=True, default=False)
    remove = BooleanField(write_only=True, default=False)

    class Meta:
        model = MyWatchlist
        fields = ['add', 'remove', 'watchlist']
        extra_kwargs = {'watchlist': {'required': True}}

    def validate(self, data):
        if not data['add'] ^ data['remove']:
            raise CustomError('Specify whether to add or remove')
        coin = Coin.objects.filter(Name = data['watchlist'][0])
        if not coin.exists():
            raise CustomError("Coin not available to trade", code=status.HTTP_404_NOT_FOUND)
        return data
        
    def update(self, instance, validated_data):
        if validated_data['remove']:
            try:
                instance.watchlist.remove(validated_data['watchlist'][0])
            except:
                pass
        else:
            for obj in instance.watchlist:
                if obj == validated_data['watchlist'][0]:
                    break
            else:
                instance.watchlist.append(validated_data['watchlist'][0])
        instance.save()
        return validated_data


class NEWSSerializer(ModelSerializer):
    class Meta:
        model = News
        exclude = ['id']


class CoinSerializer(ModelSerializer):
    class Meta:
        model = Coin
        exclude = ['id']


class TransactionsSerializer(ModelSerializer):
    class Meta:
        model = TransactionHistory
        fields = ['transactions']
