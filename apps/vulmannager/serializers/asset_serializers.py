# -*- coding: utf-8 -*-
# author: zltningx

from rest_framework.serializers import ModelSerializer, ListSerializer

from apps.vulmannager.models import Asset, Port


class PortListSerializer(ListSerializer):
    def create(self, validated_data):
        ports = []
        for item in validated_data:
            v = Port.objects.create(**item)
            ports.append(v)
        return ports


class PortSerializer(ModelSerializer):

    class Meta:
        list_serializer_class = PortListSerializer
        model = Port
        fields = '__all__'


class AssetSerializer(ModelSerializer):
    ports = PortSerializer(many=True, required=False)

    class Meta:
        model = Asset
        fields = ('id', 'name', 'domain', 'ip', 'pics', 'info', 'ports',
                  'create_time', 'update_time')

    def create(self, validated_data):
        # if validated_data['vulnerabilities']:
        #     for i in range(len(validated_data['ports'])):
        #         validated_data['ports'][i]['reporter'] = self.context['request'].user
        ports_serializer = self.fields['ports']
        ports_data = validated_data.pop('ports')
        ports = ports_serializer.create(ports_data)
        instance = super(AssetSerializer, self).create(validated_data)
        instance.ports.set(ports)
        for p in ports:
            p.asset = instance
        instance.save()
        return instance

    def update(self, instance, validated_data):
        """
        不对ports更新操作。只可创建。
        :param instance:
        :param validated_data:
        :return:
        """
        validated_data.pop('ports')
        return super(AssetSerializer, self).update(instance, validated_data)
