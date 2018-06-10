from __future__ import unicode_literals

from django.contrib import admin
from knowledge.models import KnowledgeStore, Category, ExpertiseLevel, MediaType


class CategoriesInline(admin.TabularInline):
    model = KnowledgeStore.categories.through


class KnowledgeStoreInline(admin.TabularInline):
    model = KnowledgeStore


class KnowledgeStoreAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'expertise_level', 'difficulty_sort')
    search_fields = ['name']
    list_display_links = ['__str__']
    list_filter = ['categories']

    inlines = [CategoriesInline]

    class Meta:
        model = KnowledgeStore


admin.site.register(KnowledgeStore, KnowledgeStoreAdmin)


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'description', 'slug')
    search_fields = ['name', 'slug']
    list_display_links = ['__str__']

    class Meta:
        model = Category


admin.site.register(Category, CategoriesAdmin)


class MediaTypesAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'description', 'slug')
    search_fields = ['name', 'slug']
    list_display_links = ['__str__']

    inlines = [KnowledgeStoreInline]

    class Meta:
        model = MediaType


admin.site.register(MediaType, MediaTypesAdmin)


class ExpertiseLevelAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'description', 'slug')
    search_fields = ['name', 'slug']
    list_display_links = ['__str__']

    inlines = [KnowledgeStoreInline]

    class Meta:
        model = ExpertiseLevel


admin.site.register(ExpertiseLevel, CategoriesAdmin)