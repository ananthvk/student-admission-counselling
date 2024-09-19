#include "da_algorithm.hpp"

RankList::RankList(const std::vector<int> &rank_list) : rank_list(rank_list) {}

// Returns the rank/priority of the student, lower the number, higher the priority
int RankList::get_rank(int student_id) const { return rank_list[student_id]; }

Course::Course(const RankList &ranklist, int capacity)
    : ranklist(ranklist), capacity(capacity), available(capacity)
{
}

int Course::get_last_alloted_student() const
{
    if (pq_rank_student.empty())
        return -1;
    return pq_rank_student.top().second;
}

int Course::get_last_alloted_rank() const
{
    if (pq_rank_student.empty())
        return -1;
    return pq_rank_student.top().first;
}

int Course::get_total_slots() const { return capacity; }

int Course::get_available_slots() const { return available; }

Student::Student(const std::vector<int> &preferences, int id)
    : preferences(preferences), alloted_course(-1), current_preference_index(0), id(id)
{
}

int Student::get_alloted_course_id() const { return alloted_course; }

int Student::get_id() const { return id; }

void GaleShapley::perform_allotment(std::vector<Student> &students, std::vector<Course> &courses)
{
    // Contains a queue of students who have not been alloted, and still have pending choices to
    // be considered
    std::queue<Student *> not_alloted_students;
    for (auto &student : students)
        not_alloted_students.push(&student);

    while (!not_alloted_students.empty())
    {
        auto student = not_alloted_students.front();
        not_alloted_students.pop();

        for (; student->current_preference_index < static_cast<int>(student->preferences.size());
             student->current_preference_index++)
        {
            auto course_id = student->preferences[student->current_preference_index];
            Course &course = courses[course_id];
            int rank = course.ranklist.get_rank(student->id);

            if (rank == -1)
            {
                // The student is not eligible for this course
                continue;
            }

            // If the course has vacancy, allot the course to the student
            if (courses[course_id].available > 0)
            {
                course.available--;
                student->alloted_course = course_id;
                course.pq_rank_student.push(std::make_pair(rank, student->id));
                break;
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
                    students[rejected_student.second].alloted_course = -1;
                    student->alloted_course = course_id;
                    course.pq_rank_student.push(std::make_pair(rank, student->id));
                    break;
                }
            }
        }
    }
}

// Removes allocation details from the student objects
void GaleShapley::reset(std::vector<Student> &students)
{
    for (auto &student : students)
    {
        student.alloted_course = -1;
        student.current_preference_index = 0;
    }
}

// Resets courses to their state before allocation
void GaleShapley::reset(std::vector<Course> &courses)
{
    for (auto &course : courses)
    {
        course.available = course.capacity;
        course.pq_rank_student = decltype(course.pq_rank_student)();
    }
}
