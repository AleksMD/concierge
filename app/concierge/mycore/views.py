import os
from django.db.utils import IntegrityError
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
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.contrib.auth.decorators import login_required


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INVALID_FORM_MESSAGE = ("You entered inappropriate data in form's fields."
                        "Please try again if neccessary.")


def get_user():
    ukey = 'users_all'
    users = cache.get(ukey)
    if not users:
        users = get_user_model().objects.all()
        cache.set(ukey, users, settings.CACHE_TTL)
    return users


def health_check(request):
    return HttpResponse("OK")


def index(request):
    return HttpResponse(render_to_string('index.html', {'title': 'concierge'}))


@cache_page(settings.CACHE_TTL)
@login_required(login_url='/accounts/login/')
def api_entry_page(request):
    return HttpResponse(render_to_string('api_entry.html'))


@login_required(login_url='/accounts/login/')
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


class JournalView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    login_url = '/accounts/login/'
    template_name = 'journal_update.html'
    form_class = JournalUpdateForm
    success_message = "Journal was successfully updated!"
    success_url = f'/success/{success_message}'
    permission_required = 'mycore.create_journal'

    def form_valid(self, form):
        try:
            form.save_journal()
        except (ValueError, IntegrityError) as err:
            if isinstance(err, IntegrityError):
                err = "You can't update journal with those values"
            return HttpResponse(
                render_to_string('error.html', {'message': err}),
                status=HTTPStatus.BAD_REQUEST)
        return super().form_valid(form)

    def form_invalid(self, form):
        return HttpResponse(
            render_to_string('error.html', {'message': INVALID_FORM_MESSAGE}),
            status=HTTPStatus.BAD_REQUEST)


class JournalSearchView(LoginRequiredMixin, FormView):
    template_name = 'journal_search.html'
    form_class = JournalSearchForm
    login_url = '/accounts/login/'

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
            render_to_string('error.html', {'message': INVALID_FORM_MESSAGE}),
            status=HTTPStatus.BAD_REQUEST)


class TenantCreateView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = 'tenant_create.html'
    form_class = TenantCreateForm
    success_message = "Tenant successfully created!"
    success_url = f'/success/{success_message}'
    login_url = '/accounts/login/'
    permission_required = 'tenant.create_tenant'

    def form_valid(self, form):
        try:
            form.save_tenant()
        except IntegrityError as err:
            if 'DUPLICATE' in str(err):
                err = 'Tenant already exists'
            err = "You can't create tenant with those values"
            return HttpResponse(
                       render_to_string('error.html', {'message': err}),
                       status=HTTPStatus.BAD_REQUEST)

        return super().form_valid(form)

    def form_invalid(self, form):
        return HttpResponse(
            render_to_string('error.html', {'message': INVALID_FORM_MESSAGE}))


class TenantSearchView(LoginRequiredMixin, FormView):
    template_name = 'tenant_search.html'
    form_class = TenantSearchForm
    login_url = '/accounts/login/'

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


class RoomCreateView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = 'room_create.html'
    form_class = RoomCreateForm
    success_message = "Room successfully created!"
    success_url = f'/success/{success_message}'
    permission_required = 'mycore.create_room'

    def form_valid(self, form):
        try:
            form.save_room()
        except IntegrityError as err:
            if 'DUPLICATE' in str(err):
                err = 'Room already exists'
            err = "You can't create room with those values"
            return HttpResponse(
                       render_to_string('error.html', {'message': err}))

        return super().form_valid(form)

    def form_invalid(self, form):
        return HttpResponse(
            render_to_string('error.html', {'message': INVALID_FORM_MESSAGE}))


class RoomSearchView(LoginRequiredMixin, FormView):
    template_name = 'room_search.html'
    form_class = RoomSearchForm
    success_url = '/room_detailed'
    login_url = '/accounts/login/'

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


class TenantDetailView(LoginRequiredMixin, DetailView):
    model = models.Tenant
    template = 'tenant_detail.html'
    login_url = '/accounts/login/'

    def get_template_names(self):
        return [os.path.join(BASE_DIR, 'templates', self.template)]


class RoomDetailView(LoginRequiredMixin, DetailView):
    model = models.Room
    template = 'room_detail.html'
    login_url = '/accounts/login/'

    def get_template_names(self):
        return [os.path.join(BASE_DIR, 'templates', self.template)]


class TenantListView(LoginRequiredMixin, ListView):
    model = models.Tenant
    template = 'tenant_list.html'
    login_url = '/accounts/login/'

    def get_queryset(self):
        tenants_id = getattr(self.request.session, 'tenants_id', None)
        if tenants_id:
            query_set = models.Tenant.objects.filter(id__in=tenants_id)
            delattr(self.request.session, 'tenants_id')
            return query_set
        return models.Tenant.objects.all()

    def get_template_names(self):
        return [os.path.join(BASE_DIR, 'templates', self.template)]


class RoomListView(LoginRequiredMixin, ListView):
    model = models.Room
    template = 'room_list.html'
    login_url = '/accounts/login/'

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
