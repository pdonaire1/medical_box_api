"""
    Created by: @pdonaire1
    Ing. Pablo Alejandro Gonzalez Donaire
"""
from dry_rest_permissions.generics import DRYPermissions
from rest_framework import filters, status, viewsets
from rest_framework.decorators import detail_route, list_route
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import parsers, renderers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token
from utils.serializers import UserSerializer

class ChangePasswordViewSet(APIView):
    
    def get(self, request, format=None):
        return Response([{
            "message": "fields {old_password, new_password}"}])

    def post(self, request, format=None):
        """
            This function recibe: old_password, new_password
        """
        user = request.user
        old_password = request.data["old_password"]
        new_password = request.data["new_password"]
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(
                [{"message": "password cambiada", "success": True}], 
                status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)


# source: https://github.com/pdonaire1/diccionario_de_comandos/blob/master/Django/create_temporary_token.md
class ResetPasswordViewSet(APIView):
    permission_classes = ()

    def send_forgot_password_email(self, user, email_token):
        template = render_to_string('./email/forgot_password.html',
            {
                'email_token': email_token,
                'username': user.username,
                'url': settings.URL_RECOVER_PASS})
        try:
            subject = "Recuperar usuario @ Mall4G"
            email_to = user.email
            from_email = settings.DEFAULT_FROM_EMAIL
            text_plain = "Hola,\n. Ingrese para recuperar su usuario.\nGracias."
            send_mail(subject, text_plain, from_email, [email_to], html_message=template)
        except: pass

    def send_forgot_password_changed_successfully(self, user):
        template = render_to_string('./email/send_forgot_password_changed_successfully.html',{})
        try:
            subject = "Recuperar usuario @ Mall4G"
            email_to = user.email
            from_email = settings.DEFAULT_FROM_EMAIL
            text_plain = "Hola,\n. Ingrese para recuperar su usuario.\nGracias."
            send_mail(subject, text_plain, from_email, [email_to], html_message=template)
        except: pass

    def get(self, request, format=None):
        username = request.GET.get("username", None)
        if username and User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            # Let's send an email to recover password
            temporary_token = TemporaryToken(user)
            token = Token.objects.get_or_create(user=user)
            token = token[0].key
            email_token = temporary_token.hash_user_encode(
                hours_limit=24, extra_token=token)
            self.send_forgot_password_email(user, email_token)
            return Response([{
                "message": "Un correo ha sido enviado a su usuario",
                "success": True
            }])
        return Response([{
            "POST": "Reset password params: {email_token, new_password, username}",
            "GET": "Send email forgot password params: {username}",
        }])

    def post(self, request, format=None):
        """
            This function recibe: 
            email_token, new_password, username
        """
        email_token = request.data["email_token"]
        new_password = request.data["new_password"]
        username = request.data["username"]
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            temporary_token = TemporaryToken(user)
            token = Token.objects.get(user=user).key
            if temporary_token.hash_user_valid(email_token, extra_token=token):
                user.set_password(new_password)
                user.save()
                self.send_forgot_password_changed_successfully(user)
                return Response(
                    [{"message": "password cambiada", "success": True}], 
                    status=status.HTTP_201_CREATED)

        return Response([{"message": "Token or username error", "success": False}],
            status=status.HTTP_400_BAD_REQUEST)

from doctors.models import Doctor
from patients.models import Patient
class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        user = User.objects.get(id=user.id)
        user_serialized = UserSerializer(user)
        doctor = Doctor.objects.filter(user=user)
        patient = Patient.objects.filter(user=user)

        customer_serlialized = []
        stores_serialized = []
        if (len(doctor) > 0):
            doc = doctor.first()
            doctor_serlialized = {
                "id": doc.id,
                "name": doc.name,
                "phone_number": doc.phone_number,
                "is_active": doc.is_active
            }
        
        if (len(patient) > 0):
            p = patient.first()
            patient_serialized = {
                "id": p.id,
                "phone_number": p.phone_number,
                "address": p.address,
                "is_active": p.is_active
            }
        
        return Response({'token': token.key, 
            'user': user_serialized.data,
            'patient': patient_serialized,
            'doctor': doctor_serlialized
        })