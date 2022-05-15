from math import sin, cos, sqrt, atan2, radians
from flask import g

# Heruistic Function
def straight_line_distance(  src_city_name , goal_city_name ):
        ''' takes city names and returns the straight line distance between them using an equation the depends on the radian coordinates of each city '''
        # approximate radius of earth in km
        R = 6373.0
        
        
        
        src = g.city_dict[src_city_name]
        goal = g.city_dict[goal_city_name]
        
        lat1 = radians(src.lat)
        lon1 = radians(src.lng)
        lat2 = radians(goal.lat)
        lon2 = radians(goal.lng)
        
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        
        distance = R * c * 1000
        
        return distance

def walking_distance(src_city_name , goal_city_name):
    ''' takes city names and returns the walking distance between them using the data returned by google maps matrix API '''
        
    from . import astar_path, path_length
    
    path = astar_path(g.full_g, source=src_city_name, destination=goal_city_name, heuristic=straight_line_distance, mode="walking_cost")
    
    return path_length(g.full_g, path=path, mode="walking_cost")[0]

def zero_heruistic(src, dest):
    ''' used to make the A star act like a UCS '''
    return 0 
