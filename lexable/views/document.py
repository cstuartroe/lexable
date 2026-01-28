from django import http, views

from lexable.models import document


class DocumentView(views.View):
    def get(self, request: http.HttpRequest):
        id = request.GET.get("id")
        document_record = (
            document.Document.objects
            .select_related("collection")
            .prefetch_related("sections")
            .prefetch_related("sections__sentences")
            .get(id=id)
        )

        document_json = document_record.to_json(with_content=True)

        return http.JsonResponse(document_json)
