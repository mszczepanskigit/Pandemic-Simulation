from random import randint, sample
from Day import Day
from Events import NormalDay
from Population import Population
from Virus import Virus
from Vaccine import Vaccine
import matplotlib.pyplot as plt


class Simulation:
    def __init__(self, populations: list, days: list, events: dict):
        self.populations = populations
        self.days = days
        self.events = events

    def simulation_start(self, virus: Virus, vac: Vaccine):
        diary = ""
        for population in self.populations:
            diary += str(population) + "\n"
            pop_budget_per_day = population.government.budget
            zero_day = self.set_zero_day(population)
            diary += str(zero_day) + "\n" + 30 * "-" + "\n"
            for day in self.days:
                day.null_lists()
                population.government.budget = pop_budget_per_day
                list_of_alive = population.get_alive()
                event_this_day = NormalDay()
                if population.government.kav:
                    prob = randint(1, 100)
                    for event in self.events:
                        if self.events[event][0] <= prob <= self.events[event][1]:
                            event_this_day = event
                num_of_meet, add_budget, add_deaths_tuple = \
                    event_this_day.set_parameters_of_the_day(population)
                num_of_meet = int(num_of_meet * len(list_of_alive) / len(population.people))
                budget_for_vacs = population.government.budget + add_budget
                buyed_vaccines = budget_for_vacs // abs(vac.price)
                if add_deaths_tuple[1] == "all":
                    for _ in range(num_of_meet):
                        first_person = sample(list_of_alive, 1)[0]
                        second_person = sample(list_of_alive, 1)[0]
                        first_person.die()
                        second_person.die()
                else:
                    for _ in range(num_of_meet):
                        first_person = sample(list_of_alive, 1)[0]
                        second_person = sample(list_of_alive, 1)[0]
                        first_person.meet(second_person, virus, vac)
                if add_deaths_tuple[1] == "medic" or add_deaths_tuple[1] == "slave":
                    deaths, death_job = add_deaths_tuple
                    for person in list_of_alive:
                        if person.job == death_job:
                            person.die()
                            deaths -= 1
                        if deaths <= 0:
                            break
                day.set_lists(population)
                num_of_healthy, num_of_infected, num_of_dead = day.get_numbers()
                num_of_medics = 0
                for person in list_of_alive:
                    if person.is_infected():
                        if virus.mort > randint(1, 100):
                            person.die()
                    if person.job == "medic":
                        num_of_medics += 1
                if population.government.kav:
                    if vac.done:
                        if num_of_medics > 0:
                            population.cure_people(buyed_vaccines, vac)
                        else:
                            diary += "No medics!\n"
                    else:
                        vac.make_progress(population.government.lor * 0.3 * randint(5, 15))
                        if vac.done:
                            diary += "Vaccine is done!\n"
                else:
                    if num_of_infected > 0.2 * population.government.lor * 0.05 * len(population.people):
                        population.government.kav = True
                        population.attitude_to_gov *= 0.6
                        diary += "We know about virus!\n"
                if 2 > randint(1, 100):
                    virus.mutate(randint(0, 10), randint(1, 10), randint(1, 3))
                    diary += f"Virus mutated to: {str(virus)}!\n"
                diary += f"Day {day.day} has {day.get_numbers()}\n" + 30 * "-" + "\n"
            self.plot_data(population)
        self.save_data(diary)

    @staticmethod
    def save_data(diary):
        with open("symulacja.txt", 'w', encoding='utf-8') as file:
            file.write(diary)
            file.write(10 * "-")

    @staticmethod
    def set_zero_day(population: Population):
        zero_day = Day(0)
        zero_day.set_lists(population)
        return zero_day

    def plot_data(self, population: Population):
        healthy = []
        infected = []
        dead = []
        for day in self.days:
            numbers = day.get_numbers()
            healthy.append(numbers[0])
            infected.append(numbers[1])
            dead.append(numbers[2])
        plt.plot([x for x in range(len(self.days))], healthy, label="Healthy")
        plt.plot([x for x in range(len(self.days))], infected, label="Infected")
        plt.plot([x for x in range(len(self.days))], dead, label="Dead")
        plt.title("Epidemic for {} population".format(population.name))
        plt.legend()
        plt.savefig("{}.png".format(population.name))
        plt.show()
