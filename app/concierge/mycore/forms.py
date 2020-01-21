from django import forms
from mycore.models import Tenant, Room, Journal


class JournalForm(forms.Form):
    tenant_first_name = forms.CharField()
    tenant_last_name = forms.CharField()
    room_number = forms.IntegerField()
    guests = forms.IntegerField()
    comments = forms.CharField()

    def save_journal(self):
        tenant = Tenant.objects.get(first_name=self.data['tenant_first_name'],
                                    last_name=self.data['tenant_last_name'])
        room = Room.objects.get(number=self.data['room_number'])
        journal = Journal(room=room,
                          tenant=tenant,
                          guests=self.data['guests'],
                          comments=self.data['comments'])
        journal.save()
