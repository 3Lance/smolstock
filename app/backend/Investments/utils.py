from Authentication.utils import CustomError


def update_my_holdings(obj, coinname, number_of_coins):
    found = False
    updated_holdings = []
    for i in obj.MyHoldings:
        if i[0] == coinname:
            found = True
            if round( float(i[1]) + number_of_coins, 8) == 0:
                continue
            updated_holdings.append([i[0], round( float(i[1]) + number_of_coins, 8)])
        else:
            updated_holdings.append(i)
    if not found : 
        updated_holdings.append([coinname, number_of_coins])
    obj.MyHoldings = updated_holdings
    obj.save()