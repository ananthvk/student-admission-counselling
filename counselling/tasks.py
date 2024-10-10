from celery import shared_task
import time
from .reports import PreferenceListReport
from .models import User, RankList, RankListEntry, Student, ChoiceEntry, Program
from pymatcher import PyRankList, PyGaleShapley, Students, Courses
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def generate_report_task(self, user_id):
    user = User.objects.get(pk=user_id)
    path = f"{user.username}_choice_report.pdf"
    # If the report has already been generated, delete it
    if default_storage.exists(path):
        default_storage.delete(path)

    print("Start report generation....")
    pref_report = PreferenceListReport(user)
    print("Finished report generation")
    path = default_storage.save(
        path,
        ContentFile(pref_report.as_bytes().getvalue()),
        
    )
    return {"user_id": user_id, "path": path}

@shared_task
def perform_allotment_da():
    # Just to make sure it works
    # For now, just do it for ENG-RL, not all ranklists
    # TODO: Implement for all ranklists
    logger.info("Performing allotment: Building data structures")
    start_time = time.time()
    ranklist = RankList.objects.get(short_name="ENG-RL")

    mapped_id = dict()
    mapped_rev_id = dict()
    program_id_map = dict()
    program_rev_id_map = dict()

    counter = -1
    counter2 = -1
    rank_entries = RankListEntry.objects.filter(ranklist=ranklist).order_by("rank")
    programs = Program.objects.all().order_by("id")

    rl = []
    for entry in rank_entries:
        counter += 1
        mapped_id[entry.student_id] = counter
        mapped_rev_id[counter] = entry.student_id
        rl += [entry.rank]

    py_rank_list = PyRankList(rl)
    py_courses = Courses()
    py_students = Students()

    for program in programs:
        counter2 += 1
        py_courses.add(py_rank_list, program.total_seats)
        program_id_map[program.id] = counter2
        program_rev_id_map[counter2] = program.id

    for entry in rank_entries:
        preferences = [
            program_id_map[i.program_id]
            for i in ChoiceEntry.objects.filter(student_id=entry.student_id)
        ]
        # if preferences:
        #    logger.info(f'Preferences for {mapped_id[entry.student_id]}({entry.student_id}) {preferences}')
        py_students.add(preferences, mapped_id[entry.student_id])

    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.info(f"Data generation time: {elapsed_time:.6f} seconds")

    start_time = time.time()
    PyGaleShapley.perform_allotment(py_students, py_courses)
    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.info(f"Allotment time: {elapsed_time:.6f} seconds")

    data = []
    for i in range(0, len(py_students)):
        prog_id = py_students[i].get_alloted_course_id()
        student_id = mapped_rev_id[i]
        alloted_program = "No program alloted"
        if prog_id != -1:
            program = Program.objects.get(pk=(prog_id + 1))
            alloted_program = f"{program.college.name} {program.course.name}"

        student = Student.objects.get(pk=student_id)
        student_name = (
            f"Rank({i+1}) {student.user.username} {student.user.get_full_name()}"
        )
        data += [(student_name, alloted_program)]
    logger.info("Allotment done")
