from django import http, views

from lexable import settings
from lexable.models import document


class ShowCollectionView(views.View):
    def get(self, request: http.HttpRequest):
        id = request.GET.get("id")
        collection = document.Collection.objects.prefetch_related("documents").get(id=id)

        if (not request.user.is_superuser) and (not collection.published) and (not settings.DEBUG):
            return http.HttpResponse(status=404)

        data = collection.to_json(with_documents=True)
        return http.JsonResponse(data)
