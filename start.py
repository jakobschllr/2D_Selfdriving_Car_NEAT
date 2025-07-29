from neat_classes.PopulationHandler import PopulationHandler
from simulation.test import test_simulation
from simulation.SimulationHandler import SimulationHandler
import numpy as np



def main():
    simulation_handler = SimulationHandler()
    simulation_handler.initialize()

    population_handler = PopulationHandler(150,4,2,simulation_handler)
    population_handler.initial_population()
    population_handler.start_evolution_process() 
    

def run_tests():
    test_simulation()

#run_tests()
main()