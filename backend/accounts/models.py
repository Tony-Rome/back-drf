from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

#writer = settings.AUTH_USER_MODEL
'''
    Por defecto las tablas se llman: nombre_app.nombre_modelo.
        ej: accounts.comment
'''


class WriterManager(BaseUserManager):

    def create_user(self, email, first_name, last_name, password=None,
                    web_site=None, signing=None,
                    ):
        if not email:
            raise ValueError("Debe ingresar email valido")
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            web_site=web_site,
            signing=signing,
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, first_name, last_name, password):
        user = self.create_user(email, first_name=first_name, last_name=last_name, password=password)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class Writer(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True, null=False, blank=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    web_site = models.CharField(max_length=255, null=True, blank=True)
    signing = models.CharField(max_length=255, null=True, blank=True)
    writer_level = models.PositiveIntegerField(default=0, blank=True)  # Al tener default se ignora al crear writer
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, auto_now=False)
    '''
        auto_create = 
        auto_now_add = registra solo la 1ra vez
        auto_now = actualiza el campo
    '''

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = WriterManager()

    USERNAME_FIELD = 'email'  # PK
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        db_table = 'writer'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def has_perm(self, perm, obj=None):
        '''
            Exclusivo para verificar cierto permiso
        '''
        return True

    def has_module_perms(self, app_label):
        '''
            Exclusivo para verificar cierta accion
        '''
        return True

    @property
    def writer_level(self):
        return self.writer_level


class Collaborator(models.Model):
    '''
        Modelo para conectar tablas Many to Many
    '''

    writer = models.ForeignKey('writer', on_delete=models.CASCADE)
    range = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'collaborator'

    def __str__(self):
        return f"Collaborator: {self.writer} - {self.timestamp}"


class Comment(models.Model):

    writer = models.ForeignKey('writer', on_delete=models.CASCADE)
    reply = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    type_post = models.CharField(max_length=255, null=True, blank=True)
    type_id = models.PositiveIntegerField(null=True, blank=True)
    content = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'comment'

    def __str__(self):
        return f"Author: {self.writer} - {self.type_id} {self.type_post}"


class Decision(models.Model):

    writer = models.ForeignKey('writer', on_delete=models.CASCADE)
    state = models.BooleanField(null=True, blank=True)
    type_post = models.CharField(max_length=255, null=True, blank=True)
    type_id = models.PositiveIntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'decision'

    def __str__(self):
        return f"Decision: {self.writer} {self.state} {self.type_id} {self.type_post}"
        

