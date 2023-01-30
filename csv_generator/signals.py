import csv
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import GeneratedData
from .services import faking, uploading


@receiver(post_save, sender=GeneratedData)
def generate_csv_file(sender, instance, created, **kwargs):
    if created:
        # Get related columns and data schema
        columns = instance.data_schema.column_set.all()
        data_schema = instance.data_schema

        # Create fake data for each column
        column_names = [
            column.column_name for column in data_schema.column_set.all()]
        filename = f"{data_schema.name}--{instance.pk}.csv"
        filepath = f"media/{filename}"

        # Write csv file
        with open(f"{filepath}", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([column for column in column_names])
            for _ in instance.rows:
                fake_data = faking.generate_fake_data(columns=columns)
                print("fake data is generated! :", fake_data)
                writer.writerow([data for data in fake_data])

        response = uploading.upload_to_s3(filepath, filename)
        if response:
            instance.status = "ready"
            instance.csv_file = filename
            instance.save()
        else:
            instance.status = "error"
            instance.save()
