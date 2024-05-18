from django.core.paginator import Paginator
from django.shortcuts import render

from base.models import SiteImage

from .models import BlogCategory, BlogPost


def blog_list(request):
    blog_image = SiteImage.objects.get(place="blog")
    blog_categories = BlogCategory.objects.all()
    category_id = request.GET.get("category_id")

    if category_id:
        blogs = (
            BlogPost.objects.filter(category_id=category_id)
            .order_by("-created_at")
            .all()
        )
    else:
        blogs = (
            BlogPost.objects.select_related("category").order_by("-created_at").all()
        )

    paginator = Paginator(blogs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "blog/blog_list.html",
        {
            "blogs": blogs,
            "page_obj": page_obj,
            "blog_image": blog_image,
            "blog_categories": blog_categories,
        },
    )


def blog_details(request, blog_id):
    blog_image = SiteImage.objects.get(place="blog")
    blogs = (
        BlogPost.objects.select_related("category").order_by("-created_at").all()[:5]
    )
    blog = BlogPost.objects.select_related("category").get(id=blog_id)
    blog_categories = BlogCategory.objects.all()

    return render(
        request,
        "blog/blog_details.html",
        {
            "blogs": blogs,
            "blog": blog,
            "blog_categories": blog_categories,
            "blog_image": blog_image,
        },
    )
