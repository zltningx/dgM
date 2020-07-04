
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet, ViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.utils import timezone

from apps.backend.models import User
from apps.backend.serializers import UserReturnSerializer, UserSerializer
from apps.backend.http import ResponseBody, code
from apps.backend.permissions import IsSuperUser
from apps.utils.decorators import make_response
from apps.utils.pagination import MyPageNumberPagination


class ObtainJWT(ObtainJSONWebToken):
    def post(self, request, *args, **kwargs):
        resp = super(ObtainJWT, self).post(request, *args, **kwargs)
        resp_body = ResponseBody()
        if resp.status_code == status.HTTP_200_OK:
            user_obj = User.objects.get(email=request.data['email'])
            user_obj.last_login = timezone.datetime.now()
            user_obj.save()
            resp_body.code = code.success
            resp_body.data['token'] = resp.data['token']
            resp.data = resp_body
        return resp


@make_response
class AuthManager(ViewSet):
    @action(methods=['post'], detail=False, url_path='info')
    def get_user_info(self, request, *args, **kwargs):
        resp = ResponseBody()
        if request.user:
            user_data = UserReturnSerializer(request.user).data
            resp.code = code.success
            resp.data = user_data
        return resp

    @action(methods=['post'], detail=False, url_path='logout')
    def logout(self, request, *args, **kwargs):
        return ResponseBody()

    @action(methods=['get'], detail=False, url_path='get_transactors')
    def get_transactors(self, request, *args, **kwargs):
        queryset = User.objects.filter(groups__name__in=['审核组'])
        serializer = UserReturnSerializer(queryset, many=True)
        resp = ResponseBody()
        resp.data = serializer.data
        resp.code = code.success
        return resp

    @action(methods=['get'], detail=False, url_path='get_sec_group')
    def get_sec_group(self, request, *args, **kwargs):
        queryset = User.objects.filter(groups__name__in=['安全组'])
        serializer = UserReturnSerializer(queryset, many=True)
        resp = ResponseBody()
        resp.data = serializer.data
        resp.code = code.success
        return resp


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsSuperUser]
    serializer_class = UserSerializer
    pagination_class = MyPageNumberPagination


class UserReadOnlyViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsSuperUser]
    serializer_class = UserReturnSerializer
    pagination_class = MyPageNumberPagination
