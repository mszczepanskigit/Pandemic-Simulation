from Simulation import *
import unittest
from Person import Person
from Government import Government
from Events import *


class SimulationTest(unittest.TestCase):
    def setUp(self):
        self.Person1 = Person(3, True, "slave", hand_washing_level=4)
        self.Person2 = Person(-6, False, "medic", hand_washing_level=2)
        self.Person3 = Person(4, True, "slave", hand_washing_level=4)
        self.Person4 = Person(1, True, "slave", hand_washing_level=2)
        self.Person5 = Person(2, True, "slave", hand_washing_level=2, infected=True)

        self.Weak_Virus = Virus("Weak", 0, 1, 1)
        self.Cont_Virus = Virus("Cont", 0, 10, 3)
        self.Test_Virus = Virus("Test", 5, 5, 2)

        self.Super_Vac = Vaccine("Super", 1, self.Weak_Virus, efficiency=100)
        self.Killing_Vac = Vaccine("Killing", 1, self.Weak_Virus, efficiency=100, mortality=100)
        self.Anti_Cont = Vaccine("AntiCont", 1, self.Cont_Virus, efficiency=100)

        self.Day1 = Day(1)

        self.Gov = Government("Testgov", 5)
        self.Gov1 = Government("Testgov1", 3, 2000)
        self.Gov2 = Government("Testgov2", 7, -2000)

        self.Pop1 = Population("Testpop")
        self.Pop1.set_population(100, self.Gov, 5)
        self.Pop2 = Population("Pop2")
        self.Pop3 = Population("Pop3")
        self.Pop4 = Population("Pop4")

    def test_Person(self):
        self.assertEqual(self.Person1.id, 3)
        self.assertEqual(self.Person1.likes_gov, True)
        self.assertEqual(self.Person1.job, "slave")
        self.assertEqual(self.Person1.hand, 4)
        self.assertEqual(self.Person2.id, 6)
        with self.assertRaises(ValueError):
            Person(5, True, "job", hand_washing_level=8)

        self.assertFalse(self.Person2.is_infected())
        self.assertFalse(self.Person1.is_dead())
        self.Person3.die()
        self.assertTrue(self.Person3.is_dead())
        self.assertEqual(self.Person3.id, -4)
        self.assertLess(self.Person3.id, 0)
        self.assertFalse(self.Person2.does_like_gov())

        self.assertFalse(self.Person1.is_resistant())
        self.Person1.get_vac(self.Super_Vac)
        self.assertTrue(self.Person1.is_resistant())

        self.Person1.get_infection(self.Super_Vac)
        self.assertFalse(self.Person1.is_infected())
        self.Person2.get_infection(self.Super_Vac)
        self.assertTrue(self.Person2.is_infected())

        self.Person2.get_vac(self.Killing_Vac)
        self.assertTrue(self.Person2.is_dead())

        self.Person4.meet(self.Person5, self.Cont_Virus, self.Anti_Cont)
        self.assertTrue(self.Person4.is_infected())
        with self.assertRaises(TypeError):
            self.Person4.meet(self.Person5, self.Cont_Virus, 2)
        with self.assertRaises(TypeError):
            self.Person4.meet("a", self.Cont_Virus, self.Anti_Cont)
        with self.assertRaises(TypeError):
            self.Person1.get_infection([])

    def test_Vaccine(self):
        with self.assertRaises(ValueError):
            Vaccine("A", 0, self.Cont_Virus)
        with self.assertRaises(ValueError):
            Vaccine("A", 2, self.Cont_Virus, mortality=101)
        with self.assertRaises(ValueError):
            Vaccine("A", 2, self.Cont_Virus, mortality=-1)
        with self.assertRaises(ValueError):
            Vaccine("A", 2, self.Cont_Virus, efficiency=200)
        Vac = Vaccine("test", 20, self.Weak_Virus, 2, 50)
        self.assertEqual(Vac.progress, 0)
        self.assertFalse(Vac.done)
        Vac.make_progress(50)
        self.assertEqual(Vac.progress, 50)
        Vac.make_progress(-2.5)
        self.assertEqual(Vac.progress, 47.5)
        Vac.make_progress(-200)
        self.assertEqual(Vac.progress, 0)
        Vac.make_progress(500)
        self.assertGreaterEqual(Vac.progress, 100)
        self.assertTrue(Vac.done)

    def test_Virus(self):
        with self.assertRaises(ValueError):
            Virus("test", 10.2, 5, 2)
        with self.assertRaises(ValueError):
            Virus("test", -7, 5, 2)
        with self.assertRaises(ValueError):
            Virus("test", 5, 12, 2)
        with self.assertRaises(ValueError):
            Virus("test", 2, 5, 0)
        with self.assertRaises(ValueError):
            Virus("test", 2, 5, 4)
        self.assertEqual(self.Weak_Virus.mort, 0)
        self.assertEqual(self.Weak_Virus.cont, 1)
        self.assertEqual(self.Weak_Virus.strg, 1)
        self.Test_Virus.change_mort(6)
        self.assertEqual(self.Test_Virus.mort, 6)
        self.Test_Virus.change_cont(4)
        self.assertEqual(self.Test_Virus.cont, 4)
        self.Test_Virus.change_strg(3)
        self.assertEqual(self.Test_Virus.strg, 3)

    def test_Day(self):
        self.assertEqual(self.Day1.day, 1)
        self.assertEqual(self.Day1.get_healthy(), [])
        self.assertEqual(self.Day1.get_infected(), [])
        self.assertEqual(self.Day1.get_dead(), [])
        self.assertEqual(self.Day1.get_numbers(), (0, 0, 0))

        self.Day1.set_lists(self.Pop1)
        self.assertEqual(self.Day1.get_numbers(), (100, 0, 0))
        self.Day1.null_lists()
        self.assertEqual(self.Day1.get_numbers(), (0, 0, 0))

        self.Pop1.set_infected(10)
        self.Day1.set_lists(self.Pop1)
        self.assertEqual(self.Day1.get_numbers(), (90, 10, 0))

    def test_Government(self):
        with self.assertRaises(ValueError):
            Government("test", 0)
        with self.assertRaises(ValueError):
            Government("test", 20)
        self.assertEqual(self.Gov1.budget, self.Gov2.budget, 2000)
        self.assertFalse(self.Gov1.kav, self.Gov2.vir)

        self.Gov1.change_restrictions(4)
        self.assertEqual(self.Gov1.lor, 4)
        with self.assertRaises(ValueError):
            self.Gov1.change_restrictions(42)

        self.Gov1.get_know_about_virus()
        self.Gov2.get_know_about_virus()
        self.assertTrue(self.Gov1.kav, self.Gov2.kav)
        self.assertEqual(self.Gov1.lor, 8)
        self.assertEqual(self.Gov2.lor, 10)

    def test_Population(self):
        self.assertEqual(self.Pop1.name, "Testpop")
        self.assertEqual(self.Pop2.people, [])
        self.assertEqual(self.Pop2.government, None)
        self.assertEqual(self.Pop2.attitude_to_gov, self.Pop2.economy_level, 0)

        self.Pop2.change_attitude(5)
        self.Pop2.change_economy(5)
        self.assertEqual(self.Pop2.attitude_to_gov, self.Pop2.economy_level, 5)

        self.assertEqual(len(self.Pop1.list_of_not_vaccined()), 100)
        self.assertEqual(len(self.Pop2.list_of_vaccined()), 0)

        self.assertEqual(len(self.Pop1.get_alive()), 100)
        self.assertEqual(len(self.Pop2.get_alive()), 0)

        self.Pop2.set_population(10, self.Gov, 5)
        self.assertEqual(len(self.Pop2.people), 100)
        self.assertEqual(self.Pop2.government, self.Gov)
        self.assertEqual(self.Pop2.economy_level, 5 - 5/3)
        self.Pop3.set_population(200, self.Gov1, 2)
        self.assertEqual(self.Pop3.economy_level, 2 - 1/3)
        with self.assertRaises(ValueError):
            self.Pop4.set_population(300, self.Gov, 5, hand_min=1, distribution=(0.5, 0.4, 0.1))
        self.Pop4.set_population(100, self.Gov, 5, hand_min=-3, distribution=(0.5, 0.4, 0.1, 0.0))

    def test_Events(self):
        with self.assertRaises(TypeError):
            Event()

        tuple = NormalDay().set_parameters_of_the_day(self.Pop1)
        self.assertEqual(tuple[1], 0)
        self.assertEqual(tuple[2], (None, None))

        tuple1 = NationalVaccination().set_parameters_of_the_day(self.Pop1)
        self.assertEqual(tuple1[1], 1000)
        self.assertEqual(tuple1[2], (None, None))

        tuple2 = RobotsKillPeopleOutside().set_parameters_of_the_day(self.Pop1)
        self.assertEqual(tuple2[1], 500)
        self.assertEqual(tuple2[2], (None, "all"))

        tuple3 = ElvisConcert().set_parameters_of_the_day(self.Pop1)
        self.assertEqual(tuple3[1], 0)
        self.assertEqual(tuple3[2], (5, "slave"))

        tuple = KillMedics().set_parameters_of_the_day(self.Pop1)
        self.assertEqual(tuple[1], 0)
        self.assertEqual(tuple[2], (10, "medic"))


if __name__ == "__main__":
    unittest.main()
