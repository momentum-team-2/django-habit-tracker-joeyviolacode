from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Habit, Record
from users.models import User

# Create your views here.
def list_habits(request):
    user = request.user
    habits = user.habits.all()
    return render(request, 'core/list_habits.html', { "habits" : habits })

def show_habit(request, pk):
    habit = get_object_or_404(Habit, pk=pk)
    return render(request, 'core/show_habit.html', {"habit": habit})

def add_habit(request):
    pass

def edit_habit(request, pk):
    pass

def add_record(request):
    pass