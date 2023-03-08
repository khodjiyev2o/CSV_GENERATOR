from celery import shared_task
import csv
from .models import GeneratedData
from .services import faking, uploading
from typing import Type

from django.db import models

@shared_task
def generate_csv_task(
    instance_id : int,
    ) -> None:
        instance = GeneratedData.objects.select_related(
            'data_schema').prefetch_related('data_schema__column_set'
            ).get(pk=instance_id)

        # Access related objects
        data_schema = instance.data_schema
        columns = data_schema.column_set.all()

        # Create fake data for each column
        column_names = [
            column.column_name for column in columns]
        filename = f"{data_schema.name}--{instance.pk}.csv"
        filepath = f"media/{filename}"

        # Write csv file
        with open(f"{filepath}", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([column for column in column_names])
            for _ in range(instance.rows):
                fake_data = faking.generate_fake_data(columns=columns)
                writer.writerow([data for data in fake_data])

        response = uploading.upload_to_s3(filepath, filename)
        if response:
            try:
                instance.csv_file = filename
                instance.status = "ready"
                instance.full_clean()
                instance.save()
            except Exception:
                raise Exception
        else:
            instance.status = "error"
            instance.full_clean()
            instance.save()