import csv
import operator
from datetime import datetime
from datetime import date

# list of supported keywords
dates = ["/", "-"]
ranges = ["since", "before", "after"]
categories = ["food", "transfer", "shopping", "auto", "transport", "utilities", "fees"]
numbers = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", 
            "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
sizes = ["largest", "smallest", "most", "least", "top", "bottom"]

# dictionary to convert written words for numbers into integers
wordToNum = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10}

# not sure if I need this one - I might be able to just cycle thru the list of results and simply convert each item if
# it does not contain a dash or forward slash
strToNum = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10}

class Transaction():
    def __init__(self, transactionID, date, amount, description, category):
        self.transactionID = transactionID
        self.date = date
        self.amount = float(amount)
        self.description = description
        self.category = category.lower()

    def __str__(self):
        return "%d %s $%d %s %s" % (self.transactionID, self.date, self.amount, self.category, self.description)
        
    def __repr__(self):
        return "%s %s $%d %s %s" % (self.transactionID, self.date, self.amount, self.category, self.description)

# this function accepts a value, n, which will server as the number of transactions with the largest amounts to return
def largest(n):
    # list to store the largest expenses found, this list should be of size "n"
    largest = []

    # create a copy of the list of transactions, but sorted by the amount 
    sorted_x = sorted(transactions, key=operator.attrgetter('amount'))

    # get n largest transactions for printing out
    for i in range(1, n + 1):
        largest.append(sorted_x[i*-1])

    print("Here are your largest expenses:")

    for x in largest:
        print(x)

# this function accepts a value, n, which will server as the number of transactions with the largest amounts to return
def smallest(n):
    # list to store the largest expenses found, this list should be of size "n"
    smallest = []

    # create a copy of the list of transactions, but sorted by the amount 
    sorted_x = sorted(transactions, key=operator.attrgetter('amount'))

    # get n largest transactions for printing out
    for i in range(1, n + 1):
        smallest.append(sorted_x[i])

    print("Here are your smallest expenses:")

    for x in smallest:
        print(x)

# this function accepts a category to compare to the category of each transaction in the list of transactions. 
# if they match, this function will return a count of the total number of transaction that match the category,
# but also will print out the transactions.
def totalCategoryExpenses(categories):
    matches = []
    # a variable to keep the running total of expenses that match this category
    total = 0

    # loop through each transaction
    for x in transactions:
        # if category matches the current transaction's category
        for y in categories:
            if y in x.category:
                # add its amount to the total
                total += x.amount
                # add the transaction to a list for printing
                matches.append(x)

                break

    total = "{:.2f}".format(total)
    # print("There are " + total + " total transactions with the category: " + category)

    if float(total) > 0:
        print("You spent $" + str(total) + " on " + categories[0], end='')

        # MIGHT WANT TO DIFFERENTIATE BETWEEN 2 AND 3+ CATEGORIES WITH COMMAS
        if len(categories) > 1:
            for i in range(len(categories) - 1):
                print(" and " + categories[i + 1], end='')
        print(".\n")

        response = input("Would you like a list of those expenses?\n> ")
        response = response.lower()

        if "yes" in response or "sure" in response or "ya" in response or "ok" in response:
            for x in matches:
                print(x)
        else:
            print("Alright.")
    else:
        print("I'm sorry, your inquiry did not yield any results.")

# this function will take a start and an end date and return every transaction with a date that is greater than
# the start date and less than the end date, inclusive
def dateRange(start, end):
    # list to hold each transaction that lies within the date range
    inRange = []
    total = 0

    # replace any dashes with forward slashes instead
    start = start.replace("-", "/")
    end = end.replace("-", "/")

    # check if in YYYY/MM/DD format to switch to MM/DD/YYYY format
    # use datetime library to create datetime objects for comparison with the dates of each transaction date
    if start.find("/") > 2:
        st = datetime.strptime(start, "%Y/%m/%d")
    else:
        st = datetime.strptime(start, "%m/%d/%Y")

    if end.find("/") > 2:
        en = datetime.strptime(end, "%Y/%m/%d")
    else:
        en = datetime.strptime(end, "%m/%d/%Y")

    for x in transactions:
        # repeat this process for each transaction date
        curr = datetime.strptime(x.date, "%m/%d/%Y")

        # only return the transaction if it's within the desired range
        if curr >= st and curr <= en:
            inRange.append(x)
            total += 1
    
    if total > 0:
        print("There are " + str(total) + " transactions between " + str(start) + " and " + str(end))
        response = input("Would you like to see them?\n> ")
        response = response.lower()

        if "yes" in response or "sure" in response or "ya" in response or "ok" in response or "sure" in response:
            for x in inRange:
                print(x)
        else:
            print("Alright.")
    else:
        print("You do not have any transactions within that date range.")
        
# simple helper function meant to aid in the reading and parsing of the csv file
# this function accepts a substring as string and a list as a list of strings
# this function will find the first occurrence of the substring in the list
# parameter and return the index in which it was found 
def findIndex(substring, list):
    for index, string in enumerate(list):
        if substring in string:
              return index

def parseFile():
    indicies = []

    # open file with read access
    file = open("original.csv", "r")

    header = file.readline()
    header = header.split(',')

    # get the corresponding index values for each of the keyterms
    indicies.append(findIndex("Date", header))
    indicies.append(findIndex("Amount", header))
    indicies.append(findIndex("Description", header))
    indicies.append(findIndex("Category", header))

    # make tuples of each row
    with open('original.csv', newline='') as f:
        reader = csv.reader(f)
        data = [tuple(row) for row in reader]

    # insert each row of data into a list of transactions
    for i, row in enumerate(data):
        if (i != 0):
            transactions.append( Transaction(i, row[indicies[0]], row[indicies[1]], row[indicies[2]], row[indicies[3]]) )
    
    # print(*transactions, sep='\n')

def parseInput(userInput):
    # list to hold the keywords found
    result = []

    # split the string 
    words = userInput.split(' ')

    # remove any punctuation problems
    for i in range(len(words)):
        if words[i][-1] == ',' or words[i][-1] == '?' or words[i][-1] == '.':
            words[i] = words[i][:-1]

    # check the input for any of the keywords
    for x in words:
        if dates[0] in x or dates[1] in x or x in categories or (x in numbers and (dates[0] not in x or dates[1] not in x)) or x in sizes or x in ranges:
            result.append(x)

    # check for any issues with the number of keywords found, such as more than a single number (What are the top 1 5 expenses? 1 or 5? 15?)
    # for x in result:
        
    # return a curated list of the keywords found
    return result

# list to hold all of the transactions in the csv file
transactions = []

def main():
    # parse the csv
    parseFile()

    print("Hello, what would you like to know about your finances?")

    # user input loop
    while(1):
        userInput = input("> ")
        userInput = userInput.lower() # convert to all lower case for easy testing

        # call to parseInput to break down and identify keywords that are relevant to the
        # functions that provide functionality
        if len(userInput) > 1:
            keywords = parseInput(userInput)
        else:
            keywords = []
        
        if userInput.lower() == "bye" or userInput.lower() == "no" or userInput.lower() == "quit":
            keywords.append("no")

        # ensure that a keyword was found, if none are found, the chatbot simply 
        # replies that it does not understand and allows the user to retry
        if len(keywords) != 0:
            if "largest" in keywords or "most" in keywords or "top" in keywords:
                
                # find the corresponding value for n
                for x in keywords:
                    if x in numbers:
                        n = x
                        if len(n) > 2: # word-version of number
                            n = wordToNum[n]
                        else: # digit number but as string
                            n = strToNum[n]
                        break
                else: # if no number was specified, default to 1
                    n = 1

                largest(n)

            elif "smallest" in keywords or "least" in keywords or "bottom" in keywords:

                # find the corresponding value for n
                for x in keywords:
                    if x in numbers:
                        n = x
                        if len(n) > 1: # word-version of number
                            n = wordToNum[n]
                        else: # digit number but as string
                            n = strToNum[n]
                        break
                else: # if no number was specified, default to 1
                    n = 1

                smallest(n)

            elif any(item in keywords for item in categories): # "food" in userInput:
                # find all of the categories in the results list
                for x in keywords:
                    if x not in categories:
                        keywords.remove(x)

                # send the entire list of categories to the function
                totalCategoryExpenses(keywords)

            elif any(x in y for x in dates for y in keywords): # "/" in userInput or "-" in keywords:
                num = 0
                dateArgs = []
                # check whether the keywords include either 1 date or 2
                for x in keywords:
                    if "/" in x or "-" in x:
                        dateArgs.append(x)
                        num += 1
                
                today = date.today()

                # check whether keywords include words such as "since" or "before" (and a single date)
                # to use today's date or perhaps a default date like "01/01/1900" to call dateRange()
                for x in keywords:
                    # transactions after a single certain date
                    if ("since" in x or "after" in x) and num == 1:
                        dateRange(dateArgs[0], str(today))
                        break
                    # transactions before a single certain date
                    elif "before" in x and num == 1:
                        dateRange("01/01/1900", dateArgs[0])
                        break
                    # transactions on a single date
                    elif num == 1:
                        dateRange(dateArgs[0], dateArgs[0])

                # if none of those words exist (since, before, etc), then let's make sure we have 2 dates
                else:
                    # if the user provides 2 dates
                    if (num == 2):
                        dateRange(dateArgs[0], dateArgs[1])
                if num > 2:
                    print("I'm sorry, I do not understand more than 2 dates in a single question.")

                
            # ANOTHER IDEA: SINCE THERE COULD BE A NESTED QUERY LIKE: "HOW MANY *FOOD* TRANSACTIONS BETWEEN 01/01/2020 AND 02/01/2020?"
            # WHAT IF I SIMPLY CREATE ANOTHER FUNCITON THAT CHECKS IF THE RESULTANT LIST CONTAINS BOTH A CATEGORY KEYWORD AND A DATE,
            # SO THAT I CALL ANOTHER FUNCTION THAT COPIES THE FUNCTIONALITY OF BOTH THE FUNCTIONS THAT HANDLE THOSE REQUESTS INDIVIDUALLY?
            # elif ("/" in userInput or "-" in userInput) and ("food" in userInput):
                # categoriesWithinDates()
            elif "bye" in userInput or "quit" in userInput or "no" in userInput:
                break
            else:
                print("I'm sorry, I don't understand that.")
        else:
            print("I'm sorry, I don't understand that.")

        print("\nIs there anything else I can help you with?")

    print("Goodbye.")

if __name__ == '__main__': main()

# IN TERMS OF MEMORY, WHAT IF WE JUST ASK A QUESTION AFTER EACH OF THESE COMMANDS PRINTS OUT SOME INFORMATION? AND THIS
# QUESTION CAN SIMULATE A SORT OF "MEMORY" IN THE SENSE THAT IT WILL EITHER MAKE THE NECESSARY CALL(S) TO THE FUNCTIONS
# FOR ANY FOLLOW-UP QUESTIONS OR PERHAPS INTERRUPT THE NORMAL FLOW OF THIS LOOP BY PROVIDING A LIST TO SEND INTO ONE
# OF THE FUNCTIONS?

# ANOTHER IDEA: HOW ABOUT I PASS A LIST OF ARGUMENTS TO EACH FUNCTION, SO THAT EACH FUNCTION CAN SIMPLY EXTRACT THE
# ARGUMENTS THAT ARE RELEVANT TO IT

# ANOTHER IDEA: WHAT IF EACH FUNCTION ALSO CHECKS TO SEE HOW MANY RESULTS IT COMES UP WITH. INSTEAD OF THE FUNCTION
# NOT PRINTING ANYTHING, WHAT IF IT SIMPLY STATES THAT THE USER'S QUERY DID NOT YIELD ANY RESULTS? DOES THIS COUNT
# AS "BAD INPUT" HANDLING?

# Working commands:
# 1. What are my five/5 largest expenses?
# 2. How much did I spend on food or fees?
# 3. How many transactions have I had since 01/01/1900?
# 4. Bye

# Desired commands:
# 1. How many transactions over $n?