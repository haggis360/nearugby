class TeamData:

   def __init__(self):
       self.team_image_dict = {
           "Agen": None,
           "Bayonne": "bayonne.webp",
           "Biarritz": "biarritz.png",
           "Biarritz Olympique": "biarritz.png",
           "Union Bordeaux-Begles": "bordeaux.webp",
           "Bordeaux Begles": "bordeaux.webp",
           "Bourgoin": "bourgoin.png",
           "Brive": "brive.png",
           "CA Brive": "brive.webp",
           "Castres": "castres.webp",
           "Castres Olympique": "castres.webp",
           "ASM Clermont Auvergne": "clermont.webp",
           "Cleremont Auvergne": "clermont.webp",
           "Grenoble": None,
           "La Rochelle": "larochelle.webp",
           "Lyon": "larochelle.webp",
           "Mont de Marsan": None,
           "Montpellier": "montpellier.png",
           "Montpellier Herault Rugby": "montpellier.webp",
           "Oyonnax": "oyonaux.webp",
           "Pau": "pau.webp",
           "Perpignan": "perpignan.webp",
           "RC Toulon": "touloun.webp",
           "Racing 92": "racing92.webp",
           "Racing Metro": "racing92.webp",
           "Section Paloise": None,
           "Stade Francais": "stadefrancais.webp",
           "Stade Francais Paris": "stadefrancais.webp",
           "Stade Rochelais": None,
           "Stade Toulousain": "toulon.webp",
           "Toulon": "toulon.webp",
           "Toulouse": "toulouse.webp",
           "USAP": None,
       }

   def __str__(self):
       return "TeamDict"

   # return the icon for a team or a default image if blank

   def image_for_team(self, team_name):
       img = self.team_image_dict.get(team_name)
       if img is None:
           return "blank.png"
       return img