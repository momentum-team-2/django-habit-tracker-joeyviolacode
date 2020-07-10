"""habit_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include("registration.backends.simple.urls")),
    path('habits/list', core_views.list_habits, name="list_habits"),
    path('habit/<int:pk>', core_views.show_habit, name="show_habit"),
    path('habit/add', core_views.add_habit, name="add_habit"),
    path('record/<int:pk>/<str:date>', core_views.add_record, name="add_record"),
    path('record/habit/<int:pk>/<str:date>', core_views.add_record_h, name="add_record_h"),
    path('record/edit/<int:pk>', core_views.edit_record, name="edit_record"),
    path('record/habit/edit/<int:pk>', core_views.edit_record_h, name="edit_record_h"),
    path('habit/<int:pk>/delete', core_views.delete_habit, name="delete_habit"),
    path('', core_views.welcome, name="welcome"),
    path('secret-area', core_views.secret_area, name="secret_area"),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
