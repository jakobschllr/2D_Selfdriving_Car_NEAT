

class RuntimeStatus():
    def __init__(self):
        self.current_generation = 0
        self.current_species_amount = 1
        self.current_network_amount = 0
        self.best_network = None

    def update(self, current_generation, current_species_amount, current_network_amount, best_network):
        self.current_generation = current_generation
        self.current_species_amount = current_species_amount
        self.current_network_amount = current_network_amount
        self.best_network = best_network
