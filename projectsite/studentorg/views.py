from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from studentorg.models import Organization, College, Student, OrgMember, Program
from studentorg.forms import OrganizationForm, CollegeForm, StudentForm, OrgMemForm, ProgramForm
from django.urls import reverse_lazy
from typing import Any
from django.db.models.query import QuerySet
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse

@method_decorator(login_required, name='dispatch')

class HomePageView(ListView):
    model = Organization
    context_object_name = 'home'
    template_name = "home.html"

class OrganizationList(ListView):
    model = Organization
    context_object_name = 'organization'
    template_name = "org_list.html"
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        qs = super(OrganizationList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(name__icontains=query) |
            Q(description__icontains=query) | Q(college__college_name__icontains=query))
        return qs

class OrganizationCreateView(CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = "org_add.html"
    success_url = reverse_lazy('organization-list')

class OrganizationUpdateView(UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = "org_edit.html"
    success_url = reverse_lazy('organization-list')\

class OrganizationDeleteView(DeleteView):
    model = Organization
    template_name = 'org_del.html'
    success_url = reverse_lazy('organization-list')

class CollegeList(ListView):
    model = College
    context_object_name = 'college'
    template_name = "college_list.html"
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        qs = super(CollegeList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(college_name__icontains=query))
        return qs

class CollegeCreateView(CreateView):
    model = College
    form_class = CollegeForm
    template_name = "college_add.html"
    success_url = reverse_lazy('college-list') 
    
class CollegeUpdateView(UpdateView):
    model = College
    form_class = CollegeForm
    template_name = "college_edit.html"
    success_url = reverse_lazy('college-list') 

class CollegeDeleteView(DeleteView):
    model = College
    template_name = "college_del.html"
    success_url = reverse_lazy('college-list')

class StudentList(ListView):
    model = Student
    context_object_name = 'student'
    template_name = "student_list.html"
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        qs = super(StudentList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(student_id__icontains=query) |
            Q(lastname__icontains=query) | Q(firstname__icontains=query) | 
            Q(middlename__icontains=query) | Q(program__prog_name__icontains=query) )
        return qs

class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = "student_add.html"
    success_url = reverse_lazy('student-list') 
    
class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = "student_edit.html"
    success_url = reverse_lazy('student-list') 

class StudentDeleteView(DeleteView):
    model = Student
    template_name = "student_del.html"
    success_url = reverse_lazy('student-list')

class OrgMemList(ListView):
    model = OrgMember
    context_object_name = 'orgmem'
    template_name = "orgmem_list.html"
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        qs = super(OrgMemList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(student__lastname__icontains=query) |
            Q(student__firstname__icontains=query) | 
            Q(date_joined__icontains=query) | Q(organization__name__icontains=query))
        return qs

class OrgMemCreateView(CreateView):
    model = OrgMember
    form_class = OrgMemForm
    template_name = "orgmem_add.html"
    success_url = reverse_lazy('orgmem-list') 
    
class OrgMemUpdateView(UpdateView):
    model = OrgMember
    form_class = OrgMemForm
    template_name = "orgmem_edit.html"
    success_url = reverse_lazy('orgmem-list') 

class OrgMemDeleteView(DeleteView):
    model = OrgMember
    template_name = "orgmem_del.html"
    success_url = reverse_lazy('orgmem-list')

class ProgramList(ListView):
    model = Program
    context_object_name = 'program'
    template_name = "program_list.html"
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        qs = super(ProgramList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(prog_name__icontains=query) |
            Q(college__college_name__icontains=query))
        return qs

class ProgramCreateView(CreateView):
    model = Program
    form_class = ProgramForm
    template_name = "program_add.html"
    success_url = reverse_lazy('program-list') 
    
class ProgramUpdateView(UpdateView):
    model = Program
    form_class = ProgramForm
    template_name = "program_edit.html"
    success_url = reverse_lazy('program-list') 

class ProgramDeleteView(DeleteView):
    model = Program
    template_name = "program_del.html"
    success_url = reverse_lazy('program-list')

class ChartView(ListView):
    template_name = 'charts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self, *args, **kwargs):
        pass


def bar_chart_data(request):
    programs = Program.objects.all()
    data = {
        'labels': [program.prog_name for program in programs],
        'data': [program.student_set.count() for program in programs]
    }
    return JsonResponse(data)

def radar_chart_data(request):
    programs = Program.objects.all()
    data = {
        'labels': [program.prog_name for program in programs],
        'data': [program.student_set.count() for program in programs]
    }
    return JsonResponse(data)

def polar_area_chart_data(request):
    colleges = College.objects.all()
    data = {
        'labels': [college.college_name for college in colleges],
        'data': [college.organization_set.count() for college in colleges]
    }
    return JsonResponse(data)

def doughnut_chart_data(request):
    organizations = Organization.objects.annotate(num_members=Count('orgmember'))
    data = {
        'labels': [org.name for org in organizations],
        'data': [org.num_members for org in organizations]
    }
    return JsonResponse(data)

def bubble_chart_data(request):
    programs = Program.objects.all()
    data = {
        'data': [{'x': i, 'y': program.student_set.count(), 'r': program.student_set.count() / 10} for i, program in enumerate(programs)]
    }
    return JsonResponse(data)






# Create your views here.
