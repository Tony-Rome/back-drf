from django.contrib.auth import authenticate, get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token

Writer = get_user_model()

'''
    Decorador para obtener:
        - PK
        - Password
        - Token
    Si tiene los tres atributos, se autentica y se entrega respuesta.
'''

class CustomAuth():

    def __init__(self, request, *args, **kwargs):
        print("ENTRO A INIT")
        self.request = request
        print(request)

    def __call__(self, func):

        def wrapper(obj, *args, **kwargs):
            print("ENTO A WRAPPER")
            print(obj)
            print(args)
            print(kwargs)
            f = func(obj, *args, **kwargs)
            return f


        return wrapper


def custom_auth_writer(function):

    def decorator(obj, request):
        user = request.user
        if user.is_anonymous:
            raise ValueError("Acceso denegado")
        elif user.auth_token:
            key = user.auth_token.key
            email = request.data.get('email')
            try:
                writer = Writer.objects.get(email=email)
                token = Token.objects.filter(user_id=writer.id).first()  # Obtiene primero de la queeryset a obj
                if token.key == key:
                    return function(self=obj, request=request)
                raise ValueError
            except:
                raise ValueError("Acceso denegado token")

        raise ValueError("Acceso denegado usuario")

    return decorator

