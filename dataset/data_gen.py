import csv
import json
import random

SEED = 1001

# For development purpose, randomly generate the number of seats in each program,
random.seed(SEED)
# All capacities do not have the equal probability, also maintain a probability distribution
program_capacity_list = [30, 60, 90, 120, 180, 240]
weights = [0.1, 0.4, 0.2, 0.2, 0.05, 0.05]
get_capacity = lambda : random.choices(
    population=program_capacity_list, weights=weights, k=1
)[0]


city_names_alternate_names = {
    "Bagalkot": ["bagalkot"],
    "Ballari": ["bellary", "bellari", "ballari"],
    "Belgavi": ["belgavi", "belagavi", "belgaum"],
    "Bengaluru": ["bangalore", "banlore", "bengaluru", "bang rural", "banglore"],
    "Bidar": ["bidar"],
    "Bidar": ["bidar"],
    "Chamarajanagar": ["chamarajanagar", "chamaraja"],
    "Chikballapur": ["chikballapur", "chickballapur"],
    "Chikkamagaluru": ["chikkamagaluru", "chickmagalur", "magalur", "chickkaballapur"],
    "Chitradurga": ["chitradurga"],
    "Davangere": ["davangere", "davanagere"],
    "Dharwad": ["dharwad", "darward", "dharward"],
    "Gadag": ["gadag"],
    "Hassan": ["hassan"],
    "Haveri": ["haveri"],
    "Hubballi": ["hubbli", "hubballi", "hubli"],
    "Kalaburagi": ["kalaburagi", "kalburgi", "gulbarga", "gulbarga"],
    "Kodagu": ["kodagu"],
    "Kolar": ["kolar"],
    "Koppal": ["koppal"],
    "Karwar": ["karwar"],
    "Mandya": ["mandya"],
    "Mangaluru": ["mangaluru", "mangalore"],
    "Moodbidri": ["moodbidri", "moodabidri"],
    "Mysuru": ["mysuru", "mysore"],
    "Raichur": ["raichur"],
    "Ramanagara": ["ramanagara"],
    "Shivamogga": ["shivamogga", "shimoga"],
    "Tumakuru": ["tumakuru", "tumkur"],
    "Udupi": ["udupi"],
    "Vijayapura": ["vijayapura", "vijayapur", "vijaypura"],
    "Uttar Kannad": ["uttar kannad", "uttara"],
    "Dakshina Kannada": [
        "dakshin kannad",
        "dakshin",
        "dk",
        "d.k",
        "d. k",
        "d .k",
        "d . k",
        "d k",
    ],
}


def extract_city_from_address(address: str):
    address = address.lower()
    for k, v in city_names_alternate_names.items():
        for alternate_spelling in v:
            if alternate_spelling in address:
                return k
    return "-"


# Read the courses
courses = {}
with open("KCET_COURSES_LIST.csv") as f:
    reader = csv.reader(f)
    for line in reader:
        courses[line[0]] = line[1]

# Read programs from the csv file
colleges = []
with open("KCET_PROGRAMS_LIST.csv") as f:
    reader = csv.reader(f)
    for line in reader:
        college_code = line[0]
        college_type = line[1]
        college_name = line[2]
        college_address = line[3]
        college_programs = [p for p in line[4].replace(" ", "").split(";") if p]
        college_programs = {
            p: get_capacity() for p in college_programs
        }
        college_city = extract_city_from_address(college_address)
        if college_city == "-":
            print("WARNING: No city found for ", college_address)

        colleges += [
            {
                "name": college_name,
                "address": college_address,
                "code": college_code,
                "type": college_type,
                "city": college_city,
                "website": None,
                "courses": college_programs,
            }
        ]


# Write the final data as json
with open("data.json", "w") as data_file:
    data_dict = {
        "colleges": colleges,
        "courses": courses,
        "ranklists": [{"short_name": "ENG-RL", "name": "Engineering rank list"}],
    }
    json.dump(data_dict, data_file, indent=4, sort_keys=True)
