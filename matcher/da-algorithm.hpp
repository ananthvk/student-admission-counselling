#pragma once
#include <queue>
#include <vector>

class GaleShapley;

class RankList
{
    std::vector<int> rank_list;

  public:
    RankList(const std::vector<int> &rank_list) : rank_list(rank_list) {}

    // Returns the rank/priority of the student, lower the number, higher the priority
    int get_rank(int student_id) const { return rank_list[student_id]; }

    friend class GaleShapley;
};

class Course
{
    const RankList &ranklist;
    int capacity;
    int available;
    // Priority queue of (rank, student_id), all the alloted students for this course
    std::priority_queue<std::pair<int, int>> pq_rank_student;

  public:
    Course(const RankList &ranklist, int capacity)
        : ranklist(ranklist), capacity(capacity), available(capacity)
    {
    }

    int get_last_alloted_student() const
    {
        if (pq_rank_student.empty())
            return -1;
        return pq_rank_student.top().second;
    }

    int get_last_alloted_rank() const
    {
        if (pq_rank_student.empty())
            return -1;
        return pq_rank_student.top().first;
    }

    friend class GaleShapley;
};

class Student
{
    std::vector<int> preferences;
    int alloted_course;
    int current_preference_index;
    int id;

  public:
    Student() : alloted_course(-1), current_preference_index(0) {}

    friend class GaleShapley;
};

class GaleShapley
{
  public:
    void perform_allotment(std::vector<Student> &students, std::vector<Course> &courses)
    {
        // Contains a queue of students who have not been alloted, and still have pending choices to
        // be considered
        std::queue<Student *> not_alloted_students;
        for (auto &student : students)
            not_alloted_students.push(&student);

        while (not_alloted_students.empty())
        {
            auto student = not_alloted_students.front();
            not_alloted_students.pop();

            for (int i = student->current_preference_index; i < student->preferences.size(); i++)
            {
                auto course_id = student->preferences[i];
                Course &course = courses[course_id];
                int rank = course.ranklist.get_rank(student->id);

                // If the course has vacancy, allot the course to the student
                if (courses[course_id].available > 0)
                {
                    course.available--;
                    student->alloted_course = course_id;
                    course.pq_rank_student.push(std::make_pair(rank, student->id));
                }
                else
                {
                    // If the student's rank is higher than the course's last alloted rank, remove
                    // that allotment and allot this student instead
                    if (rank < course.get_last_alloted_rank())
                    {
                        auto rejected_student = course.pq_rank_student.top();
                        course.pq_rank_student.pop();
                        not_alloted_students.push(&students[rejected_student.second]);
                        student->alloted_course = course_id;
                        course.pq_rank_student.push(std::make_pair(rank, student->id));
                    }
                }
            }
        }
    }
};
