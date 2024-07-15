from django.core.paginator import Paginator

def paginate(request, queryset, per_page=12):
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj