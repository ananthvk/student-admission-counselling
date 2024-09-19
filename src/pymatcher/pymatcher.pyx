from da_algorithm cimport RankList

cdef class CRankList:
    cdef RankList c_ranklist
    
    def __init__(self, ranklist) -> None:
        self.c_ranklist = RankList(ranklist)
    
    def get_rank(self, student_id):
        return self.c_ranklist.get_rank(student_id)

