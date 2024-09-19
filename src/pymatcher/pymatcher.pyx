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

    def __init__(self, ranklist: PyRankList, capacity: int) -> None:
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

    def __init__(self, preferences, id) -> None:
        self.c_student = Student(preferences, id)
    
    def get_alloted_course_id(self):
        return self.c_student.get_alloted_course_id()
    
    def get_id(self):
        return self.get_id()
    
    def reset(self):
        self.reset()


cdef class PyGaleShapley:
    @staticmethod
    def perform_allocation(students, courses):
        # https://stackoverflow.com/questions/58171611/how-to-convert-python-object-to-a-stdvector-of-cython-extension-type-and-back
        # TODO: Try implementing it without an additional copy
        cdef vector[Student] c_students
        cdef vector[Course] c_courses

        cdef PyStudent s
        for s in students:
            c_students.push_back(s.c_student)

        cdef PyCourse c
        for c in courses:
            c_courses.push_back(c.c_course)
        GaleShapley.perform_allotment(c_students, c_courses)
