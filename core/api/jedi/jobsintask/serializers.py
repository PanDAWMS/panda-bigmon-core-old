""" 
api.jedi.jobsintask.serializers

"""
from rest_framework import serializers
from ....pandajob.models import PandaJob


class SerializerPandaJob(serializers.ModelSerializer):
    class Meta:
        model = PandaJob
        compulsory_fields = ['pandaid']

    def __init__(self, *args, **kwargs):
        many = kwargs.pop('many', True)
        super(SerializerPandaJob, self).__init__(*args, **kwargs)

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

