from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Habit, Record
from .forms import HabitForm, RecordForm
from datetime import date
from datetime import datetime
from users.models import User
import logging

# Create your views here.
def list_habits(request):
    user = request.user
    habits = user.habits.all()
    form = HabitForm()
    return render(request, 'core/list_habits.html', { "habits" : habits, "form" : form})

def show_habit(request, pk):
    habit = get_object_or_404(Habit, pk=pk)
    records_list=habit.get_record_details()
    line_data = []
    target_data = []
    label_strings = []
    for record in records_list:
        target_data.append(habit.number)
        if record["number"] is not None and record["number"] >= 0:
            line_data.append(record["number"])
        else:
            line_data.append("")
        label_strings.append(str(record["date"]))
    return render(request, 'core/show_habit.html', {"habit": habit, "line_data": line_data, "target_data":target_data, "label_strings":label_strings })

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

def add_record(request, pk, date):   # must add is_met check....
    habit = get_object_or_404(Habit, pk=pk)
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    date_obj = date_obj.date()
    if request.method == "GET":
        form = RecordForm()
    else:
        form = RecordForm(data=request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.user = request.user
            record.habit = get_object_or_404(Habit, pk=pk)
            if record.number >= habit.number:
                record.is_met = True
            else:
                record.is_met = False
            if habit.is_negative:
                record.is_met = not record.is_met
            record.date = date_obj
            record.save()
            return redirect(to="list_habits")
    return render(request, "core/add_record.html", {"form": form, "habit":habit, "date":date, "pk":pk})

def edit_record(request, pk):
    record = get_object_or_404(Record, pk=pk)
    habit = record.habit
    if request.method == 'GET':
        form = RecordForm(instance=record)
    else:
        form = RecordForm(data=request.POST, instance=record)
        if form.is_valid():
            record = form.save(commit=False)
            if record.number >= habit.number:
                record.is_met = True
            else:
                record.is_met = False
            if habit.is_negative:
                record.is_met = not record.is_met
            form.save()
            return redirect(to='list_habits')
    return render(request, "core/edit_record.html", {
        "form": form,
        "record": record
    })

def secret_area(request):
    return render(request, "core/secret_area.html")


# list(habit.records.order_by("date").filter(date__gte=date.today()-datetime.timedelta(30)).values("date", "is_met", "number"))
# start_date = earliest date in records
# build list of dates:
# dates = []
# while start_date <= date.today():
#     dates.append(start_date)
#     start_date = start_date + datetime.timedelta(1)