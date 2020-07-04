# -*- coding: utf-8 -*-
# author: zltningx

from rest_framework.serializers import ModelSerializer, ListSerializer

from apps.vulmannager.models import (
    PenetrationTestTicketResult, PenetrationTestTicket, PenetrationTestTicketSubWorkflow)
from apps.vulmannager.serializers.vulnerability_serializers import VulnerabilitySerializer
from apps.backend.serializers import UserReturnSerializer


class PenetrationTestTicketResultSerializer(ModelSerializer):
    tester = UserReturnSerializer(many=False, read_only=True)
    vulnerabilities = VulnerabilitySerializer(many=True, required=False)

    class Meta:
        model = PenetrationTestTicketResult
        fields = '__all__'

    def create(self, validated_data):
        validated_data['tester'] = self.context['request'].user
        if validated_data['vulnerabilities']:
            for i in range(len(validated_data['vulnerabilities'])):
                validated_data['vulnerabilities'][i]['reporter'] = self.context['request'].user
        vulnerabilities_serializer = self.fields['vulnerabilities']
        vulnerabilities_data = validated_data.pop('vulnerabilities')
        vulnerabilities = vulnerabilities_serializer.create(vulnerabilities_data)
        instance = PenetrationTestTicketResult.objects.create(**validated_data)
        instance.vulnerabilities.set(vulnerabilities)
        for v in vulnerabilities:
            v.penetration_test_ticket_result = instance
        instance.save()
        return instance

    def update(self, instance, validated_data):
        """
        不对vulnerabilities更新操作。只可创建。
        :param instance:
        :param validated_data:
        :return:
        """
        validated_data['tester'] = self.context['request'].user
        validated_data.pop('vulnerabilities')
        return super(PenetrationTestTicketResultSerializer, self).update(instance, validated_data)


class PenetrationTestTicketSubWorkflowSerializer(ModelSerializer):
    transactor = UserReturnSerializer(many=False, read_only=True)

    class Meta:
        # list_serializer_class = PenetrationTestTicketSubWorkflowListSerializer
        model = PenetrationTestTicketSubWorkflow
        fields = '__all__'

    def create(self, validated_data):
        validated_data['transactor'] = self.context['request'].user
        instance = super(PenetrationTestTicketSubWorkflowSerializer, self).create(validated_data)
        instance.save()
        return instance


class PenetrationTestTicketSerializer(ModelSerializer):
    ticket_result = PenetrationTestTicketResultSerializer(many=False, required=False, read_only=True)
    creator = UserReturnSerializer(many=False, read_only=True)
    sub_workflow = PenetrationTestTicketSubWorkflowSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = PenetrationTestTicket
        fields = ['id', 'status', 'title', 'priority', 'creator', 'department', 'dead_line',
                  'description', 'create_time', 'transactors', 'ticket_result', 'sub_workflow']

    def create(self, validated_data):
        if validated_data.__contains__('ticket_result'):
            validated_data.pop('ticket_result')
        if validated_data.__contains__('sub_workflow'):
            validated_data.pop('sub_workflow')
        validated_data['creator'] = self.context['request'].user
        instance = super(PenetrationTestTicketSerializer, self).create(validated_data)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        """
        ticket_result。只可创建， creator 不可更改
        :param instance:
        :param validated_data:
        :return:
        """
        if validated_data.__contains__('ticket_result'):
            validated_data.pop('ticket_result')
        if validated_data.__contains__('sub_workflow'):
            validated_data.pop('sub_workflow')
        return super(PenetrationTestTicketSerializer, self).update(instance, validated_data)
