
from simulations.covid import (
    create_covid_environment,
    get_covid_information,
    get_covid_defaults,
    validate_covid_start
)

# Create environment
settings = get_covid_defaults()

G = create_covid_environment(
    settings["infection_intensity"]
)

# Display environment
print("\n===== COVID-19 SIMULATION ENVIRONMENT =====")

print("Total zones:", G.number_of_nodes())
print("Total connections:", G.number_of_edges())

print("\nZone Information:")

for zone in get_covid_information(G):
    print(zone)

# Validate starting location
validate_covid_start(G, settings["start_zone"])

print("\nStarting zone:", settings["start_zone"])
print("Simulation steps:", settings["steps"])

print("\nCOVID environment created successfully!")
