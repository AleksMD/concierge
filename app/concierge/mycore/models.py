from django.db import models
from datetime import datetime

# Create your models here.


def key_transition_datetime(timespec='seconds'):
    return datetime.utcnow().isoformat(timespec=timespec)


class Tenant(models.Model):
    """
    Room's owner/tenant
    """
    first_name = models.CharField(
        'First name',
        max_length=250,
    )
    last_name = models.CharField(
        'Last name',
        max_length=250,
    )
    date_of_birth = models.DateField(
        blank=True,
        null=True,
        db_index=True,
    )
    phone = models.CharField(
        'Phone num',
        max_length=20,
        blank=True,
        null=True,
    )
    photo = models.ImageField(
        'Photo',
        upload_to='tenant',
        help_text='Photo of the tenant',
        null=True,
        blank=True
    )
    notes = models.TextField(
        blank=True,
        null=True,
    )

    @property
    def fullname(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.fullname

    class Meta:
        ordering = ['first_name', 'last_name']
        indexes = [
            models.Index(fields=['first_name', 'last_name']),
        ]


class Room(models.Model):
    number = models.IntegerField()
    tenant = models.ForeignKey(Tenant,
                               null=True,
                               on_delete=models.DO_NOTHING)
    max_guests = models.IntegerField(null=True)
    status = models.CharField(max_length=10, default='free')


class Journal(models.Model):
    key_on_hands = models.DateTimeField(null=True)
    key_is_back = models.DateTimeField(null=True)
    tenant = models.ForeignKey(Tenant, null=True, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.DO_NOTHING)
    comments = models.CharField(max_length=255, null=True)
    guests = models.IntegerField(default=0)
    key_is_kept = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        room = self.room
        max_guests = room.max_guests
        max_guests = self.guests
        if max_guests and self.guests > max_guests:
            raise  ValueError(f'Maximal number of guests for this room is'
                              f'{max_guests}')
        elif self.key_is_kept and self.tenant:
            self.key_is_kept = False
            self.key_on_hands = key_transition_datetime()
            room.status = 'engaged'
            room.tenant = self.tenant
            room.save()
        elif not self.key_is_kept and not self.tenant:
            self.key_is_kept = True
            self.key_is_back = key_transition_datetime()
            self.key_on_hands = None
            room.status = 'free'
            room.tenant = self.tenant
            room.save()
        else:
            raise ValueError('You try to do incompatible actions. Please check'
                             'all fields for correctness')
        super().save(*args, **kwargs)


