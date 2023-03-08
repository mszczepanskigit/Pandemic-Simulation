from Virus import Virus


class Vaccine:
    def __init__(self, name: str, price: int, virus: Virus,
                 mortality=0, efficiency=50):
        if price == 0:
            raise ValueError("Price can not be zero.")
        if mortality < 0 or mortality > 100:
            raise ValueError("Mortality has to be between 0 and 100.")
        if efficiency < 0 or efficiency > 100:
            raise ValueError("Efficiency has to be between 0 and 100.")
        self.name = name
        self.mortality = mortality
        self.done = False
        self.progress = 0
        self.price = price
        self.virus = virus
        self.efficiency = efficiency

    def make_progress(self, new_progress):
        self.progress += new_progress
        if self.progress >= 100:
            self.done = True
        if self.progress < 0:
            self.progress = 0
