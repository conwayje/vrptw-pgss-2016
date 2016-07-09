#World_record_test.py

from ImportCustomers import import_customers
from Depot import Depot
from Path import Path
from Visual import Visual
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("filename")

args = parser.parse_args()

filename = args.filename

if filename == "RC208.txt":
	rc208 = True
else:
	rc208 = False


cust = []

if rc208:
	stringroute1 = "65 83 64 95 92 71 72 38 39 44 42 61 81 94 67 62 50 34 31 29 27 26 28 30 32 33 76 89 63 85 51 84 56 66"
	stringroute2 = "69 98 88 53 12 11 15 16 47 78 73 79 7 6 2 8 46 4 45 5 3 1 43 40 36 35 37 41 54 96 93 91 80"
	stringroute3 = "90 82 99 52 57 23 21 18 19 49 22 24 20 48 25 77 58 75 97 59 87 74 86 9 13 10 14 17 60 55 100 70 68"
	cust = import_customers("RC208.txt")

else:
	stringroute1 = "93 5 75 2 1 99 100 97 92 94 95 98 7 3 4 89 91 88 84 86 83 82 85 76 71 70 73 80 79 81 78 77 96 87 90"
	stringroute2 = "67 63 62 74 72 61 64 66 69 68 65 49 55 54 53 56 58 60 59 57 40 44 46 45 51 50 52 47 43 42 41 48"
	stringroute3 = "20 22 24 27 30 29 6 32 33 31 35 37 38 39 36 34 28 26 23 18 19 16 14 12 15 17 13 25 9 11 10 8 21"
	cust = import_customers("C201.txt")

path1 = Path([])
path2 = Path([])
path3 = Path([])

route1 = []
route2 = []
route3 = []

route1 = str.split(stringroute1)
route2 = str.split(stringroute2)
route3 = str.split(stringroute3)


for i in route1:
	path1.route.append(cust[int(i)-1])

for i in route2:
	path2.route.append(cust[int(i)-1])

for i in route3:
	path3.route.append(cust[int(i)-1])


print path1.get_distance() + path2.get_distance() + path3.get_distance()
