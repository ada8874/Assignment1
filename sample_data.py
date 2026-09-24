from data_generator import generate_fitness_data


# Provides reproducible sample data for the fitness analyzer
def get_sample_data(scenario="moderate_activity"):
    return generate_fitness_data(
        participant_id="P001",
        scenario=scenario,
        seed=42,
        number_of_windows=12
    )