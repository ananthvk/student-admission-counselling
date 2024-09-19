from libcpp.vector cimport vector
cdef extern from "da_algorithm.cpp":
    pass

cdef extern from "da_algorithm.hpp":
    cdef cppclass RankList:
        vector[int] rank_list
        RankList(const vector[int]& rank_list) except +
        RankList() except +
        int get_rank(int student_id) const
        

