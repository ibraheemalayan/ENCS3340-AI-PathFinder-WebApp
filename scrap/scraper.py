import csv
from typing import List

import requests

from finder_app.path_algos.models import City

import networkx as nx
from json import dumps


count = 0
global g
g = nx.Graph()

def update_file():
    global g
    serialzable_graph  = nx.node_link_data(g)
    
    json_str = dumps(serialzable_graph, indent=4, default=lambda x: x.__dict__)
    
    with open("res.json", "w") as res_file:
        res_file.write(json_str)

def get_distance(src_cities: List[City], dest_cities: List[City]):

    global count
    global g
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    
    # deepcode ignore HardcodedNonCryptoSecret: <>
    API_KEY = "AIzaSyBAXXKZP6Sdl22Hg0m4JaWecuPnwFpqGow"
    
    
    src_query_str = "|".join([ f"{city.lat},{city.lng}" for city in src_cities])
    dest_query_str = "|".join([ f"{city.lat},{city.lng}" for city in dest_cities])
    
    args = {
        "key": API_KEY,
        "units": "si",
        "origins": src_query_str,
        "destinations": dest_query_str,    
        "mode": "walking" 
    }
    
    headers = {
        "Accept": "application/json"
    }
    
    walking_response = requests.request("GET", url, headers=headers, params=args)
    
    args["mode"] = "driving"
    
    driving_response = requests.request("GET", url, headers=headers, params=args)
    
    
    i = 0
    for i in range(len(walking_response.json()["rows"])):
        
        walk_row = walking_response.json()["rows"][i]
        drive_row = driving_response.json()["rows"][i]
        
         # working on route where origin is src_cities[i] 
        
        j = 0
        for j in range(len(walk_row["elements"])):
            
            walk_element = walk_row["elements"][j]
            drive_element = drive_row["elements"][j]
            
            try:
                g.add_edge(src_cities[i], dest_cities[j], driving_cost = drive_element["distance"]["value"], walking_cost=walk_element["distance"]["value"])
                print(f'Edge added between src: {src_cities[i].name} and dest: {dest_cities[j].name} \n\t walking={walk_element["distance"]["value"]}\t driving={drive_element["distance"]["value"]}')
            except KeyError as k:
                print(f"\n\n -- Key Error between src: {src_cities[i].name} and dest: {dest_cities[j].name}, walk_response={walking_response.text},  drive_response={driving_response.text}\n\n\n")
            
            update_file()
                
            count += 1 

    
cities: List[City] = []


def read_csv():

    with open('city_coordinates.csv') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            
            
            c = City(name=row[0], latitude=float(row[1]), longitude=float(row[2]))
            cities.append( c )
            
            g.add_node(c)
            
            
read_csv()


worklist1=[]
worklist2=[]



max=6

def prodWorkList(displ,rng,cities):
    worklist = []

    for j in range(rng):

        index=j + displ*5
        worklist.append(cities[index])
            
    return worklist

for i in range(max):

    worklist1=prodWorkList(i,5,cities)

    for j in range(max):

        worklist2=prodWorkList(j,5,cities)


        get_distance(worklist1, worklist2)


print(count)