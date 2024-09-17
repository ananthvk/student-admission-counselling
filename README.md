# student-college matcher
This is a C++ implementation of the Gale-Shapely algorithm, also known as the deferred acceptance algorithm, which is used to obtain stable matching. Here, the application tries to match a number of students to courses in various colleges. This project aims to simulate the working of a system such as KCET, COMEDK, or JOSSA.

## Getting started

To run this project, you need install meson and ninja.

For a development build, you need to install clang, along with address sanitizer.

```
$ cd student-college-matcher
$ CXX=clang++ CC=clang meson setup -Db_sanitize=address -Ddevelopment=true --reconfigure build
$ cd build
$ meson compile
```

## Algorithm
### Pseudocode
```
while there are students who have not been alloted and still have choices to be processed
    pick a student, s
    for every choice c of s, in descending order of priority
        if course c has vacancy
            allot course c to student s
            break
        else
            if priority(s) > priority(student with lowest priority alloted in c)
                remove allotment of student with lowest priority in c
                allot course c to student s
                break
```

## Design
## Broad requirements
1. Courses should be alloted in a fair manner to every student who takes part in the allotment process. Students should not be able to influence the process by the order of their choice.
2. There is a standard list of courses (CSE, ECE, etc) which can be modified by the admin.
3. Colleges should be able to specify the courses they offer, along with its capacity.
4. The system should support various rules such as home state quota, gender pool and reservation.
5. The site admin should be able to set these rules on a course by course basis, i.e. some courses may have home state quota, while others may not have it.
6. Students should be able to make a priority list of the courses they want to apply to, the student should be able apply to every course offered by every college.
7. There should be an authentication system, with various account types such as admin, student, college.
8. After a student has been alloted a course, they should have various options - Accept the seat, slide (i.e. hold the seat in hope for a better one), or withdraw.
9. Before each round, the student should be able to modify their priority list

## Technologies used
The core algorithm will be implemented in C++ and the user interface will be a web based system. The backend will be built with Python and the frontend with HTML, CSS and Javascript. The build system is meson, along with ninja.

