# helper utility functions
#John-Phillip Sims

#I guess this will just be where we'll put any random crap we need


#class representing an entry for a past trade in a user's trade history
class pastTrade:
    def __init__ (self, stockName, stockPrice, sharesTraded, totalCost)
        self.stockName = stockName
        self.stockPrice = stockPrice
        self.sharesTraded = sharesTraded
        self.totalCost = totalCost

#a class representing a stock that a user owns
class stockEntry:
    def __init__(self, stockName, amountOwned):
        self.stockName = stockName
        self.amountOwned = amountOwned


#a class containing data about a user
class userData:
    def __init__(self, username, currencyOwned, stocksOwned, stocksFollowed, savedArticles, tradeHistory):
        self.username = username
        self.currencyOwned = currencyOwned
        self.stocksOwned = stocksOwned
        self.stocksFollowed = stocksFollowed
        self.savedArticles = savedArticles
        self.tradeHistory = tradeHistory
