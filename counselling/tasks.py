from celery import shared_task
from datetime import datetime
import time
from .reports import PreferenceListReport
from .models import (
    User,
    RankList,
    RankListEntry,
    Student,
    ChoiceEntry,
    Program,
    Round,
    Allotment,
)
from pymatcher import PyRankList, PyGaleShapley, Students, Courses
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.utils import timezone
from django.core.cache import cache

import logging

logger = logging.getLogger(__name__)

def generate_report(user: User, path: str):
    logger.info("Start report generation....")
    pref_report = PreferenceListReport(user)
    logger.info("Finished report generation")
    # Overwrite the file
    if default_storage.exists(path):
        default_storage.delete(path)
        
    path = default_storage.save(
        path,
        ContentFile(pref_report.as_bytes().getvalue()),
    )
    return path

"""
This task just generates the report, it does not check if a report has to be generated or not, it is the responsibility of the caller
to do these checks
"""
@shared_task(bind=True)
def generate_report_task(self, user_id):
    user = User.objects.get(pk=user_id)
    path = f"{user.username}_choice_report.pdf"
    student: Student = user.student
    path = generate_report(user, path)
    student.last_choice_report_generation_date = timezone.now()
    student.choice_report_path = path
    student.save()
    cache.delete(user_id)
    return {"user_id": user_id, "path": path}


"""
This method performs the allotment of courses using the Gale-Shapley algorithm
https://en.wikipedia.org/wiki/Gale%E2%80%93Shapley_algorithm
For performance reasons, this calls the API implemented in C++ through a Python extension module.
"""

current_round = 1


@shared_task
def perform_allotment_da():
    start_time = time.time()
    logger.info(
        f"Building data structures: Started at {datetime.now():%Y-%m-%d %H:%M:%S.%f}"
    )
    # For now, just do it for ENG-RL, not all ranklists
    # TODO: Implement for all ranklists

    ranklist = RankList.objects.first()
    """
    The API requires that the ranklist is a vector, with ranklist[i] holding the rank of student with id `i`
    The database can assign any id to the students, so first map all student ids from db id to 0 based ids.
    """
    student_id_counter = 0
    student_id_db_to_api_mapping = dict()
    student_id_api_to_db_mapping = dict()

    program_id_counter = 0
    program_id_db_to_api_mapping = dict()
    program_id_api_to_db_mapping = dict()

    py_ranklist = []
    py_courses = Courses()
    py_students = Students()

    ranklist_entries = RankListEntry.objects.filter(ranklist=ranklist).order_by("rank")
    programs = Program.objects.all().order_by("id")

    # Create a mapping between a student's id and 0 based index
    for entry in ranklist_entries:
        student_id_db_to_api_mapping[entry.student_id] = student_id_counter
        student_id_api_to_db_mapping[student_id_counter] = entry.student_id
        student_id_counter += 1
        py_ranklist += [entry.rank]

    py_ranklist = PyRankList(py_ranklist)

    for program in programs:
        py_courses.add(py_ranklist, program.total_seats)
        program_id_db_to_api_mapping[program.id] = program_id_counter
        program_id_api_to_db_mapping[program_id_counter] = program.id
        program_id_counter += 1

    for entry in ranklist_entries:
        preferences = [
            program_id_db_to_api_mapping[choice.program_id]
            for choice in ChoiceEntry.objects.filter(
                student_id=entry.student_id
            ).order_by("priority")
        ]
        py_students.add(preferences, student_id_db_to_api_mapping[entry.student_id])

    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.info(f"Building data structures: Finished in {elapsed_time:.6f} seconds")

    start_time = time.time()
    logger.info(
        f"Performing allotment: Started at {datetime.now():%Y-%m-%d %H:%M:%S.%f}"
    )
    # Perform course allotment
    PyGaleShapley.perform_allotment(py_students, py_courses)

    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.info(f"Performing allotment: Finished in {elapsed_time:.6f} seconds")

    logger.info(
        f"Writing allotment results to database: Started at {datetime.now():%Y-%m-%d %H:%M:%S.%f}"
    )
    round = Round.objects.get(number=current_round)
    for i in range(0, len(py_students)):
        program_id = py_students[i].get_alloted_course_id()
        actual_student_id = student_id_api_to_db_mapping[i]
        
        # If the student is not alloted any program, set the program column as null
        if program_id != -1:
            actual_program_id = program_id_api_to_db_mapping[program_id]
        else:
            actual_program_id = None

        Allotment.objects.create(
            round=round,
            student_id=actual_student_id,
            program_id=actual_program_id,
        )

    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.info(
        f"Writing allotment results to database: Finished in {elapsed_time:.6f} seconds"
    )
