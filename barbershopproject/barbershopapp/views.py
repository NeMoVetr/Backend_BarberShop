from datetime import datetime

from rest_framework.exceptions import ValidationError
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView, ListAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Hall, Service, Client, Employee, Visit
from .serializers import HallSerializer, ClientSerializer, ServiceSerializer, EmployeeSerializer, VisitSerializer, \
    UserSerializer, ClientUpdateSerializer, VisitHistorySerializer
from .time_slots import get_time_slots, update_status_visits


# Create your views here.


# функция registration_client
class ClientRegistrationView(CreateAPIView):
    """
    Регистрация нового клиента
    """

    permission_classes = [AllowAny]  # Разрешаем доступ всем пользователям
    serializer_class = ClientSerializer  # Сериализатор для создания клиента

    def perform_create(self, serializer):
        """
        Метод perform_create позволяет вам добавить дополнительную логику
        перед созданием клиента, например, установку каких-то полей.
        """

        user_data = self.request.data.get('user') # Извлекаем данные пользователя
        client_data = self.request.data # Извлекаем данные клиента

        # Валидируем и создаем пользователя через UserSerializer
        user_serializer = UserSerializer(data=user_data)

        if user_serializer.is_valid():
            user = user_serializer.save()  # Сохраняем пользователя

            # Создаем клиента и связываем его с созданным пользователем
            client_data['user'] = user  # Связываем пользователя с клиентом
            serializer.save(user=user)  # Сохраняем клиента

        else:
            raise ValidationError(user_serializer.errors)  # Если ошибки при валидации пользователя, бросаем ошибку


# функция client_update
class ClientUpdateView(RetrieveUpdateAPIView):
    """
    Редактирование профиля клиента.
    Доступно только для авторизованных клиентов.
    """

    serializer_class = ClientUpdateSerializer # Сериализатор для обновления профиля
    permission_classes = [IsAuthenticated] # Разрешаем доступ только для авторизованных клиентов

    def get_object(self):
        """
        Метод get_object для получения объекта клиента.
        """

        return Client.objects.get(user=self.request.user) # Возвращаем объект клиента

    def perform_update(self, serializer):
        """
        Метод perform_update для обновления данных пользователя и клиента.
        """

        # Получаем объект клиента
        client = self.get_object()

        # Получаем данные из запроса для пользователя
        user_data = self.request.data.get('user')

        if user_data:
            # Валидируем и обновляем данные пользователя
            user_serializer = ClientUpdateSerializer(client.user, data=user_data, partial=True)

            if user_serializer.is_valid():
                user_serializer.save()  # Сохраняем пользователя
            else:
                raise ValidationError(user_serializer.errors)  # Если ошибки при валидации


        serializer.save()  # Сохраняем данные клиента


# Функция client_profile
class ClientProfileView(RetrieveAPIView):
    """
    Просмотр профиля клиента.
    Доступно только для авторизованных клиентов.
    """

    permission_classes = [IsAuthenticated] # Разрешаем доступ только для авторизованных клиентов
    serializer_class = ClientSerializer  # Сериализатор для клиента

    def get_object(self):
        """
        Метод get_object для получения объекта клиента.
        """

        return self.request.user.client  # Получаем объект клиента, связанный с текущим пользователем


# Функция employee_show
class EmployeeShowView(ListAPIView):
    """
    Показ всех сотрудников.
    Доступно только для администраторов.
    """

    queryset = Employee.objects.all()  # Указываем queryset для получения всех сотрудников
    serializer_class = EmployeeSerializer  # Указываем сериализатор для сотрудников
    permission_classes = [IsAuthenticated]  # Доступ только для авторизованных пользователей


# Функция hall_show
class HallShowView(ListAPIView):
    """
    Показ всех залов.
    Доступно только для авторизованных пользователей.
    """

    queryset = Hall.objects.all()  # Указываем queryset для получения всех залов
    serializer_class = HallSerializer  # Указываем сериализатор для залов
    permission_classes = [IsAuthenticated]  # Доступ только для авторизованных пользователей


# Функция service_show
class ServiceShowView(ListAPIView):
    """
    Показ всех услуг.
    Доступно только для авторизованных пользователей.
    """

    queryset = Service.objects.all()  # Указываем queryset для получения всех услуг
    serializer_class = ServiceSerializer  # Указываем сериализатор для услуг
    permission_classes = [IsAuthenticated]  # Доступ только для авторизованных пользователей


# Функция book_visit
class BookVisitAPIView(CreateAPIView):
    """
    Регистрация визита для клиента.
    Доступно только для авторизованных клиентов.
    """

    permission_classes = [IsAuthenticated]  # Только аутентифицированные пользователи
    serializer_class = VisitSerializer  # Сериализатор для визитов

    def perform_create(self, serializer):
        """
        Переопределение метода для добавления клиента при создании визита.
        """

        serializer.create(client=self.request.user.client)


# Функция get_available_time
class GetAvailableTimeAPIView(APIView):
    """
    Показ временных слотов для выбранного сотрудника, услуги и даты.
    Доступно только для авторизованных клиентов.
    """

    permission_classes = [IsAuthenticated]  # Только аутентифицированные пользователи

    def get(self, request, *args, **kwargs):
        employee_id = request.query_params.get('employee')  # Получение параметров из запроса
        service_id = request.query_params.get('service')
        date_id = request.query_params.get('date')

        if employee_id and service_id and date_id:
            employee = Employee.objects.get(id=employee_id)  # Поиск сотрудника
            hall = employee.service_halls.filter(service_id=service_id).first().hall  # Поиск зала

            service = Service.objects.get(id=service_id)  # Поиск услуги
            date = datetime.strptime(date_id, '%Y-%m-%d').date()  # Поиск даты

            # Получение доступных временных слотов
            available_time = get_time_slots(hall, service, date)
            return Response(available_time)

        return Response([])


# Функция get_employees_by_service
class GetEmployeesByServiceAPIView(APIView):
    """
    Показ сотрудников по выбранной услуге.
    Доступно только для авторизованных клиентов.
    """

    permission_classes = [IsAuthenticated]  # Только аутентифицированные пользователи

    def get(self, request, *args, **kwargs):
        """
        Метод get для получения списка сотрудников по выбранной услуге.
        """

        service_id = request.query_params.get('service')  # Получение параметров из запроса

        try:
            # Логика получения списка сотрудников
            service = Service.objects.get(id=service_id)
            employees = service.employees.all()

            # Используем сериализатор для сериализации данных сотрудников
            serializer = EmployeeSerializer(employees, many=True)

            return Response(serializer.data)

        except Exception as e:
            return Response({'error': str(e)})


# Функция visit_show_client
class VisitShowClientAPIView(APIView):
    """
    Показ визитов для клиента.
    Доступно только для авторизованных клиентов.
    """

    permission_classes = [IsAuthenticated]  # Доступ только для авторизованных клиентов

    update_status_visits()  # Обновляем статусы

    def get(self, request, *args, **kwargs):
        # Получаем текущего клиента
        client = request.user.client

        # Фильтруем визиты текущего клиента
        visits = Visit.objects.filter(client=client).select_related('employee', 'service')

        # Сериализуем данные
        serializer = VisitHistorySerializer(visits, many=True)

        return Response(serializer.data)


# Функция visit_update_client
class VisitUpdateClient(RetrieveUpdateAPIView):
    """
    Обновление визита для клиента.
    Доступно только для авторизованных клиентов.
    """

    permission_classes = [IsAuthenticated]  # Доступ только для авторизованных клиентов
    queryset = Visit.objects.all()  # Указываем queryset для получения данных
    serializer_class = VisitSerializer  # Указываем сериализатор

    def perform_update(self, serializer):
        """
        Метод perform_update для обновления визита.
        """

        visit = self.get_object()  # Получаем текущий визит

        serializer.update(visit, serializer.validated_data)  # Обновляем визит

        return Response(serializer.data)


# Функция visit_delete_client
class VisitDeleteClient(DestroyAPIView):
    """
    Удаление визита для клиента.
    Доступно только для авторизованных клиентов.
    """

    permission_classes = [IsAuthenticated]  # Доступ только для авторизованных клиентов
    queryset = Visit.objects.all()  # Указываем queryset для получения данных
