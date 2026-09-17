from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Permite leitura pra qualquer um, mas so o dono do objeto pode editar/deletar."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user