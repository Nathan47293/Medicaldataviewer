from django.shortcuts import render
from .models import Product, Person, Injection


def table_view(request):
    selected_table = request.GET.get('table', 'Product')  # Default to 'Product' if not specified

    if selected_table == 'Product':
        model = Product
    elif selected_table == 'Person':
        model = Person
    elif selected_table == 'Injection':
        model = Injection
    else:
        model = None

    if model:
        data = model.objects.all()
        field_names = [field.name for field in model._meta.fields]
    else:
        data = []
        field_names = []

    context = {
        'data': data,
        'field_names': field_names,
        'selected_table': selected_table,
    }

    return render(request, 'viewer/table_view.html', context)
