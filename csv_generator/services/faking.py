from faker import Faker
from django.db import models
from typing import Dict, List
import random
from django.http import HttpResponse
fake = Faker()



def generate_fake_data(columns: models.Model) -> List[List[ any ]]:
        data = []
        for column in columns:
                method_name = f"{column.column_name.lower().replace(' ', '_')}"
                method = getattr(fake, method_name, None)
                if method:
                        data.append(method())
                elif method_name == "full_name":
                        data.append(fake.name()+fake.last_name())
                elif method_name == "age":
                        if column.data_range_from and column.data_range_to:
                                data.append(random.randint(column.data_range_from,column.data_range_to))
                        else:
                                data.append(random.randint(1,100))
                else:    
                        pass
                        #handle other types of data
        return data

