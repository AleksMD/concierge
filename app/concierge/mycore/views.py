from django.http import HttpResponse
from django.template.loader import render_to_string
import mycore.models as models
from django.core import serializers
from django.core.serializers import SerializerDoesNotExist
from django.core.exceptions import ObjectDoesNotExist
from http import HTTPStatus
from django.views.generic.edit import FormView
from mycore.forms import JournalForm


def health_check(request):
    return HttpResponse("OK")


def index(request):
    return HttpResponse(render_to_string('index.html', {'title': 'concierge'}))


def api_serializer(request, model_type, model_id):
    print(request.GET['format'])
    try:
        model = getattr(models, model_type.capitalize())
        return HttpResponse(
            serializers.serialize(request.GET['format'],
                                  [model.objects.get(id=model_id)]))
    except (AttributeError, SerializerDoesNotExist,
            ObjectDoesNotExist):
        return HttpResponse(status=HTTPStatus.NOT_FOUND)


def journal_updated(request):
    return HttpResponse("JOURNAL WAS SUCCESSFULLY UPDATED!")


class JournalView(FormView):
    template_name = 'journal.html'
    form_class = JournalForm
    success_url = '/journal_updated'

    def form_valid(self, form):
        form.save_journal()
        return super().form_valid(form)

    def form_invalid(self, form):
        # TODO Add custom form validation
        return super().form_invalid(form)
