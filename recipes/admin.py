from django.contrib import admin
from .models import Recipe, Category, RecipeCategory

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'cooking_time', 'created_at')
    list_filter = ('author', 'categories', 'created_at')
    search_fields = ('title', 'description', 'ingredients')
    date_hierarchy = 'created_at'

@admin.register(RecipeCategory)
class RecipeCategoryAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'category', 'created_at')
    list_filter = ('category', 'created_at')
