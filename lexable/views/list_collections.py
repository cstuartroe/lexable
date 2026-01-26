from django import http, views

from lexable.models import document


class ListCollectionsView(views.View):
    def get(self, request: http.HttpRequest):
        language = request.GET["language"]

        collections = document.Collection.objects.filter(language=language)
        if not request.user.is_superuser:
            collections = collections.filter(published=True)

        collections_json = [
            c.to_json(with_documents=False)
            for c in collections
        ]

        return http.JsonResponse(collections_json, safe=False)
