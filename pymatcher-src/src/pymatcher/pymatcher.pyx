from da_algorithm cimport RankList, Course, Student, GaleShapley
from typing import List
from libcpp.vector cimport vector

cdef class PyRankList:
    cdef RankList c_ranklist
    
    def __init__(self, ranklist) -> None:
        self.c_ranklist = RankList(ranklist)
    
    def get_rank(self, student_id):
        return self.c_ranklist.get_rank(student_id)


cdef class PyCourse:
    cdef Course c_course

    def __init__(self, ranklist: PyRankList = None, capacity: int = None) -> None:
        if ranklist is None or capacity is None:
            return
        self.c_course = Course(&ranklist.c_ranklist, capacity)
    
    def get_last_alloted_student(self):
        return self.c_course.get_last_alloted_student()

    def get_last_alloted_rank(self):
        return self.c_course.get_last_alloted_rank()

    def get_total_slots(self):
        return self.c_course.get_total_slots()

    def get_available_slots(self):
        return self.c_course.get_available_slots()

    def reset(self):
        self.c_course.reset()


cdef class PyStudent:
    cdef Student c_student

    def __init__(self, preferences = None, id = None) -> None:
        if preferences is None or id is None:
            return
        self.c_student = Student(preferences, id)
    
    def get_alloted_course_id(self):
        return self.c_student.get_alloted_course_id()
    
    def get_id(self):
        return self.c_student.get_id()
    
    def reset(self):
        self.c_student.reset()


cdef class Students:
    cdef vector[Student] students 

    def __init__(self, li=[]):
        for item in li:
            self.add(item[0], item[1])
    
    def add(self, preferences, id):
        self.students.push_back(Student(preferences, id))

    def __getitem__(self, idx):
        s = PyStudent()
        s.c_student = self.students[idx]
        return s
    
    def __len__(self):
        return self.students.size()


cdef class Courses:
    cdef vector[Course] courses 
    
    def __init__(self, li=[]):
        for item in li:
            self.add(item[0], item[1])
    
    def add(self, ranklist: PyRankList, capacity):
        self.courses.push_back(Course(&ranklist.c_ranklist, capacity))

    def __getitem__(self, idx):
        c = PyCourse()
        c.c_course = self.courses[idx]
        return c
    
    def __len__(self):
        return self.courses.size()


cdef class PyGaleShapley:
    
    @staticmethod
    def perform_allotment(students: Students, courses: Courses):
        GaleShapley.perform_allotment(students.students, courses.courses)

        