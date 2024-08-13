class TeamData:

    def __init__(self):
        self.team_image_dict = {
            "Agen": None,
            "Bayonne": None,
            "Biarritz": None,
            "Biarritz Olympique": None,
            "Union Bordeaux-Begles": "bordeaux.webp",
            "Bordeaux Begles": "bordeaux.webp",
            "Bourgoin": None,
            "Brive": None,
            "CA Brive": None,
            "Castres": "castres.webp",
            "Castres Olympique": "castres.webp",
            "ASM Clermont Auvergne": "cleremont.webp",
            "Cleremont Auvergne": "cleremont.webp",
            "Grenoble": None,
            "La Rochelle": "larochelle.webp",
            "Lyon": "larochelle.webp",
            "Mont de Marsan": None,
            "Montpellier": "montpellier.webp",
            "Montpellier Herault Rugby": "montpellier.webp",
            "Oyonnax": "oyonaux.webp",
            "Pau": "pau.webp",
            "Perpignan": "perpignan.webp",
            "RC Toulon": "touloun.webp",
            "Racing 92": "racing92.webp",
            "Racing Metro": "racing92.webp",
            "Section Paloise": None,
            "Stade Francais": "stadefrancais.webp",
            "Stade Francais Paris": None,
            "Stade Rochelais": None,
            "Stade Toulousain": "toulon.webp",
            "Toulon": "toulon.webp",
            "Toulouse": "toulouse.webp",
            "USAP": None,
        }

    def __str__(self):
        return "TeamDict"

    # this should be in the init
    def image_for_team(self, team_name):
        img = self.team_image_dict.get(team_name)
        if img is None:
            return "blank.jpeg"
        return img
