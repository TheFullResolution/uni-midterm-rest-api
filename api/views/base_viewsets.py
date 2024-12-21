from rest_framework.viewsets import ModelViewSet


class NoPutModelViewSet(ModelViewSet):
    """
    A base viewset that disables the PUT method globally.
    """
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
