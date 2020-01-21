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


INVALID_FORM_MESSAGE = ("You entered inappropriate data in form's fields."
                        "Plase try again if neccessary.")


def health_check(request):
    return HttpResponse("OK")


def index(request):
    return HttpResponse(render_to_string('index.html', {'title': 'concierge'}))


def model_serialized_view(request, model_type, model_id):
    try:
        model = getattr(models, model_type.capitalize())
        return HttpResponse(
            serializers.serialize(request.GET['format'],
                                  [model.objects.get(id=model_id)]))
    except (AttributeError, SerializerDoesNotExist,
            ObjectDoesNotExist):
        return HttpResponse(status=HTTPStatus.NOT_FOUND)


def success(request, message='Success'):
    return HttpResponse(render_to_string('success.html', {'message': message}))


class JournalView(FormView):
    template_name = 'journal.html'
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
    success_url = '/tenant_created'

    def form_valid(self, form):
        form.save_tenant()
        return super().form_valid(form)

    def form_invalid(self, form):
        return HttpResponse(
            render_to_string('error.html', {'message': INVALID_FORM_MESSAGE}))


class TenantSearchView(FormView):
    template_name = 'tenant_search.html'
    form_class = TenantSearchForm
    success_url = '/tenant_detailed'

    def form_valid(self, form):
        form.find_tenant()
        return super().form_valid(form)

    def form_invalid(self, form):
        return HttpResponse(
            render_to_string('error.html', {'message': INVALID_FORM_MESSAGE}))


class RoomCreateView(FormView):
    template_name = 'room_create.html'
    form_class = RoomCreateForm
    success_url = '/room_created'

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
        form.find_room()
        return super().form_valid(form)

    def form_invalid(self, form):
        return HttpResponse(
            render_to_string('error.html', {'message': INVALID_FORM_MESSAGE}))


class TenantDetailView(DetailView):
    ...


class RoomDetailView(DetailView):
    ...


class TenantListView(ListView):
    ...


class RoomListView(ListView):
    ...
