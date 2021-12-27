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
    # First, just randomly, but without overlap.
    # Later, add negative weights and order of factions to calculations.

    # Not sure, if this is the most elegant approach, but:
    # 1. Choose a random faction for the first player.
    # 2. Continue to next one making sure there are no clashes.

    savedFactions = []

    for i in playersInDatabase:
        # print(i.id)

        # from faction1-faction8 take random non blank.
        factions = [i.faction1, i.faction2, i.faction3, i.faction4, i.faction5, i.faction6, i.faction7, i.faction8]
        # Turn into a set, so that all the blanks reduce into one value.
        factions = set(factions)
        # Now we can use remove to delete the one blank. (remove() only removes the first instance, hence the list containing multiple blanks isn't optimal.)
        # Because of the eight player game option, where there are no blanks, we need a if statement here.
        if numberOfPlayers != 8:
            factions.remove('')
        # Change back into a list to enable random.choice().
        factions = list(factions)
        # print(factions)
        randomFaction = random.choice(factions)
        # print(randomFaction)

        i.resultFaction = randomFaction
        i.save()
        savedFactions.append(randomFaction)

        # print(savedFactions)

        # Make sure it doesn't clash with those already saved.
        while savedFactions.count(randomFaction) > 1:
            # Change i's resultFaction.
            randomFaction = random.choice(factions)
            savedFactions.append(randomFaction)
            i.resultFaction = randomFaction
        i.save()

    # After dealing out the factions, send results via email.
    sendResults(playersInDatabase)


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
