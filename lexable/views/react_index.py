from django import http, shortcuts, views


class ReactIndexView(views.View):
    def get(self, request: http.HttpRequest):
        return shortcuts.render(request, 'react_index.html')
