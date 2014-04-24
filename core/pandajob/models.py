# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from .columns_config import COLUMNS, ORDER_COLUMNS, COL_TITLES, FILTERS


from django.db import models
models.options.DEFAULT_NAMES += ('allColumns', 'orderColumns', \
                                 'primaryColumns', 'secondaryColumns', \
                                 'columnTitles', 'filterFields',)

class PandaJob(models.Model):
    pandaid = models.BigIntegerField(primary_key=True, db_column='PANDAID') # Field name made lowercase.
    jobdefinitionid = models.BigIntegerField(db_column='JOBDEFINITIONID') # Field name made lowercase.
    schedulerid = models.CharField(max_length=384, db_column='SCHEDULERID', blank=True) # Field name made lowercase.
    pilotid = models.CharField(max_length=600, db_column='PILOTID', blank=True) # Field name made lowercase.
    creationtime = models.DateTimeField(db_column='CREATIONTIME') # Field name made lowercase.
    creationhost = models.CharField(max_length=384, db_column='CREATIONHOST', blank=True) # Field name made lowercase.
    modificationtime = models.DateTimeField(db_column='MODIFICATIONTIME') # Field name made lowercase.
    modificationhost = models.CharField(max_length=384, db_column='MODIFICATIONHOST', blank=True) # Field name made lowercase.
    atlasrelease = models.CharField(max_length=192, db_column='ATLASRELEASE', blank=True) # Field name made lowercase.
    transformation = models.CharField(max_length=750, db_column='TRANSFORMATION', blank=True) # Field name made lowercase.
    homepackage = models.CharField(max_length=240, db_column='HOMEPACKAGE', blank=True) # Field name made lowercase.
    prodserieslabel = models.CharField(max_length=60, db_column='PRODSERIESLABEL', blank=True) # Field name made lowercase.
    prodsourcelabel = models.CharField(max_length=60, db_column='PRODSOURCELABEL', blank=True) # Field name made lowercase.
    produserid = models.CharField(max_length=750, db_column='PRODUSERID', blank=True) # Field name made lowercase.
    assignedpriority = models.IntegerField(db_column='ASSIGNEDPRIORITY') # Field name made lowercase.
    currentpriority = models.IntegerField(db_column='CURRENTPRIORITY') # Field name made lowercase.
    attemptnr = models.IntegerField(db_column='ATTEMPTNR') # Field name made lowercase.
    maxattempt = models.IntegerField(db_column='MAXATTEMPT') # Field name made lowercase.
    jobstatus = models.CharField(max_length=45, db_column='JOBSTATUS') # Field name made lowercase.
    jobname = models.CharField(max_length=768, db_column='JOBNAME', blank=True) # Field name made lowercase.
    maxcpucount = models.IntegerField(db_column='MAXCPUCOUNT') # Field name made lowercase.
    maxcpuunit = models.CharField(max_length=96, db_column='MAXCPUUNIT', blank=True) # Field name made lowercase.
    maxdiskcount = models.IntegerField(db_column='MAXDISKCOUNT') # Field name made lowercase.
    maxdiskunit = models.CharField(max_length=12, db_column='MAXDISKUNIT', blank=True) # Field name made lowercase.
    ipconnectivity = models.CharField(max_length=15, db_column='IPCONNECTIVITY', blank=True) # Field name made lowercase.
    minramcount = models.IntegerField(db_column='MINRAMCOUNT') # Field name made lowercase.
    minramunit = models.CharField(max_length=6, db_column='MINRAMUNIT', blank=True) # Field name made lowercase.
    starttime = models.DateTimeField(null=True, db_column='STARTTIME', blank=True) # Field name made lowercase.
    endtime = models.DateTimeField(null=True, db_column='ENDTIME', blank=True) # Field name made lowercase.
    cpuconsumptiontime = models.BigIntegerField(db_column='CPUCONSUMPTIONTIME') # Field name made lowercase.
    cpuconsumptionunit = models.CharField(max_length=384, db_column='CPUCONSUMPTIONUNIT', blank=True) # Field name made lowercase.
    commandtopilot = models.CharField(max_length=750, db_column='COMMANDTOPILOT', blank=True) # Field name made lowercase.
    transexitcode = models.CharField(max_length=384, db_column='TRANSEXITCODE', blank=True) # Field name made lowercase.
    piloterrorcode = models.IntegerField(db_column='PILOTERRORCODE') # Field name made lowercase.
    piloterrordiag = models.CharField(max_length=1500, db_column='PILOTERRORDIAG', blank=True) # Field name made lowercase.
    exeerrorcode = models.IntegerField(db_column='EXEERRORCODE') # Field name made lowercase.
    exeerrordiag = models.CharField(max_length=1500, db_column='EXEERRORDIAG', blank=True) # Field name made lowercase.
    superrorcode = models.IntegerField(db_column='SUPERRORCODE') # Field name made lowercase.
    superrordiag = models.CharField(max_length=750, db_column='SUPERRORDIAG', blank=True) # Field name made lowercase.
    ddmerrorcode = models.IntegerField(db_column='DDMERRORCODE') # Field name made lowercase.
    ddmerrordiag = models.CharField(max_length=1500, db_column='DDMERRORDIAG', blank=True) # Field name made lowercase.
    brokerageerrorcode = models.IntegerField(db_column='BROKERAGEERRORCODE') # Field name made lowercase.
    brokerageerrordiag = models.CharField(max_length=750, db_column='BROKERAGEERRORDIAG', blank=True) # Field name made lowercase.
    jobdispatchererrorcode = models.IntegerField(db_column='JOBDISPATCHERERRORCODE') # Field name made lowercase.
    jobdispatchererrordiag = models.CharField(max_length=750, db_column='JOBDISPATCHERERRORDIAG', blank=True) # Field name made lowercase.
    taskbuffererrorcode = models.IntegerField(db_column='TASKBUFFERERRORCODE') # Field name made lowercase.
    taskbuffererrordiag = models.CharField(max_length=900, db_column='TASKBUFFERERRORDIAG', blank=True) # Field name made lowercase.
    computingsite = models.CharField(max_length=384, db_column='COMPUTINGSITE', blank=True) # Field name made lowercase.
    computingelement = models.CharField(max_length=384, db_column='COMPUTINGELEMENT', blank=True) # Field name made lowercase.
    jobparameters = models.TextField(db_column='JOBPARAMETERS', blank=True) # Field name made lowercase.
    metadata = models.TextField(db_column='METADATA', blank=True) # Field name made lowercase.
    proddblock = models.CharField(max_length=765, db_column='PRODDBLOCK', blank=True) # Field name made lowercase.
    dispatchdblock = models.CharField(max_length=765, db_column='DISPATCHDBLOCK', blank=True) # Field name made lowercase.
    destinationdblock = models.CharField(max_length=765, db_column='DESTINATIONDBLOCK', blank=True) # Field name made lowercase.
    destinationse = models.CharField(max_length=750, db_column='DESTINATIONSE', blank=True) # Field name made lowercase.
    nevents = models.IntegerField(db_column='NEVENTS') # Field name made lowercase.
    grid = models.CharField(max_length=150, db_column='GRID', blank=True) # Field name made lowercase.
    cloud = models.CharField(max_length=150, db_column='CLOUD', blank=True) # Field name made lowercase.
    cpuconversion = models.DecimalField(decimal_places=4, null=True, max_digits=11, db_column='CPUCONVERSION', blank=True) # Field name made lowercase.
    sourcesite = models.CharField(max_length=108, db_column='SOURCESITE', blank=True) # Field name made lowercase.
    destinationsite = models.CharField(max_length=108, db_column='DESTINATIONSITE', blank=True) # Field name made lowercase.
    transfertype = models.CharField(max_length=30, db_column='TRANSFERTYPE', blank=True) # Field name made lowercase.
    taskid = models.IntegerField(null=True, db_column='TASKID', blank=True) # Field name made lowercase.
    cmtconfig = models.CharField(max_length=750, db_column='CMTCONFIG', blank=True) # Field name made lowercase.
    statechangetime = models.DateTimeField(null=True, db_column='STATECHANGETIME', blank=True) # Field name made lowercase.
    proddbupdatetime = models.DateTimeField(null=True, db_column='PRODDBUPDATETIME', blank=True) # Field name made lowercase.
    lockedby = models.CharField(max_length=384, db_column='LOCKEDBY', blank=True) # Field name made lowercase.
    relocationflag = models.IntegerField(null=True, db_column='RELOCATIONFLAG', blank=True) # Field name made lowercase.
    jobexecutionid = models.BigIntegerField(null=True, db_column='JOBEXECUTIONID', blank=True) # Field name made lowercase.
    vo = models.CharField(max_length=48, db_column='VO', blank=True) # Field name made lowercase.
    pilottiming = models.CharField(max_length=300, db_column='PILOTTIMING', blank=True) # Field name made lowercase.
    workinggroup = models.CharField(max_length=60, db_column='WORKINGGROUP', blank=True) # Field name made lowercase.
    processingtype = models.CharField(max_length=192, db_column='PROCESSINGTYPE', blank=True) # Field name made lowercase.
    produsername = models.CharField(max_length=180, db_column='PRODUSERNAME', blank=True) # Field name made lowercase.
    ninputfiles = models.IntegerField(null=True, db_column='NINPUTFILES', blank=True) # Field name made lowercase.
    countrygroup = models.CharField(max_length=60, db_column='COUNTRYGROUP', blank=True) # Field name made lowercase.
    batchid = models.CharField(max_length=240, db_column='BATCHID', blank=True) # Field name made lowercase.
    parentid = models.BigIntegerField(null=True, db_column='PARENTID', blank=True) # Field name made lowercase.
    specialhandling = models.CharField(max_length=240, db_column='SPECIALHANDLING', blank=True) # Field name made lowercase.
    jobsetid = models.BigIntegerField(null=True, db_column='JOBSETID', blank=True) # Field name made lowercase.
    corecount = models.IntegerField(null=True, db_column='CORECOUNT', blank=True) # Field name made lowercase.
    ninputdatafiles = models.IntegerField(null=True, db_column='NINPUTDATAFILES', blank=True) # Field name made lowercase.
    inputfiletype = models.CharField(max_length=96, db_column='INPUTFILETYPE', blank=True) # Field name made lowercase.
    inputfileproject = models.CharField(max_length=192, db_column='INPUTFILEPROJECT', blank=True) # Field name made lowercase.
    inputfilebytes = models.BigIntegerField(null=True, db_column='INPUTFILEBYTES', blank=True) # Field name made lowercase.
    noutputdatafiles = models.IntegerField(null=True, db_column='NOUTPUTDATAFILES', blank=True) # Field name made lowercase.
    outputfilebytes = models.BigIntegerField(null=True, db_column='OUTPUTFILEBYTES', blank=True) # Field name made lowercase.
    jobmetrics = models.CharField(max_length=1500, db_column='JOBMETRICS', blank=True) # Field name made lowercase.
    workqueue_id = models.IntegerField(null=True, db_column='WORKQUEUE_ID', blank=True) # Field name made lowercase.
    jeditaskid = models.BigIntegerField(null=True, db_column='JEDITASKID', blank=True) # Field name made lowercase.

    def __str__(self):
        return 'PanDA:' + str(self.pandaid)

    # __setattr__
    def __setattr__(self, name, value):
        super(PandaJob, self).__setattr__(name, value)

    # __getattr__
    def __getattr__(self, name):
        return super(PandaJob, self).__getattr__(name)

    # __getitem__
    def __getitem__(self, name):
#        return super(HTCondorJob, self).__getattr__(name)
        return self.__dict__[name]

    class Meta:
        abstract = True
        allColumns = COLUMNS['PanDAjob-all']
        primaryColumns = [ \
            'pandaid', 'jobdefinitionid', 'creationtime', 'produserid', \
            'currentpriority', 'jobstatus', 'modificationtime', 'cloud', \
            'destinationsite'
                ]
        secondaryColumns = []
        orderColumns = ORDER_COLUMNS['PanDAjob-all']
        columnTitles = COL_TITLES['PanDAjob-all']
        filterFields = FILTERS['PanDAjob-all']


class Jobsactive4(PandaJob):
    class Meta:
#        managed = False
        db_table = u'jobsactive4'

class Jobsarchived(PandaJob):
#    pandaid = models.BigIntegerField(primary_key=True, db_column='PANDAID')  # Field name made lowercase.
#    modificationtime = models.DateTimeField(primary_key=True, db_column='MODIFICATIONTIME') # Field name made lowercase.
    class Meta:
#        managed = False
        db_table = u'jobsarchived'

class Jobsarchived4(PandaJob):
#    pandaid = models.BigIntegerField(primary_key=True, db_column='PANDAID') # Field name made lowercase.
#    modificationtime = models.DateTimeField(primary_key=True, db_column='MODIFICATIONTIME') # Field name made lowercase.
    class Meta:
#        managed = False
        db_table = u'jobsarchived4'

class Jobsdefined4(PandaJob):
    class Meta:
#        managed = False
        db_table = u'jobsdefined4'


    # __getitem__
    def __getitem__(self, name):
#        return super(HTCondorJob, self).__getattr__(name)
        return self.__dict__[name]


class Jobswaiting4(PandaJob):
    class Meta:
#        managed = False
        db_table = u'jobswaiting4'


