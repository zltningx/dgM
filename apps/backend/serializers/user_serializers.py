# -*- coding: utf-8 -*-
# author: zltningx

from rest_framework.serializers import ModelSerializer, SerializerMethodField

from apps.backend.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'is_superuser',
            'phone', 'full_name', 'user_id', 'avatar'
        ]


class UserReturnSerializer(ModelSerializer):

    role = SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'full_name', 'user_id', 'avatar', 'role']

    def get_role(self, obj):
        if obj.is_superuser:
            return 'superuser'
        elif obj.groups.filter(name__in=['审核组']).exists():
            return 'reviewer'
        elif obj.groups.filter(name__in=['安全组']).exists():
            return 'tester'
        else:
            return 'user'

