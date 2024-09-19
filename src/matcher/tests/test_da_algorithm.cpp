#include "da_algorithm.hpp"
#include <gtest/gtest.h>

TEST(Matching, SingleCourseSingleStudent)
{
    RankList main_rank_list({1});
    std::vector<Course> courses = {Course(main_rank_list, 1)};
    std::vector<Student> students = {Student({0}, 0)};
    GaleShapley::perform_allotment(students, courses);
    EXPECT_EQ(students[0].get_alloted_course_id(), 0);
    EXPECT_EQ(courses[0].get_last_alloted_rank(), 1);
    EXPECT_EQ(courses[0].get_last_alloted_student(), 0);
    EXPECT_EQ(courses[0].get_available_slots(), 0);
}

TEST(Matching, MultipleCourseSingleStudent)
{
    RankList main_rank_list({100});
    std::vector<Course> courses = {Course(main_rank_list, 2), Course(main_rank_list, 3),
                                   Course(main_rank_list, 5)};
    std::vector<Student> students = {Student({1}, 0)};
    GaleShapley::perform_allotment(students, courses);

    EXPECT_EQ(students[0].get_alloted_course_id(), 1);

    EXPECT_EQ(courses[0].get_last_alloted_rank(), -1);
    EXPECT_EQ(courses[0].get_last_alloted_student(), -1);
    EXPECT_EQ(courses[0].get_available_slots(), courses[0].get_total_slots());

    EXPECT_EQ(courses[1].get_last_alloted_rank(), 100);
    EXPECT_EQ(courses[1].get_last_alloted_student(), 0);
    EXPECT_EQ(courses[1].get_available_slots(), courses[1].get_total_slots() - 1);

    EXPECT_EQ(courses[2].get_last_alloted_rank(), -1);
    EXPECT_EQ(courses[2].get_last_alloted_student(), -1);
    EXPECT_EQ(courses[2].get_available_slots(), courses[2].get_total_slots());
}

TEST(Matching, SingleCourseMultipleStudent)
{
    RankList main_rank_list({4, 5, 6, 3, 2, 1});
    std::vector<Course> courses = {Course(main_rank_list, 6)};
    std::vector<Student> students = {
        Student({0}, 0), Student({0}, 1), Student({0}, 2),
        Student({0}, 3), Student({0}, 4), Student({}, 5), // Student has not chosen any option
    };
    GaleShapley::perform_allotment(students, courses);

    for (int i = 0; i < 5; i++)
    {
        EXPECT_EQ(students[i].get_alloted_course_id(), 0);
    }
    EXPECT_EQ(students[5].get_alloted_course_id(), -1);

    EXPECT_EQ(courses[0].get_last_alloted_rank(), 6);
    EXPECT_EQ(courses[0].get_last_alloted_student(), 2);
    EXPECT_EQ(courses[0].get_available_slots(), 1);

    // All students get alloted a course
    GaleShapley::reset(students);
    GaleShapley::reset(courses);
    students.pop_back();
    students.push_back(Student({0}, 5));
    GaleShapley::perform_allotment(students, courses);
    EXPECT_EQ(courses[0].get_available_slots(), 0);

    // Nobody gets alloted
    GaleShapley::reset(courses);
    students = {
        Student({}, 0), Student({}, 1), Student({}, 2),
        Student({}, 3), Student({}, 4), Student({}, 5),
    };
    GaleShapley::perform_allotment(students, courses);
    EXPECT_EQ(courses[0].get_available_slots(), 6);

    for (int i = 0; i < 6; i++)
    {
        EXPECT_EQ(students[i].get_alloted_course_id(), -1);
    }
}

TEST(Matching, MultipleCourseMultipleStudent)
{
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
    EXPECT_EQ(students[0].get_alloted_course_id(), 2);
    EXPECT_EQ(students[1].get_alloted_course_id(), 0);
    EXPECT_EQ(students[2].get_alloted_course_id(), 1);
    EXPECT_EQ(students[3].get_alloted_course_id(), 2);
    EXPECT_EQ(students[4].get_alloted_course_id(), 2);
    EXPECT_EQ(students[5].get_alloted_course_id(), 3);
    EXPECT_EQ(students[6].get_alloted_course_id(), -1);
    EXPECT_EQ(students[7].get_alloted_course_id(), 3);
    EXPECT_EQ(students[8].get_alloted_course_id(), 3);
    EXPECT_EQ(students[9].get_alloted_course_id(), 0);
    EXPECT_EQ(students[10].get_alloted_course_id(), 3);

}

int main(int argc, char *argv[])
{
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}