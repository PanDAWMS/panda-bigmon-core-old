# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models
models.options.DEFAULT_NAMES += ('allColumns', 'orderColumns', \
                                 'primaryColumns', 'secondaryColumns', \
                                 'columnTitles', 'filterFields')


class HTCondorJob(models.Model):
    wmsid = models.BigIntegerField(primary_key=True)
    globaljobid = models.CharField(max_length=300, primary_key=True, db_column='GlobalJobId')
    condorid = models.CharField(max_length=300, db_column='CondorID', blank=True)
    owner = models.CharField(max_length=180, db_column='OWNER', blank=True)
    submitted = models.DateTimeField(null=True, db_column='SUBMITTED', blank=True)
    run_time = models.IntegerField(null=True, db_column='RUN_TIME', blank=True)
    p_end_time = models.DateTimeField(null=True, db_column='P_END_TIME', blank=True)
    st = models.CharField(max_length=3, db_column='ST', blank=True)
    pri = models.IntegerField(null=True, db_column='PRI', blank=True)
    size = models.DecimalField(decimal_places=1, null=True, max_digits=12, db_column='SIZE', blank=True)
    cmd = models.CharField(max_length=300, db_column='CMD', blank=True)
    host = models.CharField(max_length=360, db_column='HOST', blank=True)
    status = models.CharField(max_length=33, db_column='STATUS', blank=True)
    manager = models.CharField(max_length=180, db_column='MANAGER', blank=True)
    executable = models.CharField(max_length=300, db_column='EXECUTABLE', blank=True)
    goodput = models.CharField(max_length=15, db_column='GOODPUT', blank=True)
    cpu_util = models.CharField(max_length=18, db_column='CPU_UTIL', blank=True)
    mbps = models.DecimalField(decimal_places=1, null=True, max_digits=12, db_column='MBPS', blank=True)
    read_ = models.BigIntegerField(null=True, db_column='READ_', blank=True)
    write_ = models.BigIntegerField(null=True, db_column='WRITE_', blank=True)
    seek = models.BigIntegerField(null=True, db_column='SEEK', blank=True)
    xput = models.DecimalField(decimal_places=1, null=True, max_digits=12, db_column='XPUT', blank=True)
    bufsize = models.BigIntegerField(null=True, db_column='BUFSIZE', blank=True)
    blocksize = models.IntegerField(null=True, db_column='BLOCKSIZE', blank=True)
    cpu_time = models.IntegerField(null=True, db_column='CPU_TIME', blank=True)
    removed = models.IntegerField(null=True, db_column='REMOVED', blank=True)
    p_start_time = models.DateTimeField(null=True, db_column='P_START_TIME', blank=True)
    p_modif_time = models.DateTimeField(null=True, db_column='P_MODIF_TIME', blank=True)
    p_factory = models.CharField(max_length=180, db_column='P_FACTORY', blank=True)
    p_schedd = models.CharField(max_length=180, db_column='P_SCHEDD', blank=True)
    p_description = models.CharField(max_length=300, db_column='P_DESCRIPTION', blank=True)
    p_stdout = models.CharField(max_length=765, db_column='P_STDOUT', blank=True)
    p_stderr = models.CharField(max_length=765, db_column='P_STDERR', blank=True)


    class Meta:
        db_table = u'jobshtcondor'
        unique_together = ("wmsid", "globaljobid")
        allColumns = [\
            'owner', 'wmsid', 'globaljobid', 'condorid', 'submitted', \
            'run_time', 'st', 'pri', 'size', 'cmd', 'host', 'status', \
            'manager', 'executable', 'goodput', 'cpu_util', 'mbps', 'read_', \
            'write_', 'seek', 'xput', 'bufsize', 'blocksize', 'cpu_time', \
            'p_start_time', 'p_end_time', 'p_modif_time', 'p_factory', \
            'p_schedd', 'p_description', 'p_stdout', 'p_stderr' \
        ]
        primaryColumns = [ \
            'owner', 'wmsid', 'globaljobid', 'submitted', \
            'run_time', 'st', 'status', 'pri', \
        ]
        secondaryColumns = [\
            'condorid', 'size', 'cmd', 'host', \
            'manager', 'executable', 'goodput', 'cpu_util', 'mbps', 'read_', \
            'write_', 'seek', 'xput', 'bufsize', 'blocksize', 'cpu_time', \
            'p_start_time', 'p_end_time', 'p_modif_time', 'p_factory', \
            'p_schedd', 'p_description', 'p_stdout', 'p_stderr' \
        ]
        orderColumns = [\
            'owner', 'wmsid', 'globaljobid', 'submitted', 'run_time', 'st', \
            'status', 'pri', \
#            'condorid', 'size', 'cmd', 'host', \
#            'manager', 'executable', 'goodput', 'cpu_util', 'mbps', 'read_', \
#            'write_', 'seek', 'xput', 'bufsize', 'blocksize', 'cpu_time', \
#            'p_start_time', 'p_end_time', 'p_modif_time', 'p_factory', \
#            'p_schedd', \
        ]
        columnTitles = [ \
                {'c': 'owner', 't': "Owner", 'sort': True, "vis": True}, \
                {'c': 'wmsid', 't': 'WMS ID', 'sort': True, "vis": True}, \
                {'c': 'globaljobid', 't': 'Global Job ID', 'sort': True, "vis": True}, \
                {'c': 'submitted', 't': 'Submitted', 'sort': True, "vis": True}, \
                {'c': 'run_time', 't': 'Run time', 'sort': False, "vis": True}, \
                {'c': 'st', 't': 'Status', 'sort': True, "vis": True}, \
                {'c': 'status', 't': 'Guessed status', 'sort': True, "vis": True}, \
                {'c': 'pri', 't': 'Priority', 'sort': True, "vis": True}, \
                {'c': 'condorid', 't': 'Condor ID', 'sort': False, "vis": False}, \
                {'c': 'size', 't': 'size', 'sort': False, "vis": False}, \
                {'c': 'cmd', 't': 'Command', 'sort': False, "vis": False}, \
                {'c': 'host', 't': 'host', 'sort': False, "vis": False}, \
                {'c': 'manager', 't': 'manager', 'sort': True, "vis": False}, \
                {'c': 'executable', 't': 'executable', 'sort': True, "vis": False}, \
                {'c': 'goodput', 't': 'goodput', 'sort': False, "vis": False}, \
                {'c': 'cpu_util', 't': 'cpu_util', 'sort': False, "vis": False}, \
                {'c': 'mbps', 't': 'mbps', 'sort': False, "vis": False}, \
                {'c': 'read_', 't': 'read_', 'sort': False, "vis": False}, \
                {'c': 'write_', 't': 'write_', 'sort': False, "vis": False}, \
                {'c': 'seek', 't': 'seek', 'sort': False, "vis": False}, \
                {'c': 'xput', 't': 'xput', 'sort': False, "vis": False}, \
                {'c': 'bufsize', 't': 'bufsize', 'sort': False, "vis": False}, \
                {'c': 'blocksize', 't': 'blocksize', 'sort': False, "vis": False}, \
                {'c': 'cpu_time', 't': 'cpu_time', 'sort': False, "vis": False}, \
                {'c': 'p_start_time', 't': 'p_start_time', 'sort': False, "vis": False}, \
                {'c': 'p_end_time', 't': 'p_end_time', 'sort': False, "vis": False}, \
                {'c': 'p_modif_time', 't': 'p_modif_time', 'sort': False, "vis": False}, \
                {'c': 'p_factory', 't': 'p_factory', 'sort': False, "vis": False}, \
                {'c': 'p_schedd', 't': 'p_schedd', 'sort': False, "vis": False}, \
                {'c': 'p_description', 't': 'p_description', 'sort': False, "vis": False}, \
                {'c': 'p_stdout', 't': 'p_stdout', 'sort': False, "vis": False}, \
                {'c': 'p_stderr', 't': 'p_stderr', 'sort': False, "vis": False} \
        ]
        filterFields = [ \
            # .owner
            { 'name': 'fOwn', 'field': 'owner', 'filterField': 'owner', 'type': 'string' }, \
            # .wmsid
            { 'name': 'fWmsId', 'field': 'wmsid', 'filterField': 'wmsid', 'type': 'integer' }, \
            # .globaljobid
            { 'name': 'fGlJobId', 'field': 'globaljobid', 'filterField': 'globaljobid', 'type': 'string' }, \
            # .submitted
            { 'name': 'fSubFrom', 'field': 'submitted', 'filterField': 'submitted__gte', 'type': 'datetime' }, \
            { 'name': 'fSubTo', 'field': 'submitted', 'filterField': 'submitted__lte', 'type': 'datetime'}, \
            # .run_time
            { 'name': 'fRunT', 'field': 'run_time', 'filterField': 'run_time', 'type': 'integer' }, \
            # .st
            { 'name': 'fSt', 'field': 'st', 'filterField': 'st', 'type': 'stringMultiple' }, \
            # .status
            { 'name': 'fStatus', 'field': 'status', 'filterField': 'status', 'type': 'stringMultiple' }, \
            # .pri
            { 'name': 'fPri', 'field': 'pri', 'filterField': 'pri', 'type': 'integer' }, \
        ]


    def __str__(self):
        return 'HTCondorJob:' + str(self.globaljobid)


    # __getitem__
    def __getitem__(self, name):
#        return super(HTCondorJob, self).__getattr__(name)
        return self.__dict__[name]
