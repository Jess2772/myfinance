import os
from user_api.models import *
from datetime import datetime

def run():
    User.objects.create(first_name="Jesse", last_name="Li", eff_from=datetime.now(), eff_to=datetime(1900, 1, 1), monthly_budget=1000.00)
