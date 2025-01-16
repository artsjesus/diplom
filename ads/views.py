from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView, \
    RetrieveUpdateDestroyAPIView
from ads.models import Ads, Comment
from ads.paginators import AdsPaginator
from ads.permissions import IsAdminOrAuthor
from ads.serializers import AdsSerializer, CommentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from ads.filters import AdsFilter

class AdsCreateAPIView(CreateAPIView):
    serializer_class = AdsSerializer
    permission_classes = [IsAuthenticated,]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AdsListAPIView(ListAPIView):
    queryset = Ads.objects.all()
    serializer_class = AdsSerializer
    permission_classes = [AllowAny,]
    pagination_class = AdsPaginator


class AdsDetailAPIView(RetrieveAPIView):
    queryset = Ads.objects.all()
    serializer_class = AdsSerializer
    permission_classes = [IsAuthenticated,]


class AdsUpdateAPIView(UpdateAPIView):
    queryset = Ads.objects.all()
    serializer_class = AdsSerializer
    permission_classes = [IsAdminOrAuthor,]


class AdsDeleteAPIView(DestroyAPIView):
    queryset = Ads.objects.all()
    serializer_class = AdsSerializer
    permission_classes = [IsAdminOrAuthor,]


class CommentCreateAPIView(CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        ad_pk = self.kwargs.get('ad_pk')
        ad = Ads.objects.get(id=ad_pk)
        serializer.save(author=self.request.user, ad=ad)


class CommentDetailUpdateDeliteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAdminOrAuthor]


class CommentListAPIView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AllowAny, ]
