from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse

import random

from .forms import * # i.e. import all the methods.

from .models import Game
from .models import Player

from .utils import toNegativeWeightsPage
from .utils import toEmailPage
from .utils import toFactionSelectionPage
from .utils import toThankYouPage
from .utils import raffleTime
from .utils import numberToWord


#-----------------------------------------------------------------------------#
#
#
# The first page: initialize a game.
#-----------------------------------------------------------------------------#

def mainform(request):

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = MainForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required

            # Save as a string to enable concatenation in redirect.
            numberOfPlayers = str(form.cleaned_data['numberOfPlayers'])
            numberOfNegativeWeights = str(form.cleaned_data['numberOfNegativeWeights'])

            # Generate an individual ID for the game.
            game_id = str(random.randint(100000000, 999999999))
            # Let's see if there's already a game with the generated id.
            # Seems quite unlikely though, but you never know.
            if Game.objects.filter(game_id=game_id).exists():
                # print("This ID already exists in the database.")
                # Create new IDs until one that doesn't exist in the database is found.
                while Game.objects.filter(game_id=game_id).exists():
                    game_id = str(random.randint(100000000, 999999999))

            individualGame = Game(numberOfPlayers=numberOfPlayers, numberOfNegativeWeights=numberOfNegativeWeights, game_id=game_id)

            # Save into the database.
            individualGame.save()

            # redirect to a new URL, i.e. email page.
            return HttpResponseRedirect('/'
            +numberOfPlayers+'-'
            +numberOfNegativeWeights+'-'
            +game_id+'/'
            )

    # if a GET (or any other method) we'll create a blank form
    else:
        form = MainForm()
        return render(request, 'gameinitialize.html', {'form': form})

#-----------------------------------------------------------------------------#
#
# The second page: initialize a player by giving an email.
#-----------------------------------------------------------------------------#

def emailform(request, numberOfPlayers, numberOfNegativeWeights, game_id):
        if request.method == 'POST':
            form = EmailForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']

                player_id = str(random.randint(100000000, 999999999))

                # Let's see if there's already a player with the generated ID.
                if Player.objects.filter(player_id=player_id).exists():
                    # print("This ID already exists in the database.")
                    # Create new IDs until one that doesn't exist in the database is found.
                    while Player.objects.filter(player_id=player_id).exists():
                        print(player_id)
                        player_id = str(random.randint(100000000, 999999999))
                        print(player_id)


                # Pass the previosly created game object to player
                theGame = Game.objects.get(game_id=game_id)
                individualPlayer = Player(player_id=player_id, email=email, game=theGame)
                individualPlayer.save()

                return toFactionSelectionPage(numberOfPlayers, numberOfNegativeWeights, game_id, player_id)

        else:
            form = EmailForm()
            # To render number as a word in the HTML view. Looks better than just a number.
            numberAsWord = numberToWord(numberOfPlayers)
            # So as to make sure that a link is easy to send forward, it might be a good idea to show it in the instructions in the beginning of the page.
            # linkToGame = str(request.build_absolute_uri())
            # linkToGame = linkToGame.replace("thank-you-for-using-TI4-tools/", "")

            linkToGame = "https://ti4.functional.technology/" +str(numberOfPlayers)+'-'+str(numberOfNegativeWeights)+'-'+str(game_id)+'/'

            return render(request, 'playerinitialize.html', {'form': form, "numberOfPlayers":numberAsWord, "linkToGame":linkToGame})

#-----------------------------------------------------------------------------#
#
#
# The third page: select factions you want to play.
#-----------------------------------------------------------------------------#

def factionform(request, numberOfPlayers, numberOfNegativeWeights, game_id, player_id):

    if numberOfPlayers == 3:

        # if this is a POST request we need to process the form data
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = threePlayerForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required

                thePlayer = Player.objects.get(player_id=player_id)

                thePlayer.faction1=form.cleaned_data['faction1']
                thePlayer.faction2=form.cleaned_data['faction2']
                thePlayer.faction3=form.cleaned_data['faction3']

                # Let's make sure that the selected factions do not contain duplicates.
                # If there are duplicates, return the same page.
                allChosenFactions = [thePlayer.faction1, thePlayer.faction2, thePlayer.faction3]
                uniqueChosenFactions = set(allChosenFactions)
                if len(allChosenFactions) != len(uniqueChosenFactions):
                    if numberOfNegativeWeights == 0:
                        return render(request, 'factionselectionsubmitguided.html', {'form': form})
                    else:
                        return render(request, 'factionselectionnextguided.html', {'form': form})

                # Let's make sure there are no "Select a faction" values.
                if 'Select' in allChosenFactions:
                    if numberOfNegativeWeights == 0:
                        return render(request, 'factionselectionsubmitguided.html', {'form': form})
                    else:
                        return render(request, 'factionselectionnextguided.html', {'form': form})

                thePlayer.save()

                return toNegativeWeightsPage(numberOfPlayers, numberOfNegativeWeights, game_id, player_id)

        else:
            form = threePlayerForm()

            # If negative weights are not used, show Submit but, else Next-button.
            if numberOfNegativeWeights == 0:
                return render(request, 'factionselectionsubmit.html', {'form': form})
            else:
                return render(request, 'factionselectionnext.html', {'form': form})

# The rest in this section is the same ase above "if numberOfPlayers == 3:"
# Only difference is the number of players.
# Could these sections be coded with less copy+paste?
# At least renderings and if statements would seem like a good candidate for a helper function. Then again, I couldn't get render working outside of views.py.

    elif numberOfPlayers == 4:
        if request.method == 'POST':
            form = fourPlayerForm(request.POST)
            if form.is_valid():
                thePlayer = Player.objects.get(player_id=player_id)

                thePlayer.faction1=form.cleaned_data['faction1']
                thePlayer.faction2=form.cleaned_data['faction2']
                thePlayer.faction3=form.cleaned_data['faction3']
                thePlayer.faction4=form.cleaned_data['faction4']

                chosenFactions = [thePlayer.faction1, thePlayer.faction2, thePlayer.faction3, thePlayer.faction4]
                if len(chosenFactions) != len(set(chosenFactions)):
                    if numberOfNegativeWeights == 0:
                        return render(request, 'factionselectionsubmitguided.html', {'form': form})
                    else:
                        return render(request, 'factionselectionnextguided.html', {'form': form})

                if 'Select' in chosenFactions:
                    if numberOfNegativeWeights == 0:
                        return render(request, 'factionselectionsubmitguided.html', {'form': form})
                    else:
                        return render(request, 'factionselectionnextguided.html', {'form': form})

                thePlayer.save()

            return toNegativeWeightsPage(numberOfPlayers, numberOfNegativeWeights, game_id, player_id)

        else:
            form = fourPlayerForm()
            if numberOfNegativeWeights == 0:
                return render(request, 'factionselectionsubmit.html', {'form': form})
            else:
                return render(request, 'factionselectionnext.html', {'form': form})

    elif numberOfPlayers == 5:
        if request.method == 'POST':
            form = fivePlayerForm(request.POST)
            if form.is_valid():
                thePlayer = Player.objects.get(player_id=player_id)

                thePlayer.faction1=form.cleaned_data['faction1']
                thePlayer.faction2=form.cleaned_data['faction2']
                thePlayer.faction3=form.cleaned_data['faction3']
                thePlayer.faction4=form.cleaned_data['faction4']
                thePlayer.faction5=form.cleaned_data['faction5']

                chosenFactions = [thePlayer.faction1, thePlayer.faction2, thePlayer.faction3, thePlayer.faction4, thePlayer.faction5]
                if len(chosenFactions) != len(set(chosenFactions)):
                    if numberOfNegativeWeights == 0:
                        return render(request, 'factionselectionsubmitguided.html', {'form': form})
                    else:
                        return render(request, 'factionselectionnextguided.html', {'form': form})

                if 'Select' in chosenFactions:
                    if numberOfNegativeWeights == 0:
                        return render(request, 'factionselectionsubmitguided.html', {'form': form})
                    else:
                        return render(request, 'factionselectionnextguided.html', {'form': form})

                thePlayer.save()

            return toNegativeWeightsPage(numberOfPlayers, numberOfNegativeWeights, game_id, player_id)

        else:
            form = fivePlayerForm()
            if numberOfNegativeWeights == 0:
                return render(request, 'factionselectionsubmit.html', {'form': form})
            else:
                return render(request, 'factionselectionnext.html', {'form': form})

    elif numberOfPlayers == 6:

        if request.method == 'POST':
            form = sixPlayerForm(request.POST)
            if form.is_valid():
                thePlayer = Player.objects.get(player_id=player_id)

                thePlayer.faction1=form.cleaned_data['faction1']
                thePlayer.faction2=form.cleaned_data['faction2']
                thePlayer.faction3=form.cleaned_data['faction3']
                thePlayer.faction4=form.cleaned_data['faction4']
                thePlayer.faction5=form.cleaned_data['faction5']
                thePlayer.faction6=form.cleaned_data['faction6']

                chosenFactions = [thePlayer.faction1, thePlayer.faction2, thePlayer.faction3, thePlayer.faction4, thePlayer.faction5, thePlayer.faction6]
                if len(chosenFactions) != len(set(chosenFactions)):
                    if numberOfNegativeWeights == 0:
                        return render(request, 'factionselectionsubmitguided.html', {'form': form})
                    else:
                        return render(request, 'factionselectionnextguided.html', {'form': form})

                if 'Select' in chosenFactions:
                    if numberOfNegativeWeights == 0:
                        return render(request, 'factionselectionsubmitguided.html', {'form': form})
                    else:
                        return render(request, 'factionselectionnextguided.html', {'form': form})

                thePlayer.save()

            return toNegativeWeightsPage(numberOfPlayers, numberOfNegativeWeights, game_id, player_id)

        else:
            form = sixPlayerForm()
            if numberOfNegativeWeights == 0:
                return render(request, 'factionselectionsubmit.html', {'form': form})
            else:
                return render(request, 'factionselectionnext.html', {'form': form})

    elif numberOfPlayers == 7:
        if request.method == 'POST':
            form = sevenPlayerForm(request.POST)
            if form.is_valid():
                thePlayer = Player.objects.get(player_id=player_id)

                thePlayer.faction1=form.cleaned_data['faction1']
                thePlayer.faction2=form.cleaned_data['faction2']
                thePlayer.faction3=form.cleaned_data['faction3']
                thePlayer.faction4=form.cleaned_data['faction4']
                thePlayer.faction5=form.cleaned_data['faction5']
                thePlayer.faction6=form.cleaned_data['faction6']
                thePlayer.faction7=form.cleaned_data['faction7']

                chosenFactions = [thePlayer.faction1, thePlayer.faction2, thePlayer.faction3, thePlayer.faction4, thePlayer.faction5, thePlayer.faction6, thePlayer.faction7]
                if len(chosenFactions) != len(set(chosenFactions)):
                    if numberOfNegativeWeights == 0:
                        return render(request, 'factionselectionsubmitguided.html', {'form': form})
                    else:
                        return render(request, 'factionselectionnextguided.html', {'form': form})

                if 'Select' in chosenFactions:
                    if numberOfNegativeWeights == 0:
                        return render(request, 'factionselectionsubmitguided.html', {'form': form})
                    else:
                        return render(request, 'factionselectionnextguided.html', {'form': form})

                thePlayer.save()

            return toNegativeWeightsPage(numberOfPlayers, numberOfNegativeWeights, game_id, player_id)

        else:
            form = sevenPlayerForm()
            if numberOfNegativeWeights == 0:
                return render(request, 'factionselectionsubmit.html', {'form': form})
            else:
                return render(request, 'factionselectionnext.html', {'form': form})

    elif numberOfPlayers == 8:
        if request.method == 'POST':
            form = eightPlayerForm(request.POST)
            if form.is_valid():
                thePlayer = Player.objects.get(player_id=player_id)

                thePlayer.faction1=form.cleaned_data['faction1']
                thePlayer.faction2=form.cleaned_data['faction2']
                thePlayer.faction3=form.cleaned_data['faction3']
                thePlayer.faction4=form.cleaned_data['faction4']
                thePlayer.faction5=form.cleaned_data['faction5']
                thePlayer.faction6=form.cleaned_data['faction6']
                thePlayer.faction7=form.cleaned_data['faction7']
                thePlayer.faction8=form.cleaned_data['faction8']

                chosenFactions = [thePlayer.faction1, thePlayer.faction2, thePlayer.faction3, thePlayer.faction4, thePlayer.faction5, thePlayer.faction6, thePlayer.faction7, thePlayer.faction8]
                if len(chosenFactions) != len(set(chosenFactions)):
                    if numberOfNegativeWeights == 0:
                        return render(request, 'factionselectionsubmitguided.html', {'form': form})
                    else:
                        return render(request, 'factionselectionnextguided.html', {'form': form})

                if 'Select' in chosenFactions:
                    if numberOfNegativeWeights == 0:
                        return render(request, 'factionselectionsubmitguided.html', {'form': form})
                    else:
                        return render(request, 'factionselectionnextguided.html', {'form': form})

                thePlayer.save()

            return toNegativeWeightsPage(numberOfPlayers, numberOfNegativeWeights, game_id, player_id)

        else:
            form = eightPlayerForm()
            if numberOfNegativeWeights == 0:
                return render(request, 'factionselectionsubmit.html', {'form': form})
            else:
                return render(request, 'factionselectionnext.html', {'form': form})

#-----------------------------------------------------------------------------#
#
# The fourth page: select factions you do not wish to be included in the game.
#-----------------------------------------------------------------------------#

def negativeweightsform(request, numberOfPlayers, numberOfNegativeWeights, game_id, player_id):

    # When a game is full of players, deal the factions.
    # The raffle should be done here, in the last page.

    # We need to check how many players have registered.
    # The "game_id" in this view.py is slightly different to one the players have in the database, so we'll have to get the proper ID from a game's ID-field.
    gameDatabaseId = Game.objects.get(game_id=game_id).id
    # Let's make a query set of our players ordered by player_id, i.e. randomly.
    # Supposedly randomizing makes it fairer later when we run the raffle.
    playersInDatabase = Player.objects.filter(game_id=gameDatabaseId).order_by('player_id')
    # Count how many players have the proper id.
    numberOfPlayersInDatabase = playersInDatabase.count()

    if numberOfNegativeWeights == 0:
        # Finally we get to the actual if-statement:
        if numberOfPlayers == numberOfPlayersInDatabase:
            # Deal out the factions.
            # First, just randomly, but without overlap.
            # Later, add negative weights and order of factions to calculations.

            # Not sure, if this is the most elegant approach, but:
            # 1. Choose a random faction for the first player.
            # 2. Continue to next one making sure there are no clashes.
            raffleTime(playersInDatabase, numberOfPlayers)
            # Note that raffleTime also calls the method that sends the emails.

        return toThankYouPage(numberOfPlayers, numberOfNegativeWeights, game_id)

    elif numberOfNegativeWeights == 1:
        if request.method == 'POST':
            form = oneWeightForm(request.POST)
            if form.is_valid():

                thePlayer = Player.objects.get(player_id=player_id)
                thePlayer.negativeFaction1=form.cleaned_data['faction1']
                thePlayer.save()

                if numberOfPlayers == numberOfPlayersInDatabase:
                    raffleTime(playersInDatabase, numberOfPlayers)

                return toThankYouPage(numberOfPlayers, numberOfNegativeWeights, game_id)
        else:
            form = oneWeightForm()
            return render(request, 'negativessubmit.html', {'form': form})

# The rest in this section is the same ase above "numberOfNegativeWeights == 1:"
    elif numberOfNegativeWeights == 2:
        if request.method == 'POST':
            form = twoWeightForm(request.POST)
            if form.is_valid():
                thePlayer = Player.objects.get(player_id=player_id)
                thePlayer.negativeFaction1=form.cleaned_data['faction1']
                thePlayer.negativeFaction2=form.cleaned_data['faction2']
                thePlayer.save()

                if numberOfPlayers == numberOfPlayersInDatabase:
                    raffleTime(playersInDatabase, numberOfPlayers)

                return toThankYouPage(numberOfPlayers, numberOfNegativeWeights, game_id)
        else:
            form = twoWeightForm()
            return render(request, 'negativessubmit.html', {'form': form})

    elif numberOfNegativeWeights == 3:
        if request.method == 'POST':
            form = threeWeightForm(request.POST)
            if form.is_valid():
                thePlayer = Player.objects.get(player_id=player_id)
                thePlayer.negativeFaction1=form.cleaned_data['faction1']
                thePlayer.negativeFaction2=form.cleaned_data['faction2']
                thePlayer.negativeFaction3=form.cleaned_data['faction3']
                thePlayer.save()

                if numberOfPlayers == numberOfPlayersInDatabase:
                    raffleTime(playersInDatabase, numberOfPlayers)

                return toThankYouPage(numberOfPlayers, numberOfNegativeWeights, game_id)
        else:
            form = threeWeightForm()
            return render(request, 'negativessubmit.html', {'form': form})

    elif numberOfNegativeWeights == 4:
        if request.method == 'POST':
            form = fourWeightForm(request.POST)
            if form.is_valid():
                thePlayer = Player.objects.get(player_id=player_id)
                thePlayer.negativeFaction1=form.cleaned_data['faction1']
                thePlayer.negativeFaction2=form.cleaned_data['faction2']
                thePlayer.negativeFaction3=form.cleaned_data['faction3']
                thePlayer.negativeFaction4=form.cleaned_data['faction4']
                thePlayer.save()

                if numberOfPlayers == numberOfPlayersInDatabase:
                    raffleTime(playersInDatabase, numberOfPlayers)

                return toThankYouPage(numberOfPlayers, numberOfNegativeWeights, game_id)
        else:
            form = fourWeightForm()
            return render(request, 'negativessubmit.html', {'form': form})

    elif numberOfNegativeWeights == 5:
        if request.method == 'POST':
            form = fiveWeightForm(request.POST)
            if form.is_valid():
                thePlayer = Player.objects.get(player_id=player_id)
                thePlayer.negativeFaction1=form.cleaned_data['faction1']
                thePlayer.negativeFaction2=form.cleaned_data['faction2']
                thePlayer.negativeFaction3=form.cleaned_data['faction3']
                thePlayer.negativeFaction4=form.cleaned_data['faction4']
                thePlayer.negativeFaction5=form.cleaned_data['faction5']
                thePlayer.save()

                if numberOfPlayers == numberOfPlayersInDatabase:
                    raffleTime(playersInDatabase, numberOfPlayers)

                return toThankYouPage(numberOfPlayers, numberOfNegativeWeights, game_id)
        else:
            form = fiveWeightForm()
            return render(request, 'negativessubmit.html', {'form': form})

    elif numberOfNegativeWeights == 6:
        if request.method == 'POST':
            form = sixWeightForm(request.POST)
            if form.is_valid():
                thePlayer = Player.objects.get(player_id=player_id)
                thePlayer.negativeFaction1=form.cleaned_data['faction1']
                thePlayer.negativeFaction2=form.cleaned_data['faction2']
                thePlayer.negativeFaction3=form.cleaned_data['faction3']
                thePlayer.negativeFaction4=form.cleaned_data['faction4']
                thePlayer.negativeFaction5=form.cleaned_data['faction5']
                thePlayer.negativeFaction6=form.cleaned_data['faction6']
                thePlayer.save()

                if numberOfPlayers == numberOfPlayersInDatabase:
                    raffleTime(playersInDatabase, numberOfPlayers)

                return toThankYouPage(numberOfPlayers, numberOfNegativeWeights, game_id)
        else:
            form = sixWeightForm()
            return render(request, 'negativessubmit.html', {'form': form})

    elif numberOfNegativeWeights == 7:
        if request.method == 'POST':
            form = sevenWeightForm(request.POST)
            if form.is_valid():
                thePlayer = Player.objects.get(player_id=player_id)
                thePlayer.negativeFaction1=form.cleaned_data['faction1']
                thePlayer.negativeFaction2=form.cleaned_data['faction2']
                thePlayer.negativeFaction3=form.cleaned_data['faction3']
                thePlayer.negativeFaction4=form.cleaned_data['faction4']
                thePlayer.negativeFaction5=form.cleaned_data['faction5']
                thePlayer.negativeFaction6=form.cleaned_data['faction6']
                thePlayer.negativeFaction7=form.cleaned_data['faction7']
                thePlayer.save()

                if numberOfPlayers == numberOfPlayersInDatabase:
                    raffleTime(playersInDatabase, numberOfPlayers)

                return toThankYouPage(numberOfPlayers, numberOfNegativeWeights, game_id)
        else:
            form = sevenWeightForm()
            return render(request, 'negativessubmit.html', {'form': form})

    elif numberOfNegativeWeights == 8:
        if request.method == 'POST':
            form = eightWeightForm(request.POST)
            if form.is_valid():
                thePlayer = Player.objects.get(player_id=player_id)
                thePlayer.negativeFaction1=form.cleaned_data['faction1']
                thePlayer.negativeFaction2=form.cleaned_data['faction2']
                thePlayer.negativeFaction3=form.cleaned_data['faction3']
                thePlayer.negativeFaction4=form.cleaned_data['faction4']
                thePlayer.negativeFaction5=form.cleaned_data['faction5']
                thePlayer.negativeFaction6=form.cleaned_data['faction6']
                thePlayer.negativeFaction7=form.cleaned_data['faction7']
                thePlayer.negativeFaction8=form.cleaned_data['faction8']
                thePlayer.save()

                if numberOfPlayers == numberOfPlayersInDatabase:
                    raffleTime(playersInDatabase, numberOfPlayers)

                return toThankYouPage(numberOfPlayers, numberOfNegativeWeights, game_id)

        else:
            form = eightWeightForm()
            return render(request, 'negativessubmit.html', {'form': form})

#-----------------------------------------------------------------------------#
#
# The last page: thank you.
#-----------------------------------------------------------------------------#

def thankyoupage(request, numberOfPlayers, numberOfNegativeWeights, game_id):

    # linkToGame = str(request.build_absolute_uri())
    # linkToGame = linkToGame.replace("thank-you-for-using-TI4-tools/", "")

    linkToGame = "https://ti4.functional.technology/" +str(numberOfPlayers)+'-'+str(numberOfNegativeWeights)+'-'+str(game_id)+'/'

    return render(request, 'thankyou.html', {"linkToGame":linkToGame})
