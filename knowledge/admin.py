from __future__ import unicode_literals

from django.contrib import admin
from jet.admin import CompactInline
from django.utils.html import format_html

from knowledge.models import KnowledgeStore, Category, ExpertiseLevel, MediaType

from hustlers.models import Hustler


# create a hustler mixin

class CategoriesInline(CompactInline):
    model = Category
    can_delete = False


class KnowledgeStoreCategoriesInline(CategoriesInline):
    model = KnowledgeStore.categories.through


class KnowledgeStoreInline(CompactInline):
    model = KnowledgeStore
    readonly_fields = ('name', 'expertise_level', 'slug',
                       'categories', 'description',
                       'resource_url', 'media_type', 'created_by')
    list_display_links = ['__str__']
    exclude = ('is_active', 'created_at', 'modified_at', 'difficulty_sort', 'url',)
    can_delete = False

    @staticmethod
    def resource_url(obj):
        if obj.url:
            return format_html('<a href="{0}" target="_blank" >{0}</a>', obj.url)


class KnowledgeStoreAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'expertise_level', 'difficulty_sort', 'resource_url')
    search_fields = ['name', 'url']
    list_display_links = ['__str__']
    list_filter = ['categories', 'expertise_level']
    readonly_fields = ('slug',)
    list_select_related = ['expertise_level', 'media_type', 'created_by']

    inlines = [KnowledgeStoreCategoriesInline]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            custom_readonly_fields = ('created_by',)
            return self.readonly_fields + custom_readonly_fields
        return self.readonly_fields

    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        # TODO optimize this
        if db_field.name == 'created_by':
            requester_django_user = request.user
            kwargs['initial'] = requester_django_user.hustler if hasattr(requester_django_user, 'hustler') else None
            kwargs['queryset'] = Hustler.objects.filter(django_user=requester_django_user)
            return db_field.formfield(**kwargs)

        return super(KnowledgeStoreAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    class Meta:
        model = KnowledgeStore

    @staticmethod
    def resource_url(obj):
        return format_html('<a href="{0}" target="_blank" >{0}</a>', obj.url)


admin.site.register(KnowledgeStore, KnowledgeStoreAdmin)


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'description', 'slug', 'created_by')
    search_fields = ['name', 'slug']
    list_display_links = ['__str__']
    readonly_fields = ('slug',)
    list_select_related = ['created_by']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            custom_readonly_fields = ('created_by',)
            return self.readonly_fields + custom_readonly_fields
        return self.readonly_fields

    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        # TODO optimize this
        if db_field.name == 'created_by':
            requester_django_user = request.user
            kwargs['initial'] = requester_django_user.hustler if hasattr(requester_django_user, 'hustler') else None
            kwargs['queryset'] = Hustler.objects.filter(django_user=requester_django_user)
            return db_field.formfield(**kwargs)

        return super(CategoriesAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    class Meta:
        model = Category


admin.site.register(Category, CategoriesAdmin)


class MediaTypesAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'description', 'slug', 'created_by')
    search_fields = ['name', 'slug']
    list_display_links = ['__str__']
    readonly_fields = ('slug',)
    list_select_related = ['created_by']

    inlines = [KnowledgeStoreInline]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            custom_readonly_fields = ('created_by',)
            return self.readonly_fields + custom_readonly_fields
        return self.readonly_fields

    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        # TODO optimize this
        if db_field.name == 'created_by':
            requester_django_user = request.user
            kwargs['initial'] = requester_django_user.hustler if hasattr(requester_django_user, 'hustler') else None
            kwargs['queryset'] = Hustler.objects.filter(django_user=requester_django_user)
            return db_field.formfield(**kwargs)

        return super(MediaTypesAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    class Meta:
        model = MediaType


admin.site.register(MediaType, MediaTypesAdmin)


class ExpertiseLevelAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'description', 'slug', 'created_by')
    search_fields = ['name', 'slug']
    list_display_links = ['__str__']
    readonly_fields = ('slug',)
    list_select_related = ['created_by']

    inlines = [KnowledgeStoreInline]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            custom_readonly_fields = ('created_by',)
            return self.readonly_fields + custom_readonly_fields
        return self.readonly_fields

    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        # TODO optimize this
        if db_field.name == 'created_by':
            requester_django_user = request.user
            kwargs['initial'] = requester_django_user.hustler if hasattr(requester_django_user, 'hustler') else None
            kwargs['queryset'] = Hustler.objects.filter(django_user=requester_django_user)
            return db_field.formfield(**kwargs)

        return super(ExpertiseLevelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    class Meta:
        model = ExpertiseLevel


admin.site.register(ExpertiseLevel, ExpertiseLevelAdmin)
