from django.db import models
from django.core.exceptions import ValidationError
from .services.data_types import STATUS_CHOICES, COL_SEP_CHOICES, QUOTE_CHOICES, DATA_TYPE_CHOICES
from django.utils import timezone
from django.urls import reverse


class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class DataSchema(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    column_separator = models.CharField(
        max_length=1,
        choices=COL_SEP_CHOICES,
        default=","
    )
    string_character = models.CharField(
        max_length=1, choices=QUOTE_CHOICES, default='"')

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('schema_detail', kwargs={'pk': self.pk})


class Column(BaseModel):
    data_schema = models.ForeignKey(DataSchema, on_delete=models.CASCADE)
    column_name = models.CharField(max_length=15)
    data_type = models.CharField(max_length=15, choices=DATA_TYPE_CHOICES)
    order = models.PositiveIntegerField()
    data_range_from = models.PositiveIntegerField(
        blank=True, null=True, verbose_name="from")
    data_range_to = models.PositiveIntegerField(
        blank=True, null=True, verbose_name="to")

    def __str__(self):
        return str(f'{self.column_name} column for {self.data_schema}')

    def clean(self):
        # Check if order is unique for the DataSchema
        if Column.objects.filter(
            data_schema=self.data_schema, 
            order=self.order).exclude(
                pk=self.pk).exists():
            raise ValidationError('Order must be unique for each DataSchema')


class GeneratedData(BaseModel):
    data_schema = models.ForeignKey(
        DataSchema, on_delete=models.CASCADE, related_name='generated_data')
    csv_file = models.FileField(null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICES,
                              max_length=15, default='processing')
    rows = models.PositiveIntegerField()

    def __str__(self):
        return str(f'CSV for {self.data_schema}, {self.status}')

    def clean(self):
        if not self.csv_file and self.status == "ready":
            raise ValidationError("Status cannot be ready without csv file")
