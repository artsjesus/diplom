from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView, \
    RetrieveUpdateDestroyAPIView
from ads.filters import AdsFilter
from ads.models import Ads, Comment
from ads.paginators import AdsPaginator
from ads.permissions import IsAdminOrAuthor
from ads.serializers import AdsSerializer, CommentSerializer
from django_filters.rest_framework import DjangoFilterBackend


class AdsCreateAPIView(CreateAPIView):
    """Создание объявления"""
    serializer_class = AdsSerializer
    permission_classes = [IsAuthenticated,]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AdsListAPIView(ListAPIView):
    """Просмотр списка объявлений"""
    queryset = Ads.objects.all()
    serializer_class = AdsSerializer
    permission_classes = [AllowAny,]
    pagination_class = AdsPaginator
    filter_backends = [DjangoFilterBackend,]
    filterset_class = AdsFilter


class AdsDetailAPIView(RetrieveAPIView):
    """Просмотр одного объявления"""
    queryset = Ads.objects.all()
    serializer_class = AdsSerializer
    permission_classes = [IsAuthenticated,]


class AdsUpdateAPIView(UpdateAPIView):
    """Изменение объявления"""
    queryset = Ads.objects.all()
    serializer_class = AdsSerializer
    permission_classes = [IsAdminOrAuthor,]


class AdsDeleteAPIView(DestroyAPIView):
    """Удаление объявления"""
    queryset = Ads.objects.all()
    serializer_class = AdsSerializer
    permission_classes = [IsAdminOrAuthor,]


class CommentCreateAPIView(CreateAPIView):
    """Создание комментария"""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        ad_pk = self.kwargs.get('ad_pk')
        ad = Ads.objects.get(id=ad_pk)
        serializer.save(author=self.request.user, ad=ad)


class CommentDetailUpdateDeliteAPIView(RetrieveUpdateDestroyAPIView):
    """Создание, изменение, удаление комментария"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAdminOrAuthor]


class CommentListAPIView(ListAPIView):
    """Просмотр списка комментариев"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AllowAny, ]
