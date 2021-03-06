from django import forms
from mycore.models import Tenant, Room, Journal
# from django.core.exceptions import ObjectDoesNotExist


class TenantCreateForm(forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    date_of_birth = forms.DateField(required=True)
    phone = forms.CharField(required=True)
    photo = forms.ImageField(required=False)
    notes = forms.CharField(required=False)

    def save_tenant(self):
        fields = {k: v for k, v in self.data.items()
                  if not k.endswith('token') and v}
        tenant = Tenant(**fields)
        tenant.save()


class TenantSearchForm(forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    date_of_birth = forms.DateField(required=False)
    phone = forms.CharField(required=False)

    def find_tenant(self):
        filter_keys = {k: v for k, v in self.data.items()
                       if not k.endswith('token') and v}
        tenant = Tenant.objects.filter(**filter_keys).all()
        return tenant


class RoomCreateForm(forms.Form):
    number = forms.IntegerField(required=True)
    max_guests = forms.IntegerField(required=False)

    def save_room(self):
        fields = {k: v for k, v in self.data.items()
                  if not k.endswith('token') and v}
        room = Room(**fields)
        room.save()


class RoomSearchForm(forms.Form):
    number = forms.IntegerField(required=False)
    status = forms.CharField(required=False)

    def find_room(self):
        filter_keys = {k: v for k, v in self.data.items()
                       if v and not k.endswith('token')}
        room = Room.objects.filter(**filter_keys).all()
        return room


class JournalUpdateForm(forms.Form):
    tenant_first_name = forms.CharField()
    tenant_last_name = forms.CharField()
    room_number = forms.IntegerField()
    guests = forms.IntegerField(required=False)
    comments = forms.CharField(required=False)
    clear_the_room = forms.BooleanField(required=False)

    def save_journal(self):
        tenant = Tenant.objects.get(first_name=self.data['tenant_first_name'],
                                    last_name=self.data['tenant_last_name'])
        room = Room.objects.get(number=self.data['room_number'])
        if self.data.get('clear_the_room'):
            journal = Journal.objects.filter(
                room__number=room.number,
                tenant__first_name=tenant.first_name,
                tenant__last_name=tenant.last_name).all()
            if len(journal) == 1:
                journal = journal[0]
                journal.tenant = None
                journal.save()
            elif len(journal) == 0:
                raise ValueError("You can't clear an empty room")
            else:
                raise ValueError(
                    "It seems you have provided wrong options for update!")
        else:
            journal = Journal(room=room,
                              tenant=tenant,
                              guests=int(self.data.get('guests', 0)),
                              comments=self.data.get('comments'))
            journal.save()


class JournalSearchForm(forms.Form):
    tenant__first_name = forms.CharField(required=False)
    tenant__last_name = forms.CharField(required=False)
    room__number = forms.IntegerField(required=False)

    def find_journal(self):
        filter_keys = {k: v for k, v in self.data.items()
                       if v and not k.endswith('token')}
        journal = Journal.objects.filter(**filter_keys).all()
        return journal
