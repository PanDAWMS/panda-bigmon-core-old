""" 
htcondorapi.serializers

"""
from rest_framework import serializers
from ...htcondor.models import HTCondorJob


class SerializerHTCondorJob(serializers.ModelSerializer):
    class Meta:
        model = HTCondorJob
        compulsory_fields = ['globaljobid', 'wmsid']
#        datetime_fields = []

    def __init__(self, *args, **kwargs):
#        many = kwargs.pop('many', True)
        self.many = kwargs.pop('many', True)
        super(SerializerHTCondorJob, self).__init__(*args, **kwargs)

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

#    wmsid = serializers.IntegerField
#    globaljobid = serializers.CharField()
#    condorid = serializers.CharField()
#    owner = serializers.CharField()
#    submitted = serializers.DateTimeField()
#    run_time = serializers.IntegerField()
#    p_end_time = serializers.DateTimeField()
#    st = serializers.CharField()
#    pri = serializers.IntegerField()
#    size = serializers.DecimalField()
#    cmd = serializers.CharField()
#    host = serializers.CharField()
#    status = serializers.CharField()
#    manager = serializers.CharField()
#    executable = serializers.CharField()
#    goodput = serializers.CharField()
#    cpu_util = serializers.CharField()
#    mbps = serializers.DecimalField()
#    read_ = serializers.IntegerField()
#    write_ = serializers.IntegerField()
#    seek = serializers.IntegerField()
#    xput = serializers.DecimalField()
#    bufsize = serializers.IntegerField()
#    blocksize = serializers.IntegerField()
#    cpu_time = serializers.IntegerField()
#    removed = serializers.IntegerField()
#    p_start_time = serializers.DateTimeField()
#    p_modif_time = serializers.DateTimeField()
#    p_factory = serializers.CharField()
#    p_schedd = serializers.CharField()
#    p_description = serializers.CharField()
#    p_stdout = serializers.CharField()
#    p_stderr = serializers.CharField()

