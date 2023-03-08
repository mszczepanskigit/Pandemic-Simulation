from random import shuffle, sample, choices, randint
from Person import Person


class Population:
    def __init__(self, name: str):
        self.name = name
        self.people = []
        self.government = None
        self.attitude_to_gov = 0
        self.economy_level = 0

    def change_attitude(self, new_attitude):
        self.attitude_to_gov = new_attitude

    def change_economy(self, new_level):
        self.economy_level = new_level

    def list_of_not_vaccined(self):
        lst = []
        for person in self.people:
            if not person.is_resistant():
                lst.append(person)
        return lst

    def list_of_vaccined(self):
        lst = []
        for person in self.people:
            if person.is_resistant():
                lst.append(person)
        return lst

    def cure_people(self, number_of_cures, vac):
        people_to_cure = self.list_of_not_vaccined()
        number_of_not_vaccined = len(people_to_cure)
        shuffle(people_to_cure)

        if number_of_cures >= number_of_not_vaccined:
            for person in people_to_cure:
                person.get_vac(vac)
        else:
            for i in range(number_of_cures):
                people_to_cure[i].get_vac(vac)

    def set_population(self, num_of_people, government, pot_economy_level,
                       hand_min=1, distribution=(0.25, 0.25, 0.25, 0.25), jobs=("jobless", "medic", "slave", "thief")):
        if num_of_people < 100:
            num_of_people = 100
        if 1 > pot_economy_level or 10 < pot_economy_level:
            pot_economy_level = randint(1, 10)
        if hand_min < 1 or hand_min > 5:
            hand_min = 1
        if len(distribution) != len(jobs):
            raise ValueError("Job list must have the same length as a distribution list")
        self.people = [Person(id,
                              sample([True, False], 1)[0],
                              choices(jobs, weights=distribution)[0],
                              sample(range(hand_min, 6), 1)[0]) for id in range(num_of_people)]
        self.government = government
        self.economy_level = (5 - 2 * government.lor)/3 + pot_economy_level
        for person in self.people:
            if person.does_like_gov():
                self.attitude_to_gov += 1
        self.attitude_to_gov = 10 * self.attitude_to_gov / num_of_people

    def set_infected(self, num_of_infections):
        for i in range(num_of_infections):
            self.people[i].infected = True
        shuffle(self.people)

    def __str__(self):
        return f"Pop name: {self.name}\n" + \
               f"Pop size: {len(self.people)}\n" + \
               f"Pop gov: {self.government.name} with {self.government.lor} level of restrictions\n" + \
               f"Pop atg, eco_lev: {self.attitude_to_gov, self.economy_level}"

    def get_alive(self):
        list_of_alive = []
        for person in self.people:
            if not person.is_dead():
                list_of_alive.append(person)
        return list_of_alive
