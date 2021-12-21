from django.db import models

class Game(models.Model):

    # Automatically create a timestamp, when a game is initialized.
    # Does this show up correctly in a proper server and database?
    # This is needed to delete old information.
    created = models.DateTimeField('created', auto_now_add=True, null=True)

    # modified = models.DateTimeField('modified', auto_now=True, null=True)
    game_id = models.CharField(max_length=9)
    numberOfPlayers = models.CharField(max_length=1)
    numberOfNegativeWeights = models.CharField(max_length=1)
    pass


# I suppose this ought to be many-to-one relationship.
# Game has multiple players, but one player has one game.

class Player(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    email = models.EmailField()

    player_id = models.CharField(max_length=9)

    faction1 = models.CharField(max_length=30, blank=True)
    faction2 = models.CharField(max_length=30, blank=True)
    faction3 = models.CharField(max_length=30, blank=True)
    faction4 = models.CharField(max_length=30, blank=True)
    faction5 = models.CharField(max_length=30, blank=True)
    faction6 = models.CharField(max_length=30, blank=True)
    faction7 = models.CharField(max_length=30, blank=True)
    faction8 = models.CharField(max_length=30, blank=True)

    resultFaction = models.CharField(max_length=30, blank=True)

    negativeFaction1 = models.CharField(max_length=30, blank=True)
    negativeFaction2 = models.CharField(max_length=30, blank=True)
    negativeFaction3 = models.CharField(max_length=30, blank=True)
    negativeFaction4 = models.CharField(max_length=30, blank=True)
    negativeFaction5 = models.CharField(max_length=30, blank=True)
    negativeFaction6 = models.CharField(max_length=30, blank=True)
    negativeFaction7 = models.CharField(max_length=30, blank=True)
    negativeFaction8 = models.CharField(max_length=30, blank=True)
