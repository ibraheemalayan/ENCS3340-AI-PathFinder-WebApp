
from os import path
from typing import Dict, List, Tuple
import csv
import networkx as nx
from json import load

from flask import g

from finder_app.path_algos.heuristics import straight_line_distance



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
    
    
    g.city_dict = read_csv()
    
    data = None
    with open(path.join("finder_app", "data", 'scraped_link_data.json'), "r") as res_file:
        data = load(res_file)
    
    g.G = nx.Graph()
    g.full_g = nx.Graph()
    
    for node in data["nodes"]:
        
        g.G.add_node(
            node["id"]["name"],
            latitude=node["id"]["lat"],
            longitude=node["id"]["lng"],
            pos=(node["id"]["lng"],node["id"]["lat"]))
        
        g.full_g.add_node(
            node["id"]["name"],
            latitude=node["id"]["lat"],
            longitude=node["id"]["lng"],
            pos=(node["id"]["lng"],node["id"]["lat"]))
        
    edge_count = 0
    full_edge_count = 0
    
    for e in data["links"]:
        
        src_city = e["source"]["name"]
        
        target_city = e["target"]["name"]
        
        aerial_distance = round(straight_line_distance(src_city_name=src_city, goal_city_name=target_city))
        
        g.full_g.add_edge(src_city, target_city, driving_cost=e["driving_cost"], walking_cost=e["walking_cost"], aerial_cost=aerial_distance)
        
        full_edge_count += 1
        
        if src_city == target_city:
            continue
                
        if e["driving_cost"] < 3000:
            continue
            
        if e["driving_cost"] > cost_limit:
            continue
        
        edge_count += 1
        
        
        g.G.add_edge(src_city, target_city, driving_cost=e["driving_cost"], walking_cost=e["walking_cost"], aerial_cost=aerial_distance)
    
    

    
    return g.G, g.city_dict, g.full_g



class NoRouteException(Exception):
    pass

class NodeNotFound(Exception):
    pass