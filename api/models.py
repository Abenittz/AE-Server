from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    registration_start_date = models.DateTimeField()
    registration_end_date = models.DateTimeField()
    location = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    available_seat = models.IntegerField()

    speakers = models.ManyToManyField(
        'Speaker', related_name='events_speaking', blank=True)

    sponsors = models.ManyToManyField(
        'Sponsor', related_name='events_sponsor', blank=True)

    attendees = models.ManyToManyField(
        'Attendee', related_name='events_attending', blank=True)

    schedules = models.ManyToManyField(
        'Schedule', related_name='events_scheduled', blank=True)
    
    roomids = models.ManyToManyField(
        'RoomId', related_name='events_roomid', blank=True
    )
    

    def __str__(self):
        return self.title

    @property
    def status(self):
        if self.end_date < timezone.now():
            return 'passed'
        else:
            return 'upcoming'


class Attendee(models.Model):
    fullname = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    
    

    def __str__(self):
        return self.fullname


class Speaker(models.Model):
    fullname = models.CharField(max_length=255)
    organization = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    
    
    def __str__(self):
        return self.fullname


class Sponsor(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    
    

    def __str__(self):
        return self.name


class Schedule(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    activity = models.TextField()

    
    def __str__(self):
        return self.activity
    
class RoomId(models.Model):
    roomId = models.CharField(max_length=255, ) 

    def __str__(self):
        return self.roomId
    
    
class Videos(models.Model):
    video = models.FileField(upload_to="vedeos/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.video
    


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)

class EventUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    fullname = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['fullname', 'email', 'password']

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'event_users'
        default_related_name = 'event_user'
        permissions = (  
            ("view_user", "Can view user"),
            ("add_speaker", "Can add speaker"),
            ("add_sponsor", "Can add sponsor"),
            ("change_event", "Can edit event"),
            ("delete_event", "Can delete event"),
            ("change_user", "Can edit user"),
            ("delete_user", "Can delete user"),
            ("add_admin", "Can add admin"),
        )

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='customuser_groups',
        related_query_name='customuser_group',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='customuser_permissions',
        related_query_name='customuser_permission',
        help_text='Specific permissions for this user.',
    )