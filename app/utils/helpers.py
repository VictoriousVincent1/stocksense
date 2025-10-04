# helper utility functions
#John-Phillip Sims

#I guess this will just be where we'll put any random crap we need


#class representing an entry for a past trade in a user's trade history
#   stockName is a string
#   stockPrice is a number
#   stockGrowth is a number representing how much the stock's growth percentage at time of trade
#   sharesTraded is a number
#   totalCost is a number
#   timeMade is the time and date at which the trade was carried out
class pastTrade:
    def __init__ (self, stockName, stockPrice, stockGrowth, sharesTraded, totalCost, timeMade):
        self.stockName = stockName
        self.stockPrice = stockPrice
        self.stockGrowth = stockGrowth
        self.sharesTraded = sharesTraded
        self.totalCost = totalCost
        self.timeMade = timeMade

#a class representing a stock that a user owns
class stockEntry:
    def __init__(self, stockName, amountOwned):
        self.stockName = stockName
        self.amountOwned = amountOwned

#a class containing data about a user
#   username is a string
#   currencyOwned is an number (probably a float)
#   stocksOwned is a list of stockEntry objects
#   savedArticles is a list of links
#   tradeHistory is a list of pastTrade objects sorted by chronological order
class userData:
    def __init__(self, username, currencyOwned, stocksOwned, stocksFollowed, savedArticles, tradeHistory):
        self.username = username
        self.currencyOwned = currencyOwned
        self.stocksOwned = stocksOwned
        self.stocksFollowed = stocksFollowed
        self.savedArticles = savedArticles
        self.tradeHistory = tradeHistory
