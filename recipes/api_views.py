from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Recipe, Category, Comment, Rating, Favorite
from .serializers import (
    RecipeSerializer, CategorySerializer, CommentSerializer,
    RatingSerializer, FavoriteSerializer
)

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'])
    def rate(self, request, pk=None):
        recipe = self.get_object()
        rating = request.data.get('rating')
        
        if not rating or not isinstance(rating, int) or rating < 1 or rating > 5:
            return Response(
                {'error': 'Rating must be an integer between 1 and 5'},
                status=status.HTTP_400_BAD_REQUEST
            )

        rating_obj, created = Rating.objects.get_or_create(
            recipe=recipe,
            user=request.user,
            defaults={'rating': rating}
        )

        if not created:
            rating_obj.rating = rating
            rating_obj.save()

        return Response({'status': 'rating saved'})

    @action(detail=True, methods=['post'])
    def favorite(self, request, pk=None):
        recipe = self.get_object()
        favorite, created = Favorite.objects.get_or_create(
            recipe=recipe,
            user=request.user
        )

        if not created:
            favorite.delete()
            return Response({'status': 'removed from favorites'})

        return Response({'status': 'added to favorites'})

    @action(detail=False)
    def search(self, request):
        query = request.query_params.get('q', '')
        category = request.query_params.get('category')
        min_rating = request.query_params.get('min_rating')

        recipes = self.queryset

        if query:
            recipes = recipes.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(ingredients__icontains=query)
            )

        if category:
            recipes = recipes.filter(categories__name=category)

        if min_rating:
            try:
                min_rating = float(min_rating)
                recipes = recipes.filter(average_rating__gte=min_rating)
            except ValueError:
                pass

        serializer = self.get_serializer(recipes, many=True)
        return Response(serializer.data)

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        recipe_id = self.kwargs.get('recipe_pk')
        return Comment.objects.filter(recipe_id=recipe_id)

    def perform_create(self, serializer):
        recipe_id = self.kwargs.get('recipe_pk')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        serializer.save(author=self.request.user, recipe=recipe)

class RatingViewSet(viewsets.ModelViewSet):
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        recipe_id = self.kwargs.get('recipe_pk')
        return Rating.objects.filter(recipe_id=recipe_id)

    def perform_create(self, serializer):
        recipe_id = self.kwargs.get('recipe_pk')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        serializer.save(user=self.request.user, recipe=recipe)

class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user) 