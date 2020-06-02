from math import sin, cos, sqrt, atan2, radians

class Coords:
    """
    Geographical coordinates.
    """

    def __init__(self, lat, lon):
        self.lat = float(lat)
        self.lon = float(lon)

    def dist(self, other):
        "Distance to other location"
        R = 6373000.0
        dlon = radians(self.lon - other.lon)
        dlat = radians(self.lat - other.lat)
        
        a = sin(dlat / 2)**2 + cos(radians(other.lat)) * cos(radians(self.lat)) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c
        
        return round(distance)

class OSM:
    """
    Map information wrapper
    HIGHWAY defines osm highway filters
    """
    HIGHWAY = ['primary', 'motorway', 'proposed', 'trunk', 'primary_link', 'motorway_link', 'trunk_link', 'give_way', 'motorway_junction']
    COLOR = 'b'

    def __init__(self, jsonfile=None):
        if jsonfile is not None:
            with open(jsonfile, 'r', encoding = 'utf-8') as f:
                json = f.read()
            self.load(json)

    def filter(self, func):
        """
        Filter out roads.
        func: item -> bool
        """
        return list(filter(func, self.roads))

    def load(self, json):
        "Load and filter data"
        def f(i):
            if 'highway' in i['properties']:
                precond = i['properties']['highway'] in self.HIGHWAY
                if 'proposed' in i['properties']:
                    return precond and i['properties']['proposed'] in self.HIGHWAY
                return precond
            else:
                return False
        data = eval(json)
        bbox = data['bbox']
        self.bbox = {'x': (bbox[0], bbox[2]), 'y': (bbox[1], bbox[3])}
        self.roads = data['features']
        self.roads = self.filter(f)
