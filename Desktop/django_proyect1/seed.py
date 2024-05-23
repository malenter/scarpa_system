import os
import django
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
os.environ["DJANGO_SETTINGS_MODULE"] = "crm.settings"
django.setup()
from usuairo.load_data import DepartamentoSeed


def execute_seed():
    departamento_seed = DepartamentoSeed()
    if departamento_seed.should_run():
        departamento_seed.run()


execute_seed()