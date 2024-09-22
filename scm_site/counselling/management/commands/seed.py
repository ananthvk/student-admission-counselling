from django.core.management.base import BaseCommand
import os
import logging
import json
from ...models import *

logger = logging.getLogger(__name__)

courses = {
    "AI": "Artificial Intelligence",
    "BT": "Bio Technology",
    "CE": "Civil Engineering",
    "CH": "Chemical Engineering",
    "CS": "Computer Science Engineering",
    "EC": "Electronics and Communications Engineering",
    "IS": "Information Science and Engineering",
    "ME": "Mechanical Engineering",
}


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
    # for k, v in courses.items():
    #    Course(code=k, name=v).save()
    for college in seed_data["colleges"]:
        College(
            name=college["name"],
            city=college["city"],
            address=college["address"],
            website=college["website"],
            college_type=college["college_type"],
            code=college["code"],
        ).save()
    logger.info(f'Added {len(seed_data["colleges"])} college(s)')
