# TODO(mirco): add more providers
# TODO(mirco): add way to query for more fields
# TODO(mirco): add way to query for text inside of feed entires
# TODO(mirco): pagination

from flask import Flask, jsonify, request
import feedparser
from datetime import datetime

from dataclasses import dataclass
from typing import List


@dataclass
class FeedEntry:
    link: str
    title: str
    description: str
    date: int
    media: str


class Feed(object):

    def __init__(self):
        pass

    def feeds(self) -> List[str]:
        raise "unimplementd"

    def get(self, f: str) -> List[FeedEntry]:
        raise "unimplementd"


class NewYorkTimes(Feed):

    def __init__(self):
        self.RSS_FEEDS = {
            "business": "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml",
            "energy_environment": "https://rss.nytimes.com/services/xml/rss/nyt/EnergyEnvironment.xml",
            "small_business": "https://rss.nytimes.com/services/xml/rss/nyt/SmallBusiness.xml",
            "economy": "https://rss.nytimes.com/services/xml/rss/nyt/Economy.xml",
            "dealbook": "https://rss.nytimes.com/services/xml/rss/nyt/Dealbook.xml",
            "media_advertising": "https://rss.nytimes.com/services/xml/rss/nyt/MediaandAdvertising.xml",
            "your_money": "https://rss.nytimes.com/services/xml/rss/nyt/YourMoney.xml",
        }

    def feeds(self) -> List[str]:
        return list(self.RSS_FEEDS.keys())

    def get(self, f: str) -> List[FeedEntry]:
        if f not in self.RSS_FEEDS.keys():
            raise Exception("no such feed")

        feed = feedparser.parse(self.RSS_FEEDS[f])

        return [
            FeedEntry(
                link=item.link,
                title=item.title,
                description=item.summary,
                date=datetime.strptime(item.get("published"), "%a, %d %b %Y %H:%M:%S %z"),
                media=item.media_content[0]["url"] if item.get("media_content") is not None and len(item.media_content) > 0 else None,
            ) for item in feed.entries
        ]


providers = [
    NewYorkTimes()
]


provider_feeds = {}
for provider in providers:
    feeds = provider.feeds()
    for feed in feeds:
        if feed in provider_feeds:
            raise "Feed Already Registered"
        provider_feeds[feed] = provider


app = Flask(__name__)


@app.route("/feeds")
def index():
    feed = request.args.get("q")

    if not feed:
        return jsonify(list(provider_feeds.keys()))

    provider = provider_feeds.get(feed)
    if not provider:
        return jsonify({'error': 'no such feed'})

    return provider.get(feed)


if __name__ == "__main__":
    app.run(debug=True)
