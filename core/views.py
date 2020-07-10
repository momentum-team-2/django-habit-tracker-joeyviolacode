from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Habit, Record
from .forms import HabitForm, RecordForm
from datetime import date
from datetime import datetime
from users.models import User
import logging

# Create your views here.
def welcome(request):
    return render(request, 'core/welcome.html')


@login_required
def list_habits(request):
    user = request.user
    habits = user.habits.all()
    form = HabitForm()
    return render(request, 'core/list_habits.html', { "habits" : habits, "form" : form})

@login_required
def show_habit(request, pk):
    habit = get_object_or_404(Habit, pk=pk)
    records_list=habit.get_record_details()
    line_data = []
    target_data = []
    label_strings = []
    total = 0
    count = 0
    average_data = []
    for record in records_list:
        target_data.append(habit.number)
        if record["number"] is not None and record["number"] >= 0:
            line_data.append(record["number"])
            total = total + record["number"]
            count = count + 1
            average_data.append(((total / count)//.01) / 100)
        else:
            average_data.append(((total / count)//.01) / 100)
            line_data.append("")
        label_strings.append(str(record["date"])[5:])
    minimum = min( [ min(float(num) for num in line_data if num is not "") , target_data[0]] )
    maximum = max( [ max(float(num) for num in line_data if num is not "") , target_data[0]] )
    min_val = minimum - ((maximum - minimum) / 10)
    max_val = maximum + ((maximum - minimum) / 10)
    #min_val = max(min_val, 0)
    print(min_val)
    return render(request, 'core/show_habit.html', 
                {"habit": habit, "line_data": line_data, 
                "target_data":target_data, "label_strings":label_strings, 
                "average_data":average_data, "min_val":min_val,
                "max_val": max_val })

# This may require that we change the way dates are implemented either here or in the model.  Auto_now_add
# is not set in the model to make it easier for DB entry creation of multiple dates.  Needs to be decided and
# addressed before production
@login_required
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

@login_required
def delete_habit(request, pk):
    habit = get_object_or_404(Habit, pk=pk)
    habit.delete()
    return redirect(to="list_habits")

@login_required
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


@login_required
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
        "record": record,
        "habit": habit
    })

@login_required #Login_DEFINITELY_required.  :)
def secret_area(request):
    return render(request, "core/secret_area.html")







@login_required
def add_record_h(request, pk, date):   # must add is_met check....
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
            return redirect(to="show_habit", pk=habit.pk)
    return render(request, "core/add_record_h.html", {"form": form, "habit":habit, "date":date, "pk":pk})

@login_required
def edit_record_h(request, pk):
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
            return redirect(to="show_habit", pk=habit.pk)
    return render(request, "core/edit_record_h.html", {
        "form": form,
        "record": record
    })
