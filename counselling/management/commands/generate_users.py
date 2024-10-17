from django.core.management.base import BaseCommand
import os
import random
import logging
import json
from faker import Faker
from datetime import date
from ...models import *
from django.contrib.auth.hashers import make_password
from django.db import transaction

# This script generates the users, the students and assigns a rank to them, currently only for ENG-RL

NUMBER_OF_USERS = 10**3
NUM_ZEROS = 5
MIN_NUMBER_OF_CHOICES = 0
MAX_NUMBER_OF_CHOICES = 30
CONST_PASSWORD = 'password'

logger = logging.getLogger(__name__)
Faker.seed(100)
random.seed(42)

faker = Faker('en_IN')
counter = 0

def get_application_id():
    global counter
    counter += 1
    #return f'241{random.randint(10, 99)}{("%s" % counter).zfill(NUM_ZEROS)}'
    return f'{("%s" % counter).zfill(NUM_ZEROS)}'
    


class Command(BaseCommand):
    help = "Seeds the database with random username/passwords"


    def handle(self, *args, **options):
        seed_data()


def seed_data():
    logger.info("Seeding data...")
    logger.info(f"Adding {NUMBER_OF_USERS} users")
    # Delete all non super users
    User.objects.filter(is_superuser=False).delete()
    ChoiceEntry.objects.all().delete()
    Student.objects.all().delete()
    RankListEntry.objects.all().delete()
    ChoiceEntry.objects.all().delete()
    try:
        Student(user=User.objects.first(), date_of_birth='2000-12-20').save()
    except:
        logger.warning("Could not set student model for admin user")
        
    usr_psd = []
    ranklist = RankList.objects.get(short_name="ENG-RL")
    ranks = list(range(1, NUMBER_OF_USERS + 1))
    random.shuffle(ranks)
    
    program_ids = sorted(Program.objects.values_list('pk', flat=True))
    total_choices = 0
    
    for i in range(NUMBER_OF_USERS):
        with transaction.atomic():
            username=get_application_id()
            password=CONST_PASSWORD #faker.password()

            user = User(
                username=username,
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                email=faker.unique.email(),
                password=make_password(password, None, 'md5')
            )
            user.save()
            usr_psd += [(username, password)]

            dob = faker.date_between(start_date=date(2000,1,1), end_date=date(2005,1,1))
            student = Student(user=user, date_of_birth=dob)
            student.save()
            
            RankListEntry(ranklist=ranklist, student=student, rank=ranks[i]).save()
            
            
            # Also generate a random choice list for each user
            number_of_choices = random.randint(MIN_NUMBER_OF_CHOICES, MAX_NUMBER_OF_CHOICES)
            total_choices += number_of_choices
            chosen_programs = random.sample(program_ids, k=number_of_choices)
            for i, program in enumerate(chosen_programs):
                ChoiceEntry(student=student, program_id=program, priority=(i+1)).save()


    logger.info(f'Added {NUMBER_OF_USERS} users')
    logger.info(f'Added {total_choices} choices for students')
    with open('credentials.txt', 'w') as cred:
        for username, password in usr_psd:
            cred.write(f'{username} {password}\n')
        
