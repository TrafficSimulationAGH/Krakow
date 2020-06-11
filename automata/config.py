"Automata settings and parameters."

class DefaultConfig:
    """
    TIMESTEP - simulation constant time step in seconds
    RADIUS - cell radius, distance to another cell
    SPAWN_RATE - probability of spawning a car over single step
    AGENT_DRIVEOFF - default agent chance of exiting road
    AGENT_SLOW - default agent chance of slowing down
    AGENT_FAST - default agent chance of accelerating
    AGENT_LIMIT - default agent chance of matching speed limit
    AGENT_VMAX - default agent max speed (km/h)
    """
    TIMESTEP = 1.0
    RADIUS = 5e-5
    SPAWN_RATE = 0.8

    AGENT_DRIVEOFF = 0.5
    AGENT_SLOW = 0.2
    AGENT_FAST = 0.3
    AGENT_LIMIT = 0.3
    AGENT_VMAX = 190.0

# Select config
CONFIG = DefaultConfig
