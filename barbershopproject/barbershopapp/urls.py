from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import ClientRegistrationView, ClientUpdateView, ClientProfileView, EmployeeShowView, HallShowView, \
    ServiceShowView, BookVisitAPIView, GetAvailableTimeAPIView, VisitShowClientAPIView, VisitUpdateClient, \
    VisitDeleteClient, GetEmployeesByServiceAPIView

urlpatterns = [

    path('api-token-auth/', obtain_auth_token),

    # Регистрация клиентов
    path('registration/client/', ClientRegistrationView.as_view(), name='registration_client'),

    # Обновление профиля клиента и сотрудника
    path('client/update/', ClientUpdateView.as_view(), name='client_update'),

    # Профили клиента и сотрудника
    path('client/profile/', ClientProfileView.as_view(), name='client_profile'),

    # Управление сотрудниками
    path('employee/show/', EmployeeShowView.as_view(), name='employee_show'),

    # Управление залами
    path('hall/show/', HallShowView.as_view(), name='hall_show'),

    # Управление услугами
    path('service/show/', ServiceShowView.as_view(), name='service_show'),

    # Бронирование посещений
    path('book/visit/', BookVisitAPIView.as_view(), name='book_visit'),
    path('visit/show/client/', VisitShowClientAPIView.as_view(), name='visit_show_client'),

    # Обновление и удаление визитов
    path('visits/<int:pk>/update/', VisitUpdateClient.as_view(), name='visit_update_client'),
    path('visit/<int:pk>/delete/', VisitDeleteClient.as_view(), name='visit_delete_client'),

    # Получение доступного времени для посещений
    path('get_available_time/', GetAvailableTimeAPIView.as_view(), name='get_available_time'),
    path('get_employee_for_service/', GetEmployeesByServiceAPIView.as_view(), name='get_employee_for_service')

]
