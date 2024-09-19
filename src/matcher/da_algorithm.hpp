#pragma once
#include <queue>
#include <vector>

class GaleShapley;

class RankList
{
    std::vector<int> rank_list;

  public:
    RankList(const std::vector<int> &rank_list);

    // Temporary
    RankList() {}

    // Returns the rank/priority of the student, lower the number, higher the priority
    int get_rank(int student_id) const;

    friend class GaleShapley;
};

class Course
{
    const RankList *ranklist;
    int capacity;
    int available;
    // Priority queue of (rank, student_id), all the alloted students for this course
    std::priority_queue<std::pair<int, int>> pq_rank_student;

  public:
    Course() : ranklist(nullptr) {}

    Course(const RankList *ranklist, int capacity);

    Course(const RankList &ranklist, int capacity);

    int get_last_alloted_student() const;

    int get_last_alloted_rank() const;

    int get_total_slots() const;

    int get_available_slots() const;

    void reset();

    friend class GaleShapley;
};

class Student
{
    std::vector<int> preferences;
    int alloted_course;
    int current_preference_index;
    int id;

  public:
    Student(const std::vector<int> &preferences, int id);

    Student() {}

    int get_alloted_course_id() const;

    int get_id() const;
    void reset();

    friend class GaleShapley;
};

class GaleShapley
{
  public:
    static void perform_allotment(std::vector<Student> &students, std::vector<Course> &courses);
};
