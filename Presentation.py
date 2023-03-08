from Simulation import Simulation
from Day import Day
from Events import NormalDay, RobotsKillPeopleOutside, NationalVaccination, ElvisConcert
from Population import Population
from Government import Government
from Virus import Virus
from Vaccine import Vaccine


if __name__ == "__main__":
    Yellow = Population("Yellow")
    Yellow.set_population(num_of_people=1000,
                          government=Government("Liberals", 2),
                          pot_economy_level=7,
                          hand_min=2,
                          distribution=(0.3, 0.3, 0.2, 0.2))
    Red = Population("Red")
    Red.set_population(num_of_people=1000,
                       government=Government("Communists", 4),
                       pot_economy_level=4,
                       hand_min=3)

    Yellow.set_infected(10)
    Red.set_infected(10)

    days_list = [Day(i) for i in range(1, 366)]

    events_dict = {NormalDay(): (1, 84),
                   RobotsKillPeopleOutside(): (85, 85),
                   NationalVaccination(): (86, 95),
                   ElvisConcert(): (96, 100)}

    Typical_Virus = Virus(name="Smiler",
                          mortality=5,
                          contagiousness=5,
                          strength=1)
    Antismiler = Vaccine("Antismiler", 1, Typical_Virus, 1, efficiency=100)

    Death_one = Virus(name="Killer",
                      mortality=9,
                      contagiousness=5,
                      strength=3)
    Antikiller = Vaccine("Antikiller", 30, Death_one, 25, efficiency=50)

    S = Simulation([Yellow, Red], days_list, events_dict)
    S.simulation_start(Typical_Virus, Antismiler)

