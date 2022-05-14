from math import sin, cos, sqrt, atan2, radians
from os import path
from typing import Dict, List, Tuple
import csv
import networkx as nx
from json import load


class City():
    ''' class representing a node (city) '''
    
    def __init__(self, name: str, latitude: float, longitude: float) -> None:
        
        self.lat = latitude
        self.lng = longitude
        
        self.name = name 
        
    def __str__(self) -> str:
        
        return f"City[ name={self.name}, lat={self.lat}, lng={self.lng}]"
    
    def to_json(self) -> dict:
        """returns dictionary object representing this object"""

        return{
            "name":self.name,
            "lat":self.lat,
            "lng":self.lng
        }


def read_csv():
    
    cities: Dict[str, City] = {}
    
    

    with open(path.join("finder_app", "data", 'city_coordinates.csv')) as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            
            c = City(name=row[0], latitude=float(row[1]), longitude=float(row[2]))
            cities[c.name] = c
    
    return cities
    

def load_graph_and_cities(cost_limit=50000) -> Tuple[nx.Graph, Dict[str, City]]:
    
    data = None
    with open(path.join("finder_app", "data", 'scraped_link_data.json'), "r") as res_file:
        data = load(res_file)
    
    g = nx.Graph()
    
    for node in data["nodes"]:
        
        g.add_node(
            node["id"]["name"],
            latitude=node["id"]["lat"],
            longitude=node["id"]["lng"],
            pos=(node["id"]["lng"],node["id"]["lat"]))
        
    edge_count = 0
    
    for e in data["links"]:
        
        src_city = e["source"]["name"]
        
        target_city = e["target"]["name"]
        
        if src_city == target_city:
            continue
                
        if e["driving_cost"] < 3000:
            continue
            
        if e["driving_cost"] > 50000:
            continue
        
        edge_count += 1
        
        
        g.add_edge(src_city, target_city, driving_cost=e["driving_cost"], walking_cost=e["walking_cost"])
    
    

    
    return g, read_csv()


from finder_app.path_algos.cfg import city_dict, g

# Heruistic Function
def straight_line_distance(  src_city_name , goal_city_name ):
        ''' takes city names and returns the straight line distance between them using an equation the depends on the radian coordinates of each city '''
        # approximate radius of earth in km
        R = 6373.0
        
        src = city_dict[src_city_name]
        goal = city_dict[goal_city_name]
        
        lat1 = radians(src.lat)
        lon1 = radians(src.lng)
        lat2 = radians(goal.lat)
        lon2 = radians(goal.lng)
        
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        
        distance = R * c * 1000
        
        print(f"Heuristic called for {src_city_name}, {goal_city_name} and returned {distance}")
        
        return distance

class NoRouteException(Exception):
    pass

class NodeNotFound(Exception):
    pass