from django.shortcuts import redirect, render,HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from ..decorators import student_required
from django.contrib.auth import login
from ..forms import  PasswordChangeForm,UserCreationForm,UserUpdateForm,StudentSignUpForm,TeacherSignUpForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.views.generic import CreateView
from ..models import User


class SignUpView(TemplateView):
    template_name = 'classroom/user/signup.html'


class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'classroom/user/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('login')

class TeacherSignUpView(CreateView):
    model = User
    form_class = TeacherSignUpForm
    template_name = 'classroom/user/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('login')



@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request,'classroom/user/change_password.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('home')
    else:
        u_form = UserUpdateForm(instance=request.user)
    context = {'u_form': u_form}
    return render(request, 'classroom/user/edit_profile.html',context)

def home(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect('teachers:attendance_index')
            #return HttpResponse("teachers")
        else:
            return redirect('students:search_individual')
            #return HttpResponse("students")
    return render(request, 'classroom/home.html')
