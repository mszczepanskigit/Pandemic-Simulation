class Day:
    def __init__(self, day: int):
        self.day = day
        self.healthy = []
        self.infected = []
        self.dead = []

    def get_healthy(self):
        return self.healthy

    def get_infected(self):
        return self.infected

    def get_dead(self):
        return self.dead

    def set_lists(self, population):
        for person in population.people:
            if person.is_dead():
                self.dead.append(person)
            else:
                if person.is_infected():
                    self.infected.append(person)
                else:
                    self.healthy.append(person)

    def get_numbers(self):
        return len(self.healthy), len(self.infected), len(self.dead)

    def null_lists(self):
        self.healthy = []
        self.infected = []
        self.dead = []

    def __str__(self):
        return f"Day {self.day} has {self.get_numbers()}."
