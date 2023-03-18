from rest_framework import mixins, viewsets
from .permissions import IsAdminOrReadOnly


class NoPutModelViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    pass

    permission_classes = (IsAdminOrReadOnly, )
    search_fields = ('name',)
    lookup_field = 'slug'
