from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from datetime import datetime
from django.utils import timezone
from .forms import *
from django.shortcuts import redirect
from .models import Meal
from datetime import date as dt

def go(request):
    print(request.POST)
    print(request.POST['date'])
    urli = "history/"+request.POST['date']
    if request.method == "POST":
        form = DateForm(request.POST)
        if form.is_valid():
            print("dt")
            print(form)
            return redirect('history.html')
        else:
            print("f.n")
    else:
        form = PostForm()
    return render(request, "go.html", {'dte': request.POST['date']})


def meal_list_all(request):
    meals = Meal.objects.filter(consumed_date__lte=timezone.now()).order_by('consumed_date').reverse()
    return render(request, 'meal_list_all.html', {'meals': meals})

def meal_list(request):
    meals = Meal.objects.filter(consumed_date__lte=timezone.now()).order_by('consumed_date').reverse()
    return render(request, 'meal_list.html', {'meals': meals})

def meal_history_list(request, date):
    meals = Meal.objects.filter(consumed_date__lte=timezone.now()).order_by('consumed_date').reverse()
    newMeals = []
    dateTimeObj = datetime.strptime(date, "%Y-%m-%d")

    for meal in meals:
        if(meal.consumed_date.date() == dateTimeObj.date()):
            newMeals.append(meal)

    for meal in newMeals:
        print("new")
        print(meal.name)   

    print(newMeals)

    return render(request, 'meal_history_list.html', {'meals': newMeals})


def meal_detail(request, pk):
    meal = get_object_or_404(Meal, pk=pk)
    return render(request, 'meal_detail.html', {'meal': meal})

def meal_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.save()
            return redirect('meal_detail', pk=meal.pk)
    else:
        form = PostForm()
    return render(request, 'meal_edit.html', {'form': form})

def meal_edit(request, pk):
    meal = get_object_or_404(Meal, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=meal)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.name = request.name
            meal.consumed_date = timezone.now()
            meal.calorie_count = request.calorie
            meal.save()
            return redirect('meal_detail', pk=meal.pk)
    else:
        form = PostForm(instance=meal)
    return render(request, 'meal_edit.html', {'form': form})