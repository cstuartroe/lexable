from django.contrib import admin
from django.urls import path, re_path

from .views import (
    document,
    list_collections,
    react_index,
    show_collection,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path("api/collections", list_collections.ListCollectionsView.as_view(), name="list_collections"),
    path("api/collection", show_collection.ShowCollectionView.as_view(), name="show_collection"),
    path("api/document", document.DocumentView.as_view(), name="document"),

    re_path(r'^.*$', react_index.ReactIndexView.as_view(), name="react_index")
]
