from django.test import TestCase, Client, tag
from mycore.models import Tenant, Room, Journal
from datetime import date
from django.conf import settings

DOB = date.today().isoformat()


class TestJournalView(TestCase):
    client = Client()
    fixtures = settings.FIXTURES

    @tag('get_room_valid')
    def test_tenant_get_room_valid_case(self):
        data = {'tenant_first_name': 'Jane',
                'tenant_last_name': 'Doe',
                'room_number': 13}
        journal_resp = self.client.post('/journal_update/', data)
        self.assertEqual(journal_resp.status_code, 302)
        tenant = Tenant.objects.filter(first_name='Jane').first()
        self.assertIsNotNone(tenant)
        room = Room.objects.filter(number=13).first()
        self.assertIsNotNone(room)
        self.assertEqual(room.number, 13)
        self.assertEqual(room.tenant.first_name, 'Jane')
        journal = Journal.objects.first()
        self.assertFalse(journal.key_is_kept)
        self.assertEqual(journal.room.number, 13)
        self.assertEqual(journal.tenant.first_name, 'Jane')
        self.assertIsNotNone(journal.key_on_hands)
        self.assertIsNone(journal.key_is_back)

    @tag('leave_room_valid')
    def test_tenant_leave_room_valid_case(self):
        data = {'tenant_first_name': 'Jane',
                'tenant_last_name': 'Doe',
                'room_number': 13}
        journal_resp = self.client.post('/journal_update/', data)
        journal = Journal.objects.filter(room__number=13).first()
        self.assertEqual(journal_resp.status_code, 302)
        data.update({'clear_the_room': True})
        journal_resp = self.client.post('/journal_update/', data)
        self.assertEqual(journal_resp.status_code, 302)
        journal = Journal.objects.filter(room__number=13).first()
        self.assertIsNotNone(journal)
        self.assertEqual(journal.room.status, 'free')
        self.assertTrue(journal.key_is_kept)
        self.assertIsNone(journal.key_on_hands)
        self.assertIsNotNone(journal.key_is_back)

    @tag('get_engaged_room')
    def test_tenant_get_engaged_room(self):

        data = {'tenant_first_name': 'Alice',
                'tenant_last_name': 'Lee',
                'room_number': 13}
        journal_resp = self.client.post('/journal_update/', data)
        self.assertEqual(journal_resp.status_code, 302)
        data = {'tenant_first_name': 'Jane',
                'tenant_last_name': 'Doe',
                'room_number': 13}
        journal_resp = self.client.post('/journal_update/', data)
        self.assertEqual(journal_resp.status_code, 400)
        content = str(journal_resp.content, encoding='utf-8')
        self.assertInHTML("You can't update journal with those values",
                          content)

    @tag('leave_free_room')
    def test_tenant_leave_free_room(self):
        data = {'tenant_first_name': 'Alice',
                'tenant_last_name': 'Lee',
                'room_number': 13,
                'clear_the_room': True}
        journal_resp = self.client.post('/journal_update/', data)
        self.assertEqual(journal_resp.status_code, 400)
        content = str(journal_resp.content, encoding='utf-8')
        self.assertInHTML("You can't clear an empty room", content)
