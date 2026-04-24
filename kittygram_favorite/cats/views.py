from django.db.models import Count

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from .permissions import IsOwnerOrReadOnly
from .models import Achievement, Cat, Like, Favorite
from .filters import CatFilter

from .serializers import AchievementSerializer, CatSerializer


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.annotate(likes_count=Count('likes'))
    serializer_class = CatSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = CatFilter
    ordering_fields = ['id', 'likes_count']
    ordering = ['-likes_count']
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user) 

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        cat = self.get_object()
        like, created = Like.objects.get_or_create(user=request.user, cat=cat)
        if not created:
            like.delete()
            return Response({'detail': 'Лайк убран.'})
        return Response({'detail': 'Лайк поставлен.'})
    
    @action(detail=False, methods=['get'])
    def top(self, request):
        cats = Cat.objects.annotate(
            likes_count=Count('likes')
        ).order_by('-likes_count')
        page = self.paginate_queryset(cats)
        if page is not None:
            serializer = CatSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = CatSerializer(cats, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_cats(self, request):
        cats = Cat.objects.filter(owner=request.user).annotate(likes_count=Count('likes'))
        page = self.paginate_queryset(cats)
        if page is not None:
            serializer = CatSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = CatSerializer(cats, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def favorite(self, request, pk=None):
        cat = self.get_object()
        favorite, created = Favorite.objects.get_or_create(user=request.user, cat=cat)
        if not created:
            favorite.delete()
            return Response({'detail': 'Удалено из избранного.'})
        return Response({'detail': 'Добавлено в избранное.'})

    @action(detail=False, methods=['get'])
    def favorites(self, request):
        cats = Cat.objects.filter(favorites__user=request.user).annotate(likes_count=Count('likes'))
        page = self.paginate_queryset(cats)
        if page is not None:
            serializer = CatSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = CatSerializer(cats, many=True, context={'request': request})
        return Response(serializer.data)


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    pagination_class = None