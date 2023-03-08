class Virus:
    def __init__(self, name: str, mortality: int, contagiousness: int, strength: int):
        if mortality < 0 or mortality > 10:
            raise ValueError("Mortality has to be between 0 and 10.")
        if contagiousness < 1 or contagiousness > 10:
            raise ValueError("Contagiousness has to be between 1 and 10.")
        if strength < 1 or strength > 3:
            raise ValueError("Strength has to be between 1 and 3.")
        self.name = name
        self.mort = mortality
        self.cont = contagiousness
        self.strg = strength

    def change_mort(self, new_mort: int):
        if not new_mort in (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10):
            raise ValueError("Mortality has to be an integer between 0 and 10.")
        self.mort = new_mort

    def change_cont(self, new_cont: int):
        if not new_cont in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10):
            raise ValueError("Contagiousness has to be an integer between 1 and 10.")
        self.cont = new_cont

    def change_strg(self, new_strg: int):
        if not new_strg in (1, 2, 3):
            raise ValueError("Strength has to be 1, 2 or 3.")
        self.strg = new_strg

    def mutate(self, new_mort: int, new_cont: int, new_strg: int):
        self.name += ".1"
        self.change_mort(new_mort)
        self.change_cont(new_cont)
        self.change_strg(new_strg)

    def __str__(self):
        return "name: " + str(self.name) + ", mort: " + \
               str(self.mort) + ", cont: " + str(self.cont) + ", strg: " + str(self.strg)
