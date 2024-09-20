import random
import time
from pymatcher import PyRankList, PyGaleShapley, Students, Courses

NUMBER_OF_STUDENTS = 100
NUMBER_OF_COURSES = 10
MIN_CAPACITY_COURSE = 10
MAX_CAPACITY_COURSE = 20
MIN_NUMBER_OF_CHOICES = 0
MAX_NUMBER_OF_CHOICES = 10

random.seed(10001)

print('Generating data')
start_time = time.time()
ranks_list = list(range(1, NUMBER_OF_STUDENTS + 1))
random.shuffle(ranks_list)
ranks = PyRankList(ranks_list)

courses = Courses()
for i in range(NUMBER_OF_COURSES):
    courses.add(ranks, random.randint(MIN_CAPACITY_COURSE, MAX_CAPACITY_COURSE))

students = Students()
preferences = list(range(NUMBER_OF_COURSES))
for i in range(NUMBER_OF_STUDENTS):
    number_of_choices = random.randint(MIN_NUMBER_OF_CHOICES, MAX_NUMBER_OF_CHOICES)
    random.shuffle(preferences)
    students.add(preferences[:number_of_choices],i)
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Data generation time: {elapsed_time:.6f} seconds")

print('Starting algorithm')
start_time = time.time()
PyGaleShapley.perform_allotment(students, courses)
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Execution time: {elapsed_time:.6f} seconds")

for i in range(0, len(students)):
    print(students[i].get_alloted_course_id())
