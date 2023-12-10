import websockets
import asyncio
import os
import django
import json
from asgiref.sync import sync_to_async
from django.conf import settings
import jwt

import logging
logging.basicConfig(format="%(message)s", level=logging.DEBUG)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smolstock.settings')
django.setup()

from Authentication.models import User
from Investments.models import Coin
from django_celery_beat.models import PeriodicTask, IntervalSchedule


@sync_to_async
def AddToCeleryBeat():
    task = PeriodicTask.objects.filter(name = 'update_coins_data')
    if not task.exists():
        schedule, created = IntervalSchedule.objects.get_or_create(every = 10, period = IntervalSchedule.SECONDS)
        task = PeriodicTask.objects.create(interval = schedule, name = 'update_coins_data', task = 'Investments.tasks.update_coins')


@sync_to_async
def RemoveFromCeleryBeat():
    task = PeriodicTask.objects.filter(name = 'update_coins_data')
    if task.exists():
        task.delete()


@sync_to_async
def holdings_data(user):
    holdings = []
    try:
        for holding in user.my_holdings.MyHoldings:
            coin = Coin.objects.get(Name = holding[0])
            holdings.append({"Name" : coin.Name, "FullName": coin.FullName, "Price": coin.Price,"ImageURL" : coin.Image, "Coins" : holding[1]})
    except:
        pass
    return holdings


@sync_to_async
def particular_holdings_data(user, reqd_coin):
    holdings = []
    try:
        for holding in user.my_holdings.MyHoldings:
            coin = Coin.objects.get(Name = holding[0])
            if reqd_coin == coin:
                holdings.append({"Name" : coin.Name, "FullName": coin.FullName, "Price": coin.Price,"ImageURL" : coin.Image, "Coins" : holding[1]})
                break
    except:
        pass
    return holdings


@sync_to_async
def watchlist_data(user):
    watchlist = []
    try:
        for watch in user.watchlist.watchlist:
            coin = Coin.objects.get(Name = watch)
            watchlist.append({'Name': coin.Name, 'FullName' : coin.FullName, 'Price': coin.Price, 'ChangePct': coin.ChangePct, 'ImageURL': coin.Image})
    except:
        pass
    return watchlist


async def socket(websocket, user):
    try:
        while True:
            coins = Coin.objects.all()
            data = []
            async for coin in coins:
                data.append({'Name': coin.Name, 'FullName' : coin.FullName, 'Price': coin.Price, 'ChangePct': coin.ChangePct, 'ImageURL': coin.Image})
            holdings = await holdings_data(user)
            watchlist = await watchlist_data(user)
            await websocket.send(json.dumps({'data': data, 'holdings' : holdings, 'watchlist' : watchlist}))
            await asyncio.sleep(10)
    except:
        return


async def single_socket(websocket, user, req):
    try:
        while True:
            coin = await get_coin(req)
            data = {'Name': coin.Name, 'FullName' : coin.FullName, 'Price': coin.Price, 'ChangePct': coin.ChangePct, 'ImageURL': coin.Image}
            holdings = await particular_holdings_data(user, coin)
            await websocket.send(json.dumps({'data': data, 'holdings' : holdings}))
            await asyncio.sleep(10)
    except:
        return


@sync_to_async
def get_coin(name):
    try:
        return Coin.objects.get(Name = name)
    except:
        return False


@sync_to_async
def get_wallet_amount(user):
    try:
        return user.wallet.amount
    except:
        return 0


@sync_to_async
def get_holdings(user):
    try:
        return user.my_holdings.MyHoldings
    except:
        return []


async def profit_socket(websocket, user):
    try:
        while True:
            wallet = await get_wallet_amount(user)
            holdings_list = await get_holdings(user)
            holdings_value = 0
            for holding in holdings_list:
                curcoin = await get_coin(holding[0])
                holdings_value += round((float(holding[1]) * curcoin.Price), 8)
            await websocket.send(json.dumps({'wallet': wallet, 'holdings_value' : holdings_value, 'total' : wallet+holdings_value}))
            await asyncio.sleep(10)
    except:
        return


async def handler(websocket, user):
    await websocket.send('authorised, enter ALL or name of the coin ,PROFIT to get current holdings')
    req = await websocket.recv()
    global connections
    connections += 1
    if connections == 1:
        await AddToCeleryBeat()
    if req == 'ALL':
        # await websocket.send('enter in format : ', json.dumps({'sorting' : 'Name, Price, ChangePct', 'order' : 'asc, dsc'}))
        # await websocket.recv()
        await socket(websocket, user)
    elif req == 'PROFIT':
        await profit_socket(websocket, user)
    else:
        coin = await get_coin(req)
        if not coin:
            await websocket.send('invalid request')
        await single_socket(websocket, user, req)
    connections -= 1
    if connections == 0:
        await RemoveFromCeleryBeat()


@sync_to_async
def get_user(tokenset):
    return User.objects.get(id = tokenset['user_id'])


async def authorise(websocket):
    await websocket.send('connection established, send token to recieve data')    
    token = await websocket.recv()
    try: 
        tokenset = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user = await get_user(tokenset)
    except:
        await websocket.send('invalid token')
        return
    await handler(websocket, user)


async def main():
    async with websockets.serve(authorise, port = 8001):
        await asyncio.Future()


connections = 0
asyncio.run(main())