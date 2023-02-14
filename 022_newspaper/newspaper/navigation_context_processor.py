from django.db.models import Case, F, Sum, When

from newspaper.models import Category, Post, Tag


def navigation(request):
    categories = Category.objects.all()
    top_categories = (
        Post.objects.values("category__pk", "category__name")
        .annotate(
            pk=F("category__pk"), name=F("category__name"), max_views=Sum("views_count")
        )
        .order_by("-views_count")
        .distinct()
        .values("pk", "name", "max_views")
    )
    print(top_categories)
    category_ids = [top_category["pk"] for top_category in top_categories]
    order_by_max_views = Case(
        *[
            When(id=category["pk"], then=category["max_views"])
            for category in top_categories
        ]
    )
    top_categories = Category.objects.filter(pk__in=category_ids).order_by(
        -order_by_max_views
    )
    print(top_categories)
    tags = Tag.objects.all()[:10]
    return {
        "categories": categories,
        "top_categories": top_categories,
        "tags": tags,
    }
