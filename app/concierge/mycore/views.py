import os
from django.http import HttpResponse
from django.template.loader import render_to_string
import mycore.models as models
from django.core import serializers
from django.core.serializers import SerializerDoesNotExist
from django.core.exceptions import ObjectDoesNotExist
from http import HTTPStatus
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from mycore.forms import (JournalUpdateForm,
                          TenantCreateForm,
                          TenantSearchForm,
                          RoomCreateForm,
                          RoomSearchForm,
                          JournalSearchForm)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INVALID_FORM_MESSAGE = ("You entered inappropriate data in form's fields."
                        "Plase try again if neccessary.")


def health_check(request):
    return HttpResponse("OK")


def index(request):
    return HttpResponse(render_to_string('index.html', {'title': 'concierge'}))


def api_entry_page(request):
    return HttpResponse(render_to_string('api_entry.html'))


def model_serialized_view(request, model_type, model_id, format_='json'):
    try:
        model = getattr(models, model_type.capitalize())
        return HttpResponse(
            serializers.serialize(getattr(request.GET, 'format', format_),
                                  [model.objects.get(id=model_id)]))
    except (AttributeError, SerializerDoesNotExist,
            ObjectDoesNotExist):
        return HttpResponse(status=HTTPStatus.NOT_FOUND)


def success(request, message='Success'):
    return HttpResponse(render_to_string('success.html', {'message': message}))


class JournalView(FormView):
    template_name = 'journal_update.html'
    form_class = JournalUpdateForm
    success_message = "Journal was successfully updated!"
    success_url = f'/success/{success_message}'

    def form_valid(self, form):
        form.save_journal()
        return super().form_valid(form)

    def form_invalid(self, form):
        return HttpResponse(
            render_to_string('error.html', {'message': INVALID_FORM_MESSAGE}))


class JournalSearchView(FormView):
    template_name = 'journal_search.html'
    form_class = JournalSearchForm

    def form_valid(self, form):
        err_message = None
        journal = form.find_journal()
        if len(journal) == 0:
            err_message = "Nothing was found"
        return HttpResponse(render_to_string('journal_view.html',
                                             {'journal': journal,
                                              'err_message': err_message}))

    def form_invalid(self, form):
        return HttpResponse(
            render_to_string('error.html', {'message': INVALID_FORM_MESSAGE}))


class TenantCreateView(FormView):
    template_name = 'tenant_create.html'
    form_class = TenantCreateForm
    success_message = "Tenant successfully created!"
    success_url = f'/success/{success_message}'

    def form_valid(self, form):
        form.save_tenant()
        return super().form_valid(form)

    def form_invalid(self, form):
        return HttpResponse(
            render_to_string('error.html', {'message': INVALID_FORM_MESSAGE}))


class TenantSearchView(FormView):
    template_name = 'tenant_search.html'
    form_class = TenantSearchForm

    def form_valid(self, form):
        tenants = form.find_tenant()
        if len(tenants) > 1:
            tenants_id = [tenant.id for tenant in tenants]
            self.request.session['tenants_id'] = tenants_id
            self.success_url = '/tenant_list'
        elif len(tenants) == 1:
            tenant = tenants[0]
            self.success_url = f'/tenant_detailed/{tenant.id}'
        else:
            err_message = "Nothing was found"
            return HttpResponse(render_to_string('empty_result.html',
                                                 {'err_message': err_message}))
        return super().form_valid(form)

    def form_invalid(self, form):
        return HttpResponse(
            render_to_string('error.html', {'message': INVALID_FORM_MESSAGE}))


class RoomCreateView(FormView):
    template_name = 'room_create.html'
    form_class = RoomCreateForm
    success_message = "Room successfully created!"
    success_url = f'/success/{success_message}'

    def form_valid(self, form):
        form.save_room()
        return super().form_valid(form)

    def form_invalid(self, form):
        return HttpResponse(
            render_to_string('error.html', {'message': INVALID_FORM_MESSAGE}))


class RoomSearchView(FormView):
    template_name = 'room_search.html'
    form_class = RoomSearchForm
    success_url = '/room_detailed'

    def form_valid(self, form):
        rooms = form.find_room()
        if len(rooms) > 1:
            rooms_id = [room.id for room in rooms]
            self.request.session['rooms_id'] = rooms_id
            self.success_url = '/room_list'
        elif len(rooms) == 1:
            room = rooms[0]
            self.success_url = f'/room_detailed/{room.id}'
        else:
            err_message = "Nothing was found"
            return HttpResponse(render_to_string('empty_result.html',
                                                 {'err_message': err_message}))
        return super().form_valid(form)

    def form_invalid(self, form):
        return HttpResponse(
            render_to_string('error.html', {'message': INVALID_FORM_MESSAGE}))


class TenantDetailView(DetailView):
    model = models.Tenant
    template = 'tenant_detail.html'

    def get_template_names(self):
        return [os.path.join(BASE_DIR, 'templates', self.template)]


class RoomDetailView(DetailView):
    model = models.Room
    template = 'room_detail.html'

    def get_template_names(self):
        return [os.path.join(BASE_DIR, 'templates', self.template)]


class TenantListView(ListView):
    model = models.Tenant
    template = 'tenant_list.html'

    def get_queryset(self):
        tenants_id = getattr(self.request.session, 'tenants_id', None)
        if tenants_id:
            query_set = models.Tenant.objects.filter(id__in=tenants_id)
            delattr(self.request.session, 'tenants_id')
            return query_set
        return models.Tenant.objects.all()

    def get_template_names(self):
        return [os.path.join(BASE_DIR, 'templates', self.template)]


class RoomListView(ListView):
    model = models.Room
    template = 'room_list.html'

    def get_queryset(self):
        rooms_id = getattr(self.request.session, 'rooms_id', None)
        if rooms_id:
            query_set = models.Room.objects.filter(
                id__in=rooms_id).order_by('number')
            delattr(self.request.session, 'rooms_id')
            return query_set
        return models.Room.objects.all()

    def get_template_names(self):
        return [os.path.join(BASE_DIR, 'templates', self.template)]
