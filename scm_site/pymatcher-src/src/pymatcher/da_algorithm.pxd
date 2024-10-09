from libcpp.vector cimport vector
cdef extern from "da_algorithm.cpp":
    pass

cdef extern from "da_algorithm.hpp":
    cdef cppclass RankList:
        RankList(const vector[int]& rank_list) except +
        RankList() except +
        int get_rank(int student_id) except +
    
    cdef cppclass Course:
        Course() except +
        Course(const RankList *ranklist, int capacity)
        int get_last_alloted_student() except +
        int get_last_alloted_rank() except +
        int get_total_slots() except +
        int get_available_slots() except +
        void reset() except +
        
    
    cdef cppclass Student:
        Student() except +
        Student(const vector[int]& preferences, int id)
        int get_alloted_course_id() except +
        int get_id() except +
        void reset() except +
    
    cdef cppclass GaleShapley:
        @staticmethod
        void perform_allotment(vector[Student]& students, vector[Course]& courses) except +

        

