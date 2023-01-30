from django.shortcuts import render
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import *
from .services.faking import generate_fake_data
from django.http import HttpResponse
import csv
from django.views.generic.list import ListView
from django.views.generic import DeleteView
from django.views.generic.detail import DetailView
from extra_views import CreateWithInlinesView, UpdateWithInlinesView
from django.utils.decorators import method_decorator


@login_required
def generate_csv(request, range_limit: int) -> HttpResponse:
    response = HttpResponse(
        content_type='text/csv; charset=UTF-8',
        headers={'Content-Disposition': 'attachment; filename="data.csv"'},
    )
    writer = csv.writer(response,delimiter=',')
    data_schema = DataSchema.objects.prefetch_related('column_set').get(id=2)
    column_names = [column.name for column in data_schema.column_set.all()]
    ## add column headings to the csv
    writer.writerow(column_names)
    for i in range(50):
            fake_data = generate_fake_data(column_names=column_names,range_limit=range_limit)
            writer.writerow(fake_data)
    return response


@method_decorator(login_required, name='dispatch')
class DataSchemaListView(ListView):
    template_name = 'csv_generator/schemas.html'
    model = DataSchema
    queryset = DataSchema.objects.all()


@method_decorator(login_required, name='dispatch')
class DataSchemaDetailView(DetailView):
    # specify the model to use
    model = DataSchema
    template_name = 'csv_generator/detail_schema.html'

    def get_queryset(self):
        queryset = super(DataSchemaDetailView, self).get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        return queryset.filter(id=pk).prefetch_related('column_set','generated_data')
    
    def post(self, request, *args, **kwargs):
        schema = self.get_object()
        form = GeneratedDataForm(request.POST)
        rows = request.POST.get('rows')
        if not rows:
            messages.error(request, 'Please enter the number of rows',extra_tags='danger')
            return self.get(request, *args, **kwargs)
        if form.is_valid():
            messages.success(request, 'Data is being generated!')
            generated_data = form.save(commit=False)
            generated_data.data_schema = schema
            generated_data.save()
            return redirect(self.request.path)
        return render(request, self.template_name, {'form': form, 'schema': schema})


@method_decorator(login_required, name='dispatch')
class DataSchemaCreateView(CreateWithInlinesView):
    model = DataSchema
    form_class = DataSchemaForm
    inlines = [
        SchemaColumnInline,
    ]
    template_name = "csv_generator/create_schema.html"


    def get_initial(self):
        data = {"user": self.request.user}
        return data

    def get_success_url(self):
        if "action" in self.request.POST:
            if self.request.POST["action"] == "submit":
                return reverse("schemas")
            if self.request.POST["action"] == "add_column":
                obj = self.object
                return reverse("schema_update", kwargs={"pk": obj.pk})
        else:
            return reverse("schemas")


@method_decorator(login_required, name='dispatch')
class SchemaUpdateView(UpdateWithInlinesView):
    model = DataSchema
    form_class = DataSchemaForm
    inlines = [
        SchemaColumnInline,
    ]
    template_name = "csv_generator/create_schema.html"

    def get_initial(self):
        data = {"user": self.request.user}
        return data

    def get_success_url(self):
        if "action" in self.request.POST:
            if self.request.POST["action"] == "submit":
                return reverse("schemas")
            if self.request.POST["action"] == "add_column":
                obj = self.object
                return reverse("schema_update", kwargs={"pk": obj.pk})
        else:
            return reverse("schemas")


@method_decorator(login_required, name='dispatch')
class SchemaDeleteView(DeleteView):
    model = DataSchema
    template_name = "csv_generator/delete_schema.html"
    success_url = reverse_lazy("schemas")

