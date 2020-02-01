from django.test import TestCase, Client, tag


class TestJournalView(TestCase):
    client = Client()

    @tag('get_room_valid')
    def test_tenant_get_room_valid_case(self):
        ...


    @tag('leave_room_valid')
    def test_tenant_leave_room_valid_case(self):
        ...

    @tag('get_engage_room')
    def test_tenant_get_engaged_room(self):
        ...

    @tag('leave_free_room')
    def test_tenant_leave_free_room(self):
        ...

