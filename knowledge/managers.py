from django.db import models

# TODO create mixins for common managers


class CategoryQueryset(models.query.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def for_slug(self, slug):
        return self.filter(slug=slug)


class CategoryManager(models.Manager):
    def get_queryset(self):
        return CategoryQueryset(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def for_slug(self, slug):
        return self.get_queryset().for_slug(slug=slug)


class MediaTypeQueryset(models.query.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def for_slug(self, slug):
        return self.filter(slug=slug)


class MediaTypeManager(models.Manager):
    def get_queryset(self):
        return MediaTypeQueryset(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def for_slug(self, slug):
        return self.get_queryset().for_slug(slug=slug)


class ExpertiseLevelQueryset(models.query.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def for_slug(self, slug):
        return self.filter(slug=slug)


class ExpertiseLevelManager(models.Manager):
    def get_queryset(self):
        return ExpertiseLevelQueryset(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def for_slug(self, slug):
        return self.get_queryset().for_slug(slug=slug)


class KnowledgeStoreQueryset(models.query.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def for_slug(self, slug):
        return self.filter(slug=slug)


class KnowledgeStoreManager(models.Manager):
    def get_queryset(self):
        return KnowledgeStoreQueryset(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def for_slug(self, slug):
        return self.get_queryset().for_slug(slug=slug)
