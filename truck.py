# Christina LaPane Student ID: 008207171
import operator

from graph import graph
from greedy import algorithm
from hash import packageTable
from mytime import Time


# Truck class creates objects which will be loaded with package information
class Truck:
    # initialize all truck objects
    def __init__(self):
        self.truckPackage = []  # packages in the truck
        self.route = []  # the route for each truck
        self.startTime = None  # start time for each truck
        self.currentTime = None  # current time for each truck
        self.finalTime = None  # final time for each truck- when returned to hub
        self.mph = 18  # average speed is 18 mph

    # inserting package into the truck
    def insert(self, package):
        self.truckPackage.append(package)  # adds package onto truck
        self.route.append(package[1])  # package[1] == street address (which will compare to distance location)

    # removing delivered package from truck
    def remove(self, package):
        self.truckPackage.remove(package)  # remove delivered package from truck
        self.route.remove(package[1])  # package[1] == street address(compare to distance location)

    # start time is when it will leave the HUB every 2.5 hours (8:00, 10:30, 1:00)
    def start(self, start):
        self.startTime = start

    # current time is used to check status
    def current(self, current):
        self.currentTime = current
        return current

    # the final time is when truck returns to HUB
    # used because there are only 2 drivers
    def final(self, final):
        self.finalTime = final
        return final


# creating Truck objects
truck1 = Truck()
truck2 = Truck()
truck3 = Truck()

# and iterable list of locations
addressData = []

# put package information into the graph's delivery dictionary to associate locations with package address [1]
graph.load_packages(packageTable)

# Create best route pseudocode:
# If package deadline is 9:00 AM
# insert into truck 1
# If package deadline is 10:30
# insert into truck 1
# If package deadline is 10:30 and special note is delayed until 9:05
# insert into truck 2
# If package deadline is 10:30 and special note isn’t empty, isn’t delayed, isn’t wrong address or have to be on truck 2
# insert into truck 1
# If package deadline is 10:30 with no other special notes,
# insert into truck 1
# If package deadline is EOD and delayed until 9:05
# EOD and wrong address
# insert into truck 2
# EOD and must be on truck 2
# insert into truck 2
# For left over packages:
# If deadline is EOD and no special notes
# insert into truck 3
# If room for truck 1
# insert into truck 1
# If room for truck 2
# insert into truck 2
# If room for truck 3
# insert into truck 3

# Group 1 = Packages that have to be on truck 1 (deadline 9:00 AM)
# Group 2 = Packages that have to be on Truck 2. (special notes or not arriving until 9:05)
# Group 3 = Packages that have a deadline for 10:30 AM but no special notes
# Group 4 = Packages that have a deadline for EOD and special notes are: delayed, truck2, or wrong address
# Group 5 = Packages that have a deadline for EOD and no special notes
# After sorted into groups, will be loaded into algorithm to keep mileage under 140 miles
# O(N^2)
def create_best_route():
    # loads addressData with locations from graph
    for location in graph.delivery_dict:
        addressData.append(location)

    # Group 1 - information above
    for a in addressData:
        for p in graph.delivery_dict[a]:
            if p[5] == "9:00":
                truck1.insert(p)

    # Group 2 - information above
    for a in addressData:
        for p in graph.delivery_dict[a]:
            if p[5] == "10:30" and p[7] != "" and p[7] != "2" and p[7] != "W" and p[7] != "9:05":
                truck1.insert(p)
            elif p[5] == "10:30" and p[7] == "9:05":
                truck2.insert(p)

    # Group 3 - information above
    for a in addressData:
        for p in graph.delivery_dict[a]:
            if p[5] == "10:30" and p[7] == "":
                truck1.insert(p)

    # Group 4 - information above
    for a in addressData:
        for p in graph.delivery_dict[a]:
            if p[5] == "EOD" and p[7] == "9:05":
                truck2.insert(p)
            if p[5] == "EOD" and p[7] == "W":
                truck3.insert(p)
            if p[5] == "EOD" and p[7] == "2":
                truck2.insert(p)

    # Group 5 - information above
    for a in addressData:
        for p in graph.delivery_dict[a]:
            if p[5] == "EOD" and p[7] == "":
                if len(truck1.truckPackage) < 14:
                    truck1.insert(p)
                elif len(truck2.truckPackage) < 10:  # changed it from 16 to 13, so the 10:30 deadline can be met.
                    truck2.insert(p)
                elif len(truck3.truckPackage) < 16:
                    truck3.insert(p)
                else:
                    print('Package {} could not be loaded'.format(p[0]))

    truck1_start_route = truck1.route  # truck 1 start route
    truck1_start_route.append("4001 South 700 East")  # truck 1 starting with HUB address
    truck2_start_route = truck2.route  # truck 2 start route
    truck2_start_route.append("4001 South 700 East")  # truck 2 starting with HUB address
    truck3_start_route = truck3.route  # truck 3 start route
    truck3_start_route.append("4001 South 700 East")  # truck 3 starting with HUB address

    truck1.route = algorithm(truck1.route)  # route 1 sorted through the algorithm
    truck2.route = algorithm(truck2.route)  # route 2 sorted through the algorithm
    truck3.route = algorithm(truck3.route)  # route 3 sorted through the algorithm

    truck1.route.append("4001 South 700 East")  # route 1 ends at HUB address
    truck2.route.append("4001 South 700 East")  # route 2 ends at HUB address
    truck3.route.append("4001 South 700 East")  # route 3 ends at HUB address


# collects the amount of miles traveled on route for each truck
# O(N)
def traveled(route):
    edge_weight_list = graph.edge_weights
    miles = 0
    for i in range(0, len(route) - 1):
        miles = miles + edge_weight_list[route[i], route[i + 1]]
    return miles


# displays the amount of miles for each truck
# displays the total amount of miles for the entire day (max 140 miles)
def total_miles():
    t1 = traveled(truck1.route)
    t2 = traveled(truck2.route)
    t3 = traveled(truck3.route)
    total = t1 + t2 + t3
    print('---------------------------')
    print("Truck 1: ", round(t1, 2), "miles")
    print("Truck 2: ", round(t2, 2), "miles")
    print("Truck 3: ", round(t3, 2), "miles")
    print('TOTAL: ', round(total, 2), "miles")
    print('----------------------------')


# delivers all the packages throughout the day
# looks like a lot, but separates by each truck
# O(N^2)
def deliver():
    miles_between = graph.edge_weights  # gathering the edge weights, to keep track for the route

    # Truck 1
    # O(N^2)
    truck1Start = Time('8:00 AM')  # Truck 1 leaves at 8:00 AM
    truck1.startTime = truck1Start  # start time = 8:00 AM
    truck1.currentTime = truck1Start  # current time is also 8:00 AM (will be updated throughout route)
    for i in range(0, len(truck1.route) - 1):  # going through the route
        distance = miles_between[truck1.route[i], truck1.route[i + 1]]  # distance is from v1 to v2
        speed = truck1.mph  # speed is 18mph
        minutes = (distance / speed) * 60.0  # how many minutes it took. (miles/ 18mph) * 60 minutes
        truck1.currentTime.add_minutes(minutes)  # current time = adding minutes to the start/current time
        delivered = Time(truck1.currentTime.hours,
                         truck1.currentTime.minutes)  # delivered uses Time class to format the delivered time
        status = "PROJECTED TO BE DELIVERED at {}".format(delivered)  # adding the delivered time to string
        for p in truck1.truckPackage:  # for the package in packages on truck 1
            if truck1.route[i + 1] == p[1]:  # if the location equals the street address then status is updated
                p[8] = status

    truck1.finalTime = truck1.currentTime  # final time updated to current_time
    print("Truck 1: ", *truck1.truckPackage, sep="\n")  # prints the entire list, with status. Separated by newline
    print('Truck 1 leaves HUB at 8:00 AM')
    print('Truck 1 returns to HUB at {}'.format(truck1.finalTime))
    print()

    # Delivery Simulation Pseudocode:
    # for entire function - miles_between = edge weights from greedy algorithm
    # For Truck 1:
    # start time = 8:00 AM
    # current time = start time / will be updated throughout code
    # for index in truck 1 route
    # distance = miles_between(truck1.route[i], truck1.route[i + 1]) / from location one to location 2
    # speed is 18 mph
    # minutes traveled = distance travled / 18mph * 60 minutes
    # add minutes to current time
    # for index in truck1 packages:
    # if truck1.route[i + 1] == p[1] / if next point = current package location
    # delivery status is projected to be delivered at how much longer it will be to get from current location to next
    # otherwise its status is delivered and finaltime = current time
    # loops through the entire route until 0 addresses left
    # repeat for truck 2 route
    # start time = 9:05 AM
    # repeat for truck 3 route
    # start time = truck1.finaltime

    # Truck 2
    # O(N^2)
    truck2Start = Time('9:05 AM')  # Truck leaves at 9:15 AM
    truck2.startTime = truck2Start  # Start time is 9:15 AM
    truck2.currentTime = truck2Start  # current time is also 10:30 AM (will be updated throughout route)
    for i in range(0, len(truck2.route) - 1):  # going through the route
        distance = miles_between[truck2.route[i], truck2.route[i + 1]]  # distance is from v1 to v2
        speed = truck2.mph  # speed is 18mph
        minutes = (distance / speed) * 60  # how many minutes it took. (miles/ 18 mph) * 60 minutes
        truck2.currentTime.add_minutes(minutes)  # current time = adding minutes to the start/current time
        delivered = Time(truck2.currentTime.hours,
                         truck2.currentTime.minutes)  # delivered uses Time class to format the delivered time
        status = "PROJECTED TO BE DELIVERED AT {}".format(delivered)  # adding the delivered time to string
        for p in truck2.truckPackage:  # for package on truck 2
            if truck2.route[i + 1] == p[1]:  # if location equals the street address then status is updated
                p[8] = status
    truck2.finalTime = truck2.currentTime  # final time updated to current_time
    print("TRUCK 2: ", *truck2.truckPackage, sep="\n")  # prints the entire list, with status. Separated by newline
    print('Truck 2 leaves HUB at 9:05 AM')
    print("Truck 2 returns to HUB at {}".format(truck2.finalTime))
    print()

    # Truck 3
    # O(N^2)
    truck3Start = Time('10:20 AM')  # Truck leaves at 10:20
    truck3.startTime = truck3Start  # Start time 10:20
    truck3.currentTime = truck3Start  # current time is start time (will be updated throughout route)
    for i in range(0, len(truck3.route) - 1):  # going through the route
        distance = miles_between[truck3.route[i], truck3.route[i + 1]]  # distance is v1 to v2
        speed = truck3.mph  # speed is 18 mph
        minutes = (distance / speed) * 60  # how many minutes it took. (miles/ 18mph) * 60 minutes
        truck3.currentTime.add_minutes(minutes)  # current time = adding minutes to the start/current time
        delivered = Time(truck3.currentTime.hours,
                         truck3.currentTime.minutes)  # delivered uses Time class to format the delivered time
        status = "PROJECTED TO BE DELIVERED AT {}".format(delivered)  # adding delivered to string
        for p in truck3.truckPackage:  # for package on truck 3
            if truck3.route[i + 1] == p[1]:  # if location equals street address then status is updated
                p[8] = status
    truck3.finalTime = truck3.currentTime  # final time updated to current_time
    print("TRUCK 3: ", *truck3.truckPackage, sep="\n")  # print the entire list, with status. Separated by newline
    print('Truck 3 leaves HUB at {}'.format(truck1.finalTime))
    print('Truck 3 returns to HUB at {}'.format(truck3.finalTime))
    print()


# Allows the user in main to view all packages based off question G1.
# G1 - show the status of all packages at a time between 8:35 a.m. and 9:25 a.m.
# O(N^2)
def first_round():
    # Truck 1
    # O(N^2)
    miles_between = graph.edge_weights  # gathering the edge weights, to keep track for the route
    stopTime = Time('9:25 AM')  # the end time for the search
    truck1Start = Time('8:00 AM')
    truck1.startTime = Time(truck1Start.hours, truck1Start.minutes)  # truck 1 leaves the HUB at 8:00 AM
    truck1.currentTime = Time('8:35 AM')  # current time is start of the search - 8:35 AM
    for i in range(0, len(truck1.route) - 1):  # going through the route
        distance = miles_between[truck1.route[i], truck1.route[i + 1]]  # distance is from v1 to v2
        speed = truck1.mph  # speed is 18 mph
        minutes = (distance / speed) * 60.0  # minutes added to current_time is (distance/ 18mph) * 60 minutes
        truck1.startTime.add_minutes(minutes)  # minutes added to the start time
        truck1.currentTime = Time(truck1.startTime.hours, truck1.startTime.minutes)  # current time = the new start time
        delivered = Time(truck1.currentTime.hours,
                         truck1.currentTime.minutes)  # delivered = the Time format of current time
        if delivered <= Time(stopTime.hours, stopTime.minutes):  # if the current_time is earlier than the stop time
            truck1.currentTime = Time(delivered.hours, delivered.minutes)  # then current time is the delivered time
            status = "DELIVERED AT {}".format(truck1.currentTime)  # current_time(delivered) is added to string
            for p in truck1.truckPackage:  # package inside of packages on truck
                if truck1.route[i + 1] == p[1]:  # if location equals address, then status is updated
                    p[8] = status
    truck1.finalTime = truck1.currentTime  # final time = current_time

    # Truck 2
    # O(N^2)
    stopTime = Time('9:25 AM')  # end time for the search
    truck2Start = Time('9:05 AM')  # truck 2 leaves at 9:05 AM
    truck2.startTime = Time(truck2Start.hours, truck2Start.minutes)  # start time is 10:30 AM
    truck2.currentTime = Time('8:35 AM')  # current_time is start of search
    for i in range(0, len(truck2.route) - 1):  # going through route
        distance = miles_between[truck2.route[i], truck2.route[i + 1]]  # distance is from v1 - v2
        speed = truck2.mph  # speed is 18 mph
        minutes = (distance / speed) * 60.0  # minutes added to current time = (distance/ 18mph) * 60 minutes
        truck2.startTime.add_minutes(minutes)  # adding those minutes to startTime
        truck2.currentTime = Time(truck2.startTime.hours, truck2.startTime.minutes)  # current time = the new start time
        delivered = Time(truck2.currentTime.hours, truck2.currentTime.minutes)  # delivered = current_time
        if delivered <= Time(stopTime.hours,
                             stopTime.minutes):  # if current_time(delivered) is earlier than the stop time
            truck1.currentTime = Time(delivered.hours, delivered.minutes)  # then current_time is the delivered time
            status = "DELIVERED AT {}".format(truck2.currentTime)  # current_time(delivered) added to string
            for p in truck2.truckPackage:  # package inside of packages on truck
                if truck2.route[i + 1] == p[1]:  # if location equals address, then status is updated
                    p[8] = status
    truck2.finalTime = truck2.currentTime  # final_time = current_time

    # Truck 3
    # O(N^2)
    stopTime = Time('9:25 AM')  # end time for search
    truck3Start = Time('10:20 AM')  # truck 3 leaves at 10:20
    truck3.startTime = Time(truck3Start.hours, truck3Start.minutes)  # start time is 10:20
    truck3.currentTime = Time('8:35 AM')  # current_time is start of search
    for i in range(0, len(truck3.route) - 1):  # going through the route
        distance = miles_between[truck3.route[i], truck3.route[i + 1]]  # distance is from v1 to v2
        speed = truck3.mph  # speed is 18.0
        minutes = (distance / speed) * 60.0  # adding minutes = (distance / 18.0mph) * 60 minutes
        truck3.startTime.add_minutes(minutes)  # add those minutes to start time
        truck3.currentTime = Time(truck3.startTime.hours, truck3.startTime.minutes)  # current time = the new start time
        delivered = Time(truck3.currentTime.hours, truck3.currentTime.minutes)  # delivered equals current
        if delivered <= Time(stopTime.hours, stopTime.minutes):  # if delivered time is before stop
            truck3.currentTime = Time(delivered.hours, delivered.minutes)  # current time becomes delivered time
            status = "DELIVERED AT {}".format(truck3.currentTime)  # add on current time (delivered) to string
            for p in truck3.truckPackage:  # for package in truck
                if truck3.route[i + 1] == p[1]:  # if location equals address
                    p[8] = status  # update status to delivered
    truck3.finalTime = truck3.currentTime

    # print list of all packages separated by newline
    print('----------------------------------------------------------------------------------------------------------')
    print('ALL PACKAGES STATUS BETWEEN 8:35 AM AND 9:25 AM')
    print('----------------------------------------------------------------------------------------------------------')
    print(*truck1.truckPackage, sep="\n")
    print(*truck2.truckPackage, sep="\n")
    print(*truck3.truckPackage, sep="\n")
    print(
        'Truck 1 left HUB at 8:00 AM and returns at {} \n Truck 2 left HUB at 9:05 AM and returns at {} \nTruck 3 will leave HUB at 10:20 AM '.format(
            truck1.finalTime, truck2.finalTime))


# Allows the user in main to view all packages based off question G2.
# G2 - show the status of all packages at a time between 9:35 a.m. and 10:25 a.m.
# O(N^2)
def secondRound():
    # Truck 1
    # O(N^2)
    miles_between = graph.edge_weights  # gathering the edge weights, to keep track for the route
    stopTime = Time('10:25 AM')  # the end time for the search
    truck1Start = Time('8:00 AM')
    truck1.startTime = Time(truck1Start.hours, truck1Start.minutes)  # truck 1 leaves the HUB at 8:00 AM
    truck1.currentTime = Time('9:35 AM')  # current time is start of the search - 8:35 AM
    for i in range(0, len(truck1.route) - 1):  # going through the route
        distance = miles_between[truck1.route[i], truck1.route[i + 1]]  # distance is from v1 to v2
        speed = truck1.mph  # speed is 18 mph
        minutes = (distance / speed) * 60.0  # minutes added to current_time is (distance/ 18mph) * 60 minutes
        truck1.startTime.add_minutes(minutes)  # minutes added to the start time
        truck1.currentTime = Time(truck1.startTime.hours, truck1.startTime.minutes)  # current time = the new start time
        delivered = Time(truck1.currentTime.hours,
                         truck1.currentTime.minutes)  # delivered = the Time format of current time
        if delivered <= Time(stopTime.hours, stopTime.minutes):  # if the current_time is earlier than the stop time
            truck1.currentTime = Time(delivered.hours, delivered.minutes)  # then current time is the delivered time
            status = "DELIVERED AT {}".format(truck1.currentTime)  # current_time(delivered) is added to string
            for p in truck1.truckPackage:  # package inside of packages on truck
                if truck1.route[i + 1] == p[1]:  # if location equals address, then status is updated
                    p[8] = status
    truck1.finalTime = truck1.currentTime  # final time = current_time



    # Truck 2
    # O(N^2)
    stopTime = Time('10:25 AM')  # end time for the search
    truck2Start = Time('9:05 AM')  # truck 2 leaves at 9:05 AM
    truck2.startTime = Time(truck2Start.hours, truck2Start.minutes)  # start time is 9:05 AM
    truck2.currentTime = Time('9:35 AM')  # current_time is start of search
    for i in range(0, len(truck2.route) - 1):  # going through route
        distance = miles_between[truck2.route[i], truck2.route[i + 1]]  # distance is from v1 - v2
        speed = truck2.mph  # speed is 18 mph
        minutes = (distance / speed) * 60.0  # minutes added to current time = (distance/ 18mph) * 60 minutes
        truck2.startTime.add_minutes(minutes)  # adding those minutes to startTime
        truck2.currentTime = Time(truck2.startTime.hours, truck2.startTime.minutes)  # current time = the new start time
        delivered = Time(truck2.currentTime.hours, truck2.currentTime.minutes)  # delivered = current_time
        if delivered <= Time(stopTime.hours,
                             stopTime.minutes):  # if current_time(delivered) is earlier than the stop time
            truck1.currentTime = Time(delivered.hours, delivered.minutes)  # then current_time is the delivered time
            status = "DELIVERED AT {}".format(truck2.currentTime)  # current_time(delivered) added to string
            for p in truck2.truckPackage:  # package inside of packages on truck
                if truck2.route[i + 1] == p[1]:  # if location equals address, then status is updated
                    p[8] = status
    truck2.finalTime = truck2.currentTime  # final_time = current_time


    # Truck 3
    # O(N^2)
    stopTime = Time('10:25 AM')  # end time for search
    truck3Start = Time('10:20 AM')  # truck 3 leaves at 10:20 AM
    truck3.startTime = Time(truck3Start.hours, truck3Start.minutes)  # start time is 10:20
    truck3.currentTime = Time('9:35 AM')  # current_time is start of search
    for i in range(0, len(truck3.route) - 1):  # going through the route
        distance = miles_between[truck3.route[i], truck3.route[i + 1]]  # distance is from v1 to v2
        speed = truck3.mph  # speed is 18.0
        minutes = (distance / speed) * 60.0  # adding minutes = (distance / 18.0mph) * 60 minutes
        truck3.startTime.add_minutes(minutes)  # add those minutes to start time
        truck3.currentTime = Time(truck3.startTime.hours,
                                  truck3.startTime.minutes)  # current time = the new start time
        delivered = Time(truck3.currentTime.hours, truck3.currentTime.minutes)  # delivered equals current
        if delivered <= Time(stopTime.hours, stopTime.minutes):  # if delivered time is before stop
            truck3.currentTime = Time(delivered.hours, delivered.minutes)  # current time becomes delivered time
            status = "DELIVERED AT {}".format(truck3.currentTime)  # add on current time (delivered) to string
            for p in truck3.truckPackage:  # for package in truck
                if truck3.route[i + 1] == p[1]:  # if location equals address
                    p[8] = status  # update status to delivered

    truck3.finalTime = truck3.currentTime


    # print all packages separated by newline
    print('ALL PACKAGES STATUS BETWEEN 9:35 AM AND 10:25 AM')
    print('----------------------------------------------------------------------------------------------------------')
    print(*truck1.truckPackage, sep="\n")
    print(*truck2.truckPackage, sep="\n")
    print(*truck3.truckPackage, sep="\n")
    print(
        'Truck 1 left HUB at 8:00 AM and returned at {} \n Truck 2 left HUB at 9:05 AM and returns at {} \nTruck 3 left HUB at 10:20 AM and returns at {} '.format(
            truck1.finalTime, truck2.finalTime,  truck3.finalTime))


# Allows the user in main to view all packages based off question G3.
# G3 - show the status of all packages at a time between 12:03 p.m. and 1:12 p.m.
# O(N^2)
def thirdRound():
    # Truck 1
    # O(N^2)

    miles_between = graph.edge_weights  # gathering the edge weights, to keep track for the route
    stopTime = Time('1:12 PM')  # the end time for the search
    truck1Start = Time('8:00 AM')  # truck 1 leaves at 8:00 AM
    truck1.startTime = Time(truck1Start.hours, truck1Start.minutes)  # truck 1 leaves the HUB at 8:00 AM
    truck1.currentTime = Time('12:03 PM')  # current time is start of the search - 8:35 AM
    for i in range(0, len(truck1.route) - 1):  # going through the route
        distance = miles_between[truck1.route[i], truck1.route[i + 1]]  # distance is from v1 to v2
        speed = truck1.mph  # speed is 18 mph
        minutes = (distance / speed) * 60.0  # minutes added to current_time is (distance/ 18mph) * 60 minutes
        truck1.startTime.add_minutes(minutes)  # minutes added to the start time
        truck1.currentTime = Time(truck1.startTime.hours, truck1.startTime.minutes)  # current time = the new start time
        delivered = Time(truck1.currentTime.hours,
                         truck1.currentTime.minutes)  # delivered = the Time format of current time
        if delivered <= Time(stopTime.hours, stopTime.minutes):  # if the current_time is earlier than the stop time
            truck1.currentTime = Time(delivered.hours, delivered.minutes)  # then current time is the delivered time
            status = "DELIVERED AT {}".format(truck1.currentTime)  # current_time(delivered) is added to string
            for p in truck1.truckPackage:  # package inside of packages on truck
                if truck1.route[i + 1] == p[1]:  # if location equals address, then status is updated
                    p[8] = status
    truck1.finalTime = truck1.currentTime  # final time = current_time


    # Truck 2
    # O(N^2)
    stopTime = Time('1:12 PM')  # end time for the search
    truck2Start = Time('9:05 AM')  # truck 2 leaves at 9:05 AM
    truck2.startTime = Time(truck2Start.hours, truck2Start.minutes)  # start time is 9:05 AM
    truck2.currentTime = Time('12:03 PM')  # current_time is start of search
    for i in range(0, len(truck2.route) - 1):  # going through route
        distance = miles_between[truck2.route[i], truck2.route[i + 1]]  # distance is from v1 - v2
        speed = truck2.mph  # speed is 18 mph
        minutes = (distance / speed) * 60.0  # minutes added to current time = (distance/ 18mph) * 60 minutes
        truck2.startTime.add_minutes(minutes)  # adding those minutes to startTime
        truck2.currentTime = Time(truck2.startTime.hours, truck2.startTime.minutes)  # current time = the new start time
        delivered = Time(truck2.currentTime.hours, truck2.currentTime.minutes)  # delivered = current_time
        if delivered <= Time(stopTime.hours,
                             stopTime.minutes):  # if current_time(delivered) is earlier than the stop time
            truck1.currentTime = Time(delivered.hours, delivered.minutes)  # then current_time is the delivered time
            status = "DELIVERED AT {}".format(truck2.currentTime)  # current_time(delivered) added to string
            for p in truck2.truckPackage:  # package inside of packages on truck
                if truck2.route[i + 1] == p[1]:  # if location equals address, then status is updated
                    p[8] = status
    truck2.finalTime = truck2.currentTime  # final_time = current_time

    # Truck 3
    # O(N^2)
    stopTime = Time('1:12 PM')  # end time for search
    truck3Start = Time('10:20 AM')  # truck 3 leaves 10:20
    truck3.startTime = Time(truck3Start.hours, truck3Start.minutes)  # start time
    truck3.currentTime = Time('12:03 PM')  # current_time is start of search
    for i in range(0, len(truck3.route) - 1):  # going through the route
        distance = miles_between[truck3.route[i], truck3.route[i + 1]]  # distance is from v1 to v2
        speed = truck3.mph  # speed is 18.0
        minutes = (distance / speed) * 60.0  # adding minutes = (distance / 18.0mph) * 60 minutes
        truck3.startTime.add_minutes(minutes)  # add those minutes to start time
        truck3.currentTime = Time(truck3.startTime.hours,
                                  truck3.startTime.minutes)  # current time = the new start time
        delivered = Time(truck3.currentTime.hours, truck3.currentTime.minutes)  # delivered equals current
        if delivered <= Time(stopTime.hours, stopTime.minutes):  # if delivered time is before stop
            truck3.currentTime = Time(delivered.hours, delivered.minutes)  # current time becomes delivered time
            status = "DELIVERED AT {}".format(truck3.currentTime)  # add on current time (delivered) to string
            for p in truck3.truckPackage:  # for package in truck - updating address at 10:20
                if p[7] == 'W':
                    truck3.remove(p)  # remove all information
                    updateP9 = ['9', '410 S State St', 'Salt Lake City', 'UT', '84111', 'EOD', '2',
                                'Updated to new address', status]  # insert package 9 to updated address
                    truck3.insert(updateP9)
                if truck3.route[i + 1] == p[1]:  # if location equals address
                    p[8] = status  # update status to delivered
    truck3.finalTime = truck3.currentTime

    # print all packages separated by newline
    print('ALL PACKAGES STATUS BETWEEN 12:03 PM AND 1:12 PM')
    print('----------------------------------------------------------------------------------------------------------')
    print(*truck1.truckPackage, sep="\n")
    print(*truck2.truckPackage, sep="\n")
    print(*truck3.truckPackage, sep="\n")
    print(
        'Truck 1 left HUB at 8:00 AM and returned at {} \n Truck 2 left HUB at 9:05 AM and returned at {} \nTruck 3 left HUB at 10:20 AM  and returned at {} '.format(
            truck1.finalTime, truck2.finalTime, truck3.finalTime))


# function allowing user to search for a time to check on status of all packages
# status_time is grabbed from main as input from user
def allTimes(status_time):
    create_best_route()
    # Truck 1
    # O(N^2)
    miles_between = graph.edge_weights  # gathering the edge weights, to keep track for the route
    stopTime = Time(status_time)  # stop time is the input on main
    truck1Start = Time('8:00 AM')  # truck 1 leaves at 8:00 AM
    truck1.startTime = Time(truck1Start.hours, truck1Start.minutes)  # startTime = Time format
    truck1.currentTime = Time(truck1Start.hours, truck1Start.minutes)  # current time is also 8:00 AM (start of day)
    for i in range(0, len(truck1.route) - 1):  # go through packages on truck
        distance = miles_between[truck1.route[i], truck1.route[i + 1]]  # distance is from v1 to v2
        speed = truck1.mph  # speed is 18.0 mph
        minutes = (distance / speed) * 60.0  # added minutes = (distance / 18.0mph) * 60.0 minutes
        truck1.currentTime.add_minutes(minutes)  # add those minutes to current time
        delivered = Time(truck1.currentTime.hours, truck1.currentTime.minutes)  # delivered = Time format of current
        if delivered < Time(stopTime.hours,
                            stopTime.minutes):  # if delivered (current) is before or equal to status_time
            truck1.currentTime = Time(delivered.hours, delivered.minutes)  # current = delivered time
            status = "DELIVERED AT {}".format(truck1.currentTime)  # delivered added to str
            for p in truck1.truckPackage:  # for packages in packages one truck
                if truck1.route[i + 1] == p[1]:  # if location equals address
                    p[8] = status  # update status
        truck1.finalTime = truck1.currentTime

    # Truck 2
    # O(N^2)
    truck2Start = Time('9:05 AM')  # truck 2 leaves at 9:05 AM
    truck2.startTime = Time(truck2Start.hours, truck2Start.minutes)  # start time is 9:05
    truck2.currentTime = Time(truck2Start.hours, truck2Start.minutes)  # current time = 9:05
    for i in range(0, len(truck2.route) - 1):  # go through packages on truck
        distance = miles_between[truck2.route[i], truck2.route[i + 1]]  # distance is from v1 to v2
        speed = truck2.mph  # speed = 18.0
        minutes = (distance / speed) * 60.0  # minutes to add = (distnace/ 18.0mph) * 60.0 mph
        truck2.currentTime.add_minutes(minutes)  # add those minutes to curent time
        delivered = Time(truck2.currentTime.hours,
                         truck2.currentTime.minutes)  # delivered = Time format of current time
        if delivered <= Time(stopTime.hours,
                             stopTime.minutes):  # if delivered (current) is before or equal to status_time
            truck1.currentTime = Time(delivered.hours, delivered.minutes)  # current = delivered time
            status = "DELIVERED AT {}".format(truck2.currentTime)  # delivered added to str
            for p in truck2.truckPackage:  # for packages in packages one truck
                if truck2.route[i + 1] == p[1]:  # if location equals address
                    p[8] = status  # update status
    truck2.finalTime = truck2.currentTime

    # Truck 3
    # O(N^2)
    truck3Start = Time('10:20 AM')  # truck leaves at 10:20 AM
    truck3.startTime = Time(truck3Start.hours, truck3Start.minutes)  # starttime
    truck3.currentTime = Time(truck3Start.hours, truck3Start.minutes)  # current time is start time
    for i in range(0, len(truck3.route) - 1):  # go through packages on truck
        distance = miles_between[truck3.route[i], truck3.route[i + 1]]  # distance is from v1 to v2
        speed = truck3.mph  # speed = 18.0
        minutes = (distance / speed) * 60.0  # minutes to add = (distnace/ 18.0mph) * 60.0 mph
        truck3.currentTime.add_minutes(minutes)  # add those minutes to curent time
        delivered = Time(truck3.currentTime.hours,
                         truck3.currentTime.minutes)  # delivered = Time format of current time
        if delivered <= Time(stopTime.hours,
                             stopTime.minutes):  # if delivered (current) is before or equal to status_time
            truck3.currentTime = Time(delivered.hours, delivered.minutes)  # current = delivered time
            status = "DELIVERED AT {}".format(truck3.currentTime)  # delivered added to str
            for p in truck3.truckPackage:  # for packages in packages one truck
                if truck3.route[i + 1] == p[1]:  # if location equals address
                    p[8] = status  # update status
    truck3.finalTime = truck3.currentTime

    # print all packages, seperated by newline
    print('----------------------------------------------------------------------------------------------------------')
    print(*truck1.truckPackage, sep="\n")
    print(*truck2.truckPackage, sep="\n")
    print(*truck3.truckPackage, sep="\n")
    print(
        'Truck 1 leaves HUB from 8:00 AM until {} \n Truck 2 leaves HUB from 9:05 AM until {} \nTruck 3 leaves HUB from {} until {} '.format(
            truck1.finalTime, truck2.finalTime, truck1.finalTime, truck3.finalTime))


def search_id(package_id):
    miles_between = graph.edge_weights  # gathering the edge weights, to keep track for the route

    # Truck 1
    # O(N^2)
    truck1Start = Time('8:00 AM')  # Truck 1 leaves at 8:00 AM
    truck1.startTime = truck1Start  # start time = 8:00 AM
    truck1.currentTime = truck1Start  # current time is also 8:00 AM (will be updated throughout route)
    for i in range(0, len(truck1.route) - 1):  # going through the route
        distance = miles_between[truck1.route[i], truck1.route[i + 1]]  # distance is from v1 to v2
        speed = truck1.mph  # speed is 18mph
        minutes = (distance / speed) * 60.0  # how many minutes it took. (miles/ 18mph) * 60 minutes
        truck1.currentTime.add_minutes(minutes)  # current time = adding minutes to the start/current time
        delivered = Time(truck1.currentTime.hours,
                         truck1.currentTime.minutes)  # delivered uses Time class to format the delivered time
        status = "PROJECTED TO BE DELIVERED at {}".format(delivered)  # adding the delivered time to string
        for p in truck1.truckPackage:  # for the package in packages on truck 1
            if truck1.route[i + 1] == p[1] and package_id == p[0]:  # if the location equals the street address then status is updated and if input equals id
                p[8] = status
                print(p)  # print package information
    truck1.finalTime = truck1.currentTime  # final time updated to current_time

    # Truck 2
    # O(N^2)
    truck2Start = Time('9:05 AM')  # Truck leaves at 9:15 AM
    truck2.startTime = truck2Start  # Start time is 9:15 AM
    truck2.currentTime = truck2Start  # current time is also 10:30 AM (will be updated throughout route)
    for i in range(0, len(truck2.route) - 1):  # going through the route
        distance = miles_between[truck2.route[i], truck2.route[i + 1]]  # distance is from v1 to v2
        speed = truck2.mph  # speed is 18mph
        minutes = (distance / speed) * 60  # how many minutes it took. (miles/ 18 mph) * 60 minutes
        truck2.currentTime.add_minutes(minutes)  # current time = adding minutes to the start/current time
        delivered = Time(truck2.currentTime.hours,
                         truck2.currentTime.minutes)  # delivered uses Time class to format the delivered time
        status = "PROJECTED TO BE DELIVERED AT {}".format(delivered)  # adding the delivered time to string
        for p in truck2.truckPackage:  # for package on truck 2
            if truck2.route[i + 1] == p[1] and package_id == p[0]:  # if location equals the street address then and input equals ID  status is updated
                p[8] = status
                print(p)  # print all information for package
    truck2.finalTime = truck2.currentTime  # final time updated to current_time

    # Truck 3
    # O(N^2)
    truck3Start = Time('10:20 AM')  # Truck leaves at 10:20
    truck3.startTime = truck3Start  # Start time
    truck3.currentTime = truck3Start  # current time is start time (will be updated throughout route)
    for i in range(0, len(truck3.route) - 1):  # going through the route
        distance = miles_between[truck3.route[i], truck3.route[i + 1]]  # distance is v1 to v2
        speed = truck3.mph  # speed is 18 mph
        minutes = (distance / speed) * 60  # how many minutes it took. (miles/ 18mph) * 60 minutes
        truck3.currentTime.add_minutes(minutes)  # current time = adding minutes to the start/current time
        delivered = Time(truck3.currentTime.hours,
                         truck3.currentTime.minutes)  # delivered uses Time class to format the delivered time
        status = "PROJECTED TO BE DELIVERED AT {}".format(delivered)  # adding delivered to string
        for p in truck3.truckPackage:  # for package on truck 3
            if truck3.route[i + 1] == p[1] and p[0] == package_id:  # if location equals street address then status is updated and input matches id
                p[8] = status
                print(p)  # print information for that package
    truck3.finalTime = truck3.currentTime  # final time updated to current_time
