from django.test import TestCase, Client, tag
from datetime import date


class TenantViewsTests(TestCase):
    def setUp(self):
        self.client = Client()

    @tag('tenant_create')
    def test_tenant_create_view(self):
        response = self.client.post('/tenant_create/',
                                    {'first_name': 'Jane',
                                     'last_name': 'Doe',
                                     'date_of_birth': date.today().isoformat(),
                                     'phone': 123456789})
        self.assertEqual(response.status_code, 302)

    @tag('tenant_detail')
    def test_tenant_detail_view(self):
        response = self.client.get('/tenant_detailed/1')
        self.assertEqual(response.status_code, 200)

    @tag('tenant_list')
    def test_tenant_list_view(self):
        response = self.client.get('/tenants_list/')
        self.assertEqual(response.status_code, 200)

    @tag('tenant_search')
    def test_tenant_search_view(self):
        response = self.client.post('/tenant_search/',
                                    {'first_name': 'Jane',
                                     'last_name': 'Doe'})
        self.assertEqual(response.status_code, 302)


class RoomViewsTests(TestCase):
    def setUp(self):
        self.client = Client()

    @tag('room_create')
    def test_room_create_view(self):
        response = self.client.post('/room_create/',
                                    {'number': 21,
                                     'max_guests': 7})
        self.assertEqual(response.status_code, 302)

    @tag('room_detail')
    def test_room_detail_view(self):
        response = self.client.get('/room_detailed/1')
        self.assertEqual(response.status_code, 200)

    @tag('room_list')
    def test_room_list_view(self):
        response = self.client.get('/room_list/')
        self.assertEqual(response.status_code, 200)

    @tag('room_search')
    def test_room_search_view(self):
        response = self.client.post('/room_search/',
                                    {'number': 21})
        self.assertEqual(response.status_code, 302)
