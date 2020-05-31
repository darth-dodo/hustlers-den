from django.contrib import admin

from hustlers.models import Hustler, User


class HustlersAdmin(admin.ModelAdmin):
    list_display = ("__str__", "bio", "hustler_interests", "created_by")
    list_display_links = ["__str__"]
    search_fields = ["full_name", "email"]
    list_select_related = ["django_user", "created_by"]
    readonly_fields = (
        "modified_at",
        "created_at",
    )

    def get_readonly_fields(self, request, obj=None):

        # if hustler has already been created, make the django user and created at read only
        if obj:
            custom_readonly_fields = (
                ("django_user", "created_by", "modified_by")
                if hasattr(obj, "django_user")
                else ("created_at",)
            )
            return self.readonly_fields + custom_readonly_fields
        return self.readonly_fields

    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        # TODO optimize this
        if db_field.name == "django_user":
            # fetch only those django users which do not have a hustler mapped to them
            kwargs["initial"] = None
            kwargs["queryset"] = User.objects.filter(hustler=None)
            return db_field.formfield(**kwargs)

        if db_field.name in ["created_by", "modified_by"]:
            requester_django_user = request.user
            kwargs["initial"] = (
                requester_django_user.hustler
                if hasattr(requester_django_user, "hustler")
                else None
            )
            kwargs["queryset"] = Hustler.objects.filter(
                django_user=requester_django_user
            )
            return db_field.formfield(**kwargs)

        return super(HustlersAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )

    class Meta:
        model = Hustler

    @staticmethod
    def hustler_interests(obj):
        return (
            ", ".join(obj.interests.values_list("name", flat=True))
            if obj.interests.exists()
            else "NA"
        )

    hustler_interests.short_description = "Interests"


admin.site.register(Hustler, HustlersAdmin)
