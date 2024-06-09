from rest_framework import serializers
from .models import Event, Attendee, RoomId, Speaker, Sponsor, Schedule, Videos
from django.contrib.auth import get_user_model
from .models import EventUser
from django.contrib.auth import authenticate

# User = get_user_model()

class EventUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventUser
        fields = ['id', 'username', 'fullname', 'email', 'password', 'is_staff', 'is_active']
        # extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = EventUser.objects.create_user(**validated_data)
        return user

class EventUserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            print(user)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    raise serializers.ValidationError("User is not active.")
            else:
                raise serializers.ValidationError("Unable to log in with provided credentials.")
        else:
            raise serializers.ValidationError("Must provide username and password.")
        return data
    
    
    
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email', 'first_name', 'last_name')


class AttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        fields = '__all__'


class SpeakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speaker
        fields = '__all__'


class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = '__all__'


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'
        
class RoomIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomId
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    speakers = SpeakerSerializer(many=True, read_only=True)
    sponsors = SponsorSerializer(many=True, read_only=True)
    attendees = AttendeeSerializer(many=True, read_only=True)
    schedules = ScheduleSerializer(many=True, read_only=True)
    roomids = RoomIdSerializer(many=True, read_only=True)

    start_date = serializers.DateTimeField(format="%Y-%m-%d %I:%M %p")
    end_date = serializers.DateTimeField(format="%Y-%m-%d %I:%M %p")
    registration_start_date = serializers.DateTimeField(
        format="%Y-%m-%d %I:%M %p")
    registration_end_date = serializers.DateTimeField(
        format="%Y-%m-%d %I:%M %p")

    def get_status(self, obj):
        return obj.status

    class Meta:
        model = Event
        fields = '__all__'
        

class AttendeeRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        fields = ('fullname', 'phone', 'email')
        


class AttendeeLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    event_id = serializers.IntegerField()


class SpeakerRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speaker
        fields = ('fullname', 'organization', 'role')


class SponsorRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = ('name', 'description')


class ScheduleRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ('date', 'start_time', "end_time", "activity")
        
class RoomIdRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomId
        fields = ('roomId',)
        
class VideoUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Videos
        fields = '__all__'
