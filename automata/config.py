"Module with settings and parameters."

class DefaultConfig:
    """
    Timestep - simulation constant time step in seconds
    Radius - cell radius, distance to another cell
    """
    TIMESTEP = 1.0
    RADIUS = 1e-3
    SPAWN_RATE = 0.3

    AGENT_DRIVEOFF = 0.4
    AGENT_SLOW = 0.05
    AGENT_FAST = 0.05
    AGENT_LIMIT = 0.05
    AGENT_VMAX = 150.0

CONFIG = DefaultConfig