from django.db import models
from django.template.defaultfilters import slugify


class BlogCategory(models.Model):
    name = models.CharField(max_length=1000, help_text="Enter the blog category name")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return str(self.name)

    def total_listing(self):
        return self.category.count()

    class Meta:
        verbose_name_plural = "Blog Categories"
        ordering = ("name",)


class BlogPost(models.Model):
    title = models.CharField(max_length=500, help_text="Enter the blog title")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    image = models.ImageField(
        upload_to="blog/images", help_text="Upload the blog image (751*422)"
    )
    body = models.TextField(help_text="Enter the blog body")
    category = models.ForeignKey(
        BlogCategory,
        on_delete=models.CASCADE,
        related_name="category",
        help_text="Choose the blog category",
    )
    tags = models.CharField(help_text="Enter the blog tags", max_length=500)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name_plural = "Blog Posts"
        ordering = ["title", "updated_at"]
