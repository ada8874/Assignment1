from sample_data import get_sample_data


from fitness_analyzer import (
    Observation,
    Participant,
    WorkoutSession,
    AnalysisResult,
    validate_observation
)

profile_data, observation_data = get_sample_data("moderate_activity")

# Convert participant profile dictionary into a Participant object
participant = Participant.from_dict(profile_data)

#creates a new blank workout session
session = WorkoutSession(participant)

#go through each generated observation dictionary
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
    session.average_activity_level(),
    session.heart_rate_difference(),
    session.average_skin_response(),
    session.skin_response_difference(),
    session.average_temperature(),
    session.temperature_difference(),
    total_observations,
    usable_observations,
    rejected_observations,
    session.classify_intensity(),
    session.classification_explanation()
)

result_dict = result.to_dict()

# Display workout results
print("Participant:", session.participant.participant_id)
print("Baseline heart rate:", session.participant.baseline_heart_rate)

print("Total observations:", total_observations)
print("Usable observations:", usable_observations)
print("Rejected observations:", rejected_observations)

print("Classification:", session.classify_intensity())
print("Explanation:", session.classification_explanation())

if usable_observations > 0:
    print("Average heart rate:", round(session.average_heart_rate(), 2))
    print("Minimum heart rate:", session.minimum_heart_rate())
    print("Maximum heart rate:", session.maximum_heart_rate())
    print("Average skin response:", round(session.average_skin_response(), 2))
    print("Skin response difference:", round(session.skin_response_difference(), 2))

    print("Average temperature:", round(session.average_temperature(), 2))
    print("Temperature difference:", round(session.temperature_difference(), 2))

    print("Average activity level:", round(session.average_activity_level(), 2))
    print("Difference from baseline:",round(session.heart_rate_difference(), 2))
else:
    print("No usable observations available")