from django.db import models
from datetime import datetime
from django.core.validators import MinValueValidator

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
    number = models.IntegerField(validators=[MinValueValidator(1)],
                                 unique=True)
    tenant = models.ForeignKey(Tenant,
                               null=True,
                               on_delete=models.DO_NOTHING)
    max_guests = models.IntegerField(null=True)
    status = models.CharField(max_length=10, default='free')

    def save(self, *args, **kwargs):
        self.status = 'engaged' if self.tenant else 'free'
        super().save(*args, **kwargs)


class Journal(models.Model):
    key_on_hands = models.DateTimeField(null=True)
    key_is_back = models.DateTimeField(null=True)
    tenant = models.ForeignKey(Tenant, null=True, on_delete=models.DO_NOTHING)
    room = models.OneToOneField(Room, on_delete=models.DO_NOTHING)
    comments = models.CharField(max_length=255, null=True)
    guests = models.IntegerField(default=0)
    key_is_kept = models.BooleanField(default=True)

    def make_room_free(self):
        self.key_is_kept = True
        self.key_is_back = key_transition_datetime()
        self.key_on_hands = None
        self.room.tenant = self.tenant
        self.guests = 0
        self.room.save()

    def room_engaged_with_new_tenant(self):
        self.key_is_kept = False
        self.key_on_hands = key_transition_datetime()
        self.room.tenant = self.tenant
        self.room.save()

    def save(self, *args, **kwargs):
        max_guests = self.room.max_guests
        if max_guests and self.guests > max_guests:
            return (f'Maximal number of guests for this room is'
                    f'{max_guests}')
        if self.key_is_kept and self.tenant:
            self.room_engaged_with_new_tenant()
        elif not self.key_is_kept and not self.tenant:
            self.make_room_free()
        else:
            return ('You tried to do incompatible actions. Please check'
                    'all fields for correctness')
        super().save(*args, **kwargs)
