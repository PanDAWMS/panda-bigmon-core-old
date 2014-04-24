""" 
    api.user.serializers

"""
from rest_framework import serializers
from ...common.models import Users

import logging
_logger = logging.getLogger('bigpandamon')


class SerializerUsers(serializers.ModelSerializer):
    class Meta:
        model = Users
        compulsory_fields = ['name']

    def __init__(self, *args, **kwargs):
        _logger.debug('kwargs=' + str(kwargs))
        many = kwargs.pop('many', True)
        if 'fields' in kwargs:
            self.Meta.fields = kwargs['fields']
        try:
            del kwargs['fields']
        except:
            _logger.error('SerializerUsers __init__ cannot remove fields from kwargs:' + str(kwargs))
        super(SerializerUsers, self).__init__(*args, **kwargs)


    def validate(self, attrs):
        """
            Check that the self.Meta.compulsory_fields are present.
        
        """
        for field in self.Meta.compulsory_fields:
            try:
                if not len(attrs[field]) > 0:
                    raise serializers.ValidationError("%s must not be empty!" % field)
            except KeyError:
                raise serializers.ValidationError("%s must be filled!" % field)
            return attrs


