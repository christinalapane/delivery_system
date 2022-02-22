# Christina LaPane Student ID: 008207171
import csv


# Hash Table is a chaining table
# Improves the speed that packages can be accessed


class HashTable:
    # 10 buckets, all start as empty
    # O(N)
    def __init__(self, initial_capacity=10):
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # Insert new package into table. [0], first index, from 'package.csv' is the package_id
    # The package_id acts as teh key
    # O(1)
    def insert(self, key, package):
        package[0] = int(package[0])
        bucket = key % len(self.table)
        self.table[bucket].append(package)
        if package[7] != "9:05":
            package.append("AT_HUB")  # Packages all start out as 'AT HUB'.. changes after 8:00 AM
        if package[7] == "9:05":  # Packages that are delayed
            package.append("DELAYED_ON_FLIGHT")

    # Searches package with matching key (package_id)
    # O(N)
    def search(self, key):

        # bucket list where key should be found
        bucket = key % len(self.table)
        bucketList = self.table[bucket]

        # In bucket, search for key (package_id)
        for package in bucketList:
            if package[0] == key:  # if package_id equals key
                return package  # package is found and returned all information
        return None  # Package is not found and returns no information

    # Removes a package that matches with the key (package_id)
    # O(N)
    def remove(self, key):

        # bucket list where key should be found
        bucket = hash(key) % len(self.table)
        bucketList = self.table[bucket]

        # in bucket, search for key(package_id)
        for package in bucketList:
            if package[0] == key:  # if package_id equals key
                bucketList.remove(key)  # remove all package information for that package_id


# reads all data from 'package.csv'
# Enters all information into table
# O(N)
def get_package_data(file):
    hash_package = HashTable()  # declaring to this class
    with open(file) as csvFile:  # open 'package.csv' and read
        csvReader = csv.reader(csvFile)
        next(csvReader, None)  # skips the header
        for row in csvReader:  # for each remaining row, insert all information through row[0] (package_id)
            hash_package.insert(int(row[0]), row)
    return hash_package  # returns all infomration through table


# Initializes the packageTable
packageTable = get_package_data('package.csv')



