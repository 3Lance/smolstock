from django.core.management.base import BaseCommand
import cryptocompare
from Investments.models import Coin


class Command(BaseCommand):
    """
    Command to add cryptocurrencies to the database

    Usage:
        python manage.py add_coins_to_db
    """

    help = "Add cryptocurrencies to the database"

    def handle(self, *args, **options):
        """Function to add cryptocurrencies to the database"""
        # adding the coins to the database and updating if already present
        try:
            # fetching all the INR coins from Zecoex exchange
            coins_in_exchange = [
                coin['fsym']
                for coin in cryptocompare.get_pairs(exchange='btse')
                if coin['tsym'] == 'INR'
                                ]
            # fetching the details of all the coins from cryptocompare
            coin_details = cryptocompare.get_coin_list(format=False)

            Coin.objects.bulk_create(
                [
                    Coin(
                        Name=coin_details[coin]['Symbol'],
                        FullName=coin_details[coin]['CoinName'],
                        Image=f"cryptocompare.com{coin_details[coin]['ImageUrl']}",
                        Description=coin_details[coin]['Description'],
                    )
                    for coin in set(coins_in_exchange)
                    if coin in coin_details
                ],
                update_conflicts=True,
                unique_fields=['Name'],
                update_fields=['Image', 'Description'],
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f"Error while adding coins to the database: {e}".strip()
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    "Successfully added coins to the database"
                )
            )
        finally:
            self.stdout.write(
                self.style.NOTICE(
                    f"Coins in the database: {Coin.objects.count()}"
                )
            )
