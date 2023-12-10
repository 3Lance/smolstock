from celery import shared_task
import cryptocompare
import time
import queue
from threading import Thread
from .models import Coin, News
from .web_scrapping import web_scrap_news, web_scrap_coins


@shared_task(bind=True)
def update_coins(self):
    coins = Coin.objects.all()
    threadlist = []
    que = queue.Queue()
    for coin in coins:
        thread = Thread(target=lambda q, args: q.put({coin.Name: cryptocompare.get_price(
            coin.Name, currency='INR', full=True)}), args=(que, coin.Name))
        threadlist.append(thread)
        threadlist[-1].start()
        if len(threadlist) == 50:
            time.sleep(1)
    for thread in threadlist:
        thread.join()
    data = {}
    while not que.empty():
        result = que.get()
        data.update(result)
    for coin in coins:
        try:
            coindata = data[coin.Name]['RAW'][coin.Name]['INR']
            coin.Price = round(coindata['PRICE'], 8)
            coin.ChangePct = round(coindata['CHANGEPCTHOUR'], 8)
        except TypeError:
            coin.Price = 0
            coin.ChangePct = 0
        coin.save()
    # coinslist = web_scrap_coins()
    # for coin in coinslist:
    #     try:
    #         cur_coin = Coin.objects.get(Name = coin[0])
    #         cur_coin.Price = coin[1]
    #         cur_coin.ChangePct = coin[2]
    #         cur_coin.save()
    #     except:
    #         Coin.objects.create(
    #             Name = coin[0],
    #             Price = coin[1],
    #             ChangePct = coin[2]
    #         )
    return 'COINS UPDATED'


@shared_task(bind=True)
def update_news(self):
    News.objects.all().delete()
    newslist = web_scrap_news()
    for news in newslist:
        News.objects.create(
            headline = news[0],
            news = news[1],
            image = news[2]
        )
    return 'NEWS UPDATED'