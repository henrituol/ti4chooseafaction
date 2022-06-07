# Helper functions for views etc.
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail

import random

from .models import Game


#-----------------------------------------------------------------------------#
#
# Page redirects
#-----------------------------------------------------------------------------#
def toEmailPage(numberOfPlayers, numberOfNegativeWeights, game_id):
    return HttpResponseRedirect('/'
    +str(numberOfPlayers)+'-'
    +str(numberOfNegativeWeights)+'-'
    +str(game_id)+'/'
    )


def toFactionSelectionPage(numberOfPlayers, numberOfNegativeWeights, game_id, player_id):
    return HttpResponseRedirect('/'
    +str(numberOfPlayers)+'-'
    +str(numberOfNegativeWeights)+'-'
    +str(game_id)+'/'
    +str(player_id)+
    '/choose-your-factions/'
    )

def toNegativeWeightsPage(numberOfPlayers, numberOfNegativeWeights, game_id, player_id):
    return HttpResponseRedirect('/'
    +str(numberOfPlayers)+'-'
    +str(numberOfNegativeWeights)+'-'
    +str(game_id)+'/'
    +str(player_id)+
    '/negative-weights/'
    )


def toThankYouPage(numberOfPlayers, numberOfNegativeWeights, game_id):
    return HttpResponseRedirect('/'
    +str(numberOfPlayers)+'-'
    +str(numberOfNegativeWeights)+'-'
    +str(game_id)+'/thank-you-for-using-TI4-tools/'
    )

#-----------------------------------------------------------------------------#
#
# Deal out the factions.
#-----------------------------------------------------------------------------#
def raffleTime(playersInDatabase, numberOfPlayers):
    # Deal out the factions.

    # Not sure, if this is the most elegant approach, but:
    # 1. Choose a faction for the first player. First selection has the highest probability of being chosen etc.
    # 2. Continue to next one making sure there are no clashes.

    savedFactions = []

    for i in playersInDatabase:

        factions = [i.faction1, i.faction2, i.faction3, i.faction4, i.faction5, i.faction6, i.faction7, i.faction8]

        # Remove blanks in less than 8-player games.
        factions = list(filter(None, factions))

        # Totally random vs. weighted raffle
        #randomFaction = random.choice(factions)
        randomFaction = weightedRaffle(factions)

        i.resultFaction = randomFaction
        i.save()
        savedFactions.append(randomFaction)
        print(randomFaction)

        # Make sure it doesn't clash with those already saved.
        while savedFactions.count(randomFaction) > 1:
            # Change i's resultFaction.
            #randomFaction = random.choice(factions)
            randomFaction = weightedRaffle(factions)
            savedFactions.append(randomFaction)
            i.resultFaction = randomFaction
            print(randomFaction)
        i.save()

    # After dealing out the factions, send results via email.
    sendResults(playersInDatabase)

#-----------------------------------------------------------------------------#
#
# Weighted raffle addon to the Raffle Time.
#-----------------------------------------------------------------------------#
def weightedRaffle(factions):

    # How many factions there are in the list?
    numberOfSelectedFactions = len(factions)

    # Relative probabilities
    probabilities = [64, 32, 16, 8, 4, 2, 1, 1]

    #
    weightsOfFactions = probabilities[:numberOfSelectedFactions]

    # Select a random faction within set probabilities.
    resultFaction = random.choices(factions, weights = weightsOfFactions, k = 1)
    # The above code is a list containing one element. How to access the element straight? I suppose, this is the way:
    resultFaction = resultFaction[0]

    return resultFaction

#-----------------------------------------------------------------------------#
#
# Send factions with email
#-----------------------------------------------------------------------------#

def sendResults(playersInDatabase):
    for i in playersInDatabase:
        subject = "Twilight Imperium 4 faction"

        gameOfThePlayer = Game.objects.get(id=i.game_id)

        idOfTheGame = str(gameOfThePlayer.numberOfPlayers)+'-'+str(gameOfThePlayer.numberOfNegativeWeights)+'-'+str(gameOfThePlayer.game_id)

        message = "Your faction in the game " + idOfTheGame + " is " + i.resultFaction + ". Do not reply to this email."

        #print(i.email)
        fromEmail = settings.EMAIL_HOST_USER
        recipient = [i.email] # Must be a list

        # For testing purposes.
        # print(subject + message + fromEmail + str(recipient))
        """ Enable this in production. """
        send_mail(subject, message, fromEmail, recipient)

    # After sending the emails, delete game along with the players from the database.
    # I suppose I cannot refer to gameOfThePlayer, because it is local in the loop, but let's take the first player from the playersInDatabase and delete his/her game.
    gameData = Game.objects.get(id=playersInDatabase[1].game_id)
    """ Enable this in production. """
    gameData.delete()


#-----------------------------------------------------------------------------#
#
# Other helpers
#-----------------------------------------------------------------------------#

# To render number as a word in the HTML view. Looks better than just a number.
def numberToWord(numberOfPlayers):
    if numberOfPlayers == 3:
        return "three"
    if numberOfPlayers == 4:
        return "four"
    if numberOfPlayers == 5:
        return "five"
    if numberOfPlayers == 6:
        return "six"
    if numberOfPlayers == 7:
        return "seven"
    if numberOfPlayers == 8:
        return "eight"
