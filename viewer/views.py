from django.shortcuts import render
from django.db.models import Count
from .models import Product, Person, Injection
import json

# Main Table View Function
def table_view(request):
    selected_table = request.GET.get('table', 'Product')  # Default to 'Product'
    data = None
    filters = {}
    field_names = []
    model = None

    # Determine if the table selection has changed
    previous_table = request.session.get('previous_table')
    table_changed = previous_table != selected_table
    request.session['previous_table'] = selected_table

    # Set up data and filters for each table
    if selected_table == 'Product':
        model = Product
        data = model.objects.all()

        # Get filter parameters
        id_value = request.GET.get('id', '')
        product_name = request.GET.get('product', '')

        # Reset filters if table changed
        if table_changed:
            id_value = ''
            product_name = ''

        # Apply filters
        if id_value:
            data = data.filter(id=id_value)
        if product_name:
            data = data.filter(product__icontains=product_name)

        # Store current filter values
        filters = {
            'id': id_value,
            'product': product_name,
        }

    elif selected_table == 'Person':
        model = Person
        data = model.objects.all()

        # Get filter parameters
        id_value = request.GET.get('id', '')
        age_min = request.GET.get('age_min', '')
        age_max = request.GET.get('age_max', '')
        sex = request.GET.get('sex', '')
        qualification = request.GET.get('qualification', '')
        country = request.GET.get('country', '')
        death = request.GET.get('death', '')
        disability = request.GET.get('disability', '')

        # Reset filters if table changed
        if table_changed:
            id_value = age_min = age_max = sex = qualification = country = death = disability = ''

        # Apply filters
        if id_value:
            data = data.filter(id=id_value)
        if age_min:
            data = data.filter(age__gte=age_min)
        if age_max:
            data = data.filter(age__lte=age_max)
        if sex:
            data = data.filter(sex=sex)
        if qualification:
            data = data.filter(qualification=qualification)
        if country:
            data = data.filter(country__icontains=country)
        if death:
            data = data.filter(death=death)
        if disability:
            data = data.filter(disability=disability)

        # Store current filter values
        filters = {
            'id': id_value,
            'age_min': age_min,
            'age_max': age_max,
            'sex': sex,
            'qualification': qualification,
            'country': country,
            'death': death,
            'disability': disability,
        }

    elif selected_table == 'Injection':
        model = Injection
        data = model.objects.all()

        # Get filter parameters
        id_value = request.GET.get('id', '')
        drug = request.GET.get('drug', '')
        injection_type = request.GET.get('injection', '')

        # Reset filters if table changed
        if table_changed:
            id_value = drug = injection_type = ''

        # Apply filters
        if id_value:
            data = data.filter(id=id_value)
        if drug:
            data = data.filter(drug=drug)
        if injection_type:
            data = data.filter(injection__icontains=injection_type)

        # Store current filter values
        filters = {
            'id': id_value,
            'drug': drug,
            'injection': injection_type,
        }

    # Get field names for the table
    if model:
        field_names = [field.name for field in model._meta.fields]

    # List of fields to display using get_FIELD_display()
    person_display_fields = ['sex', 'qualification', 'death', 'disability']

    context = {
        'data': data,
        'field_names': field_names,
        'selected_table': selected_table,
        'filters': filters,
        'Person': Person,
        'Injection': Injection,
        'person_display_fields': person_display_fields,
    }

    return render(request, 'viewer/table_view.html', context)

# Person Stats View Function
def person_stats(request):
    # Apply filters based on GET parameters
    filters = {
        'id': request.GET.get('id', ''),
        'age_min': request.GET.get('age_min', ''),
        'age_max': request.GET.get('age_max', ''),
        'sex': request.GET.get('sex', ''),
        'qualification': request.GET.get('qualification', ''),
        'country': request.GET.get('country', ''),
        'death': request.GET.get('death', ''),
        'disability': request.GET.get('disability', ''),
    }

    # Query the Person model based on filters
    persons = Person.objects.all()
    if filters['id']:
        persons = persons.filter(id=filters['id'])
    if filters['age_min']:
        persons = persons.filter(age__gte=filters['age_min'])
    if filters['age_max']:
        persons = persons.filter(age__lte=filters['age_max'])
    if filters['sex']:
        persons = persons.filter(sex=filters['sex'])
    if filters['qualification']:
        persons = persons.filter(qualification=filters['qualification'])
    if filters['country']:
        persons = persons.filter(country__icontains=filters['country'])
    if filters['death']:
        persons = persons.filter(death=filters['death'])
    if filters['disability']:
        persons = persons.filter(disability=filters['disability'])

    # Prepare data for charts
    # Age Distribution Histogram
    age_labels = ['0-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80', '81+']
    age_counts = [
        persons.filter(age__lte=10).count(),
        persons.filter(age__gte=11, age__lte=20).count(),
        persons.filter(age__gte=21, age__lte=30).count(),
        persons.filter(age__gte=31, age__lte=40).count(),
        persons.filter(age__gte=41, age__lte=50).count(),
        persons.filter(age__gte=51, age__lte=60).count(),
        persons.filter(age__gte=61, age__lte=70).count(),
        persons.filter(age__gte=71, age__lte=80).count(),
        persons.filter(age__gte=81).count(),
    ]

    # Gender Distribution Pie Chart
    gender_labels = [choice[1] for choice in Person.SEX_CHOICES if choice[0] in persons.values_list('sex', flat=True).distinct()]
    gender_counts = [persons.filter(sex=choice[0]).count() for choice in Person.SEX_CHOICES if choice[0] in persons.values_list('sex', flat=True).distinct()]

    # Qualification Distribution Bar Chart
    qualification_labels = [choice[1] for choice in Person.QUALIFICATION_CHOICES if choice[0] in persons.values_list('qualification', flat=True).distinct()]
    qualification_counts = [persons.filter(qualification=choice[0]).count() for choice in Person.QUALIFICATION_CHOICES if choice[0] in persons.values_list('qualification', flat=True).distinct()]

    context = {
        'filters': filters,
        'selected_table': 'Person',
        'age_labels': json.dumps(age_labels),
        'age_counts': json.dumps(age_counts),
        'gender_labels': json.dumps(gender_labels),
        'gender_counts': json.dumps(gender_counts),
        'qualification_labels': json.dumps(qualification_labels),
        'qualification_counts': json.dumps(qualification_counts),
    }

    return render(request, 'viewer/person_stats.html', context)

# Product Stats View Function
def product_stats(request):
    filters = {
        'id': request.GET.get('id', ''),
        'product': request.GET.get('product', ''),
    }

    # Query the Product model based on filters
    products = Product.objects.all()
    if filters['id']:
        products = products.filter(id=filters['id'])
    if filters['product']:
        products = products.filter(product__icontains=filters['product'])

    # Prepare data for charts
    product_usage = products.values('product').annotate(count=Count('product')).order_by('-count')
    product_labels = [entry['product'] for entry in product_usage]
    product_counts = [entry['count'] for entry in product_usage]

    context = {
        'filters': filters,
        'selected_table': 'Product',
        'product_labels': product_labels,
        'product_counts': product_counts,
    }

    return render(request, 'viewer/product_stats.html', context)

# Injection Stats View Function
def injection_stats(request):
    filters = {
        'id': request.GET.get('id', ''),
        'drug': request.GET.get('drug', ''),
        'injection': request.GET.get('injection', ''),
    }

    injections = Injection.objects.all()
    if filters['id']:
        injections = injections.filter(id=filters['id'])
    if filters['drug']:
        injections = injections.filter(drug=filters['drug'])
    if filters['injection']:
        injections = injections.filter(injection__icontains=filters['injection'])

    drug_usage = injections.values('drug').annotate(count=Count('drug')).order_by('-count')
    DRUG_CHOICES_DICT = dict(Injection.DRUG_CHOICES)
    drug_labels = [DRUG_CHOICES_DICT.get(entry['drug'], 'Unknown') for entry in drug_usage]
    drug_counts = [entry['count'] for entry in drug_usage]

    injection_type_distribution = injections.values('injection').annotate(count=Count('injection')).order_by('-count')
    injection_type_labels = [entry['injection'] for entry in injection_type_distribution]
    injection_type_counts = [entry['count'] for entry in injection_type_distribution]

    context = {
        'filters': filters,
        'selected_table': 'Injection',
        'drug_labels': drug_labels,
        'drug_counts': drug_counts,
        'injection_type_labels': injection_type_labels,
        'injection_type_counts': injection_type_counts,
    }

    return render(request, 'viewer/injection_stats.html', context)
