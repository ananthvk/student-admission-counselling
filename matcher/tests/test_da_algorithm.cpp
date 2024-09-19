#include "da-algorithm.hpp"
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
    RankList main_rank_list({1});
    std::vector<Course> courses = {Course(main_rank_list, 1)};
    std::vector<Student> students = {Student({0}, 0)};
    GaleShapley::perform_allotment(students, courses);
    EXPECT_EQ(students[0].get_alloted_course_id(), 0);
    EXPECT_EQ(courses[0].get_last_alloted_rank(), 1);
    EXPECT_EQ(courses[0].get_last_alloted_student(), 0);

}

int main(int argc, char *argv[])
{
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}