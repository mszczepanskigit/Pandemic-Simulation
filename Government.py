class Government:
    def __init__(self, name: str, level_of_restrictions: int, budget=1000):
        if level_of_restrictions < 1 or level_of_restrictions > 10:
            raise ValueError("Level of restrictions has to be between 1 and 10")
        self.name = name
        self.lor = level_of_restrictions
        self.vir = False  # vaccine_is_ready
        self.kav = False  # know_about_virus
        self.budget = abs(budget)  # budget_to_buy_vaccines_per_day

    def change_restrictions(self, new_level):
        if new_level > 10 or new_level < 1:
            raise ValueError("Level of restrictions has to be between 1 and 10")
        self.lor = new_level

    def get_know_about_virus(self):
        self.change_restrictions(min(10, 2 * self.lor))
        self.kav = True
