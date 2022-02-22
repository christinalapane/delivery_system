# Christina LaPane Student ID: 008207171
from graph import graph


# Greedy Algorithm Pseudocode
# greedy_algorithm(route)
# start = HUB
# edge_weights = edge_weights{}
# sorted_route = route
# sorted_path = [start]
# while length of sorted_route is not 0:
# current_edge_weight = [0, start]
# for location in sorted_route:
# distance = current_edge_weights[path[-1], location] the distance is between the two locations
# if location is at start:
# then current_edge_weight is at start
# if distance is less than current_edge_weight and distance does not equal 0
# then current_edge_weight is at current location
# if next_location is not in sorted_path[],
# then add location to the sorted_path[]
# if the next_location already exists in sorted_path
# then remove from sorted_route
# return the sorted_path
# O(N^2)
def algorithm(route):
    start = "4001 South 700 East"  # the HUB (starting and ending location for all trucks)
    graph_edge_weights = graph.edge_weights  # gathers edge_weights (mileage)
    sort_truck_route = route  # route is created once packages are loaded onto trucks

    path = [start]  # path is the route that will taken, starting with HUB

    # a loop that removes locations from route as they are being added to 'path
    # O (log N)
    while len(sort_truck_route) != 0:
        min = [0, start]  # '0' is starting edge weight, and start is hub
        for location in sort_truck_route:
            distance = graph_edge_weights[path[-1], location]  # getting edge weights between each location
            if min[0] == 0:  # establishing start location
                min = [distance, location]
            if distance < min[0] and distance != 0:  # allows loop to continue through thr graph
                min = [distance, location]
        if min[1] not in path:  # prevents double visits
            path.append(min[1])
        sort_truck_route.remove(min[1])  # removes the location. Continues until empty
    return path
