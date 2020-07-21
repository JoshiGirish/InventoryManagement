from django.shortcuts import render
from django.shortcuts import redirect
from InvManage.forms import *
from InvManage.models import *
from InvManage.filters import ConsumerFilter
from InvManage.serializers import ConsumerSerializer
from django.http import JsonResponse
from InvManage.scripts.filters import *


def create_consumer_view(request):
    if request.method == 'GET':
        consumers = []
        for i, consumer in enumerate(Consumer.objects.all()):
            consumers.append(
                {'id': consumer.id, 'name': consumer.name, 'code': consumer.identifier})
        consumer_form = ConsumerForm()
        return render(request, 'consumer.html', {'consumer_form': consumer_form, 'consumers': consumers, 'requested_view_type': 'create'})
    if request.method == 'POST':
        data = {}
        form = ConsumerForm(request.POST, prefix='consumer')
        if form.is_valid():
            data.update(form.cleaned_data)
        Consumer.objects.create(**data)
        return redirect('consumer')


def delete_consumer_view(request, pk):
    if request.method == 'POST':
        consumer = Consumer.objects.get(id=pk)
        consumer.delete()
        return redirect('consumer')


def get_consumer(request):
    if request.method == 'GET':
        consumer_id = request.GET.get('consumer_id')
        consumer = ConsumerSerializer(Consumer.objects.get(id=consumer_id))
        return JsonResponse(consumer.data)


def display_consumers_view(request):
    if request.method == 'GET':
        consumers = sort_ascending_descending(request, Consumer)
        state = FilterState.objects.get(name='Consumers_basic')
        column_list = change_column_position(request, state)
        myFilter = ConsumerFilter(request.GET, queryset=consumers)
        queryset = myFilter.qs
        number_of_objects = len(queryset)
        page_number = request.GET.get('page')
        print(number_of_objects)
        page_obj, dictionaries = paginate(queryset, myFilter, page_number)
        return render(request, 'consumer/consumer_contents.html', {'page_obj': page_obj,
                                                               'myFilter': myFilter,
                                                               'n_prod': number_of_objects,
                                                               'columns': column_list,
                                                               'dicts': dictionaries})

def update_consumer_view(request):
    if request.method == 'GET':
        pk = request.GET.get('pk')
        consumer = Consumer.objects.get(id=pk)
        data = consumer.__dict__
        consumer_form = ConsumerForm(initial=data)
        return render(request, 'consumer/update_consumer.html', {'consumer_form': consumer_form, 'requested_view_type': 'update','pk':pk})
    if request.method == 'POST':
        pk = request.POST.get('pk')
        print(pk)
        data = {}
        form = ConsumerForm(request.POST, prefix='consumer')
        if form.is_valid():
            data.update(form.cleaned_data)
        print('Printing DATA:', data)
        Consumer.objects.filter(id=pk).update(**data)
        return redirect('consumer')
