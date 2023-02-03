from django.contrib import admin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .models import Post, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["__str__"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "author", "publication_date", "status"]
    list_filter = ["publication_date", "created_at", "updated_at"]
    search_fields = ["title", "content"]
    prepopulated_fields = {"slug": ["title"]}
    raw_id_fields = ["author"]
    date_hierarchy = "publication_date"
    ordering = ["-publication_date"]

    @admin.display
    def status(self, obj: Post):
        if obj.publication_date is None:
            return _("Draft")
        if obj.publication_date < timezone.now():
            return _("Published")
        if obj.publication_date >= timezone.now():
            return _("Awaiting publication")
