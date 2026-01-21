from django.contrib import admin
from django.urls import path, re_path

from .views.react_index import ReactIndexView

urlpatterns = [
    path('admin/', admin.site.urls),

    re_path(r'^.*$', ReactIndexView.as_view(), name="react_index")
]
