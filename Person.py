from random import randint
from Vaccine import Vaccine
from Virus import Virus


class Person:
    def __init__(self, id: int, likes_gov: bool, job: str, hand_washing_level: int,
                 infected=False):
        if hand_washing_level < 1 or hand_washing_level > 5:
            raise ValueError("Hand washing level has to be between 1 and 5.")
        self.id = abs(id)
        self.infected = infected
        self.likes_gov = likes_gov
        self.job = job
        self.hand = hand_washing_level
        self.resist = False
        self.dead = False

    def is_infected(self):
        return self.infected

    def is_dead(self):
        return self.dead

    def does_like_gov(self):
        return self.likes_gov

    def is_resistant(self):
        return self.resist

    def get_infection(self, vac: Vaccine):
        if not isinstance(vac, Vaccine):
            raise TypeError
        if vac.efficiency >= randint(1, 100) and self.is_resistant():
            pass
        else:
            self.infected = True

    def get_vac(self, vac: Vaccine):
        if not isinstance(vac, Vaccine):
            raise TypeError
        if randint(1, 100) < vac.mortality:
            self.die()
        else:
            if vac.virus.strg == 1 and 1 <= randint(1, 100) <= 100:
                self.infected = False
                self.resist = True
            elif vac.virus.strg == 2 and 1 <= randint(1, 100) <= 70:
                self.infected = False
                self.resist = True
            elif vac.virus.strg == 3 and 1 <= randint(1, 100) <= 50:
                self.infected = False
                self.resist = True
            else:
                pass

    def meet(self, other_person, virus: Virus, vac: Vaccine):
        if not (isinstance(vac, Vaccine) and isinstance(virus, Virus) and isinstance(other_person, Person)):
            raise TypeError
        if self.is_infected() or other_person.is_infected():
            if virus.cont >= randint(0, 10):
                if self.hand < 4 or other_person.hand < 4:  # 'or' or 'and'
                    self.get_infection(vac)
                    other_person.get_infection(vac)
                else:
                    if virus.strg * randint(1, 10) > 15:
                        self.get_infection(vac)
                        other_person.get_infection(vac)

    def die(self):
        self.dead = True
        self.id = -self.id

    def __str__(self):
        if self.dead:
            return "This person is dead"
        else:
            return "Person's id: " + str(self.id) +\
                   "\nOccupation: " + str(self.job) +\
                   "\nIs infected? " + str(self.is_infected()) +\
                   "\nIs vaccined? " + str(self.is_resistant()) +\
                   "\n Hand washing level: " + str(self.hand)
