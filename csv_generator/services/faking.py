from faker import Faker
from django.db import models
from typing import Dict
import random
from django.http import HttpResponse
fake = Faker()



def generate_fake_data(column_names: list[str], range_limit: int = 100) -> list[ any ]:
    data = []
    for column_name in column_names:
        method_name = f"{column_name.lower().replace(' ', '_')}"
        method = getattr(fake, method_name, None)
        if method:
                data.append(method())
        elif method_name == "full_name":
                data.append(fake.name()+fake.last_name())
        elif method_name == "age":
                data.append(random.randint(1,range_limit))
        else:    
            pass
            #handle other types of data
    return data

