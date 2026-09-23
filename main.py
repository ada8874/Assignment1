from data_generator import generate_fitness_data

#calculating average of a list of numbers
def calculate_average(values):

    #prevents division by zero if there are no valid values
    if len(values) == 0:
        return None 
    return sum(values) / len(values)

# Calculates the difference between a measured value and a reference value
def calculate_difference(value, reference):
    return value - reference

# Finds the lowest value in a list
def calculate_minimum(values):
    if len(values) == 0:
        return None

    return min(values)


# Finds the highest value in a list
def calculate_maximum(values):
    if len(values) == 0:
        return None

    return max(values)

#observations that will be displayed in the fitness analyzer
class Observation:
    def __init__(
        self,
        timestamp,
        heart_rate,
        skin_response,
        temperature,
        activity_level,
        signal_quality
    ):
        self.timestamp = timestamp
        self.heart_rate = heart_rate
        self.skin_response = skin_response
        self.temperature = temperature
        self.activity_level = activity_level
        self.signal_quality = signal_quality

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["timestamp"],
            data["heart_rate"],
            data["skin_response"],
            data["temperature"],
            data["activity_level"],
            data["signal_quality"]
        )

#class for participant observations
class Participant:
    def __init__(
        self,
        participant_id,
        baseline_heart_rate,
        baseline_skin_response,
        baseline_temperature):

        self.participant_id = participant_id
        self.baseline_heart_rate = baseline_heart_rate
        self.baseline_skin_response = baseline_skin_response
        self.baseline_temperature = baseline_temperature

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["participant_id"],
            data["baseline_heart_rate"],
            data["baseline_skin_response"],
            data["baseline_temperature"]
        )

# Represents a workout session that has multiple observations
class WorkoutSession:
    def __init__(self, participant):
        self.participant = participant
        self._observation_list = []

    # Adds an Observation object to workout session
    def add_observation(self, new_observation):
        self._observation_list.append(new_observation)
#
    @property
    def observations(self):
        return self._observation_list.copy()

    # Calculates average heart rate
    def average_heart_rate(self):
        heart_rates = []

        for item in self._observation_list:
            heart_rates.append(item.heart_rate)

        return calculate_average(heart_rates)

    def minimum_heart_rate(self):
        heart_rates = []

        for item in self._observation_list:
            heart_rates.append(item.heart_rate)

        return calculate_minimum(heart_rates)

    def maximum_heart_rate(self):
        heart_rates = []

        for item in self._observation_list:
            heart_rates.append(item.heart_rate)

        return calculate_maximum(heart_rates)

    # Calculates the difference between average heart rate and baseline
    def heart_rate_difference(self):
        average = self.average_heart_rate()

        if average is None:
            return None

        baseline = self.participant.baseline_heart_rate

        return calculate_difference(average, baseline)

# Stores the results from analyzing a workout session
class AnalysisResult:
    def __init__(
        self,
        average_heart_rate,
        minimum_heart_rate,
        maximum_heart_rate,
        heart_rate_difference,
        total_observations,
        usable_observations,
        rejected_observations
    ):
        self.average_heart_rate = average_heart_rate
        self.minimum_heart_rate = minimum_heart_rate
        self.maximum_heart_rate = maximum_heart_rate
        self.heart_rate_difference = heart_rate_difference
        self.total_observations = total_observations
        self.usable_observations = usable_observations
        self.rejected_observations = rejected_observations

    # Returns the analysis results as a dictionary
    def to_dict(self):
        return {
            "average_heart_rate": self.average_heart_rate,
            "minimum_heart_rate": self.minimum_heart_rate,
            "maximum_heart_rate": self.maximum_heart_rate,
            "heart_rate_difference": self.heart_rate_difference,
            "total_observations": self.total_observations,
            "usable_observations": self.usable_observations,
            "rejected_observations": self.rejected_observations
        }

# Checks if an observation contains valid sensor values (error handling)
def validate_observation(data):
    errors = []

    # Check timestamp
    if data["timestamp"] is None or data["timestamp"] < 0:
        errors.append("Invalid timestamp")

    # Check heart rate
    if data["heart_rate"] is None:
        errors.append("Heart rate is missing")
    elif data["heart_rate"] < 35 or data["heart_rate"] > 205:
        errors.append("Heart rate is outside the valid range")

    # Check skin response
    if data["skin_response"] is None:
        errors.append("Skin response is missing")
    elif data["skin_response"] < 0:
        errors.append("Skin response can't be negative")

    # Check temperature
    if data["temperature"] is None:
        errors.append("Temperature is missing")
    elif data["temperature"] < 25 or data["temperature"] > 42:
        errors.append("Temperature is outside the valid range")

    # Check activity level
    if data["activity_level"] is None:
        errors.append("Activity level is missing")
    elif data["activity_level"] < 0 or data["activity_level"] > 1:
        errors.append("Activity level must be between 0 and 1")

    # Check signal quality
    if data["signal_quality"] is None:
        errors.append("Signal quality is missing")
    elif data["signal_quality"] < 0 or data["signal_quality"] > 1:
        errors.append("Signal quality must be between 0 and 1")

    return errors

profile_data, observation_data = generate_fitness_data(
    participant_id="P001",
    scenario="moderate_activity",
    seed=42,
    number_of_windows=12
)

# Convert participant profile dictionary into a Participant object
participant = Participant.from_dict(profile_data)

#creates a new blank workout session
session = WorkoutSession(participant)

#go through each dict in sample_data
for record in observation_data:
    # Check the observation before creating an object
    errors = validate_observation(record)

    # Only add the observation if there are no validation errors
    if len(errors) == 0:
        new_observation = Observation.from_dict(record)
        session.add_observation(new_observation)

    # Otherwise print why the observation was rejected
    else:
        print("Observation rejected:", errors)


total_observations = len(observation_data)
usable_observations = len(session.observations)
rejected_observations = total_observations - usable_observations

result = AnalysisResult(
    session.average_heart_rate(),
    session.minimum_heart_rate(),
    session.maximum_heart_rate(),
    session.heart_rate_difference(),
    total_observations,
    usable_observations,
    rejected_observations
)

# Display workout results
print("Participant:", session.participant.participant_id)
print("Baseline heart rate:", session.participant.baseline_heart_rate)

print("Total observations:", total_observations)
print("Usable observations:", usable_observations)
print("Rejected observations:", rejected_observations)

if usable_observations > 0:
    print("Average heart rate:", round(session.average_heart_rate(), 2))
    print("Minimum heart rate:", session.minimum_heart_rate())
    print("Maximum heart rate:", session.maximum_heart_rate())
    print(
        "Difference from baseline:",
        round(session.heart_rate_difference(), 2)
    )
else:
    print("No usable observations available")