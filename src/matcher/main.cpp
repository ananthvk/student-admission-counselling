#include "da-algorithm.hpp"
#include <iostream>

int main()
{
    // Sample ranks
    // Student id | Rank
    // There are 11 students
    // -----------|-------
    //    0           3
    //    1           5
    //    2           4
    //    3           1
    //    4           2
    //    5           8
    //    6           10
    //    7           7
    //    8           9
    //    9           6
    //    10          11

    std::vector<int> ranks = {3, 5, 4, 1, 2, 8, 10, 7, 9, 6, 11};
    RankList main_rank_list(ranks);
    std::vector<Course> courses = {Course(main_rank_list, 2), Course(main_rank_list, 1),
                                   Course(main_rank_list, 3), Course(main_rank_list, 4)};
    
    std::vector<Student> students = {
        Student({2}, 0),             // 0 3 
        Student({2, 0}, 1),          // 1 5
        Student({2, 1, 0}, 2),       // 2 4
        Student({2, 3, 1}, 3),       // 3 1
        Student({2, 3, 1}, 4),       // 4 2
        Student({2, 3, 1}, 5),       // 5 8
        Student({0, 1, 2}, 6),       // 6 10
        Student({0, 1, 3}, 7),       // 7 7
        Student({0, 2, 1, 3}, 8),    // 8 9
        Student({0, 3, 1, 2}, 9),    // 9 6
        Student({2, 0, 1, 3}, 10),   // 10 11
    };
    
    GaleShapley::perform_allotment(students, courses);
    
    for(const auto& student: students)
    {
        std::cout << student.get_id() << ": " << student.get_alloted_course_id() << std::endl;
    }

    std::cout << "Hello, world" << std::endl;
}