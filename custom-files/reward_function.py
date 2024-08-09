def reward_function(params):
    '''
    Example of penalize steering, which helps mitigate zig-zag behaviors
    '''
    reward = 1
    # Read input parameters
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    steering = abs(params['steering_angle']) # Only need the absolute steering angle

    all_wheels_on_track = params['all_wheels_on_track']
    if not all_wheels_on_track:
        return 1e-3

    # Calculate 3 marks that are farther and father away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width

    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_1:
        reward = 1
    elif distance_from_center <= marker_2:
        reward = 0.5
    elif distance_from_center <= marker_3:
        reward = 0.1
    else:
        reward = 1e-3  # likely crashed/ close to off track
        return reward

    MAX_SPEED = 4.0
    MIN_SPEED = 2.0
    MAX_STEERING_ANGLE = 15.0
    speed = params['speed']
    steering_angle = abs(params['steering_angle'])

    # Reward for speed
    if speed >= MIN_SPEED:
        speed_reward = speed / MAX_SPEED
    else:
        speed_reward = 0.5 * (speed / MIN_SPEED)  # penalize for being too slow

    # Reward for steering angle (penalize sharp turns)
    if steering_angle <= MAX_STEERING_ANGLE:
        steering_reward = 1.0
    else:
        steering_reward = 1.0 - (steering_angle / 50.0)  # gradually reduce reward as steering angle increases

    # Combine the rewards
    comp_reward = speed_reward * steering_reward

    # Ensure the reward is non-negative
    reward = max(comp_reward+reward, 0.01)

    return float(reward)
