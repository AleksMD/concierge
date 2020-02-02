from django.test import TestCase
from mycore.models import Journal, Room, Tenant
from django.conf import settings


class TenantModelTests(TestCase):

    def test_tenant_model_creation(self):
        tenant = Tenant(first_name='Susan',
                        last_name='Stone',
                        date_of_birth='2000-01-01',
                        phone='111-22-33')
        tenant.save()
        self.assertEqual(tenant.first_name, 'Susan')
        self.assertEqual(tenant.last_name, 'Stone')
        self.assertEqual(tenant.date_of_birth, '2000-01-01')
        self.assertEqual(tenant.phone, '111-22-33')


class RoomModelTests(TestCase):

    def test_room_model_creation(self):
        room = Room(number=13,
                    max_guests=4)
        room.save()
        self.assertEqual(room.number, 13)
        self.assertEqual(room.max_guests, 4)
        tenant = Tenant(first_name='Susan',
                        last_name='Stone',
                        date_of_birth='2000-01-01',
                        phone='111-22-33')
        tenant.save()
        room.tenant = tenant
        room.save()
        self.assertEqual(room.tenant.first_name, 'Susan')
        self.assertEqual(room.tenant.last_name, 'Stone')


class JournalModelTests(TestCase):

    fixtures = settings.FIXTURES

    def test_journal_model_creation(self):
        room = Room.objects.filter(number=33).first()
        tenant = Tenant.objects.filter(first_name='Jane',
                                       last_name='Doe').first()
        journal = Journal(room=room)
        journal.tenant = tenant
        journal.save()
        self.assertEqual(journal.room.number, 33)
        self.assertEqual(journal.room.max_guests, 22)
        self.assertEqual(journal.tenant.first_name, 'Jane')
        self.assertEqual(journal.room.status, 'engaged')
        self.assertIsNone(journal.key_is_back)
        self.assertIsNotNone(journal.key_on_hands)
        self.assertFalse(journal.key_is_kept)
