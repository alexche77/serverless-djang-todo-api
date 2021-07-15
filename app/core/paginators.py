from rest_framework import pagination
from rest_framework.response import Response


class DataPageNumberPagination(pagination.PageNumberPagination):

    page_query_param = 'page[number]'
    page_size_query_param = 'page[size]'

    def get_paginated_response(self, data):
        current_page = self.page.number
        last_page = self.page.paginator.num_pages
        payload = {
            'data': data,
            'meta': {
                "current_page": current_page,
                "from": None if current_page == 1 else current_page - 1,
                "last_page": last_page,
                "per_page": self.page.paginator.per_page,
                "to": None if current_page == last_page else current_page + 1,
                "total": self.page.paginator.count,
            },
        }
        return Response(payload)

    def get_paginated_response_schema(self, schema):
        return {
            'type': 'object',
            'properties': {
                'data': schema,
                'meta': {
                    'type': 'object',
                    'properties': {
                        'current_page': {
                            'type': 'integer',
                            'example': 1,
                        },
                        'from': {
                            'type': 'integer',
                            'example': None,
                        },
                        'last_page': {
                            'type': 'integer',
                            'example': 10,
                        },
                        'per_page': {
                            'type': 'integer',
                            'example': 5,
                        },
                        'to': {
                            'type': 'integer',
                            'example': 2,
                        },
                        'total': {
                            'type': 'integer',
                            'example': 50,
                        },
                    }
                },
            },
        }
