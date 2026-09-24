from data_generator import generate_fitness_data

from fitness_analyzer import (
    Observation,
    Participant,
    WorkoutSession,
    validate_observation
)

# Creates a complete workout session for a selected test scenario
def create_session(scenario):
    profile_data, observation_data = generate_fitness_data(
        participant_id="P001",
        scenario=scenario,
        seed=42,
        number_of_windows=12
    )

    participant = Participant.from_dict(profile_data)
    session = WorkoutSession(participant)

    # Only valid observations are added to the workout session
    for record in observation_data:
        errors = validate_observation(record)

        if len(errors) == 0:
            new_observation = Observation.from_dict(record)
            session.add_observation(new_observation)

    return session

# Tests the five required workout scenarios
def test_resting():
    session = create_session("resting")

    assert session.classify_intensity() == "resting"

def test_moderate_activity():
    session = create_session("moderate_activity")

    assert session.classify_intensity() == "moderate activity"

def test_high_activity():
    session = create_session("high_activity")

    assert session.classify_intensity() == "high activity"

def test_recovery():
    session = create_session("recovery")

    assert session.classify_intensity() == "recovering"

def test_poor_quality():
    session = create_session("poor_quality")

    assert session.classify_intensity() == "insufficient data"

# Tests validation of invalid and missing sensor values
def test_missing_heart_rate():
    bad_data = {
        "timestamp": 0,
        "heart_rate": None,
        "skin_response": 1.5,
        "temperature": 32.5,
        "activity_level": 0.4,
        "signal_quality": 0.9
    }

    errors = validate_observation(bad_data)

    assert "Heart rate is missing" in errors

def test_invalid_heart_rate():
    bad_data = {
        "timestamp": 0,
        "heart_rate": 265,
        "skin_response": 1.5,
        "temperature": 32.5,
        "activity_level": 0.4,
        "signal_quality": 0.9
    }

    errors = validate_observation(bad_data)

    assert "Heart rate is outside the valid range" in errors

def test_negative_activity_level():
    bad_data = {
        "timestamp": 0,
        "heart_rate": 100,
        "skin_response": 1.5,
        "temperature": 32.5,
        "activity_level": -0.20,
        "signal_quality": 0.9
    }

    errors = validate_observation(bad_data)

    assert "Activity level must be between 0 and 1" in errors

def test_low_signal_quality():
    bad_data = {
        "timestamp": 0,
        "heart_rate": 100,
        "skin_response": 1.5,
        "temperature": 32.5,
        "activity_level": 0.4,
        "signal_quality": 0.20
    }

    errors = validate_observation(bad_data)

    assert "Signal quality is too low" in errors

# Confirms that valid sensor data passes validation without errors
def test_valid_observation():
    good_data = {
        "timestamp": 0,
        "heart_rate": 100,
        "skin_response": 1.5,
        "temperature": 32.5,
        "activity_level": 0.4,
        "signal_quality": 0.9
    }

    errors = validate_observation(good_data)

    assert len(errors) == 0

#runs all tests
test_resting()
test_moderate_activity()
test_high_activity()
test_recovery()
test_poor_quality()

test_missing_heart_rate()
test_invalid_heart_rate()
test_negative_activity_level()
test_low_signal_quality()
test_valid_observation()

print("All tests passed")