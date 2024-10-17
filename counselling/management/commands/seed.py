from django.core.management.base import BaseCommand
import os
import logging
import json
from django.core.cache import cache
from ...models import *

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Seeds the database with data to help in testing"

    def add_arguments(self, parser):
        parser.add_argument(
            "file_path",
            type=str,
            help="Path to the file containing the seed data in json",
        )

    def handle(self, *args, **options):
        file_path = options["file_path"]
        if not os.path.isfile(file_path):
            logger.error("Seed file does not exist")
        with open(file_path, "r") as f:
            ob = json.load(f)

        seed_data(ob)


def seed_data(seed_data: dict):
    logger.info("Seeding data...")

    Program.objects.all().delete()
    Course.objects.all().delete()
    College.objects.all().delete()
    RankList.objects.all().delete()
    Round.objects.all().delete()
    Allotment.objects.all().delete()
    Student.objects.all().delete()
    User.objects.all().delete()
    cache.clear()
    
    Round.objects.create(number=1, name="First round")
    Round.objects.create(number=2, name="Second round")
    Round.objects.create(number=3, name="Second extended round")

    logger.info("Adding ranklist")
    for ranklist in seed_data["ranklists"]:
        rank_list = RankList(short_name=ranklist["short_name"], name=ranklist["name"])
        rank_list.save()
    logger.info(f'Added {len(seed_data["ranklists"])} ranklist(s)')

    logger.info("Adding courses")
    for course_code, course_name in seed_data["courses"].items():
        Course(code=course_code, name=course_name).save()
    logger.info(f'Added {len(seed_data["courses"])} course(s)')

    total_programs = 0
    total_number_of_seats = 0

    logger.info("Adding colleges...")
    for college in seed_data["colleges"]:
        college_model = College(
            name=college["name"],
            city=college["city"],
            address=college["address"],
            website=college["website"],
            college_type=college["type"],
            code=college["code"],
        )
        college_model.save()
        # Add programs offered by this college

        for course_code, capacity in college["courses"].items():
            course = Course.objects.get(code=course_code)

            # Hardcode it for now, TOOD: Get it from data.json
            ranklist = RankList.objects.get(short_name='ENG-RL')
            Program(
                college=college_model,
                course=course,
                total_seats=capacity,
                ranklist=ranklist,
            ).save()
            total_programs += 1
            total_number_of_seats += capacity

    logger.info(f'Added {len(seed_data["colleges"])} college(s)')
    logger.info(f'Added {total_programs} programs, with {total_number_of_seats} seats')
