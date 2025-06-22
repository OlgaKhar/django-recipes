from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    RecipeViewSet, CategoryViewSet, CommentViewSet,
    RatingViewSet, FavoriteViewSet
)

router = DefaultRouter()
router.register(r'recipes', RecipeViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'favorites', FavoriteViewSet, basename='favorite')

recipe_router = DefaultRouter()
recipe_router.register(r'comments', CommentViewSet, basename='recipe-comment')
recipe_router.register(r'ratings', RatingViewSet, basename='recipe-rating')

urlpatterns = [
    path('', include(router.urls)),
    path('recipes/<int:recipe_pk>/', include(recipe_router.urls)),
] 