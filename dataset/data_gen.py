import csv
import json
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

validator = URLValidator()

COLLEGE_CODE_NAME_LENGTH = 3
COLLEGE_CODE_NUMERIC_LENGTH = 3

# First clean the input data
colleges = []
running_id = 0
with open("KCET_COLLEGE_LIST.csv") as f:
    reader = csv.reader(f)
    for line in reader:
        cleaned_line = []
        for column in line:
            if column.endswith(","):
                column = column[:-1]
            column = column.strip()
            if column.endswith("&"):
                column = column[:-1]
            column = column.strip()
            column = column.replace("\n", "")
            cleaned_line += [column]
        # Remove the last column, which is ''
        cleaned_line.pop()

        filter_expr = lambda x: x not in ["\n", ",", '"']

        filter_clean = lambda x: "".join(
            filter(filter_expr, x.encode("ascii", errors="ignore").decode())
        )

        website = filter_clean(cleaned_line[3]).replace(" ", "")

        if not website.startswith("http"):
            website = "http://" + website

        try:
            validator(website)
        except ValidationError:
            website = None

        college = {
            "name": filter_clean(cleaned_line[0]),
            "city": filter_clean(cleaned_line[1]),
            "address": filter_clean(cleaned_line[2]),
            "website": website,
            "college_type": filter_clean(cleaned_line[4]),
        }

        # Generate a college code based on city and college_type
        code = (
            college["college_type"][0].upper()
            + college["city"][:COLLEGE_CODE_NAME_LENGTH].upper()
        )
        running_id += 1
        if running_id >= 10 ** (COLLEGE_CODE_NUMERIC_LENGTH + 1):
            raise Exception(
                f"College numeric code exceeds ${COLLEGE_CODE_NUMERIC_LENGTH} digits"
            )

        code += str(running_id).zfill(COLLEGE_CODE_NUMERIC_LENGTH)
        college["code"] = code

        colleges += [college]

# Read the courses

courses = {}
with open("KCET_COURSES_LIST.csv") as f:
    reader = csv.reader(f)
    for line in reader:
        courses[line[0]] = line[1]


with open("data.json", "w") as data_file:
    data_dict = {"colleges": colleges, "courses": courses}
    json.dump(data_dict, data_file, indent=4, sort_keys=True)


"""
f = "courses": {
        "AI": "Artificial Intelligence",
        "BT": "Bio Technology",
        "CE": "Civil Engineering",
        "CH": "Chemical Engineering",
        "CS": "Computer Science Engineering",
        "EC": "Electronics and Communications Engineering",
        "IS": "Information Science and Engineering",
        "ME": "Mechanical Engineering"
    }
"""
