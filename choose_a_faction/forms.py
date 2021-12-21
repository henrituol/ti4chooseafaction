from django import forms
from .models import Game

allFactions = [
        ('Select', 'Select a faction'),
        ('The Arborec', 'The Arborec'),
        ('The Barony of Letnev', 'The Barony of Letnev'),
        ('The Clan of Saar', 'The Clan of Saar'),
        ('The Embers of Muaat', 'The Embers of Muaat'),
        ('The Emirates of Hacan', 'The Emirates of Hacan'),
        ('The Federation of Sol', 'The Federation of Sol'),
        ('The Ghosts of Creuss', 'The Ghosts of Creuss'),
        ('The L1Z1X Mindnet', 'The L1Z1X Mindnet'),
        ('The Mentak Coalition', 'The Mentak Coalition'),
        ('The Naalu Collective', 'The Naalu Collective'),
        ('The Nekro Virus', 'The Nekro Virus'),
        ("Sardakk N'orr", "Sardakk N'orr"),
        ('The Universities of Jol-Nar', 'The Universities of Jol-Nar'),
        ('The Winnu', 'The Winnu'),
        ('The Xxcha Kingdom', 'The Xxcha Kingdom'),
        ('The Yin Brotherhood', 'The Yin Brotherhood'),
        ('The Yssaril Tribes', 'The Yssaril Tribes'),
        ('The Argent Flight', 'The Argent Flight'),
        ('The Empyrean', 'The Empyrean'),
        ('The Mahact Gene-Sorcerers', 'The Mahact Gene-Sorcerers'),
        ('The Naaz-Rokha Alliance', 'The Naaz-Rokha Alliance'),
        ('The Nomad', 'The Nomad'),
        ('The Titans of Ul', 'The Titans of Ul'),
        ("The Vuil'Raith Cabal", "The Vuil'Raith Cabal")
]

class MainForm(forms.Form):

    numberOfPlayers = forms.IntegerField(label='Number of players', min_value=3, max_value=8, initial="3")

    numberOfNegativeWeights = forms.IntegerField(label='For how many factions would you like to use negative weights?', min_value=0, max_value=8, initial="0")

#-----------------------------------------------------------------------------#

class EmailForm(forms.Form):
    email = forms.EmailField(label='E-mail')

#-----------------------------------------------------------------------------#

class threePlayerForm(forms.Form):
    faction1 = forms.ChoiceField(label= '1st selection', choices=allFactions)
    faction2 = forms.ChoiceField(label= '2nd selection', choices=allFactions)
    faction3 = forms.ChoiceField(label= '3rd selection', choices=allFactions)

class fourPlayerForm(forms.Form):
    faction1 = forms.ChoiceField(label= '1st selection', choices=allFactions)
    faction2 = forms.ChoiceField(label= '2nd selection', choices=allFactions)
    faction3 = forms.ChoiceField(label= '3rd selection', choices=allFactions)
    faction4 = forms.ChoiceField(label= '4th selection', choices=allFactions)


class fivePlayerForm(forms.Form):
    faction1 = forms.ChoiceField(label= '1st selection', choices=allFactions)
    faction2 = forms.ChoiceField(label= '2nd selection', choices=allFactions)
    faction3 = forms.ChoiceField(label= '3rd selection', choices=allFactions)
    faction4 = forms.ChoiceField(label= '4th selection', choices=allFactions)
    faction5 = forms.ChoiceField(label= '5th selection', choices=allFactions)


class sixPlayerForm(forms.Form):
    faction1 = forms.ChoiceField(label= '1st selection', choices=allFactions)
    faction2 = forms.ChoiceField(label= '2nd selection', choices=allFactions)
    faction3 = forms.ChoiceField(label= '3rd selection', choices=allFactions)
    faction4 = forms.ChoiceField(label= '4th selection', choices=allFactions)
    faction5 = forms.ChoiceField(label= '5th selection', choices=allFactions)
    faction6 = forms.ChoiceField(label= '6th selection', choices=allFactions)


class sevenPlayerForm(forms.Form):
    faction1 = forms.ChoiceField(label= '1st selection', choices=allFactions)
    faction2 = forms.ChoiceField(label= '2nd selection', choices=allFactions)
    faction3 = forms.ChoiceField(label= '3rd selection', choices=allFactions)
    faction4 = forms.ChoiceField(label= '4th selection', choices=allFactions)
    faction5 = forms.ChoiceField(label= '5th selection', choices=allFactions)
    faction6 = forms.ChoiceField(label= '6th selection', choices=allFactions)
    faction7 = forms.ChoiceField(label= '7th selection', choices=allFactions)

class eightPlayerForm(forms.Form):
    faction1 = forms.ChoiceField(label= '1st selection', choices=allFactions)
    faction2 = forms.ChoiceField(label= '2nd selection', choices=allFactions)
    faction3 = forms.ChoiceField(label= '3rd selection', choices=allFactions)
    faction4 = forms.ChoiceField(label= '4th selection', choices=allFactions)
    faction5 = forms.ChoiceField(label= '5th selection', choices=allFactions)
    faction6 = forms.ChoiceField(label= '6th selection', choices=allFactions)
    faction7 = forms.ChoiceField(label= '7th selection', choices=allFactions)
    faction8 = forms.ChoiceField(label= '8th selection', choices=allFactions)


#-----------------------------------------------------------------------------#
class oneWeightForm(forms.Form):
    faction1 = forms.ChoiceField(label= '1st selection', choices=allFactions, required=False)

class twoWeightForm(forms.Form):
    faction1 = forms.ChoiceField(label= '1st selection', choices=allFactions, required=False)
    faction2 = forms.ChoiceField(label= '2nd selection', choices=allFactions, required=False)

class threeWeightForm(forms.Form):
    faction1 = forms.ChoiceField(label= '1st selection', choices=allFactions, required=False)
    faction2 = forms.ChoiceField(label= '2nd selection', choices=allFactions, required=False)
    faction3 = forms.ChoiceField(label= '3rd selection', choices=allFactions, required=False)

class fourWeightForm(forms.Form):
    faction1 = forms.ChoiceField(label= '1st selection', choices=allFactions, required=False)
    faction2 = forms.ChoiceField(label= '2nd selection', choices=allFactions, required=False)
    faction3 = forms.ChoiceField(label= '3rd selection', choices=allFactions, required=False)
    faction4 = forms.ChoiceField(label= '4th selection', choices=allFactions, required=False)


class fiveWeightForm(forms.Form):
    faction1 = forms.ChoiceField(label= '1st selection', choices=allFactions, required=False)
    faction2 = forms.ChoiceField(label= '2nd selection', choices=allFactions, required=False)
    faction3 = forms.ChoiceField(label= '3rd selection', choices=allFactions, required=False)
    faction4 = forms.ChoiceField(label= '4th selection', choices=allFactions, required=False)
    faction5 = forms.ChoiceField(label= '5th selection', choices=allFactions, required=False)


class sixWeightForm(forms.Form):
    faction1 = forms.ChoiceField(label= '1st selection', choices=allFactions, required=False)
    faction2 = forms.ChoiceField(label= '2nd selection', choices=allFactions, required=False)
    faction3 = forms.ChoiceField(label= '3rd selection', choices=allFactions, required=False)
    faction4 = forms.ChoiceField(label= '4th selection', choices=allFactions, required=False)
    faction5 = forms.ChoiceField(label= '5th selection', choices=allFactions, required=False)
    faction6 = forms.ChoiceField(label= '6th selection', choices=allFactions, required=False)


class sevenWeightForm(forms.Form):
    faction1 = forms.ChoiceField(label= '1st selection', choices=allFactions, required=False)
    faction2 = forms.ChoiceField(label= '2nd selection', choices=allFactions, required=False)
    faction3 = forms.ChoiceField(label= '3rd selection', choices=allFactions, required=False)
    faction4 = forms.ChoiceField(label= '4th selection', choices=allFactions, required=False)
    faction5 = forms.ChoiceField(label= '5th selection', choices=allFactions, required=False)
    faction6 = forms.ChoiceField(label= '6th selection', choices=allFactions, required=False)
    faction7 = forms.ChoiceField(label= '7th selection', choices=allFactions, required=False)

class eightWeightForm(forms.Form):
    faction1 = forms.ChoiceField(label= '1st selection', choices=allFactions, required=False)
    faction2 = forms.ChoiceField(label= '2nd selection', choices=allFactions, required=False)
    faction3 = forms.ChoiceField(label= '3rd selection', choices=allFactions, required=False)
    faction4 = forms.ChoiceField(label= '4th selection', choices=allFactions, required=False)
    faction5 = forms.ChoiceField(label= '5th selection', choices=allFactions, required=False)
    faction6 = forms.ChoiceField(label= '6th selection', choices=allFactions, required=False)
    faction7 = forms.ChoiceField(label= '7th selection', choices=allFactions, required=False)
    faction8 = forms.ChoiceField(label= '8th selection', choices=allFactions, required=False)
