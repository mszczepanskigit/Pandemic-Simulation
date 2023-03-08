import abc
from Population import Population
from random import randint


class Event(abc.ABC):  # interface
    @abc.abstractmethod
    def set_parameters_of_the_day(self, population: Population):
        raise NotImplementedError


class NormalDay(Event):

    def __init__(self):
        self.name = "NormalDay"

    def set_parameters_of_the_day(self, pop: Population):
        pop_size = len(pop.people)
        lor = 0.1 * pop.government.lor
        number_of_meetings = int(randint(int(pop_size * 0.9), int(pop_size * 1.1) + 1) - 0.6 * lor * pop_size)
        additional_budget_for_vac = 0
        additional_deaths, specific_job = None, None

        return number_of_meetings, additional_budget_for_vac, (additional_deaths, specific_job)


class NationalVaccination(Event):

    def __init__(self):
        self.name = "NationalVaccination"

    def set_parameters_of_the_day(self, pop: Population):
        pop_size = len(pop.people)
        number_of_meetings = randint(int(pop_size * 0.5), int(pop_size * 0.7) + 1)
        additional_budget_for_vac = 1000
        additional_deaths, specific_job = None, None

        return number_of_meetings, additional_budget_for_vac, (additional_deaths, specific_job)


class RobotsKillPeopleOutside(Event):

    def __init__(self):
        self.name = "RobotsKillPeopleOutside"

    def set_parameters_of_the_day(self, pop: Population):
        pop_size = len(pop.people)
        number_of_meetings = randint(int(0.5 * pop_size * 0.01), int(0.5 * pop_size * 0.1))
        additional_budget_for_vac = 500
        additional_deaths, specific_job = None, "all"

        return number_of_meetings, additional_budget_for_vac, (additional_deaths, specific_job)


class ElvisConcert(Event):

    def __init__(self):
        self.name = "ElvisConcert"

    def set_parameters_of_the_day(self, pop: Population):
        pop_size = len(pop.people)
        number_of_meetings = randint(int(pop_size * 1.5), int(pop_size * 2) + 1)
        additional_budget_for_vac = 0
        additional_deaths, specific_job = 5, "slave"

        return number_of_meetings, additional_budget_for_vac, (additional_deaths, specific_job)


class KillMedics(Event):

    def __init__(self):
        self.name = "KillMedics"

    def set_parameters_of_the_day(self, pop: Population):
        pop_size = len(pop.people)
        lor = 0.1 * pop.government.lor
        number_of_meetings = int(randint(int(pop_size * 0.9), int(pop_size * 1.1) + 1) - 0.6 * lor * pop_size)
        additional_budget_for_vac = 0
        additional_deaths, specific_job = 10, "medic"

        return number_of_meetings, additional_budget_for_vac, (additional_deaths, specific_job)
