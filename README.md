# Smart Fitness Session Analyzer

# Selected Option - Option A

# Ada Hashemi, 8874

## Description

This program analyzes simulated fitness data collected during a workout session.
It validates sensor observations, compares measurements with a participant's
normal reference values, calculates workout statistics and classifies the
session based on heart rate and activity level.

## Running Instructions:

1. git clone https://github.com/ada8874/Assignment1.git
2. cd REPOSITORY
3. python3 main.py

This project uses only the Python standard library and does not require any
third-party packages.

## Class design

The program uses four main classes:

### Observation

The Observation class represents one sensor reading from a workout session.
Each observation stores:

- timestamp
- heart rate
- skin response
- temperature
- activity level
- signal quality

The from_dict() class method is used to convert the raw dictionaries from the
provided data generator into Observation objects.

### Participant

The Participant class represents the person taking part in the workout.
It stores the participant ID together with the participant's normal reference
values:

- baseline heart rate
- baseline skin response
- baseline temperature

The from_dict() class method converts the participant profile from the data
generator into a Participant object.

### WorkoutSession

The WorkoutSession class represents one complete workout session. It contains
a participant and a collection of Observation objects.

The class is responsible for calculating workout statistics such as:

- average heart rate
- minimum and maximum heart rate
- average activity level
- average skin response
- average temperature
- differences from the participant's baseline values

It also classifies the session as resting, moderate activity, high activity,
recovering or insufficient data.

### AnalysisResult

The AnalysisResult class stores the final results of the workout analysis.
It contains the calculated values, number of usable and rejected observations,
classification and explanation.

The to_dict() method converts the result into a dictionary so the program
provides a structured result.

## Object-oriented design

### Composition

Composition is used in WorkoutSession. A workout session contains a
Participant object and multiple Observation objects.

This reflects the structure of the problem because a workout session belongs
to a participant and is made up of multiple sensor observations.

### Encapsulation

The observations in WorkoutSession are stored in the protected-style
attribute \_observation_list.

Observations are added through the add_observation() method and can be
accessed through the observations property. The property returns a copy of
the list instead of giving direct access to the original list.

### Class methods

Both Observation and Participant use a from_dict() class method. These
methods are used to convert the raw dictionaries produced by the supplied data
generator into objects used by the program.

### Inheritance

Inheritance was not used because there is no natural inheritance relationship
between the main classes.

For example, a Participant is not a type of observation, and a
WorkoutSession is not a type of Participant. Composition therefore gives
a clearer representation of the problem, because a workout session has a
participant and has observations.

## Assumptions and classification rules

The supplied data generator provides simulated sensor measurements, but it does
not provide the expected classification. The program therefore uses its own
rules to determine the workout type.

### Observation validation

An observation is considered invalid if:

- the timestamp is missing or below 0
- heart rate is missing or outside 35–205 bpm
- skin response is missing or below 0
- temperature is missing or outside 25–42 °C
- activity level is missing or outside 0–1
- signal quality is missing or outside 0–1
- signal quality is below 0.60

A signal quality below 0.60 is treated as too unreliable to use in the
analysis. This threshold is a design decision made for this project.

Invalid observations are rejected and are not added to the workout session.

### Insufficient data

A workout is classified as insufficient data when fewer than 3 valid
observations remain after validation.

The minimum of 3 observations is a design decision made to avoid classifying
a workout from too little information.

### Resting

A workout is classified as resting when:

- average activity level is below 0.25, and
- average heart rate is less than 15 bpm above the participant's baseline.

### Moderate activity

A workout is classified as moderate activity when:

- average activity level is below 0.67, and
- average heart rate is less than 45 bpm above the participant's baseline.

This rule is checked after the resting rule.

### High activity

If the workout does not meet the rules for resting, moderate activity,
recovery or insufficient data, it is classified as high activity.

### Recovery

Recovery is detected by comparing the beginning and end of the workout.

The program compares:

- the first 3 valid observations
- the last 3 valid observations

A workout is classified as recovering when:

- average heart rate decreases by at least 15 bpm, and
- average activity level decreases by at least 0.15.

At least 6 valid observations are required before recovery can be evaluated.

Recovery is checked before the normal resting, moderate and high activity
rules because a recovering session may have overall averages that otherwise
look like moderate activity.

## Example output

The following is an example of the console output when analyzing a
high_activity session:

Participant: P001
Baseline heart rate: 78

Total observations: 12
Usable observations: 12
Rejected observations: 0

Classification: high activity
Explanation: Average activity level was 0.80 and heart rate was 57.67 bpm above baseline.

Average heart rate: 135.67
Average activity level: 0.80
Difference from baseline: 57.67

Average skin response: 1.80
Skin response difference from baseline: 0.63

Average temperature: 33.34
Temperature difference from baseline: 0.59

## Known limitations

- The program only analyzes simulated data from the supplied data generator.
  It has not been tested with real wearable-device data.

- The classification rules use manually chosen thresholds for activity level,
  heart-rate difference and recovery detection. These thresholds are suitable
  for this assignment but should not be treated as medical or fitness advice.

- Recovery detection only compares the first three and last three valid
  observations. It does not analyze the complete trend of the workout.

- An entire observation is rejected if one of its required sensor values is
  invalid or missing. The program does not attempt to repair or estimate
  missing values.

- A signal quality below 0.60 is rejected based on a threshold chosen for this
  project. The supplied data does not define 0.60 as an official cutoff.

- The program mainly uses average values for classification. Short spikes or
  unusual changes during the middle of a session may therefore have limited
  influence on the final classification.

- The current program analyzes one generated participant and one workout
  session at a time.

- The classification system is rule-based and does not use machine learning
  or external services.
