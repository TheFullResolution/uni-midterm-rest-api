from rest_framework.viewsets import ModelViewSet


class NoPutModelViewSet(ModelViewSet):
    """
    Custom ViewSet that disables the PUT method globally.

    This class inherits from Django REST Framework's `ModelViewSet` and overrides the
    `http_method_names` attribute to exclude the PUT method. By default, `ModelViewSet`
    supports the following methods:
    - GET: Retrieve list or detail views.
    - POST: Create new resources.
    - PUT: Fully replace an existing resource (excluded here).
    - PATCH: Partially update an existing resource.
    - DELETE: Remove an existing resource.
    - HEAD and OPTIONS: HTTP specification compliant meta requests.

    Excluding the PUT method enforces the use of PATCH for updates, which aligns
    with RESTful design principles that recommend partial updates for most scenarios.
    """
    # Restrict HTTP methods to exclude PUT.
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
