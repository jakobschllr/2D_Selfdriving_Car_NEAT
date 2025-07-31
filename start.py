from neat_classes.PopulationHandler import PopulationHandler
from simulation.test import test_simulation
from simulation.SimulationHandler import SimulationHandler
from neat_classes.RuntimeStatus import RuntimeStatus



def main():
    run_stat = RuntimeStatus()
    simulation_handler = SimulationHandler(run_stat)
    simulation_handler.initialize()

    population_handler = PopulationHandler(150,4,2,simulation_handler, run_stat)
    population_handler.initial_population()
    population_handler.start_evolution_process() 
    
def run_tests():
    test_simulation()

#run_tests()
main()