from django.shortcuts import render
from django.shortcuts import redirect
from InvManage.forms import *
from InvManage.models import *
from InvManage.filters import ConsumerFilter
from InvManage.serializers import ConsumerSerializer
from django.http import JsonResponse
from InvManage.scripts.filters import *
from InvManage.scripts.helpers import create_event


def create_consumer_view(request):
    """ 
        Creates a consumer on ``POST`` request, and returns a consumer creation form on ``GET`` request. 

        .. http:get:: /consumer

            Gets the consumer creation form.

            **Example request**:

            .. sourcecode:: http

                GET /consumer/ HTTP/1.1
                Host: localhost:8000
                Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
            
    
            **Example response**:

            .. sourcecode:: http

                HTTP/1.1 200 OK
                Vary: Accept
                Content-Type: text/html; charset=utf-8

            :reqheader Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
            :statuscode 200: Consumer creation form received successfully.

        .. http:post:: /consumer

            Creates a consumer.

            **Example request**:

            .. sourcecode:: http

                POST /consumer/ HTTP/1.1
                Host: localhost:8000
                Content-Type: multipart/form-data;

            :form consumer-name: ``The Music Store``

            :form consumer-identifier: ``CONS1256``

            :form consumer-gstin: ``89ACC654654335``

            :form consumer-phone: ``+91 6543525422``

            :form consumer-address: ``Plot no. 958, N-4, Neo Complex, Barh, Wokha, Nagaland, 797111``

            :form consumer-email: ``johnDoe@themusic.store``

            :form consumer-location: ``Wokha``
            
            :resheader Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryLTR88aZAnBUSE7mv
            :statuscode 302: Redirects to ``/consumer``.

    """
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
        new_consumer = Consumer.objects.create(**data)
        create_event(new_consumer,'Created')
        return redirect('consumer')
        


def update_consumer_view(request):
    """ 
        Updates a consuemr on ``POST`` request and returns the consumer update form for ``GET`` request. 

        .. http:get:: /consumer/update

            Gets the consumer update form whose primary key matches the query parameter ``pk``.

            **Example request**:

            .. sourcecode:: http

                GET /consumer/update HTTP/1.1
                Host: localhost:8000
                Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
            
            :query pk: The primary key of the consumer.
            
            **Example response**:

            .. sourcecode:: http

                HTTP/1.1 200 OK
                Vary: Accept
                Content-Type: text/html; charset=utf-8

            :reqheader Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
            :statuscode 200: Consumer update form received successfully.

        .. http:post:: /consumer/update

            Updates the consumer.

            **Example request**:

            .. sourcecode:: http

                POST /company/update HTTP/1.1
                Host: localhost:8000
                Content-Type: multipart/form-data;
    
            :form pk: ``7``
            
            :form consumer-name: ``The Music Store``

            :form consumer-identifier: ``CONS1256``

            :form consumer-gstin: ``89ACC654654335``

            :form consumer-phone: ``+91 6543525422``

            :form consumer-address: ``Plot no. 958, N-4, Neo Complex, Barh, Wokha, Nagaland, 797111``

            :form consumer-email: ``johnDoe@themusic.store``

            :form consumer-location: ``Wokha``

            :resheader Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryLTR88aZAnBUSE7mv
            :statuscode 302: Redirects to ``/consumer``.

    """
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
        create_event(Consumer.objects.get(id=pk),'Updated')
        return redirect('consumer')


def delete_consumer_view(request, pk):
    """ 
        Deletes the consumer with primary key ``pk`` on ``POST`` request.

        .. http:post:: /consumer/<str:object_id>/delete

            Deletes the consumer represented by the primary key ``object_id``.

            **Example request**:

            .. sourcecode:: http

                POST /consumer/5/delete HTTP/1.1
                Host: localhost:8000
                Content-Type: application/x-www-form-urlencoded
                
            :param object_id: Consumer primary key.
            :resheader Content-Type: application/x-www-form-urlencoded
            :statuscode 302: Redirects to ``/consumer``.
            :statuscode 500: Consumer matching query does not exist.

    """
    if request.method == 'POST':
        consumer = Consumer.objects.get(id=pk)
        create_event(consumer,'Deleted')
        consumer.delete()
        return redirect('consumer')


def display_consumers_view(request):
    """ 
        Retrieves the list of consumers on ``GET`` request.

        .. http:get:: /consumers/

            Gets the list of all consumers.

            **Example request**:

            .. sourcecode:: http

                GET /companies/ HTTP/1.1
                Host: localhost:8000
                Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
            
            :form page: The page number of the consumers list.
    
            **Example response**:

            .. sourcecode:: http

                HTTP/1.1 200 OK
                Vary: Accept
                Content-Type: text/html; charset=utf-8

            :reqheader Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
            :statuscode 200: List of consumers received successfully.
    """
    if request.method == 'GET':
        consumers = Consumer.objects.all()
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
                                                               'dicts': dictionaries,
                                                               'url': request.build_absolute_uri('/consumers/')})


def get_consumer(request):
    """ 
        Returns the ``JSON`` serialized data of the requested consumer on ``GET`` request.

        .. http:get:: /get_consumer/

            Gets the JSON serialized data of the requested consumer.

            **Example request**:

            .. sourcecode:: http

                GET /get_consumer/ HTTP/1.1
                Host: localhost:8000
                Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
                
            **Example response**:

            .. sourcecode:: http

                HTTP/1.1 200 OK
                Vary: Accept
                Content-Type: application/json; charset=utf-8

                [
                    {
                        "name": "The Music Store",
                        "identifier": "CONS1256",
                        "gstin": "89AAC4633353643",
                        "phone": "+91 8325642358",
                        "address": "Plot no 958, N- 4, Neo Complex, Barh, Wokha, Nagaland, 797111",
                        "email": "JohnDoe@themusic.store",
                        "location": "Wokha"
                    }
                ]

            :resheader Content-Type: application/json
            :statuscode 200: List of consumers received successfully.
            :statuscode 400: Bad request version
            :statuscode 500: Consumer matching query does not exist.
    """
    if request.method == 'GET':
        consumer_id = request.GET.get('consumer_id')
        consumer = ConsumerSerializer(Consumer.objects.get(id=consumer_id))
        return JsonResponse(consumer.data)