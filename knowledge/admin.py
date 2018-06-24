from __future__ import unicode_literals

from django.contrib import admin
from knowledge.models import KnowledgeStore, Category, ExpertiseLevel, MediaType
from jet.admin import CompactInline
from django.utils.html import format_html


class CategoriesInline(CompactInline):
    model = Category
    can_delete = False


class KnowledgeStoreCategoriesInline(CategoriesInline):
    model = KnowledgeStore.categories.through


class KnowledgeStoreInline(CompactInline):
    model = KnowledgeStore
    readonly_fields = ('name', 'expertise_level', 'slug',
                       'categories', 'description',
                       'resource_url', 'media_type', )
    list_display_links = ['__str__']
    exclude = ('is_active', 'created_at', 'modified_at', 'difficulty_sort', 'url',)
    can_delete = False

    @staticmethod
    def resource_url(obj):
        return format_html('<a href="{0}" target="_blank" >{0}</a>', obj.url)


class KnowledgeStoreAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'expertise_level', 'difficulty_sort', 'resource_url')
    search_fields = ['name', 'url']
    list_display_links = ['__str__']
    list_filter = ['categories', 'expertise_level']

    inlines = [KnowledgeStoreCategoriesInline]

    class Meta:
        model = KnowledgeStore

    @staticmethod
    def resource_url(obj):
        return format_html('<a href="{0}" target="_blank" >{0}</a>', obj.url)


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


admin.site.register(ExpertiseLevel, ExpertiseLevelAdmin)
