""" 
api.jedi.jobsintask.serializers

"""
from rest_framework import serializers
from ....pandajob.models import PandaJob

import logging
_logger = logging.getLogger('bigpandamon')


class SerializerPandaJob(serializers.ModelSerializer):
    class Meta:
        model = PandaJob
        compulsory_fields = ['pandaid']

    def __init__(self, *args, **kwargs):
        many = kwargs.pop('many', True)
#        _logger.debug('SerializerPandaJob.Meta.__dict__=' + str(self.Meta.__dict__))
        if 'fields' in kwargs:
#            _logger.debug('SerializerPandaJob __init__ kwargs=' + str(kwargs))
            self.Meta.fields = kwargs['fields']
#        _logger.debug('SerializerPandaJob.Meta.__dict__=' + str(self.Meta.__dict__))
        try:
            del kwargs['fields']
        except:
            _logger.error('SerializerPandaJob __init__ cannot remove fields from kwargs:' + str(kwargs))
        super(SerializerPandaJob, self).__init__(*args, **kwargs)
#        _logger.debug('SerializerPandaJob.Meta.__dict__=' + str(self.Meta.__dict__))


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


