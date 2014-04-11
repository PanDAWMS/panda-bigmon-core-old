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
#        allColumns = [\
#        'pandaid', 'jobdefinitionid', 'schedulerid', 'pilotid', 'creationtime', \
#        'creationhost', 'modificationtime', 'modificationhost', 'atlasrelease', \
#        'transformation', 'homepackage', 'prodserieslabel', 'prodsourcelabel', \
#        'produserid', 'assignedpriority', 'currentpriority', 'attemptnr', \
#        'maxattempt', 'jobstatus', 'jobname', 'maxcpucount', 'maxcpuunit', \
#        'maxdiskcount', 'maxdiskunit', 'ipconnectivity', 'minramcount', \
#        'minramunit', 'starttime', 'endtime', 'cpuconsumptiontime', \
#        'cpuconsumptionunit', 'commandtopilot', 'transexitcode', \
#        'piloterrorcode', 'piloterrordiag', 'exeerrorcode', 'exeerrordiag', \
#        'superrorcode', 'superrordiag', 'ddmerrorcode', 'ddmerrordiag', \
#        'brokerageerrorcode', 'brokerageerrordiag', 'jobdispatchererrorcode', \
#        'jobdispatchererrordiag', 'taskbuffererrorcode', 'taskbuffererrordiag', \
#        'computingsite', 'computingelement', 'jobparameters', 'metadata', \
#        'proddblock', 'dispatchdblock', 'destinationdblock', 'destinationse', \
#        'nevents', 'grid', 'cloud', 'cpuconversion', 'sourcesite', \
#        'destinationsite', 'transfertype', 'taskid', 'cmtconfig', \
#        'statechangetime', 'proddbupdatetime', 'lockedby', 'relocationflag', \
#        'jobexecutionid', 'vo', 'pilottiming', 'workinggroup', 'processingtype', \
#        'produsername', 'ninputfiles', 'countrygroup', 'batchid', 'parentid', \
#        'specialhandling', 'jobsetid', 'corecount', 'ninputdatafiles', \
#        'inputfiletype', 'inputfileproject', 'inputfilebytes', \
#        'noutputdatafiles', 'outputfilebytes', 'jobmetrics', 'workqueue_id', \
#        'jeditaskid'
#            ]
        primaryColumns = [ \
            'pandaid', 'jobdefinitionid', 'creationtime', 'produserid', \
            'currentpriority', 'jobstatus', 'modificationtime', 'cloud', \
            'destinationsite'
                ]
        secondaryColumns = []
        orderColumns = ORDER_COLUMNS['PanDAjob-all']
#        orderColumns = [\
#            'pandaid', 'jobdefinitionid', 'creationtime', 'modificationtime', \
#            'jobstatus', 'currentpriority', 'cloud', \
##            'produserid', 'destinationsite'\
#                ]
        columnTitles = COL_TITLES['PanDAjob-all']
#        columnTitles = [ \
#                        {'sort': True, 'vis': True, 'c': 'pandaid', 't': 'PanDA ID'}, \
#                        {'sort': True, 'vis': True, 'c': 'jobdefinitionid', 't': 'Job Definition ID'}, \
#                        {'sort': True, 'vis': True, 'c': 'creationtime', 't': 'Creation Time'}, \
#                        {'sort': True, 'vis': True, 'c': 'modificationtime', 't': 'Modification Time'}, \
#                        {'sort': True, 'vis': True, 'c': 'jobstatus', 't': 'Job Status'}, \
#                        {'sort': True, 'vis': True, 'c': 'currentpriority', 't': 'Current Priority'}, \
#                        {'sort': True, 'vis': True, 'c': 'cloud', 't': 'Cloud'}, \
#                        {'sort': True, 'vis': False, 'c': 'schedulerid', 't': 'Scheduler ID'}, \
#                        {'sort': True, 'vis': False, 'c': 'pilotid', 't': 'Pilot ID'}, \
#                        {'sort': True, 'vis': False, 'c': 'creationhost', 't': 'Creation Host'}, \
#                        {'sort': True, 'vis': False, 'c': 'modificationhost', 't': 'Modification Host'}, \
#                        {'sort': True, 'vis': False, 'c': 'atlasrelease', 't': 'ATLAS release'}, \
#                        {'sort': True, 'vis': False, 'c': 'transformation', 't': 'Transformation'}, \
#                        {'sort': True, 'vis': False, 'c': 'homepackage', 't': 'Home package'}, \
#                        {'sort': True, 'vis': False, 'c': 'prodserieslabel', 't': 'prodserieslabel'}, \
#                        {'sort': True, 'vis': False, 'c': 'prodsourcelabel', 't': 'prodsourcelabel'}, \
#                        {'sort': True, 'vis': False, 'c': 'produserid', 't': 'Prod User ID'}, \
#                        {'sort': True, 'vis': False, 'c': 'assignedpriority', 't': 'Assigned Priority'}, \
#                        {'sort': True, 'vis': False, 'c': 'attemptnr', 't': 'Attempt #'}, \
#                        {'sort': True, 'vis': False, 'c': 'maxattempt', 't': 'Max Attempt'}, \
#                        {'sort': True, 'vis': False, 'c': 'jobname', 't': 'Job name'}, \
#                        {'sort': True, 'vis': False, 'c': 'maxcpucount', 't': 'Max CPU count'}, \
#                        {'sort': True, 'vis': False, 'c': 'maxcpuunit', 't': 'Unit of Max CPU count'}, \
#                        {'sort': True, 'vis': False, 'c': 'maxdiskcount', 't': 'Max Disk count'}, \
#                        {'sort': True, 'vis': False, 'c': 'maxdiskunit', 't': 'Unit of Max Disk count'}, \
#                        {'sort': True, 'vis': False, 'c': 'ipconnectivity', 't': 'IP Connectivity'}, \
#                        {'sort': True, 'vis': False, 'c': 'minramcount', 't': 'Min RAM count'}, \
#                        {'sort': True, 'vis': False, 'c': 'minramunit', 't': 'Unit of Min RAM count'}, \
#                        {'sort': True, 'vis': False, 'c': 'starttime', 't': 'Start Time'}, \
#                        {'sort': True, 'vis': False, 'c': 'endtime', 't': 'End Time'}, \
#                        {'sort': True, 'vis': False, 'c': 'cpuconsumptiontime', 't': 'CPU Consumption time'}, \
#                        {'sort': True, 'vis': False, 'c': 'cpuconsumptionunit', 't': 'Unit of CPU Consumption time'}, \
#                        {'sort': True, 'vis': False, 'c': 'commandtopilot', 't': 'Command to pilot'}, \
#                        {'sort': True, 'vis': False, 'c': 'transexitcode', 't': 'Trans Exit Code'}, \
#                        {'sort': True, 'vis': False, 'c': 'piloterrorcode', 't': 'Pilot Error Code'}, \
#                        {'sort': True, 'vis': False, 'c': 'piloterrordiag', 't': 'Pilot Error Diag'}, \
#                        {'sort': True, 'vis': False, 'c': 'exeerrorcode', 't': 'Exe Error Code'}, \
#                        {'sort': True, 'vis': False, 'c': 'exeerrordiag', 't': 'Exe Error Diag'}, \
#                        {'sort': True, 'vis': False, 'c': 'superrorcode', 't': 'Sup Error Code'}, \
#                        {'sort': True, 'vis': False, 'c': 'superrordiag', 't': 'Sup Error Diag'}, \
#                        {'sort': True, 'vis': False, 'c': 'ddmerrorcode', 't': 'DDM Error Code'}, \
#                        {'sort': True, 'vis': False, 'c': 'ddmerrordiag', 't': 'DDM Error Diag'}, \
#                        {'sort': True, 'vis': False, 'c': 'brokerageerrorcode', 't': 'Brokerage Error Code'}, \
#                        {'sort': True, 'vis': False, 'c': 'brokerageerrordiag', 't': 'Brokerage Error Diag'}, \
#                        {'sort': True, 'vis': False, 'c': 'jobdispatchererrorcode', 't': 'Job Dispatcher Error Code'}, \
#                        {'sort': True, 'vis': False, 'c': 'jobdispatchererrordiag', 't': 'Job Dispatcher Error Diag'}, \
#                        {'sort': True, 'vis': False, 'c': 'taskbuffererrorcode', 't': 'Taskbuffer Error Code'}, \
#                        {'sort': True, 'vis': False, 'c': 'taskbuffererrordiag', 't': 'Taskbuffer Error Diag'}, \
#                        {'sort': True, 'vis': False, 'c': 'computingsite', 't': 'Computing Site'}, \
#                        {'sort': True, 'vis': False, 'c': 'computingelement', 't': 'Computing Element'}, \
#                        {'sort': True, 'vis': False, 'c': 'jobparameters', 't': 'Job Parameters'}, \
#                        {'sort': True, 'vis': False, 'c': 'metadata', 't': 'Metadata'}, \
#                        {'sort': True, 'vis': False, 'c': 'proddblock', 't': 'proddblock'}, \
#                        {'sort': True, 'vis': False, 'c': 'dispatchdblock', 't': 'dispatchdblock'}, \
#                        {'sort': True, 'vis': False, 'c': 'destinationdblock', 't': 'destinationdblock'}, \
#                        {'sort': True, 'vis': False, 'c': 'destinationse', 't': 'destinationse'}, \
#                        {'sort': True, 'vis': False, 'c': 'nevents', 't': 'N events'}, \
#                        {'sort': True, 'vis': False, 'c': 'grid', 't': 'Grid'}, \
#                        {'sort': True, 'vis': False, 'c': 'cpuconversion', 't': 'CPU Conversion'}, \
#                        {'sort': True, 'vis': False, 'c': 'sourcesite', 't': 'Source Site'}, \
#                        {'sort': True, 'vis': False, 'c': 'destinationsite', 't': 'Destination Site'}, \
#                        {'sort': True, 'vis': False, 'c': 'transfertype', 't': 'Transfer Type'}, \
#                        {'sort': True, 'vis': False, 'c': 'taskid', 't': 'Task ID'}, \
#                        {'sort': True, 'vis': False, 'c': 'cmtconfig', 't': 'CMT config'}, \
#                        {'sort': True, 'vis': False, 'c': 'statechangetime', 't': 'State Change Time'}, \
#                        {'sort': True, 'vis': False, 'c': 'proddbupdatetime', 't': 'Prod DB Update Time'}, \
#                        {'sort': True, 'vis': False, 'c': 'lockedby', 't': 'Locked By'}, \
#                        {'sort': True, 'vis': False, 'c': 'relocationflag', 't': 'Relocation Flag'}, \
#                        {'sort': True, 'vis': False, 'c': 'jobexecutionid', 't': 'Job Execution ID'}, \
#                        {'sort': True, 'vis': False, 'c': 'vo', 't': 'VO'}, \
#                        {'sort': True, 'vis': False, 'c': 'pilottiming', 't': 'Pilot timing'}, \
#                        {'sort': True, 'vis': False, 'c': 'workinggroup', 't': 'Working Group'}, \
#                        {'sort': True, 'vis': False, 'c': 'processingtype', 't': 'Processing Type'}, \
#                        {'sort': True, 'vis': False, 'c': 'produsername', 't': 'Produsername'}, \
#                        {'sort': True, 'vis': False, 'c': 'ninputfiles', 't': 'N input files'}, \
#                        {'sort': True, 'vis': False, 'c': 'countrygroup', 't': 'Country Group'}, \
#                        {'sort': True, 'vis': False, 'c': 'batchid', 't': 'Batch ID'}, \
#                        {'sort': True, 'vis': False, 'c': 'parentid', 't': 'Parent ID'}, \
#                        {'sort': True, 'vis': False, 'c': 'specialhandling', 't': 'Special Handling'}, \
#                        {'sort': True, 'vis': False, 'c': 'jobsetid', 't': 'Jobset ID'}, \
#                        {'sort': True, 'vis': False, 'c': 'corecount', 't': 'Core Count'}, \
#                        {'sort': True, 'vis': False, 'c': 'ninputdatafiles', 't': 'N input data files'}, \
#                        {'sort': True, 'vis': False, 'c': 'inputfiletype', 't': 'Input file type'}, \
#                        {'sort': True, 'vis': False, 'c': 'inputfileproject', 't': 'Input file project'}, \
#                        {'sort': True, 'vis': False, 'c': 'inputfilebytes', 't': 'Input file bytes'}, \
#                        {'sort': True, 'vis': False, 'c': 'noutputdatafiles', 't': 'N output data files'}, \
#                        {'sort': True, 'vis': False, 'c': 'outputfilebytes', 't': 'Output file bytes'}, \
#                        {'sort': True, 'vis': False, 'c': 'jobmetrics', 't': 'Job Metrics'}, \
#                        {'sort': True, 'vis': False, 'c': 'workqueue_id', 't': 'Work queue ID'}, \
#                        {'sort': True, 'vis': False, 'c': 'jeditaskid', 't': 'JEDI Task ID'}, \
#              ]
        filterFields = FILTERS['PanDAjob-all']
#        filterFields = [ \
##            # .starttime
##            { 'name': 'fStartFrom', 'field': 'starttime', 'filterField': 'starttime__gte', 'type': 'datetime' }, \
##            { 'name': 'fStartTo', 'field': 'starttime', 'filterField': 'starttime__lte', 'type': 'datetime'}, \
#            # .creationtime
#            { 'name': 'fCrFrom', 'field': 'creationtime', 'filterField': 'creationtime__gte', 'type': 'datetime' }, \
#            { 'name': 'fCrTo', 'field': 'creationtime', 'filterField': 'creationtime__lte', 'type': 'datetime'}, \
#        ]


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


