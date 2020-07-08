from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Habit, Record
from .forms import HabitForm
from datetime import date
from users.models import User
import logging

# Create your views here.
def list_habits(request):
    logging.error('Ran list_habits')
    user = request.user
    habits = user.habits.all()
    form = HabitForm()
    return render(request, 'core/list_habits.html', { "habits" : habits, "form" : form})

def show_habit(request, pk):
    habit = get_object_or_404(Habit, pk=pk)
    return render(request, 'core/show_habit.html', {"habit": habit})

# This may require that we change the way dates are implemented either here or in the model.  Auto_now_add
# is not set in the model to make it easier for DB entry creation of multiple dates.  Needs to be decided and
# addressed before production
def add_habit(request):
    logging.error("Running add_habit")
    form = HabitForm(data=request.POST)
    user = request.user
    is_negative = False
    habit = None
    if form.is_valid():
        noun = form.cleaned_data.get('noun')
        noun_singular = form.cleaned_data.get('noun_singular')
        number = form.cleaned_data.get('number')
        more_less = form.cleaned_data.get('more_less')
        verb = form.cleaned_data.get('verb')
        if (more_less == "less"):
            is_negative = True
        habit = Habit(verb=verb, noun=noun, noun_singular=noun_singular, number=number, is_negative=is_negative, user=user, created_date=date.today())
        habit.save()
    else: 
        logging.error("Form not valid.")
    return redirect(to="list_habits")

def edit_habit(request, pk):
    pass

def add_record(request):
    pass

def secret_area(request):
    return render(request, "core/secret_area.html")


# list(habit.records.order_by("date").filter(date__gte=date.today()-datetime.timedelta(30)).values("date", "is_met", "number"))
# start_date = earliest date in records
# build list of dates:
# dates = []
# while start_date <= date.today():
#     dates.append(start_date)
#     start_date = start_date + datetime.timedelta(1)