from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField, CharField, ValidationError

from .models import Client, Employee, Hall, Service, Visit


class UserSerializer(ModelSerializer):
    password2 = CharField(style={'input_type': 'password'}, write_only=True, label=_('Подтверждение пароля'))
    password = CharField(style={'input_type': 'password'}, write_only=True, label=_('Пароль'))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        """
        Проверка на совпадение паролей
        """

        if attrs['password'] != attrs['password2']:
            raise ValidationError("Пароли не совпадают")
        return attrs

    def create(self, validated_data):
        """
        Создание пользователя
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        return user


class UserUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class ClientSerializer(ModelSerializer):
    user = UserSerializer()  # Используем вложенный сериализатор для отображения данных пользователя

    class Meta:
        model = Client
        fields = ['id', 'user', 'phone_number', 'date_of_birth', 'gender']
        extra_kwargs = {
            'phone_number': {'label': _('Номер телефона')},
            'date_of_birth': {'label': _('Дата рождения')},
            'gender': {'label': _('Пол')},
        }


class ClientUpdateSerializer(ModelSerializer):
    user = UserUpdateSerializer()  # Используем вложенный сериализатор для отображения данных пользователя

    class Meta:
        model = Client
        fields = ['id', 'user', 'phone_number', 'date_of_birth', 'gender']

    def update(self, instance, validated_data):
        """
        Переопределяем метод update для обновления данных клиента и пользователя.
        """

        # Извлекаем данные для вложенного пользователя
        user_data = validated_data.pop('user', None)

        # Обновляем данные пользователя, если они переданы
        if user_data:
            user_serializer = UserUpdateSerializer(instance.user, data=user_data,
                                                   partial=True)  # partial - чтобы не обновлять пароль
            if user_serializer.is_valid(
                    raise_exception=True):  # Валидируем и обновляем пользователя. raise_exception - принудительная ошибка
                user_serializer.save()

        # Обновляем остальные поля клиента
        for attr, value in validated_data.items():
            setattr(instance, attr, value)  # setattr - установить атрибут

        instance.save()
        return instance


class HallSerializer(ModelSerializer):
    # Добавляем сериализатор для отображения времени начала и окончания зала
    start_time = SerializerMethodField()
    end_time = SerializerMethodField()

    class Meta:
        model = Hall
        fields = ['id', 'name', 'description', 'capacity', 'location', 'start_time', 'end_time']

    def get_start_time(self, obj):
        """
        Добавляем сериализатор для отображения времени начала работы зала
        """

        return obj.start_time.strftime('%H:%M')

    def get_end_time(self, obj):
        """
        Добавляем сериализатор для отображения времени окончания работы зала
        """

        return obj.end_time.strftime('%H:%M')


class ServiceSerializer(ModelSerializer):
    duration = SerializerMethodField()  # Добавляем сериализатор для отображения продолжительности услуги

    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'price', 'duration']

    def get_duration(self, obj):
        """
        Добавляем сериализатор для отображения продолжительности услуги
        """

        return obj.duration.strftime('%H:%M')


class EmployeeSerializer(ModelSerializer):
    user = UserSerializer()  # Сериализуем данные пользователя
    halls = HallSerializer(many=True)  # Сериализуем список залов
    services = ServiceSerializer(many=True)  # Сериализуем список услуг

    class Meta:
        model = Employee
        fields = ['id', 'user', 'phone_number', 'position', 'halls', 'services']


class VisitHistorySerializer(ModelSerializer):
    employee_name = SerializerMethodField()  # Добавляем сериализатор для отображения имени сотрудника
    employee_phone = SerializerMethodField()  # Добавляем сериализатор для отображения номера телефона сотрудника
    service_price = SerializerMethodField()  # Добавляем сериализатор для отображения цены услуги
    service_name = SerializerMethodField()  # Добавляем сериализатор для отображения названия услуги
    date_time = SerializerMethodField()  # Добавляем сериализатор для отображения даты и времени

    class Meta:
        model = Visit
        fields = ['id', 'employee_name', 'employee_phone', 'service_name', 'service_price', 'date_time', 'status']

    def get_employee_name(self, obj):
        """
        Добавляем сериализатор для отображения имени сотрудника
        """

        return f"{obj.employee.user.first_name} {obj.employee.user.last_name}"

    def get_employee_phone(self, obj):
        """
        Добавляем сериализатор для отображения номера телефона сотрудника
        """

        return obj.employee.phone_number

    def get_service_price(self, obj):
        """
        Добавляем сериализатор для отображения цены услуги
        """

        return obj.service.price

    def get_service_name(self, obj):
        """
        Добавляем сериализатор для отображения названия услуги
        """

        return obj.service.name

    def get_date_time(self, obj):
        """
        Добавляем сериализатор для отображения даты и времени
        """

        return f"{obj.date} {obj.time.strftime('%H:%M')}"


class VisitSerializer(ModelSerializer):
    employee = PrimaryKeyRelatedField(queryset=Employee.objects.all())  # Сериализуем данные сотрудника
    service = PrimaryKeyRelatedField(queryset=Service.objects.all())  # Сериализуем данные услуги
    client = PrimaryKeyRelatedField(queryset=Client.objects.all(), required=False,
                                    default=None)  # Сериализуем данные клиента

    class Meta:
        model = Visit
        fields = ['employee', 'service', 'date', 'time', 'client']

    def validate(self, attrs):
        """
        Проверка переполненности зала при валидации данных
        """

        employee = attrs.get('employee')  # Получаем данные сотрудника
        service = attrs.get('service')  # Получаем данные услуги
        date = attrs.get('date')  # Получаем данные даты
        time = attrs.get('time')  # Получаем данные времени

        if employee and service and date and time:
            # Найти доступные залы для сотрудника
            service_hall = employee.service_halls.filter(service=service).first()

            hall = service_hall.hall  # Найти зал
            existing_visits = Visit.objects.filter(hall=hall, date=date, time=time)  # Найти существующие визиты

            # Проверка переполненности зала
            if existing_visits.count() >= hall.capacity:
                raise ValidationError("Зал переполнен на выбранное время.")

            attrs['hall'] = hall  # Устанавливаем автоматически зал

        return attrs

    def create(self, client=None, commit=True):
        """
        Переопределяем сохранение формы, чтобы автоматически устанавливать зал и проверять переполненность зала
        """

        validated_data = self.validated_data  # Получаем данные валидированных данных
        employee = validated_data.get('employee')  # Получаем данные сотрудника
        service = validated_data.get('service')  # Получаем данные услуги
        date = validated_data.get('date')  # Получаем данные даты
        time = validated_data.get('time')  # Получаем данные времени

        # Создание визита с учетом зала
        visit = Visit.objects.create(
            employee=employee,
            service=service,
            date=date,
            time=time,
            hall=validated_data.get('hall'),
            client=client
        )

        return visit

    def update(self, instance, validated_data):
        """
        Обновляем существующий визит
        """

        # Обновляем поля визита
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Сохраняем обновленный визит
        instance.save()
        return instance
