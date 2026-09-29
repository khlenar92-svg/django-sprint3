from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from .models import Category, Post, POSTS_LIMIT


def index(request):
    posts = Post.objects.published()[:POSTS_LIMIT]
    return render(request, 'blog/index.html', {'posts': posts})


def post_detail(request, id):
    post = get_object_or_404(
        Post.objects.select_related(
            'author',
            'category',
            'location',
        ),
        pk=id,
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now(),
    )

    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )

    posts = Post.objects.filter(
        category=category,
        is_published=True,
        pub_date__lte=timezone.now(),
    ).select_related(
        'author',
        'category',
        'location',
    )

    return render(
        request,
        'blog/category.html',
        {
            'category': category,
            'posts': posts,
        },
    )
