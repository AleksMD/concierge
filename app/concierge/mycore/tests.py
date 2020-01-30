from django.test import TestCase
from mycore.models import Journal, Room, Tenant


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
        room = Room(number=3,
                    max_guests=4)
        room.save()
        self.assertEqual(room.number, 3)
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
    def test_journal_model_creation(self):
        room = Room(number=3,
                    max_guests=4)
        room.save()
        tenant = Tenant(first_name='Susan',
                        last_name='Stone',
                        date_of_birth='2000-01-01',
                        phone='111-22-33')
        tenant.save()
        journal = Journal(room=room)
        journal.tenant = tenant
        journal.save()
        self.assertEqual(journal.room.number, 3)
        self.assertEqual(journal.room.max_guests, 4)
        self.assertEqual(journal.tenant.first_name, 'Susan')
        self.assertEqual(journal.room.status, 'engaged')
        self.assertIsNone(journal.key_is_back)
        self.assertIsNotNone(journal.key_on_hands)
        self.assertFalse(journal.key_is_kept)
        journal.guests = 5
        with self.assertRaises(ValueError):
            journal.save()
