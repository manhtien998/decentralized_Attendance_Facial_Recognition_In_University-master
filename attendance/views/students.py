from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from ..models import User
from ..decorators import student_required
from ..forms import  StudentSignUpForm
from django.shortcuts import render
from attendance.models import DEPT, SEM, Student, Attendance
from PIL import Image, ImageTk
import os, os.path
import pandas as pd
import numpy as np
import shutil
import json
import cv2
import csv
import glob
import datetime
import time




def search_individual(request):
    context = {
            'ids': Student.objects.all(),
            'depts': DEPT.objects.all(),
            # 'sems': SEM.objects.all(),
    }
    return render(request,'classroom/students/search_individual.html', context=context)

def search_individual_details(request):
    if request.method == 'POST':

        id_student = request.POST['ID'].split(' ', 1)[0]
        full_name = str(Student.objects.filter(id_student = id_student)[0]).split(' ', 2)[2]
        ss = list(Attendance.objects.only('id_student').filter(id_student=id_student, DEPT = 'INF0324'))
        # ss = Attendance.objects.raw('SELECT id_student FROM attendance_attendance')
        print(ss)
        for s in ss:    
            print(type(s))
        dept_name = request.POST['DEPT'].split(' ', 1)[0]
        # sem_name = request.POST['SEM'].split(' ', 1)[0]
        # date = request.POST['Date']

        
        context = {
            'id_student': id_student,
            'full_name': full_name,
            'dept_name': dept_name,
            # 'sem_name': sem_name,
            # 'date': date
        }
        
    return render(request,'classroom/students/search_individual_details.html', context=context)
