from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from django.forms import BaseModelForm
from .forms import LoginForm, SchemaColumnForm, DataSchemaForm
from django.contrib.auth.decorators import login_required
from .models import Column, DataSchema
from .services.faking import generate_fake_data
from django.http import HttpResponse
import csv
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView





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


class DataSchemaListView(ListView):
    template_name = 'csv_generator/schemas.html'
    model = DataSchema
    queryset = DataSchema.objects.all()

class DataSchemaDetailView(DetailView):
    # specify the model to use
    model = DataSchema
    template_name = 'csv_generator/detail_schema.html'

    def get_queryset(self):
        queryset = super(DataSchemaDetailView, self).get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        return queryset.filter(id=pk).prefetch_related('column_set')


class DataSchemaCreateView(CreateView):
    template_name = 'csv_generator/create_schema.html'
    form_class = DataSchemaForm
    form_class2 = SchemaColumnForm
    queryset = DataSchema.objects.all()

    def get(self, request):
        return render(request, 'csv_generator/create_schema.html', {
            'form': self.form_class,
            "form2": self.form_class2
        })

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        print(form.cleaned_data)
        return super().form_valid(form)
    
@login_required
def logout_view(request):
    logout(request)
    return render(request,'csv_generator/logout.html')
    

class LoginView(View):
    form_class = LoginForm
    template_name = 'csv_generator/login.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(data=request.POST)
        print(form.is_valid())
        if form.is_valid():
            username = form.cleaned_data.get('username')
            print(username)
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('schemas')
                else:
                    error = 'Your account is not active.'
            else:
                error = 'Invalid username or password'
        else:
            error = form.errors
            print(form.errors)
        return render(request, self.template_name, {'form': form, 'error': error})