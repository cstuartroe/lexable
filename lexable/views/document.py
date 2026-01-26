from django import http, views
from django.db import connection

from lexable.models import document


class DocumentView(views.View):
    def get(self, request: http.HttpRequest):
        id = request.GET.get("id")
        document_record = document.Document.objects.select_related("collection").prefetch_related("sections").get(id=id)
        document_json = document_record.to_json(with_content=True)

        print(connection.queries)
        print(document_json)

        return http.JsonResponse(document_json)
