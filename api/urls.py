from django.urls import path, include
from rest_framework.routers import DefaultRouter


# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView
)


from . import views

router = DefaultRouter()
# router.register(r'/', )
router.register(r'attendees', views.AttendeeViewSet)
router.register(r'events', views.EventViewSet)
router.register(r'speakers', views.SpeakerViewSet)
router.register(r'sponsors', views.SponsorViewSet)
# router.register(r'users', views.UserViewSet)
router.register(r'eventusers', views.EventUSers)
router.register(r'roomid', views.RoomIdViewSet)
router.register(r'videos', views.uploadsViewset)


urlpatterns = [
    path('', include(router.urls)),
    
    path('token/', views.MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    
    path('register/', views.EventUserRegisterView.as_view(), name='user-register'),
    path('login/', views.EventUserLoginView.as_view(), name='user-login'),
#     path('login/', views.LoginView.as_view(), name='user-login'),
    path('users/<int:user_id>/', views.EventUsersById.as_view(), name='get_user_by_id'),
    
    
#     path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('event/register/', views.EventRegistrationView.as_view(), 
         name='event-registration'),
    
    path('attendee/register/', views.AttendeeRegistrationView.as_view(),
         name='attendee-registration'),
    
    path('attendee/login',  views.AttendeeLoginView.as_view(), name='attendee-login'),
    
    path('speaker/register/', views.SpeakerRegistrationView.as_view(),
         name='speaker-registration'),

    path('sponsor/register/', views.SponsorRegistrationView.as_view(),
         name='sponsor-registration'),

    path('schedule/register/', views.ScheduleRegistrationView.as_view(),
         name='schedule-registration'),
    
    path('roomId/register/', views.RoomIdRegistrationView.as_view(),
         name='roomid-registration'),
    
    path('send_mails/', views.SendMail.as_view(),
         name='mail'),
    
    path('send_test_email/', views.SendTestEmailView.as_view(),
         name='test_mail'),
    
    
    
    path('videos/upload', views.VideoUpload.as_view(), name='upload_videos'),
    

#     path('users/<int:pk>/',
#          views.UserViewSet.as_view({'get': 'retrieve'}), name='user-detail'),


    path('download-attendees-pdf/<int:event_id>/',
         views.AttendeesPDFDownload.as_view(), name='download-attendees-pdf'),
    
    path('download-event-report-pdf/<int:event_id>/',
         
         views.EventReportPDFDownload.as_view(), name='download-event-report-pdf'),
    path('download-event-schedule-pdf/<int:event_id>/',
         
         views.SchedulePDFDownload.as_view(), name='download-event-schedule-pdf'),
]
