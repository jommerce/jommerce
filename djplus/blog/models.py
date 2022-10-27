from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from .managers import PublishedManager


class Post(models.Model):
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name=_("author"),
    )
    title = models.CharField(_("title"), max_length=100, unique=True)
    slug = models.SlugField(_("slug"), max_length=100, unique=True)
    content = models.TextField(_("content"), blank=True)
    publication_date = models.DateTimeField(_("publication date"), null=True, blank=True, default=None)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        verbose_name = _("post")
        verbose_name_plural = _("posts")
        ordering = ("-publication_date",)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post", args=[self.slug])
