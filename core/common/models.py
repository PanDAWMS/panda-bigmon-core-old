# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from __future__ import unicode_literals

from ..pandajob.columns_config import COLUMNS, ORDER_COLUMNS, COL_TITLES, FILTERS


from django.db import models
models.options.DEFAULT_NAMES += ('allColumns', 'orderColumns', \
                                 'primaryColumns', 'secondaryColumns', \
                                 'columnTitles', 'filterFields',)

class Cache(models.Model):
#    type = models.CharField(max_length=750, primary_key=True, db_column='TYPE') # Field name made lowercase.
#    value = models.CharField(max_length=750, primary_key=True, db_column='VALUE') # Field name made lowercase.
#    qurl = models.CharField(max_length=750, db_column='QURL') # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=250)  # Field name made lowercase.
    value = models.CharField(db_column='VALUE', max_length=250)  # Field name made lowercase.
    qurl = models.CharField(db_column='QURL', max_length=250)  # Field name made lowercase.
    modtime = models.DateTimeField(db_column='MODTIME') # Field name made lowercase.
    usetime = models.DateTimeField(db_column='USETIME') # Field name made lowercase.
    updmin = models.IntegerField(null=True, db_column='UPDMIN', blank=True) # Field name made lowercase.
    data = models.TextField(db_column='DATA', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'cache'

class Certificates(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    cert = models.CharField(max_length=12000, db_column='CERT') # Field name made lowercase.
    class Meta:
        db_table = u'certificates'

class Classlist(models.Model):
    class_field = models.CharField(max_length=90, primary_key=True, db_column='CLASS') # Field name made lowercase. Field renamed because it was a Python reserved word.
    name = models.CharField(max_length=180, primary_key=True, db_column='NAME') # Field name made lowercase.
    rights = models.CharField(max_length=90, db_column='RIGHTS') # Field name made lowercase.
    priority = models.IntegerField(null=True, db_column='PRIORITY', blank=True) # Field name made lowercase.
    quota1 = models.BigIntegerField(null=True, db_column='QUOTA1', blank=True) # Field name made lowercase.
    quota7 = models.BigIntegerField(null=True, db_column='QUOTA7', blank=True) # Field name made lowercase.
    quota30 = models.BigIntegerField(null=True, db_column='QUOTA30', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'classlist'

class Cloudconfig(models.Model):
    name = models.CharField(max_length=60, primary_key=True, db_column='NAME') # Field name made lowercase.
    description = models.CharField(max_length=150, db_column='DESCRIPTION') # Field name made lowercase.
    tier1 = models.CharField(max_length=60, db_column='TIER1') # Field name made lowercase.
    tier1se = models.CharField(max_length=1200, db_column='TIER1SE') # Field name made lowercase.
    relocation = models.CharField(max_length=30, db_column='RELOCATION', blank=True) # Field name made lowercase.
    weight = models.IntegerField(db_column='WEIGHT') # Field name made lowercase.
    server = models.CharField(max_length=300, db_column='SERVER') # Field name made lowercase.
    status = models.CharField(max_length=60, db_column='STATUS') # Field name made lowercase.
    transtimelo = models.IntegerField(db_column='TRANSTIMELO') # Field name made lowercase.
    transtimehi = models.IntegerField(db_column='TRANSTIMEHI') # Field name made lowercase.
    waittime = models.IntegerField(db_column='WAITTIME') # Field name made lowercase.
#    comment_ = models.CharField(max_length=600, db_column='COMMENT_', blank=True) # Field name made lowercase.
    comment_field = models.CharField(max_length=600, db_column='COMMENT_', blank=True)  # Field name made lowercase.
    space = models.IntegerField(db_column='SPACE') # Field name made lowercase.
    moduser = models.CharField(max_length=90, db_column='MODUSER', blank=True) # Field name made lowercase.
    modtime = models.DateTimeField(db_column='MODTIME') # Field name made lowercase.
    validation = models.CharField(max_length=60, db_column='VALIDATION', blank=True) # Field name made lowercase.
    mcshare = models.IntegerField(db_column='MCSHARE') # Field name made lowercase.
    countries = models.CharField(max_length=240, db_column='COUNTRIES', blank=True) # Field name made lowercase.
    fasttrack = models.CharField(max_length=60, db_column='FASTTRACK', blank=True) # Field name made lowercase.
    nprestage = models.BigIntegerField(db_column='NPRESTAGE') # Field name made lowercase.
    pilotowners = models.CharField(max_length=900, db_column='PILOTOWNERS', blank=True) # Field name made lowercase.
    dn = models.CharField(max_length=300, db_column='DN', blank=True) # Field name made lowercase.
    email = models.CharField(max_length=180, db_column='EMAIL', blank=True) # Field name made lowercase.
    fairshare = models.CharField(max_length=384, db_column='FAIRSHARE', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'cloudconfig'

class Cloudspace(models.Model):
    cloud = models.CharField(max_length=60, primary_key=True, db_column='CLOUD') # Field name made lowercase.
    store = models.CharField(max_length=150, primary_key=True, db_column='STORE') # Field name made lowercase.
    space = models.IntegerField(db_column='SPACE') # Field name made lowercase.
    freespace = models.IntegerField(db_column='FREESPACE') # Field name made lowercase.
    moduser = models.CharField(max_length=90, db_column='MODUSER') # Field name made lowercase.
    modtime = models.DateTimeField(db_column='MODTIME') # Field name made lowercase.
    class Meta:
        db_table = u'cloudspace'

class Cloudtasks(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    taskname = models.CharField(max_length=384, db_column='TASKNAME', blank=True) # Field name made lowercase.
    taskid = models.IntegerField(null=True, db_column='TASKID', blank=True) # Field name made lowercase.
    cloud = models.CharField(max_length=60, db_column='CLOUD', blank=True) # Field name made lowercase.
    status = models.CharField(max_length=60, db_column='STATUS', blank=True) # Field name made lowercase.
    tmod = models.DateTimeField(db_column='TMOD') # Field name made lowercase.
    tenter = models.DateTimeField(db_column='TENTER') # Field name made lowercase.
    class Meta:
        db_table = u'cloudtasks'

class Datasets(models.Model):
    vuid = models.CharField(max_length=120, primary_key=True, db_column='VUID') # Field name made lowercase.
    name = models.CharField(max_length=765, db_column='NAME') # Field name made lowercase.
    version = models.CharField(max_length=30, db_column='VERSION', blank=True) # Field name made lowercase.
    type = models.CharField(max_length=60, db_column='TYPE') # Field name made lowercase.
    status = models.CharField(max_length=30, db_column='STATUS', blank=True) # Field name made lowercase.
    numberfiles = models.IntegerField(null=True, db_column='NUMBERFILES', blank=True) # Field name made lowercase.
    currentfiles = models.IntegerField(null=True, db_column='CURRENTFILES', blank=True) # Field name made lowercase.
    creationdate = models.DateTimeField(null=True, db_column='CREATIONDATE', blank=True) # Field name made lowercase.
    modificationdate = models.DateTimeField(primary_key=True, db_column='MODIFICATIONDATE') # Field name made lowercase.
    moverid = models.BigIntegerField(db_column='MOVERID') # Field name made lowercase.
    transferstatus = models.IntegerField(db_column='TRANSFERSTATUS') # Field name made lowercase.
    subtype = models.CharField(max_length=15, db_column='SUBTYPE', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'datasets'

#class DeftDataset(models.Model):
#    dataset_id = models.CharField(max_length=768, primary_key=True, db_column='DATASET_ID') # Field name made lowercase.
#    dataset_meta = models.BigIntegerField(null=True, db_column='DATASET_META', blank=True) # Field name made lowercase.
#    dataset_state = models.CharField(max_length=48, db_column='DATASET_STATE', blank=True) # Field name made lowercase.
#    dataset_source = models.BigIntegerField(null=True, db_column='DATASET_SOURCE', blank=True) # Field name made lowercase.
#    dataset_target = models.BigIntegerField(null=True, db_column='DATASET_TARGET', blank=True) # Field name made lowercase.
#    dataset_comment = models.CharField(max_length=384, db_column='DATASET_COMMENT', blank=True) # Field name made lowercase.
#    class Meta:
#        db_table = u'deft_dataset'
#
class DeftDataset(models.Model):
    dataset_id = models.CharField(db_column='DATASET_ID', primary_key=True, max_length=255)  # Field name made lowercase.
    dataset_meta = models.BigIntegerField(db_column='DATASET_META', blank=True, null=True)  # Field name made lowercase.
    dataset_state = models.CharField(db_column='DATASET_STATE', max_length=16, blank=True)  # Field name made lowercase.
    dataset_source = models.BigIntegerField(db_column='DATASET_SOURCE', blank=True, null=True)  # Field name made lowercase.
    dataset_target = models.BigIntegerField(db_column='DATASET_TARGET', blank=True, null=True)  # Field name made lowercase.
    dataset_comment = models.CharField(db_column='DATASET_COMMENT', max_length=128, blank=True)  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'deft_dataset'

class DeftMeta(models.Model):
    meta_id = models.BigIntegerField(primary_key=True, db_column='META_ID') # Field name made lowercase.
    meta_state = models.CharField(max_length=48, db_column='META_STATE', blank=True) # Field name made lowercase.
    meta_comment = models.CharField(max_length=384, db_column='META_COMMENT', blank=True) # Field name made lowercase.
    meta_req_ts = models.DateTimeField(null=True, db_column='META_REQ_TS', blank=True) # Field name made lowercase.
    meta_upd_ts = models.DateTimeField(null=True, db_column='META_UPD_TS', blank=True) # Field name made lowercase.
    meta_requestor = models.CharField(max_length=48, db_column='META_REQUESTOR', blank=True) # Field name made lowercase.
    meta_manager = models.CharField(max_length=48, db_column='META_MANAGER', blank=True) # Field name made lowercase.
    meta_vo = models.CharField(max_length=48, db_column='META_VO', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'deft_meta'

class DeftTask(models.Model):
    task_id = models.BigIntegerField(primary_key=True, db_column='TASK_ID') # Field name made lowercase.
    task_meta = models.BigIntegerField(null=True, db_column='TASK_META', blank=True) # Field name made lowercase.
    task_state = models.CharField(max_length=48, db_column='TASK_STATE', blank=True) # Field name made lowercase.
    task_param = models.TextField(db_column='TASK_PARAM', blank=True) # Field name made lowercase.
    task_tag = models.CharField(max_length=48, db_column='TASK_TAG', blank=True) # Field name made lowercase.
    task_comment = models.CharField(max_length=384, db_column='TASK_COMMENT', blank=True) # Field name made lowercase.
    task_vo = models.CharField(max_length=48, db_column='TASK_VO', blank=True) # Field name made lowercase.
    task_transpath = models.CharField(max_length=384, db_column='TASK_TRANSPATH', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'deft_task'

class Dslist(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    duid = models.CharField(max_length=120, db_column='DUID', blank=True) # Field name made lowercase.
    name = models.CharField(max_length=600, db_column='NAME') # Field name made lowercase.
    ugid = models.IntegerField(null=True, db_column='UGID', blank=True) # Field name made lowercase.
    priority = models.IntegerField(null=True, db_column='PRIORITY', blank=True) # Field name made lowercase.
    status = models.CharField(max_length=30, db_column='STATUS', blank=True) # Field name made lowercase.
    lastuse = models.DateTimeField(db_column='LASTUSE') # Field name made lowercase.
    pinstate = models.CharField(max_length=30, db_column='PINSTATE', blank=True) # Field name made lowercase.
    pintime = models.DateTimeField(db_column='PINTIME') # Field name made lowercase.
    lifetime = models.DateTimeField(db_column='LIFETIME') # Field name made lowercase.
    site = models.CharField(max_length=180, db_column='SITE', blank=True) # Field name made lowercase.
    par1 = models.CharField(max_length=90, db_column='PAR1', blank=True) # Field name made lowercase.
    par2 = models.CharField(max_length=90, db_column='PAR2', blank=True) # Field name made lowercase.
    par3 = models.CharField(max_length=90, db_column='PAR3', blank=True) # Field name made lowercase.
    par4 = models.CharField(max_length=90, db_column='PAR4', blank=True) # Field name made lowercase.
    par5 = models.CharField(max_length=90, db_column='PAR5', blank=True) # Field name made lowercase.
    par6 = models.CharField(max_length=90, db_column='PAR6', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'dslist'

class Etask(models.Model):
    taskid = models.IntegerField(primary_key=True, db_column='TASKID') # Field name made lowercase.
    creationtime = models.DateTimeField(db_column='CREATIONTIME') # Field name made lowercase.
    modificationtime = models.DateTimeField(db_column='MODIFICATIONTIME') # Field name made lowercase.
    taskname = models.CharField(max_length=768, db_column='TASKNAME', blank=True) # Field name made lowercase.
    status = models.CharField(max_length=384, db_column='STATUS', blank=True) # Field name made lowercase.
    username = models.CharField(max_length=768, db_column='USERNAME', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'etask'

class Filestable4(models.Model):
    row_id = models.BigIntegerField(primary_key=True, db_column='ROW_ID') # Field name made lowercase.
    pandaid = models.BigIntegerField(db_column='PANDAID') # Field name made lowercase.
    modificationtime = models.DateTimeField(primary_key=True, db_column='MODIFICATIONTIME') # Field name made lowercase.
    guid = models.CharField(max_length=192, db_column='GUID', blank=True) # Field name made lowercase.
    lfn = models.CharField(max_length=768, db_column='LFN', blank=True) # Field name made lowercase.
    type = models.CharField(max_length=60, db_column='TYPE', blank=True) # Field name made lowercase.
    dataset = models.CharField(max_length=765, db_column='DATASET', blank=True) # Field name made lowercase.
    status = models.CharField(max_length=192, db_column='STATUS', blank=True) # Field name made lowercase.
    proddblock = models.CharField(max_length=765, db_column='PRODDBLOCK', blank=True) # Field name made lowercase.
    proddblocktoken = models.CharField(max_length=750, db_column='PRODDBLOCKTOKEN', blank=True) # Field name made lowercase.
    dispatchdblock = models.CharField(max_length=765, db_column='DISPATCHDBLOCK', blank=True) # Field name made lowercase.
    dispatchdblocktoken = models.CharField(max_length=750, db_column='DISPATCHDBLOCKTOKEN', blank=True) # Field name made lowercase.
    destinationdblock = models.CharField(max_length=765, db_column='DESTINATIONDBLOCK', blank=True) # Field name made lowercase.
    destinationdblocktoken = models.CharField(max_length=750, db_column='DESTINATIONDBLOCKTOKEN', blank=True) # Field name made lowercase.
    destinationse = models.CharField(max_length=750, db_column='DESTINATIONSE', blank=True) # Field name made lowercase.
    fsize = models.BigIntegerField(db_column='FSIZE') # Field name made lowercase.
    md5sum = models.CharField(max_length=108, db_column='MD5SUM', blank=True) # Field name made lowercase.
    checksum = models.CharField(max_length=108, db_column='CHECKSUM', blank=True) # Field name made lowercase.
    scope = models.CharField(max_length=90, db_column='SCOPE', blank=True) # Field name made lowercase.
    jeditaskid = models.BigIntegerField(null=True, db_column='JEDITASKID', blank=True) # Field name made lowercase.
    datasetid = models.BigIntegerField(null=True, db_column='DATASETID', blank=True) # Field name made lowercase.
    fileid = models.BigIntegerField(null=True, db_column='FILEID', blank=True) # Field name made lowercase.
    attemptnr = models.IntegerField(null=True, db_column='ATTEMPTNR', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'filestable4'

class FilestableArch(models.Model):
    row_id = models.BigIntegerField(primary_key=True, db_column='ROW_ID')  # Field name made lowercase.
    pandaid = models.BigIntegerField(db_column='PANDAID')  # Field name made lowercase.
    modificationtime = models.DateTimeField(primary_key=True, db_column='MODIFICATIONTIME')  # Field name made lowercase.
    creationtime = models.DateTimeField(db_column='MODIFICATIONTIME')  # Field name made lowercase.
    guid = models.CharField(max_length=64, db_column='GUID', blank=True)  # Field name made lowercase.
    lfn = models.CharField(max_length=256, db_column='LFN', blank=True)  # Field name made lowercase.
    type = models.CharField(max_length=20, db_column='TYPE', blank=True)  # Field name made lowercase.
    dataset = models.CharField(max_length=255, db_column='DATASET', blank=True)  # Field name made lowercase.
    status = models.CharField(max_length=64, db_column='STATUS', blank=True)  # Field name made lowercase.
    proddblock = models.CharField(max_length=255, db_column='PRODDBLOCK', blank=True)  # Field name made lowercase.
    proddblocktoken = models.CharField(max_length=250, db_column='PRODDBLOCKTOKEN', blank=True)  # Field name made lowercase.
    dispatchdblock = models.CharField(max_length=265, db_column='DISPATCHDBLOCK', blank=True)  # Field name made lowercase.
    dispatchdblocktoken = models.CharField(max_length=250, db_column='DISPATCHDBLOCKTOKEN', blank=True)  # Field name made lowercase.
    destinationdblock = models.CharField(max_length=265, db_column='DESTINATIONDBLOCK', blank=True)  # Field name made lowercase.
    destinationdblocktoken = models.CharField(max_length=250, db_column='DESTINATIONDBLOCKTOKEN', blank=True)  # Field name made lowercase.
    destinationse = models.CharField(max_length=250, db_column='DESTINATIONSE', blank=True)  # Field name made lowercase.
    fsize = models.BigIntegerField(db_column='FSIZE')  # Field name made lowercase.
    md5sum = models.CharField(max_length=40, db_column='MD5SUM', blank=True)  # Field name made lowercase.
    checksum = models.CharField(max_length=40, db_column='CHECKSUM', blank=True)  # Field name made lowercase.
    scope = models.CharField(max_length=30, db_column='SCOPE', blank=True)  # Field name made lowercase.
    jeditaskid = models.BigIntegerField(null=True, db_column='JEDITASKID', blank=True)  # Field name made lowercase.
    datasetid = models.BigIntegerField(null=True, db_column='DATASETID', blank=True)  # Field name made lowercase.
    fileid = models.BigIntegerField(null=True, db_column='FILEID', blank=True)  # Field name made lowercase.
    attemptnr = models.IntegerField(null=True, db_column='ATTEMPTNR', blank=True)  # Field name made lowercase.

    class Meta:
        db_table = u'filestable_arch'

class Groups(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    name = models.CharField(max_length=180, db_column='NAME') # Field name made lowercase.
    description = models.CharField(max_length=360, db_column='DESCRIPTION') # Field name made lowercase.
    url = models.CharField(max_length=300, db_column='URL', blank=True) # Field name made lowercase.
    classa = models.CharField(max_length=90, db_column='CLASSA', blank=True) # Field name made lowercase.
    classp = models.CharField(max_length=90, db_column='CLASSP', blank=True) # Field name made lowercase.
    classxp = models.CharField(max_length=90, db_column='CLASSXP', blank=True) # Field name made lowercase.
    njobs1 = models.IntegerField(null=True, db_column='NJOBS1', blank=True) # Field name made lowercase.
    njobs7 = models.IntegerField(null=True, db_column='NJOBS7', blank=True) # Field name made lowercase.
    njobs30 = models.IntegerField(null=True, db_column='NJOBS30', blank=True) # Field name made lowercase.
    cpua1 = models.BigIntegerField(null=True, db_column='CPUA1', blank=True) # Field name made lowercase.
    cpua7 = models.BigIntegerField(null=True, db_column='CPUA7', blank=True) # Field name made lowercase.
    cpua30 = models.BigIntegerField(null=True, db_column='CPUA30', blank=True) # Field name made lowercase.
    cpup1 = models.BigIntegerField(null=True, db_column='CPUP1', blank=True) # Field name made lowercase.
    cpup7 = models.BigIntegerField(null=True, db_column='CPUP7', blank=True) # Field name made lowercase.
    cpup30 = models.BigIntegerField(null=True, db_column='CPUP30', blank=True) # Field name made lowercase.
    cpuxp1 = models.BigIntegerField(null=True, db_column='CPUXP1', blank=True) # Field name made lowercase.
    cpuxp7 = models.BigIntegerField(null=True, db_column='CPUXP7', blank=True) # Field name made lowercase.
    cpuxp30 = models.BigIntegerField(null=True, db_column='CPUXP30', blank=True) # Field name made lowercase.
    allcpua1 = models.BigIntegerField(null=True, db_column='ALLCPUA1', blank=True) # Field name made lowercase.
    allcpua7 = models.BigIntegerField(null=True, db_column='ALLCPUA7', blank=True) # Field name made lowercase.
    allcpua30 = models.BigIntegerField(null=True, db_column='ALLCPUA30', blank=True) # Field name made lowercase.
    allcpup1 = models.BigIntegerField(null=True, db_column='ALLCPUP1', blank=True) # Field name made lowercase.
    allcpup7 = models.BigIntegerField(null=True, db_column='ALLCPUP7', blank=True) # Field name made lowercase.
    allcpup30 = models.BigIntegerField(null=True, db_column='ALLCPUP30', blank=True) # Field name made lowercase.
    allcpuxp1 = models.BigIntegerField(null=True, db_column='ALLCPUXP1', blank=True) # Field name made lowercase.
    allcpuxp7 = models.BigIntegerField(null=True, db_column='ALLCPUXP7', blank=True) # Field name made lowercase.
    allcpuxp30 = models.BigIntegerField(null=True, db_column='ALLCPUXP30', blank=True) # Field name made lowercase.
    quotaa1 = models.BigIntegerField(null=True, db_column='QUOTAA1', blank=True) # Field name made lowercase.
    quotaa7 = models.BigIntegerField(null=True, db_column='QUOTAA7', blank=True) # Field name made lowercase.
    quotaa30 = models.BigIntegerField(null=True, db_column='QUOTAA30', blank=True) # Field name made lowercase.
    quotap1 = models.BigIntegerField(null=True, db_column='QUOTAP1', blank=True) # Field name made lowercase.
    quotap7 = models.BigIntegerField(null=True, db_column='QUOTAP7', blank=True) # Field name made lowercase.
    quotap30 = models.BigIntegerField(null=True, db_column='QUOTAP30', blank=True) # Field name made lowercase.
    quotaxp1 = models.BigIntegerField(null=True, db_column='QUOTAXP1', blank=True) # Field name made lowercase.
    quotaxp7 = models.BigIntegerField(null=True, db_column='QUOTAXP7', blank=True) # Field name made lowercase.
    quotaxp30 = models.BigIntegerField(null=True, db_column='QUOTAXP30', blank=True) # Field name made lowercase.
    allquotaa1 = models.BigIntegerField(null=True, db_column='ALLQUOTAA1', blank=True) # Field name made lowercase.
    allquotaa7 = models.BigIntegerField(null=True, db_column='ALLQUOTAA7', blank=True) # Field name made lowercase.
    allquotaa30 = models.BigIntegerField(null=True, db_column='ALLQUOTAA30', blank=True) # Field name made lowercase.
    allquotap1 = models.BigIntegerField(null=True, db_column='ALLQUOTAP1', blank=True) # Field name made lowercase.
    allquotap7 = models.BigIntegerField(null=True, db_column='ALLQUOTAP7', blank=True) # Field name made lowercase.
    allquotap30 = models.BigIntegerField(null=True, db_column='ALLQUOTAP30', blank=True) # Field name made lowercase.
    allquotaxp1 = models.BigIntegerField(null=True, db_column='ALLQUOTAXP1', blank=True) # Field name made lowercase.
    allquotaxp7 = models.BigIntegerField(null=True, db_column='ALLQUOTAXP7', blank=True) # Field name made lowercase.
    allquotaxp30 = models.BigIntegerField(null=True, db_column='ALLQUOTAXP30', blank=True) # Field name made lowercase.
    space1 = models.IntegerField(null=True, db_column='SPACE1', blank=True) # Field name made lowercase.
    space7 = models.IntegerField(null=True, db_column='SPACE7', blank=True) # Field name made lowercase.
    space30 = models.IntegerField(null=True, db_column='SPACE30', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'groups'

class History(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    entrytime = models.DateTimeField(db_column='ENTRYTIME') # Field name made lowercase.
    starttime = models.DateTimeField(db_column='STARTTIME') # Field name made lowercase.
    endtime = models.DateTimeField(db_column='ENDTIME') # Field name made lowercase.
    cpu = models.BigIntegerField(null=True, db_column='CPU', blank=True) # Field name made lowercase.
    cpuxp = models.BigIntegerField(null=True, db_column='CPUXP', blank=True) # Field name made lowercase.
    space = models.IntegerField(null=True, db_column='SPACE', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'history'

class Incidents(models.Model):
    at_time = models.DateTimeField(primary_key=True, db_column='AT_TIME') # Field name made lowercase.
    typekey = models.CharField(max_length=60, db_column='TYPEKEY', blank=True) # Field name made lowercase.
    description = models.CharField(max_length=600, db_column='DESCRIPTION', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'incidents'

class InfomodelsSitestatus(models.Model):
    id = models.BigIntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    sitename = models.CharField(max_length=180, db_column='SITENAME', blank=True) # Field name made lowercase.
    active = models.IntegerField(null=True, db_column='ACTIVE', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'infomodels_sitestatus'

class Installedsw(models.Model):
    siteid = models.CharField(max_length=180, primary_key=True, db_column='SITEID') # Field name made lowercase.
    cloud = models.CharField(max_length=30, db_column='CLOUD', blank=True) # Field name made lowercase.
    release = models.CharField(max_length=30, primary_key=True, db_column='RELEASE') # Field name made lowercase.
    cache = models.CharField(max_length=120, primary_key=True, db_column='CACHE') # Field name made lowercase.
    validation = models.CharField(max_length=30, db_column='VALIDATION', blank=True) # Field name made lowercase.
    cmtconfig = models.CharField(max_length=120, primary_key=True, db_column='CMTCONFIG') # Field name made lowercase.
    class Meta:
        db_table = u'installedsw'

class InstalledswOld(models.Model):
    siteid = models.CharField(max_length=180, primary_key=True, db_column='SITEID') # Field name made lowercase.
    cloud = models.CharField(max_length=30, db_column='CLOUD', blank=True) # Field name made lowercase.
    release = models.CharField(max_length=30, db_column='RELEASE', blank=True) # Field name made lowercase.
    cache = models.CharField(max_length=120, db_column='CACHE', blank=True) # Field name made lowercase.
    validation = models.CharField(max_length=30, db_column='VALIDATION', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'installedsw_old'

class Jdllist(models.Model):
    name = models.CharField(max_length=180, primary_key=True, db_column='NAME') # Field name made lowercase.
    host = models.CharField(max_length=180, db_column='HOST', blank=True) # Field name made lowercase.
    system = models.CharField(max_length=60, db_column='SYSTEM') # Field name made lowercase.
    jdl = models.CharField(max_length=12000, db_column='JDL', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'jdllist'

class JediAuxStatusMintaskid(models.Model):
    status = models.CharField(max_length=192, primary_key=True, db_column='STATUS') # Field name made lowercase.
    min_jeditaskid = models.BigIntegerField(db_column='MIN_JEDITASKID') # Field name made lowercase.
    class Meta:
        db_table = u'jedi_aux_status_mintaskid'

class JediDatasetContents(models.Model):
    jeditaskid = models.BigIntegerField(primary_key=True, db_column='JEDITASKID') # Field name made lowercase.
    datasetid = models.BigIntegerField(primary_key=True, db_column='DATASETID') # Field name made lowercase.
    fileid = models.BigIntegerField(primary_key=True, db_column='FILEID') # Field name made lowercase.
    creationdate = models.DateTimeField(db_column='CREATIONDATE') # Field name made lowercase.
    lastattempttime = models.DateTimeField(null=True, db_column='LASTATTEMPTTIME', blank=True) # Field name made lowercase.
    lfn = models.CharField(max_length=768, db_column='LFN') # Field name made lowercase.
    guid = models.CharField(max_length=192, db_column='GUID', blank=True) # Field name made lowercase.
    type = models.CharField(max_length=60, db_column='TYPE') # Field name made lowercase.
    status = models.CharField(max_length=192, db_column='STATUS') # Field name made lowercase.
    fsize = models.BigIntegerField(null=True, db_column='FSIZE', blank=True) # Field name made lowercase.
    checksum = models.CharField(max_length=108, db_column='CHECKSUM', blank=True) # Field name made lowercase.
    scope = models.CharField(max_length=90, db_column='SCOPE', blank=True) # Field name made lowercase.
    attemptnr = models.IntegerField(null=True, db_column='ATTEMPTNR', blank=True) # Field name made lowercase.
    maxattempt = models.IntegerField(null=True, db_column='MAXATTEMPT', blank=True) # Field name made lowercase.
    nevents = models.IntegerField(null=True, db_column='NEVENTS', blank=True) # Field name made lowercase.
    keeptrack = models.IntegerField(null=True, db_column='KEEPTRACK', blank=True) # Field name made lowercase.
    startevent = models.IntegerField(null=True, db_column='STARTEVENT', blank=True) # Field name made lowercase.
    endevent = models.IntegerField(null=True, db_column='ENDEVENT', blank=True) # Field name made lowercase.
    firstevent = models.IntegerField(null=True, db_column='FIRSTEVENT', blank=True) # Field name made lowercase.
    boundaryid = models.BigIntegerField(null=True, db_column='BOUNDARYID', blank=True) # Field name made lowercase.
    pandaid = models.BigIntegerField(db_column='PANDAID', blank=True)
    class Meta:
        db_table = u'jedi_dataset_contents'

class JediDatasets(models.Model):
    jeditaskid = models.BigIntegerField(primary_key=True, db_column='JEDITASKID') # Field name made lowercase.
    datasetid = models.BigIntegerField(primary_key=True, db_column='DATASETID') # Field name made lowercase.
    datasetname = models.CharField(max_length=765, db_column='DATASETNAME') # Field name made lowercase.
    type = models.CharField(max_length=60, db_column='TYPE') # Field name made lowercase.
    creationtime = models.DateTimeField(db_column='CREATIONTIME') # Field name made lowercase.
    modificationtime = models.DateTimeField(db_column='MODIFICATIONTIME') # Field name made lowercase.
    vo = models.CharField(max_length=48, db_column='VO', blank=True) # Field name made lowercase.
    cloud = models.CharField(max_length=30, db_column='CLOUD', blank=True) # Field name made lowercase.
    site = models.CharField(max_length=180, db_column='SITE', blank=True) # Field name made lowercase.
    masterid = models.BigIntegerField(null=True, db_column='MASTERID', blank=True) # Field name made lowercase.
    provenanceid = models.BigIntegerField(null=True, db_column='PROVENANCEID', blank=True) # Field name made lowercase.
    containername = models.CharField(max_length=396, db_column='CONTAINERNAME', blank=True) # Field name made lowercase.
    status = models.CharField(max_length=60, db_column='STATUS', blank=True) # Field name made lowercase.
    state = models.CharField(max_length=60, db_column='STATE', blank=True) # Field name made lowercase.
    statechecktime = models.DateTimeField(null=True, db_column='STATECHECKTIME', blank=True) # Field name made lowercase.
    statecheckexpiration = models.DateTimeField(null=True, db_column='STATECHECKEXPIRATION', blank=True) # Field name made lowercase.
    frozentime = models.DateTimeField(null=True, db_column='FROZENTIME', blank=True) # Field name made lowercase.
    nfiles = models.IntegerField(null=True, db_column='NFILES', blank=True) # Field name made lowercase.
    nfilestobeused = models.IntegerField(null=True, db_column='NFILESTOBEUSED', blank=True) # Field name made lowercase.
    nfilesused = models.IntegerField(null=True, db_column='NFILESUSED', blank=True) # Field name made lowercase.
    nevents = models.BigIntegerField(null=True, db_column='NEVENTS', blank=True) # Field name made lowercase.
    neventstobeused = models.BigIntegerField(null=True, db_column='NEVENTSTOBEUSED', blank=True) # Field name made lowercase.
    neventsused = models.BigIntegerField(null=True, db_column='NEVENTSUSED', blank=True) # Field name made lowercase.
    lockedby = models.CharField(max_length=120, db_column='LOCKEDBY', blank=True) # Field name made lowercase.
    lockedtime = models.DateTimeField(null=True, db_column='LOCKEDTIME', blank=True) # Field name made lowercase.
    nfilesfinished = models.IntegerField(null=True, db_column='NFILESFINISHED', blank=True) # Field name made lowercase.
    nfilesfailed = models.IntegerField(null=True, db_column='NFILESFAILED', blank=True) # Field name made lowercase.
    attributes = models.CharField(max_length=300, db_column='ATTRIBUTES', blank=True) # Field name made lowercase.
    streamname = models.CharField(max_length=60, db_column='STREAMNAME', blank=True) # Field name made lowercase.
    storagetoken = models.CharField(max_length=180, db_column='STORAGETOKEN', blank=True) # Field name made lowercase.
    destination = models.CharField(max_length=180, db_column='DESTINATION', blank=True) # Field name made lowercase.
    nfilesonhold = models.IntegerField(null=True, db_column='NFILESONHOLD', blank=True) # Field name made lowercase.
    templateid = models.BigIntegerField(db_column='TEMPLATEID', blank=True)
    class Meta:
        db_table = u'jedi_datasets'

class JediEvents(models.Model):
    jeditaskid = models.BigIntegerField(primary_key=True, db_column='JEDITASKID') # Field name made lowercase.
    pandaid = models.BigIntegerField(primary_key=True, db_column='PANDAID') # Field name made lowercase.
    fileid = models.BigIntegerField(primary_key=True, db_column='FILEID') # Field name made lowercase.
    job_processid = models.IntegerField(primary_key=True, db_column='JOB_PROCESSID') # Field name made lowercase.
    def_min_eventid = models.IntegerField(null=True, db_column='DEF_MIN_EVENTID', blank=True) # Field name made lowercase.
    def_max_eventid = models.IntegerField(null=True, db_column='DEF_MAX_EVENTID', blank=True) # Field name made lowercase.
    processed_upto_eventid = models.IntegerField(null=True, db_column='PROCESSED_UPTO_EVENTID', blank=True) # Field name made lowercase.
    datasetid = models.BigIntegerField(db_column='DATASETID', blank=True)
    status = models.IntegerField(db_column='STATUS', blank=True)
    attemptnr = models.IntegerField(db_column='ATTEMPTNR', blank=True)
    class Meta:
        db_table = u'jedi_events'

class JediJobparamsTemplate(models.Model):
    jeditaskid = models.BigIntegerField(primary_key=True, db_column='JEDITASKID') # Field name made lowercase.
    jobparamstemplate = models.TextField(db_column='JOBPARAMSTEMPLATE', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'jedi_jobparams_template'

class JediJobRetryHistory(models.Model):
    jeditaskid = models.BigIntegerField(primary_key=True, db_column='JEDITASKID')  # Field name made lowercase.
    oldpandaid = models.BigIntegerField(primary_key=True, db_column='OLDPANDAID')  # Field name made lowercase.
    newpandaid = models.BigIntegerField(primary_key=True, db_column='NEWPANDAID')  # Field name made lowercase.
    ins_utc_tstamp = models.BigIntegerField(db_column='INS_UTC_TSTAMP', blank=True)  # Field name made lowercase.
    class Meta:
        db_table = u'jedi_job_retry_history'

class JediOutputTemplate(models.Model):
    jeditaskid = models.BigIntegerField(primary_key=True, db_column='JEDITASKID') # Field name made lowercase.
    datasetid = models.BigIntegerField(primary_key=True, db_column='DATASETID') # Field name made lowercase.
    outtempid = models.BigIntegerField(primary_key=True, db_column='OUTTEMPID') # Field name made lowercase.
    filenametemplate = models.CharField(max_length=768, db_column='FILENAMETEMPLATE') # Field name made lowercase.
    maxserialnr = models.IntegerField(null=True, db_column='MAXSERIALNR', blank=True) # Field name made lowercase.
    serialnr = models.IntegerField(null=True, db_column='SERIALNR', blank=True) # Field name made lowercase.
    sourcename = models.CharField(max_length=768, db_column='SOURCENAME', blank=True) # Field name made lowercase.
    streamname = models.CharField(max_length=60, db_column='STREAMNAME', blank=True) # Field name made lowercase.
    outtype = models.CharField(max_length=60, db_column='OUTTYPE', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'jedi_output_template'

class JediTaskparams(models.Model):
    jeditaskid = models.BigIntegerField(primary_key=True, db_column='JEDITASKID') # Field name made lowercase.
    taskparams = models.TextField(db_column='TASKPARAMS', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'jedi_taskparams'

class JediTasks(models.Model):
    jeditaskid = models.BigIntegerField(primary_key=True, db_column='JEDITASKID') # Field name made lowercase.
    taskname = models.CharField(max_length=384, db_column='TASKNAME', blank=True) # Field name made lowercase.
    status = models.CharField(max_length=192, db_column='STATUS') # Field name made lowercase.
    username = models.CharField(max_length=384, db_column='USERNAME') # Field name made lowercase.
    creationdate = models.DateTimeField(db_column='CREATIONDATE')  # Field name made lowercase.
    modificationtime = models.DateTimeField(db_column='MODIFICATIONTIME') # Field name made lowercase.
    reqid = models.IntegerField(null=True, db_column='REQID', blank=True) # Field name made lowercase.
    oldstatus = models.CharField(max_length=192, db_column='OLDSTATUS', blank=True) # Field name made lowercase.
    cloud = models.CharField(max_length=30, db_column='CLOUD', blank=True) # Field name made lowercase.
    site = models.CharField(max_length=180, db_column='SITE', blank=True) # Field name made lowercase.
    starttime = models.DateTimeField(null=True, db_column='STARTTIME', blank=True) # Field name made lowercase.
    endtime = models.DateTimeField(null=True, db_column='ENDTIME', blank=True) # Field name made lowercase.
    frozentime = models.DateTimeField(null=True, db_column='FROZENTIME', blank=True) # Field name made lowercase.
    prodsourcelabel = models.CharField(max_length=60, db_column='PRODSOURCELABEL', blank=True) # Field name made lowercase.
    workinggroup = models.CharField(max_length=96, db_column='WORKINGGROUP', blank=True) # Field name made lowercase.
    vo = models.CharField(max_length=48, db_column='VO', blank=True) # Field name made lowercase.
    corecount = models.IntegerField(null=True, db_column='CORECOUNT', blank=True) # Field name made lowercase.
    tasktype = models.CharField(max_length=192, db_column='TASKTYPE', blank=True) # Field name made lowercase.
    processingtype = models.CharField(max_length=192, db_column='PROCESSINGTYPE', blank=True) # Field name made lowercase.
    taskpriority = models.IntegerField(null=True, db_column='TASKPRIORITY', blank=True) # Field name made lowercase.
    currentpriority = models.IntegerField(null=True, db_column='CURRENTPRIORITY', blank=True) # Field name made lowercase.
    architecture = models.CharField(max_length=768, db_column='ARCHITECTURE', blank=True) # Field name made lowercase.
    transuses = models.CharField(max_length=192, db_column='TRANSUSES', blank=True) # Field name made lowercase.
    transhome = models.CharField(max_length=384, db_column='TRANSHOME', blank=True) # Field name made lowercase.
    transpath = models.CharField(max_length=384, db_column='TRANSPATH', blank=True) # Field name made lowercase.
    lockedby = models.CharField(max_length=120, db_column='LOCKEDBY', blank=True) # Field name made lowercase.
    lockedtime = models.DateTimeField(null=True, db_column='LOCKEDTIME', blank=True) # Field name made lowercase.
    termcondition = models.CharField(max_length=300, db_column='TERMCONDITION', blank=True) # Field name made lowercase.
    splitrule = models.CharField(max_length=300, db_column='SPLITRULE', blank=True) # Field name made lowercase.
    walltime = models.IntegerField(null=True, db_column='WALLTIME', blank=True) # Field name made lowercase.
    walltimeunit = models.CharField(max_length=96, db_column='WALLTIMEUNIT', blank=True) # Field name made lowercase.
    outdiskcount = models.IntegerField(null=True, db_column='OUTDISKCOUNT', blank=True) # Field name made lowercase.
    outdiskunit = models.CharField(max_length=96, db_column='OUTDISKUNIT', blank=True) # Field name made lowercase.
    workdiskcount = models.IntegerField(null=True, db_column='WORKDISKCOUNT', blank=True) # Field name made lowercase.
    workdiskunit = models.CharField(max_length=96, db_column='WORKDISKUNIT', blank=True) # Field name made lowercase.
    ramcount = models.IntegerField(null=True, db_column='RAMCOUNT', blank=True) # Field name made lowercase.
    ramunit = models.CharField(max_length=96, db_column='RAMUNIT', blank=True) # Field name made lowercase.
    iointensity = models.IntegerField(null=True, db_column='IOINTENSITY', blank=True) # Field name made lowercase.
    iointensityunit = models.CharField(max_length=96, db_column='IOINTENSITYUNIT', blank=True) # Field name made lowercase.
    workqueue_id = models.IntegerField(null=True, db_column='WORKQUEUE_ID', blank=True) # Field name made lowercase.
    progress = models.IntegerField(null=True, db_column='PROGRESS', blank=True) # Field name made lowercase.
    failurerate = models.IntegerField(null=True, db_column='FAILURERATE', blank=True) # Field name made lowercase.
    errordialog = models.CharField(max_length=765, db_column='ERRORDIALOG', blank=True) # Field name made lowercase.
    countrygroup = models.CharField(max_length=20, db_column='COUNTRYGROUP', blank=True)  # Field name made lowercase.
    parent_tid = models.BigIntegerField(db_column='PARENT_TID', blank=True)  # Field name made lowercase.
    class Meta:
        db_table = u'jedi_tasks'

class JediWorkQueue(models.Model):
    queue_id = models.IntegerField(primary_key=True, db_column='QUEUE_ID') # Field name made lowercase.
    queue_name = models.CharField(max_length=48, db_column='QUEUE_NAME') # Field name made lowercase.
    queue_type = models.CharField(max_length=48, db_column='QUEUE_TYPE') # Field name made lowercase.
    vo = models.CharField(max_length=48, db_column='VO') # Field name made lowercase.
    status = models.CharField(max_length=192, db_column='STATUS', blank=True) # Field name made lowercase.
    partitionid = models.IntegerField(null=True, db_column='PARTITIONID', blank=True) # Field name made lowercase.
    stretchable = models.IntegerField(null=True, db_column='STRETCHABLE', blank=True) # Field name made lowercase.
    queue_share = models.IntegerField(null=True, db_column='QUEUE_SHARE', blank=True) # Field name made lowercase.
    queue_order = models.IntegerField(null=True, db_column='QUEUE_ORDER', blank=True) # Field name made lowercase.
    criteria = models.CharField(max_length=768, db_column='CRITERIA', blank=True) # Field name made lowercase.
    variables = models.CharField(max_length=768, db_column='VARIABLES', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'jedi_work_queue'

class Jobclass(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    name = models.CharField(max_length=90, db_column='NAME') # Field name made lowercase.
    description = models.CharField(max_length=90, db_column='DESCRIPTION') # Field name made lowercase.
    rights = models.CharField(max_length=90, db_column='RIGHTS', blank=True) # Field name made lowercase.
    priority = models.IntegerField(null=True, db_column='PRIORITY', blank=True) # Field name made lowercase.
    quota1 = models.BigIntegerField(null=True, db_column='QUOTA1', blank=True) # Field name made lowercase.
    quota7 = models.BigIntegerField(null=True, db_column='QUOTA7', blank=True) # Field name made lowercase.
    quota30 = models.BigIntegerField(null=True, db_column='QUOTA30', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'jobclass'

class Jobparamstable(models.Model):
    pandaid = models.BigIntegerField(primary_key=True, db_column='PANDAID') # Field name made lowercase.
    modificationtime = models.DateTimeField(primary_key=True, db_column='MODIFICATIONTIME') # Field name made lowercase.
    jobparameters = models.TextField(db_column='JOBPARAMETERS', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'jobparamstable'

class JobparamstableArch(models.Model):
    pandaid = models.BigIntegerField(db_column='PANDAID') # Field name made lowercase.
    modificationtime = models.DateTimeField(db_column='MODIFICATIONTIME') # Field name made lowercase.
    jobparameters = models.TextField(db_column='JOBPARAMETERS', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'jobparamstable_arch'

class JobsProgressTrackingOld(models.Model):
    pandaid = models.BigIntegerField(primary_key=True, db_column='PANDAID') # Field name made lowercase.
    fileid = models.BigIntegerField(primary_key=True, db_column='FILEID') # Field name made lowercase.
    job_processid = models.IntegerField(primary_key=True, db_column='JOB_PROCESSID') # Field name made lowercase.
    def_min_eventid = models.IntegerField(null=True, db_column='DEF_MIN_EVENTID', blank=True) # Field name made lowercase.
    def_max_eventid = models.IntegerField(null=True, db_column='DEF_MAX_EVENTID', blank=True) # Field name made lowercase.
    processed_upto_eventid = models.IntegerField(null=True, db_column='PROCESSED_UPTO_EVENTID', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'jobs_progress_tracking_old'

class JobsStatuslog(models.Model):
    pandaid = models.BigIntegerField(db_column='PANDAID') # Field name made lowercase.
    modificationtime = models.DateTimeField(db_column='MODIFICATIONTIME') # Field name made lowercase.
    jobstatus = models.CharField(max_length=45, db_column='JOBSTATUS') # Field name made lowercase.
    prodsourcelabel = models.CharField(max_length=60, db_column='PRODSOURCELABEL', blank=True) # Field name made lowercase.
    cloud = models.CharField(max_length=150, db_column='CLOUD', blank=True) # Field name made lowercase.
    computingsite = models.CharField(max_length=384, db_column='COMPUTINGSITE', blank=True) # Field name made lowercase.
    modificationhost = models.CharField(max_length=384, db_column='MODIFICATIONHOST', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'jobs_statuslog'


class Jobsarch4Taskinfo59StatsOld(models.Model):
    modificationtime = models.DateTimeField(primary_key=True, db_column='MODIFICATIONTIME') # Field name made lowercase.
    cloud = models.CharField(max_length=150, db_column='CLOUD', blank=True) # Field name made lowercase.
    taskid = models.IntegerField(null=True, db_column='TASKID', blank=True) # Field name made lowercase.
    jobstatus = models.CharField(max_length=45, db_column='JOBSTATUS')  # Field name made lowercase.
    processingtype = models.CharField(max_length=192, db_column='PROCESSINGTYPE', blank=True) # Field name made lowercase.
    prodsourcelabel = models.CharField(max_length=60, db_column='PRODSOURCELABEL', blank=True)  # Field name made lowercase.
    num_of_jobs = models.IntegerField(null=True, db_column='NUM_OF_JOBS', blank=True)  # Field name made lowercase.
    cur_date = models.DateTimeField(null=True, db_column='CUR_DATE', blank=True)  # Field name made lowercase.
    class Meta:
#        managed = False
        db_table = u'jobsarch4_taskinfo59_stats_old'

class Jobsarchived4WnlistStats(models.Model):
    modificationtime = models.DateTimeField(primary_key=True, db_column='MODIFICATIONTIME') # Field name made lowercase.
    computingsite = models.CharField(max_length=384, db_column='COMPUTINGSITE', blank=True) # Field name made lowercase.
    modificationhost = models.CharField(max_length=384, db_column='MODIFICATIONHOST', blank=True) # Field name made lowercase.
    jobstatus = models.CharField(max_length=45, db_column='JOBSTATUS') # Field name made lowercase.
    transexitcode = models.CharField(max_length=384, db_column='TRANSEXITCODE', blank=True) # Field name made lowercase.
    prodsourcelabel = models.CharField(max_length=60, db_column='PRODSOURCELABEL', blank=True) # Field name made lowercase.
    num_of_jobs = models.IntegerField(null=True, db_column='NUM_OF_JOBS', blank=True) # Field name made lowercase.
    max_modificationtime = models.DateTimeField(null=True, db_column='MAX_MODIFICATIONTIME', blank=True) # Field name made lowercase.
    cur_date = models.DateTimeField(null=True, db_column='CUR_DATE', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'jobsarchived4_wnlist_stats'

class Jobsdebug(models.Model):
    pandaid = models.BigIntegerField(primary_key=True, db_column='PANDAID') # Field name made lowercase.
    stdout = models.CharField(max_length=6144, db_column='STDOUT', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'jobsdebug'

class Logstable(models.Model):
    pandaid = models.IntegerField(primary_key=True, db_column='PANDAID')  # Field name made lowercase.
    log1 = models.TextField(db_column='LOG1')  # Field name made lowercase.
    log2 = models.TextField(db_column='LOG2')  # Field name made lowercase.
    log3 = models.TextField(db_column='LOG3')  # Field name made lowercase.
    log4 = models.TextField(db_column='LOG4')  # Field name made lowercase.
    class Meta:
        db_table = u'logstable'

class Members(models.Model):
    uname = models.CharField(max_length=90, primary_key=True, db_column='UNAME') # Field name made lowercase.
    gname = models.CharField(max_length=90, primary_key=True, db_column='GNAME') # Field name made lowercase.
    rights = models.CharField(max_length=90, db_column='RIGHTS', blank=True) # Field name made lowercase.
    since = models.DateTimeField(db_column='SINCE') # Field name made lowercase.
    class Meta:
        db_table = u'members'

class Metatable(models.Model):
    pandaid = models.BigIntegerField(primary_key=True, db_column='PANDAID') # Field name made lowercase.
    modificationtime = models.DateTimeField(primary_key=True, db_column='MODIFICATIONTIME') # Field name made lowercase.
    metadata = models.TextField(db_column='METADATA', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'metatable'

class MetatableArch(models.Model):
    pandaid = models.BigIntegerField(db_column='PANDAID') # Field name made lowercase.
    modificationtime = models.DateTimeField(db_column='MODIFICATIONTIME') # Field name made lowercase.
    metadata = models.TextField(db_column='METADATA', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'metatable_arch'

class MvJobsactive4Stats(models.Model):
    id = models.BigIntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    cur_date = models.DateTimeField(db_column='CUR_DATE') # Field name made lowercase.
    cloud = models.CharField(max_length=150, db_column='CLOUD', blank=True) # Field name made lowercase.
    computingsite = models.CharField(max_length=384, db_column='COMPUTINGSITE', blank=True) # Field name made lowercase.
    countrygroup = models.CharField(max_length=60, db_column='COUNTRYGROUP', blank=True) # Field name made lowercase.
    workinggroup = models.CharField(max_length=60, db_column='WORKINGGROUP', blank=True) # Field name made lowercase.
    relocationflag = models.IntegerField(null=True, db_column='RELOCATIONFLAG', blank=True) # Field name made lowercase.
    jobstatus = models.CharField(max_length=45, db_column='JOBSTATUS') # Field name made lowercase.
    processingtype = models.CharField(max_length=192, db_column='PROCESSINGTYPE', blank=True) # Field name made lowercase.
    prodsourcelabel = models.CharField(max_length=60, db_column='PRODSOURCELABEL', blank=True) # Field name made lowercase.
    currentpriority = models.IntegerField(null=True, db_column='CURRENTPRIORITY', blank=True) # Field name made lowercase.
    num_of_jobs = models.IntegerField(null=True, db_column='NUM_OF_JOBS', blank=True) # Field name made lowercase.
    vo = models.CharField(max_length=48, db_column='VO', blank=True) # Field name made lowercase.
    workqueue_id = models.IntegerField(null=True, db_column='WORKQUEUE_ID', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'mv_jobsactive4_stats'

class OldSubcounter(models.Model):
    subid = models.BigIntegerField(primary_key=True, db_column='SUBID') # Field name made lowercase.
    class Meta:
        db_table = u'old_subcounter'

class Pandaconfig(models.Model):
    name = models.CharField(max_length=180, primary_key=True, db_column='NAME') # Field name made lowercase.
    controller = models.CharField(max_length=60, db_column='CONTROLLER') # Field name made lowercase.
    pathena = models.CharField(max_length=60, db_column='PATHENA', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'pandaconfig'

class PandaidsDeleted(models.Model):
    pandaid = models.BigIntegerField(primary_key=True, db_column='PANDAID') # Field name made lowercase.
    tstamp_datadel = models.DateTimeField(null=True, db_column='TSTAMP_DATADEL', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'pandaids_deleted'

class PandaidsModiftime(models.Model):
    pandaid = models.BigIntegerField(primary_key=True, db_column='PANDAID') # Field name made lowercase.
    modiftime = models.DateTimeField(primary_key=True, db_column='MODIFTIME') # Field name made lowercase.
    class Meta:
        db_table = u'pandaids_modiftime'

class Pandalog(models.Model):
    id = models.BigIntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    bintime = models.DateTimeField(db_column='BINTIME') # Field name made lowercase.
    name = models.CharField(max_length=90, db_column='NAME', blank=True) # Field name made lowercase.
    module = models.CharField(max_length=90, db_column='MODULE', blank=True) # Field name made lowercase.
    loguser = models.CharField(max_length=240, db_column='LOGUSER', blank=True) # Field name made lowercase.
    type = models.CharField(max_length=60, db_column='TYPE', blank=True) # Field name made lowercase.
    pid = models.BigIntegerField(db_column='PID') # Field name made lowercase.
    loglevel = models.IntegerField(db_column='LOGLEVEL') # Field name made lowercase.
    levelname = models.CharField(max_length=90, db_column='LEVELNAME', blank=True) # Field name made lowercase.
    time = models.CharField(max_length=90, db_column='TIME', blank=True) # Field name made lowercase.
    filename = models.CharField(max_length=300, db_column='FILENAME', blank=True) # Field name made lowercase.
    line = models.IntegerField(db_column='LINE') # Field name made lowercase.
    message = models.CharField(max_length=12000, db_column='MESSAGE', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'pandalog'

class Passwords(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    pass_field = models.CharField(max_length=180, db_column='PASS') # Field name made lowercase. Field renamed because it was a Python reserved word.
    class Meta:
        db_table = u'passwords'

class Pilotqueue(models.Model):
#    jobid = models.CharField(max_length=300, primary_key=True, db_column='JOBID') # Field name made lowercase.
    jobid = models.CharField(db_column='JOBID', max_length=100, primary_key=True)  # Field name made lowercase.
    tpid = models.CharField(max_length=180, db_column='TPID') # Field name made lowercase.
    url = models.CharField(max_length=600, db_column='URL', blank=True) # Field name made lowercase.
    nickname = models.CharField(max_length=180, primary_key=True, db_column='NICKNAME') # Field name made lowercase.
    system = models.CharField(max_length=60, db_column='SYSTEM') # Field name made lowercase.
#    user_ = models.CharField(max_length=180, db_column='USER_') # Field name made lowercase.
    user_field = models.CharField(max_length=180, db_column='USER_')  # Field name made lowercase.
    host = models.CharField(max_length=180, db_column='HOST') # Field name made lowercase.
    submithost = models.CharField(max_length=180, db_column='SUBMITHOST') # Field name made lowercase.
    queueid = models.CharField(max_length=180, db_column='QUEUEID') # Field name made lowercase.
    type = models.CharField(max_length=60, db_column='TYPE') # Field name made lowercase.
    pandaid = models.IntegerField(null=True, db_column='PANDAID', blank=True) # Field name made lowercase.
    tcheck = models.DateTimeField(db_column='TCHECK') # Field name made lowercase.
    state = models.CharField(max_length=90, db_column='STATE') # Field name made lowercase.
    tstate = models.DateTimeField(db_column='TSTATE') # Field name made lowercase.
    tenter = models.DateTimeField(db_column='TENTER') # Field name made lowercase.
    tsubmit = models.DateTimeField(db_column='TSUBMIT') # Field name made lowercase.
    taccept = models.DateTimeField(db_column='TACCEPT') # Field name made lowercase.
    tschedule = models.DateTimeField(db_column='TSCHEDULE') # Field name made lowercase.
    tstart = models.DateTimeField(db_column='TSTART') # Field name made lowercase.
    tend = models.DateTimeField(db_column='TEND') # Field name made lowercase.
    tdone = models.DateTimeField(db_column='TDONE') # Field name made lowercase.
    tretrieve = models.DateTimeField(db_column='TRETRIEVE') # Field name made lowercase.
    status = models.CharField(max_length=60, db_column='STATUS') # Field name made lowercase.
    errcode = models.IntegerField(db_column='ERRCODE') # Field name made lowercase.
    errinfo = models.CharField(max_length=450, db_column='ERRINFO') # Field name made lowercase.
    message = models.CharField(max_length=12000, db_column='MESSAGE', blank=True) # Field name made lowercase.
    schedd_name = models.CharField(max_length=180, db_column='SCHEDD_NAME') # Field name made lowercase.
    workernode = models.CharField(max_length=180, db_column='WORKERNODE') # Field name made lowercase.
    class Meta:
        db_table = u'pilotqueue'

class PilotqueueBnl(models.Model):
    jobid = models.CharField(max_length=300, db_column='JOBID') # Field name made lowercase.
    tpid = models.CharField(max_length=180, primary_key=True, db_column='TPID') # Field name made lowercase.
    url = models.CharField(max_length=600, db_column='URL') # Field name made lowercase.
    nickname = models.CharField(max_length=180, db_column='NICKNAME') # Field name made lowercase.
    system = models.CharField(max_length=60, db_column='SYSTEM') # Field name made lowercase.
#    user_ = models.CharField(max_length=180, db_column='USER_') # Field name made lowercase.
    user_field = models.CharField(max_length=180, db_column='USER_')  # Field name made lowercase.
    host = models.CharField(max_length=180, db_column='HOST') # Field name made lowercase.
    submithost = models.CharField(max_length=180, db_column='SUBMITHOST') # Field name made lowercase.
    schedd_name = models.CharField(max_length=180, db_column='SCHEDD_NAME') # Field name made lowercase.
    queueid = models.CharField(max_length=180, db_column='QUEUEID') # Field name made lowercase.
    type = models.CharField(max_length=60, db_column='TYPE') # Field name made lowercase.
    pandaid = models.IntegerField(null=True, db_column='PANDAID', blank=True) # Field name made lowercase.
    tcheck = models.DateTimeField(db_column='TCHECK') # Field name made lowercase.
    state = models.CharField(max_length=90, db_column='STATE') # Field name made lowercase.
    tstate = models.DateTimeField(db_column='TSTATE') # Field name made lowercase.
    tenter = models.DateTimeField(db_column='TENTER') # Field name made lowercase.
    tsubmit = models.DateTimeField(db_column='TSUBMIT') # Field name made lowercase.
    taccept = models.DateTimeField(db_column='TACCEPT') # Field name made lowercase.
    tschedule = models.DateTimeField(db_column='TSCHEDULE') # Field name made lowercase.
    tstart = models.DateTimeField(db_column='TSTART') # Field name made lowercase.
    tend = models.DateTimeField(db_column='TEND') # Field name made lowercase.
    tdone = models.DateTimeField(db_column='TDONE') # Field name made lowercase.
    tretrieve = models.DateTimeField(db_column='TRETRIEVE') # Field name made lowercase.
    status = models.CharField(max_length=60, db_column='STATUS') # Field name made lowercase.
    errcode = models.IntegerField(db_column='ERRCODE') # Field name made lowercase.
    errinfo = models.CharField(max_length=450, db_column='ERRINFO') # Field name made lowercase.
    message = models.CharField(max_length=12000, db_column='MESSAGE', blank=True) # Field name made lowercase.
    workernode = models.CharField(max_length=180, db_column='WORKERNODE') # Field name made lowercase.
    class Meta:
        db_table = u'pilotqueue_bnl'

class Pilottoken(models.Model):
    token = models.CharField(max_length=192, primary_key=True, db_column='TOKEN') # Field name made lowercase.
    schedulerhost = models.CharField(max_length=300, db_column='SCHEDULERHOST', blank=True) # Field name made lowercase.
    scheduleruser = models.CharField(max_length=450, db_column='SCHEDULERUSER', blank=True) # Field name made lowercase.
    usages = models.IntegerField(db_column='USAGES') # Field name made lowercase.
    created = models.DateTimeField(db_column='CREATED') # Field name made lowercase.
    expires = models.DateTimeField(db_column='EXPIRES') # Field name made lowercase.
    schedulerid = models.CharField(max_length=240, db_column='SCHEDULERID', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'pilottoken'

class Pilottype(models.Model):
    name = models.CharField(max_length=180, primary_key=True, db_column='NAME') # Field name made lowercase.
    script = models.CharField(max_length=180, db_column='SCRIPT') # Field name made lowercase.
    url = models.CharField(max_length=450, db_column='URL') # Field name made lowercase.
    system = models.CharField(max_length=180, db_column='SYSTEM') # Field name made lowercase.
    class Meta:
        db_table = u'pilottype'

class PoolCollLock(models.Model):
    id = models.CharField(max_length=150, primary_key=True, db_column='ID') # Field name made lowercase.
    collection = models.CharField(max_length=1500, db_column='COLLECTION', blank=True) # Field name made lowercase.
    client_info = models.CharField(max_length=1500, db_column='CLIENT_INFO', blank=True) # Field name made lowercase.
    locktype = models.CharField(max_length=60, db_column='LOCKTYPE', blank=True) # Field name made lowercase.
    timestamp = models.DateTimeField(null=True, db_column='TIMESTAMP', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'pool_coll_lock'

class PoolCollectionData(models.Model):
    id = models.DecimalField(decimal_places=0, primary_key=True, db_column='ID', max_digits=11) # Field name made lowercase.
    oid_1 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='OID_1', blank=True) # Field name made lowercase.
    oid_2 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='OID_2', blank=True) # Field name made lowercase.
    var_1_oid_1 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_1_OID_1', blank=True) # Field name made lowercase.
    var_1_oid_2 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_1_OID_2', blank=True) # Field name made lowercase.
    var_2_oid_1 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_2_OID_1', blank=True) # Field name made lowercase.
    var_2_oid_2 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_2_OID_2', blank=True) # Field name made lowercase.
    var_3 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_3', blank=True) # Field name made lowercase.
    var_4 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_4', blank=True) # Field name made lowercase.
    var_5 = models.FloatField(null=True, db_column='VAR_5', blank=True) # Field name made lowercase.
    var_6 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_6', blank=True) # Field name made lowercase.
    var_7 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_7', blank=True) # Field name made lowercase.
    var_8 = models.FloatField(null=True, db_column='VAR_8', blank=True) # Field name made lowercase.
    var_9 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_9', blank=True) # Field name made lowercase.
    var_10 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_10', blank=True) # Field name made lowercase.
    var_11 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_11', blank=True) # Field name made lowercase.
    var_12 = models.FloatField(null=True, db_column='VAR_12', blank=True) # Field name made lowercase.
    var_13 = models.FloatField(null=True, db_column='VAR_13', blank=True) # Field name made lowercase.
    var_14 = models.FloatField(null=True, db_column='VAR_14', blank=True) # Field name made lowercase.
    var_15 = models.DecimalField(decimal_places=0, null=True, max_digits=2, db_column='VAR_15', blank=True) # Field name made lowercase.
    var_16 = models.DecimalField(decimal_places=0, null=True, max_digits=2, db_column='VAR_16', blank=True) # Field name made lowercase.
    var_17 = models.DecimalField(decimal_places=0, null=True, max_digits=2, db_column='VAR_17', blank=True) # Field name made lowercase.
    var_18 = models.DecimalField(decimal_places=0, null=True, max_digits=2, db_column='VAR_18', blank=True) # Field name made lowercase.
    var_19 = models.FloatField(null=True, db_column='VAR_19', blank=True) # Field name made lowercase.
    var_20 = models.FloatField(null=True, db_column='VAR_20', blank=True) # Field name made lowercase.
    var_21 = models.FloatField(null=True, db_column='VAR_21', blank=True) # Field name made lowercase.
    var_22 = models.FloatField(null=True, db_column='VAR_22', blank=True) # Field name made lowercase.
    var_23 = models.FloatField(null=True, db_column='VAR_23', blank=True) # Field name made lowercase.
    var_24 = models.FloatField(null=True, db_column='VAR_24', blank=True) # Field name made lowercase.
    var_25 = models.FloatField(null=True, db_column='VAR_25', blank=True) # Field name made lowercase.
    var_26 = models.FloatField(null=True, db_column='VAR_26', blank=True) # Field name made lowercase.
    var_27 = models.FloatField(null=True, db_column='VAR_27', blank=True) # Field name made lowercase.
    var_28 = models.FloatField(null=True, db_column='VAR_28', blank=True) # Field name made lowercase.
    var_29 = models.FloatField(null=True, db_column='VAR_29', blank=True) # Field name made lowercase.
    var_30 = models.FloatField(null=True, db_column='VAR_30', blank=True) # Field name made lowercase.
    var_31 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_31', blank=True) # Field name made lowercase.
    var_32 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_32', blank=True) # Field name made lowercase.
    var_33 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_33', blank=True) # Field name made lowercase.
    var_34 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_34', blank=True) # Field name made lowercase.
    var_35 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_35', blank=True) # Field name made lowercase.
    var_36 = models.FloatField(null=True, db_column='VAR_36', blank=True) # Field name made lowercase.
    var_37 = models.FloatField(null=True, db_column='VAR_37', blank=True) # Field name made lowercase.
    var_38 = models.FloatField(null=True, db_column='VAR_38', blank=True) # Field name made lowercase.
    var_39 = models.FloatField(null=True, db_column='VAR_39', blank=True) # Field name made lowercase.
    var_40 = models.FloatField(null=True, db_column='VAR_40', blank=True) # Field name made lowercase.
    var_41 = models.FloatField(null=True, db_column='VAR_41', blank=True) # Field name made lowercase.
    var_42 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_42', blank=True) # Field name made lowercase.
    var_43 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_43', blank=True) # Field name made lowercase.
    var_44 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_44', blank=True) # Field name made lowercase.
    var_45 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_45', blank=True) # Field name made lowercase.
    var_46 = models.FloatField(null=True, db_column='VAR_46', blank=True) # Field name made lowercase.
    var_47 = models.FloatField(null=True, db_column='VAR_47', blank=True) # Field name made lowercase.
    var_48 = models.FloatField(null=True, db_column='VAR_48', blank=True) # Field name made lowercase.
    var_49 = models.FloatField(null=True, db_column='VAR_49', blank=True) # Field name made lowercase.
    var_50 = models.FloatField(null=True, db_column='VAR_50', blank=True) # Field name made lowercase.
    var_51 = models.FloatField(null=True, db_column='VAR_51', blank=True) # Field name made lowercase.
    var_52 = models.FloatField(null=True, db_column='VAR_52', blank=True) # Field name made lowercase.
    var_53 = models.FloatField(null=True, db_column='VAR_53', blank=True) # Field name made lowercase.
    var_54 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_54', blank=True) # Field name made lowercase.
    var_55 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_55', blank=True) # Field name made lowercase.
    var_56 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_56', blank=True) # Field name made lowercase.
    var_57 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_57', blank=True) # Field name made lowercase.
    var_58 = models.FloatField(null=True, db_column='VAR_58', blank=True) # Field name made lowercase.
    var_59 = models.FloatField(null=True, db_column='VAR_59', blank=True) # Field name made lowercase.
    var_60 = models.FloatField(null=True, db_column='VAR_60', blank=True) # Field name made lowercase.
    var_61 = models.FloatField(null=True, db_column='VAR_61', blank=True) # Field name made lowercase.
    var_62 = models.FloatField(null=True, db_column='VAR_62', blank=True) # Field name made lowercase.
    var_63 = models.FloatField(null=True, db_column='VAR_63', blank=True) # Field name made lowercase.
    var_64 = models.FloatField(null=True, db_column='VAR_64', blank=True) # Field name made lowercase.
    var_65 = models.FloatField(null=True, db_column='VAR_65', blank=True) # Field name made lowercase.
    var_66 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_66', blank=True) # Field name made lowercase.
    var_67 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_67', blank=True) # Field name made lowercase.
    var_68 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_68', blank=True) # Field name made lowercase.
    var_69 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_69', blank=True) # Field name made lowercase.
    var_70 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_70', blank=True) # Field name made lowercase.
    var_71 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_71', blank=True) # Field name made lowercase.
    var_72 = models.FloatField(null=True, db_column='VAR_72', blank=True) # Field name made lowercase.
    var_73 = models.FloatField(null=True, db_column='VAR_73', blank=True) # Field name made lowercase.
    var_74 = models.FloatField(null=True, db_column='VAR_74', blank=True) # Field name made lowercase.
    var_75 = models.FloatField(null=True, db_column='VAR_75', blank=True) # Field name made lowercase.
    var_76 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_76', blank=True) # Field name made lowercase.
    var_77 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_77', blank=True) # Field name made lowercase.
    var_78 = models.FloatField(null=True, db_column='VAR_78', blank=True) # Field name made lowercase.
    var_79 = models.FloatField(null=True, db_column='VAR_79', blank=True) # Field name made lowercase.
    var_80 = models.FloatField(null=True, db_column='VAR_80', blank=True) # Field name made lowercase.
    var_81 = models.FloatField(null=True, db_column='VAR_81', blank=True) # Field name made lowercase.
    var_82 = models.FloatField(null=True, db_column='VAR_82', blank=True) # Field name made lowercase.
    var_83 = models.FloatField(null=True, db_column='VAR_83', blank=True) # Field name made lowercase.
    var_84 = models.FloatField(null=True, db_column='VAR_84', blank=True) # Field name made lowercase.
    var_85 = models.FloatField(null=True, db_column='VAR_85', blank=True) # Field name made lowercase.
    var_86 = models.FloatField(null=True, db_column='VAR_86', blank=True) # Field name made lowercase.
    var_87 = models.FloatField(null=True, db_column='VAR_87', blank=True) # Field name made lowercase.
    var_88 = models.FloatField(null=True, db_column='VAR_88', blank=True) # Field name made lowercase.
    var_89 = models.FloatField(null=True, db_column='VAR_89', blank=True) # Field name made lowercase.
    var_90 = models.FloatField(null=True, db_column='VAR_90', blank=True) # Field name made lowercase.
    var_91 = models.FloatField(null=True, db_column='VAR_91', blank=True) # Field name made lowercase.
    var_92 = models.FloatField(null=True, db_column='VAR_92', blank=True) # Field name made lowercase.
    var_93 = models.FloatField(null=True, db_column='VAR_93', blank=True) # Field name made lowercase.
    var_94 = models.FloatField(null=True, db_column='VAR_94', blank=True) # Field name made lowercase.
    var_95 = models.FloatField(null=True, db_column='VAR_95', blank=True) # Field name made lowercase.
    var_96 = models.FloatField(null=True, db_column='VAR_96', blank=True) # Field name made lowercase.
    var_97 = models.FloatField(null=True, db_column='VAR_97', blank=True) # Field name made lowercase.
    var_98 = models.FloatField(null=True, db_column='VAR_98', blank=True) # Field name made lowercase.
    var_99 = models.FloatField(null=True, db_column='VAR_99', blank=True) # Field name made lowercase.
    var_100 = models.FloatField(null=True, db_column='VAR_100', blank=True) # Field name made lowercase.
    var_101 = models.FloatField(null=True, db_column='VAR_101', blank=True) # Field name made lowercase.
    var_102 = models.FloatField(null=True, db_column='VAR_102', blank=True) # Field name made lowercase.
    var_103 = models.FloatField(null=True, db_column='VAR_103', blank=True) # Field name made lowercase.
    var_104 = models.FloatField(null=True, db_column='VAR_104', blank=True) # Field name made lowercase.
    var_105 = models.FloatField(null=True, db_column='VAR_105', blank=True) # Field name made lowercase.
    var_106 = models.FloatField(null=True, db_column='VAR_106', blank=True) # Field name made lowercase.
    var_107 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_107', blank=True) # Field name made lowercase.
    var_108 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_108', blank=True) # Field name made lowercase.
    var_109 = models.FloatField(null=True, db_column='VAR_109', blank=True) # Field name made lowercase.
    var_110 = models.FloatField(null=True, db_column='VAR_110', blank=True) # Field name made lowercase.
    var_111 = models.FloatField(null=True, db_column='VAR_111', blank=True) # Field name made lowercase.
    var_112 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_112', blank=True) # Field name made lowercase.
    var_113 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_113', blank=True) # Field name made lowercase.
    var_114 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_114', blank=True) # Field name made lowercase.
    var_115 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_115', blank=True) # Field name made lowercase.
    var_116 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_116', blank=True) # Field name made lowercase.
    var_117 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_117', blank=True) # Field name made lowercase.
    var_118 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_118', blank=True) # Field name made lowercase.
    var_119 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_119', blank=True) # Field name made lowercase.
    var_120 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_120', blank=True) # Field name made lowercase.
    var_121 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_121', blank=True) # Field name made lowercase.
    var_122 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_122', blank=True) # Field name made lowercase.
    var_123 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_123', blank=True) # Field name made lowercase.
    var_124 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_124', blank=True) # Field name made lowercase.
    var_125 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_125', blank=True) # Field name made lowercase.
    var_126 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_126', blank=True) # Field name made lowercase.
    var_127 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_127', blank=True) # Field name made lowercase.
    var_128 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_128', blank=True) # Field name made lowercase.
    var_129 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_129', blank=True) # Field name made lowercase.
    var_130 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_130', blank=True) # Field name made lowercase.
    var_131 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_131', blank=True) # Field name made lowercase.
    var_132 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_132', blank=True) # Field name made lowercase.
    var_133 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_133', blank=True) # Field name made lowercase.
    var_134 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_134', blank=True) # Field name made lowercase.
    var_135 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_135', blank=True) # Field name made lowercase.
    var_136 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_136', blank=True) # Field name made lowercase.
    var_137 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_137', blank=True) # Field name made lowercase.
    var_138 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_138', blank=True) # Field name made lowercase.
    var_139 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_139', blank=True) # Field name made lowercase.
    var_140 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_140', blank=True) # Field name made lowercase.
    var_141 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_141', blank=True) # Field name made lowercase.
    var_142 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_142', blank=True) # Field name made lowercase.
    var_143 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_143', blank=True) # Field name made lowercase.
    var_144 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_144', blank=True) # Field name made lowercase.
    var_145 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_145', blank=True) # Field name made lowercase.
    var_146 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_146', blank=True) # Field name made lowercase.
    var_147 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_147', blank=True) # Field name made lowercase.
    var_148 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_148', blank=True) # Field name made lowercase.
    var_149 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_149', blank=True) # Field name made lowercase.
    var_150 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_150', blank=True) # Field name made lowercase.
    var_151 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_151', blank=True) # Field name made lowercase.
    var_152 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_152', blank=True) # Field name made lowercase.
    var_153 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_153', blank=True) # Field name made lowercase.
    var_154 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_154', blank=True) # Field name made lowercase.
    var_155 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_155', blank=True) # Field name made lowercase.
    var_156 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_156', blank=True) # Field name made lowercase.
    var_157 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_157', blank=True) # Field name made lowercase.
    var_158 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_158', blank=True) # Field name made lowercase.
    var_159 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_159', blank=True) # Field name made lowercase.
    var_160 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_160', blank=True) # Field name made lowercase.
    var_161 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_161', blank=True) # Field name made lowercase.
    var_162 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_162', blank=True) # Field name made lowercase.
    var_163 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_163', blank=True) # Field name made lowercase.
    var_164 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_164', blank=True) # Field name made lowercase.
    var_165 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_165', blank=True) # Field name made lowercase.
    var_166 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_166', blank=True) # Field name made lowercase.
    var_167 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_167', blank=True) # Field name made lowercase.
    var_168 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_168', blank=True) # Field name made lowercase.
    var_169 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_169', blank=True) # Field name made lowercase.
    var_170 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_170', blank=True) # Field name made lowercase.
    var_171 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_171', blank=True) # Field name made lowercase.
    var_172 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_172', blank=True) # Field name made lowercase.
    var_173 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_173', blank=True) # Field name made lowercase.
    var_174 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_174', blank=True) # Field name made lowercase.
    var_175 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_175', blank=True) # Field name made lowercase.
    var_176 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_176', blank=True) # Field name made lowercase.
    var_177 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_177', blank=True) # Field name made lowercase.
    var_178 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_178', blank=True) # Field name made lowercase.
    var_179 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_179', blank=True) # Field name made lowercase.
    var_180 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_180', blank=True) # Field name made lowercase.
    var_181 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_181', blank=True) # Field name made lowercase.
    var_182 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_182', blank=True) # Field name made lowercase.
    var_183 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_183', blank=True) # Field name made lowercase.
    var_184 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_184', blank=True) # Field name made lowercase.
    var_185 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_185', blank=True) # Field name made lowercase.
    var_186 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_186', blank=True) # Field name made lowercase.
    var_187 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_187', blank=True) # Field name made lowercase.
    var_188 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_188', blank=True) # Field name made lowercase.
    var_189 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_189', blank=True) # Field name made lowercase.
    var_190 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_190', blank=True) # Field name made lowercase.
    var_191 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_191', blank=True) # Field name made lowercase.
    var_192 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_192', blank=True) # Field name made lowercase.
    var_193 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_193', blank=True) # Field name made lowercase.
    var_194 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_194', blank=True) # Field name made lowercase.
    var_195 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_195', blank=True) # Field name made lowercase.
    var_196 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_196', blank=True) # Field name made lowercase.
    var_197 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_197', blank=True) # Field name made lowercase.
    var_198 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_198', blank=True) # Field name made lowercase.
    var_199 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_199', blank=True) # Field name made lowercase.
    var_200 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_200', blank=True) # Field name made lowercase.
    var_201 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_201', blank=True) # Field name made lowercase.
    var_202 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_202', blank=True) # Field name made lowercase.
    var_203 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_203', blank=True) # Field name made lowercase.
    var_204 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_204', blank=True) # Field name made lowercase.
    var_205 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_205', blank=True) # Field name made lowercase.
    var_206 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_206', blank=True) # Field name made lowercase.
    var_207 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_207', blank=True) # Field name made lowercase.
    var_208 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_208', blank=True) # Field name made lowercase.
    var_209 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_209', blank=True) # Field name made lowercase.
    var_210 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_210', blank=True) # Field name made lowercase.
    var_211 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_211', blank=True) # Field name made lowercase.
    var_212 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_212', blank=True) # Field name made lowercase.
    var_213 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_213', blank=True) # Field name made lowercase.
    var_214 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_214', blank=True) # Field name made lowercase.
    var_215 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_215', blank=True) # Field name made lowercase.
    var_216 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_216', blank=True) # Field name made lowercase.
    var_217 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_217', blank=True) # Field name made lowercase.
    var_218 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_218', blank=True) # Field name made lowercase.
    var_219 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_219', blank=True) # Field name made lowercase.
    var_220 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_220', blank=True) # Field name made lowercase.
    var_221 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_221', blank=True) # Field name made lowercase.
    var_222 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_222', blank=True) # Field name made lowercase.
    var_223 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_223', blank=True) # Field name made lowercase.
    var_224 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_224', blank=True) # Field name made lowercase.
    var_225 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_225', blank=True) # Field name made lowercase.
    var_226 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_226', blank=True) # Field name made lowercase.
    var_227 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_227', blank=True) # Field name made lowercase.
    var_228 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_228', blank=True) # Field name made lowercase.
    var_229 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_229', blank=True) # Field name made lowercase.
    var_230 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_230', blank=True) # Field name made lowercase.
    var_231 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_231', blank=True) # Field name made lowercase.
    var_232 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_232', blank=True) # Field name made lowercase.
    var_233 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_233', blank=True) # Field name made lowercase.
    var_234 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_234', blank=True) # Field name made lowercase.
    var_235 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_235', blank=True) # Field name made lowercase.
    var_236 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_236', blank=True) # Field name made lowercase.
    var_237 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_237', blank=True) # Field name made lowercase.
    var_238 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_238', blank=True) # Field name made lowercase.
    var_239 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_239', blank=True) # Field name made lowercase.
    var_240 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_240', blank=True) # Field name made lowercase.
    var_241 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_241', blank=True) # Field name made lowercase.
    var_242 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_242', blank=True) # Field name made lowercase.
    var_243 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_243', blank=True) # Field name made lowercase.
    var_244 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_244', blank=True) # Field name made lowercase.
    var_245 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_245', blank=True) # Field name made lowercase.
    var_246 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_246', blank=True) # Field name made lowercase.
    var_247 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_247', blank=True) # Field name made lowercase.
    var_248 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_248', blank=True) # Field name made lowercase.
    var_249 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_249', blank=True) # Field name made lowercase.
    var_250 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_250', blank=True) # Field name made lowercase.
    var_251 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_251', blank=True) # Field name made lowercase.
    var_252 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_252', blank=True) # Field name made lowercase.
    var_253 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_253', blank=True) # Field name made lowercase.
    var_254 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_254', blank=True) # Field name made lowercase.
    var_255 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_255', blank=True) # Field name made lowercase.
    var_256 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_256', blank=True) # Field name made lowercase.
    var_257 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_257', blank=True) # Field name made lowercase.
    var_258 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_258', blank=True) # Field name made lowercase.
    var_259 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_259', blank=True) # Field name made lowercase.
    var_260 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_260', blank=True) # Field name made lowercase.
    var_261 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_261', blank=True) # Field name made lowercase.
    var_262 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_262', blank=True) # Field name made lowercase.
    var_263 = models.FloatField(null=True, db_column='VAR_263', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'pool_collection_data'

class PoolCollectionData1(models.Model):
    id = models.DecimalField(decimal_places=0, primary_key=True, db_column='ID', max_digits=11) # Field name made lowercase.
    oid_1 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='OID_1', blank=True) # Field name made lowercase.
    oid_2 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='OID_2', blank=True) # Field name made lowercase.
    var_1_oid_1 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_1_OID_1', blank=True) # Field name made lowercase.
    var_1_oid_2 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_1_OID_2', blank=True) # Field name made lowercase.
    var_2_oid_1 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_2_OID_1', blank=True) # Field name made lowercase.
    var_2_oid_2 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_2_OID_2', blank=True) # Field name made lowercase.
    var_3 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_3', blank=True) # Field name made lowercase.
    var_4 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_4', blank=True) # Field name made lowercase.
    var_5 = models.FloatField(null=True, db_column='VAR_5', blank=True) # Field name made lowercase.
    var_6 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_6', blank=True) # Field name made lowercase.
    var_7 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_7', blank=True) # Field name made lowercase.
    var_8 = models.FloatField(null=True, db_column='VAR_8', blank=True) # Field name made lowercase.
    var_9 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_9', blank=True) # Field name made lowercase.
    var_10 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_10', blank=True) # Field name made lowercase.
    var_11 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_11', blank=True) # Field name made lowercase.
    var_12 = models.FloatField(null=True, db_column='VAR_12', blank=True) # Field name made lowercase.
    var_13 = models.FloatField(null=True, db_column='VAR_13', blank=True) # Field name made lowercase.
    var_14 = models.FloatField(null=True, db_column='VAR_14', blank=True) # Field name made lowercase.
    var_15 = models.DecimalField(decimal_places=0, null=True, max_digits=2, db_column='VAR_15', blank=True) # Field name made lowercase.
    var_16 = models.DecimalField(decimal_places=0, null=True, max_digits=2, db_column='VAR_16', blank=True) # Field name made lowercase.
    var_17 = models.DecimalField(decimal_places=0, null=True, max_digits=2, db_column='VAR_17', blank=True) # Field name made lowercase.
    var_18 = models.DecimalField(decimal_places=0, null=True, max_digits=2, db_column='VAR_18', blank=True) # Field name made lowercase.
    var_19 = models.FloatField(null=True, db_column='VAR_19', blank=True) # Field name made lowercase.
    var_20 = models.FloatField(null=True, db_column='VAR_20', blank=True) # Field name made lowercase.
    var_21 = models.FloatField(null=True, db_column='VAR_21', blank=True) # Field name made lowercase.
    var_22 = models.FloatField(null=True, db_column='VAR_22', blank=True) # Field name made lowercase.
    var_23 = models.FloatField(null=True, db_column='VAR_23', blank=True) # Field name made lowercase.
    var_24 = models.FloatField(null=True, db_column='VAR_24', blank=True) # Field name made lowercase.
    var_25 = models.FloatField(null=True, db_column='VAR_25', blank=True) # Field name made lowercase.
    var_26 = models.FloatField(null=True, db_column='VAR_26', blank=True) # Field name made lowercase.
    var_27 = models.FloatField(null=True, db_column='VAR_27', blank=True) # Field name made lowercase.
    var_28 = models.FloatField(null=True, db_column='VAR_28', blank=True) # Field name made lowercase.
    var_29 = models.FloatField(null=True, db_column='VAR_29', blank=True) # Field name made lowercase.
    var_30 = models.FloatField(null=True, db_column='VAR_30', blank=True) # Field name made lowercase.
    var_31 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_31', blank=True) # Field name made lowercase.
    var_32 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_32', blank=True) # Field name made lowercase.
    var_33 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_33', blank=True) # Field name made lowercase.
    var_34 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_34', blank=True) # Field name made lowercase.
    var_35 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_35', blank=True) # Field name made lowercase.
    var_36 = models.FloatField(null=True, db_column='VAR_36', blank=True) # Field name made lowercase.
    var_37 = models.FloatField(null=True, db_column='VAR_37', blank=True) # Field name made lowercase.
    var_38 = models.FloatField(null=True, db_column='VAR_38', blank=True) # Field name made lowercase.
    var_39 = models.FloatField(null=True, db_column='VAR_39', blank=True) # Field name made lowercase.
    var_40 = models.FloatField(null=True, db_column='VAR_40', blank=True) # Field name made lowercase.
    var_41 = models.FloatField(null=True, db_column='VAR_41', blank=True) # Field name made lowercase.
    var_42 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_42', blank=True) # Field name made lowercase.
    var_43 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_43', blank=True) # Field name made lowercase.
    var_44 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_44', blank=True) # Field name made lowercase.
    var_45 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_45', blank=True) # Field name made lowercase.
    var_46 = models.FloatField(null=True, db_column='VAR_46', blank=True) # Field name made lowercase.
    var_47 = models.FloatField(null=True, db_column='VAR_47', blank=True) # Field name made lowercase.
    var_48 = models.FloatField(null=True, db_column='VAR_48', blank=True) # Field name made lowercase.
    var_49 = models.FloatField(null=True, db_column='VAR_49', blank=True) # Field name made lowercase.
    var_50 = models.FloatField(null=True, db_column='VAR_50', blank=True) # Field name made lowercase.
    var_51 = models.FloatField(null=True, db_column='VAR_51', blank=True) # Field name made lowercase.
    var_52 = models.FloatField(null=True, db_column='VAR_52', blank=True) # Field name made lowercase.
    var_53 = models.FloatField(null=True, db_column='VAR_53', blank=True) # Field name made lowercase.
    var_54 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_54', blank=True) # Field name made lowercase.
    var_55 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_55', blank=True) # Field name made lowercase.
    var_56 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_56', blank=True) # Field name made lowercase.
    var_57 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_57', blank=True) # Field name made lowercase.
    var_58 = models.FloatField(null=True, db_column='VAR_58', blank=True) # Field name made lowercase.
    var_59 = models.FloatField(null=True, db_column='VAR_59', blank=True) # Field name made lowercase.
    var_60 = models.FloatField(null=True, db_column='VAR_60', blank=True) # Field name made lowercase.
    var_61 = models.FloatField(null=True, db_column='VAR_61', blank=True) # Field name made lowercase.
    var_62 = models.FloatField(null=True, db_column='VAR_62', blank=True) # Field name made lowercase.
    var_63 = models.FloatField(null=True, db_column='VAR_63', blank=True) # Field name made lowercase.
    var_64 = models.FloatField(null=True, db_column='VAR_64', blank=True) # Field name made lowercase.
    var_65 = models.FloatField(null=True, db_column='VAR_65', blank=True) # Field name made lowercase.
    var_66 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_66', blank=True) # Field name made lowercase.
    var_67 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_67', blank=True) # Field name made lowercase.
    var_68 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_68', blank=True) # Field name made lowercase.
    var_69 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_69', blank=True) # Field name made lowercase.
    var_70 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_70', blank=True) # Field name made lowercase.
    var_71 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_71', blank=True) # Field name made lowercase.
    var_72 = models.FloatField(null=True, db_column='VAR_72', blank=True) # Field name made lowercase.
    var_73 = models.FloatField(null=True, db_column='VAR_73', blank=True) # Field name made lowercase.
    var_74 = models.FloatField(null=True, db_column='VAR_74', blank=True) # Field name made lowercase.
    var_75 = models.FloatField(null=True, db_column='VAR_75', blank=True) # Field name made lowercase.
    var_76 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_76', blank=True) # Field name made lowercase.
    var_77 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_77', blank=True) # Field name made lowercase.
    var_78 = models.FloatField(null=True, db_column='VAR_78', blank=True) # Field name made lowercase.
    var_79 = models.FloatField(null=True, db_column='VAR_79', blank=True) # Field name made lowercase.
    var_80 = models.FloatField(null=True, db_column='VAR_80', blank=True) # Field name made lowercase.
    var_81 = models.FloatField(null=True, db_column='VAR_81', blank=True) # Field name made lowercase.
    var_82 = models.FloatField(null=True, db_column='VAR_82', blank=True) # Field name made lowercase.
    var_83 = models.FloatField(null=True, db_column='VAR_83', blank=True) # Field name made lowercase.
    var_84 = models.FloatField(null=True, db_column='VAR_84', blank=True) # Field name made lowercase.
    var_85 = models.FloatField(null=True, db_column='VAR_85', blank=True) # Field name made lowercase.
    var_86 = models.FloatField(null=True, db_column='VAR_86', blank=True) # Field name made lowercase.
    var_87 = models.FloatField(null=True, db_column='VAR_87', blank=True) # Field name made lowercase.
    var_88 = models.FloatField(null=True, db_column='VAR_88', blank=True) # Field name made lowercase.
    var_89 = models.FloatField(null=True, db_column='VAR_89', blank=True) # Field name made lowercase.
    var_90 = models.FloatField(null=True, db_column='VAR_90', blank=True) # Field name made lowercase.
    var_91 = models.FloatField(null=True, db_column='VAR_91', blank=True) # Field name made lowercase.
    var_92 = models.FloatField(null=True, db_column='VAR_92', blank=True) # Field name made lowercase.
    var_93 = models.FloatField(null=True, db_column='VAR_93', blank=True) # Field name made lowercase.
    var_94 = models.FloatField(null=True, db_column='VAR_94', blank=True) # Field name made lowercase.
    var_95 = models.FloatField(null=True, db_column='VAR_95', blank=True) # Field name made lowercase.
    var_96 = models.FloatField(null=True, db_column='VAR_96', blank=True) # Field name made lowercase.
    var_97 = models.FloatField(null=True, db_column='VAR_97', blank=True) # Field name made lowercase.
    var_98 = models.FloatField(null=True, db_column='VAR_98', blank=True) # Field name made lowercase.
    var_99 = models.FloatField(null=True, db_column='VAR_99', blank=True) # Field name made lowercase.
    var_100 = models.FloatField(null=True, db_column='VAR_100', blank=True) # Field name made lowercase.
    var_101 = models.FloatField(null=True, db_column='VAR_101', blank=True) # Field name made lowercase.
    var_102 = models.FloatField(null=True, db_column='VAR_102', blank=True) # Field name made lowercase.
    var_103 = models.FloatField(null=True, db_column='VAR_103', blank=True) # Field name made lowercase.
    var_104 = models.FloatField(null=True, db_column='VAR_104', blank=True) # Field name made lowercase.
    var_105 = models.FloatField(null=True, db_column='VAR_105', blank=True) # Field name made lowercase.
    var_106 = models.FloatField(null=True, db_column='VAR_106', blank=True) # Field name made lowercase.
    var_107 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_107', blank=True) # Field name made lowercase.
    var_108 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_108', blank=True) # Field name made lowercase.
    var_109 = models.FloatField(null=True, db_column='VAR_109', blank=True) # Field name made lowercase.
    var_110 = models.FloatField(null=True, db_column='VAR_110', blank=True) # Field name made lowercase.
    var_111 = models.FloatField(null=True, db_column='VAR_111', blank=True) # Field name made lowercase.
    var_112 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_112', blank=True) # Field name made lowercase.
    var_113 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_113', blank=True) # Field name made lowercase.
    var_114 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_114', blank=True) # Field name made lowercase.
    var_115 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_115', blank=True) # Field name made lowercase.
    var_116 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_116', blank=True) # Field name made lowercase.
    var_117 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_117', blank=True) # Field name made lowercase.
    var_118 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_118', blank=True) # Field name made lowercase.
    var_119 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_119', blank=True) # Field name made lowercase.
    var_120 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_120', blank=True) # Field name made lowercase.
    var_121 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_121', blank=True) # Field name made lowercase.
    var_122 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_122', blank=True) # Field name made lowercase.
    var_123 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_123', blank=True) # Field name made lowercase.
    var_124 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_124', blank=True) # Field name made lowercase.
    var_125 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_125', blank=True) # Field name made lowercase.
    var_126 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_126', blank=True) # Field name made lowercase.
    var_127 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_127', blank=True) # Field name made lowercase.
    var_128 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_128', blank=True) # Field name made lowercase.
    var_129 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_129', blank=True) # Field name made lowercase.
    var_130 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_130', blank=True) # Field name made lowercase.
    var_131 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_131', blank=True) # Field name made lowercase.
    var_132 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_132', blank=True) # Field name made lowercase.
    var_133 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_133', blank=True) # Field name made lowercase.
    var_134 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_134', blank=True) # Field name made lowercase.
    var_135 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_135', blank=True) # Field name made lowercase.
    var_136 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_136', blank=True) # Field name made lowercase.
    var_137 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_137', blank=True) # Field name made lowercase.
    var_138 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_138', blank=True) # Field name made lowercase.
    var_139 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_139', blank=True) # Field name made lowercase.
    var_140 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_140', blank=True) # Field name made lowercase.
    var_141 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_141', blank=True) # Field name made lowercase.
    var_142 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_142', blank=True) # Field name made lowercase.
    var_143 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_143', blank=True) # Field name made lowercase.
    var_144 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_144', blank=True) # Field name made lowercase.
    var_145 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_145', blank=True) # Field name made lowercase.
    var_146 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_146', blank=True) # Field name made lowercase.
    var_147 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_147', blank=True) # Field name made lowercase.
    var_148 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_148', blank=True) # Field name made lowercase.
    var_149 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_149', blank=True) # Field name made lowercase.
    var_150 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_150', blank=True) # Field name made lowercase.
    var_151 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_151', blank=True) # Field name made lowercase.
    var_152 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_152', blank=True) # Field name made lowercase.
    var_153 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_153', blank=True) # Field name made lowercase.
    var_154 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_154', blank=True) # Field name made lowercase.
    var_155 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_155', blank=True) # Field name made lowercase.
    var_156 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_156', blank=True) # Field name made lowercase.
    var_157 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_157', blank=True) # Field name made lowercase.
    var_158 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_158', blank=True) # Field name made lowercase.
    var_159 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_159', blank=True) # Field name made lowercase.
    var_160 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_160', blank=True) # Field name made lowercase.
    var_161 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_161', blank=True) # Field name made lowercase.
    var_162 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_162', blank=True) # Field name made lowercase.
    var_163 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_163', blank=True) # Field name made lowercase.
    var_164 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_164', blank=True) # Field name made lowercase.
    var_165 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_165', blank=True) # Field name made lowercase.
    var_166 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_166', blank=True) # Field name made lowercase.
    var_167 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_167', blank=True) # Field name made lowercase.
    var_168 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_168', blank=True) # Field name made lowercase.
    var_169 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_169', blank=True) # Field name made lowercase.
    var_170 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_170', blank=True) # Field name made lowercase.
    var_171 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_171', blank=True) # Field name made lowercase.
    var_172 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_172', blank=True) # Field name made lowercase.
    var_173 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_173', blank=True) # Field name made lowercase.
    var_174 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_174', blank=True) # Field name made lowercase.
    var_175 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_175', blank=True) # Field name made lowercase.
    var_176 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_176', blank=True) # Field name made lowercase.
    var_177 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_177', blank=True) # Field name made lowercase.
    var_178 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_178', blank=True) # Field name made lowercase.
    var_179 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_179', blank=True) # Field name made lowercase.
    var_180 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_180', blank=True) # Field name made lowercase.
    var_181 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_181', blank=True) # Field name made lowercase.
    var_182 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_182', blank=True) # Field name made lowercase.
    var_183 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_183', blank=True) # Field name made lowercase.
    var_184 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_184', blank=True) # Field name made lowercase.
    var_185 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_185', blank=True) # Field name made lowercase.
    var_186 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_186', blank=True) # Field name made lowercase.
    var_187 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_187', blank=True) # Field name made lowercase.
    var_188 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_188', blank=True) # Field name made lowercase.
    var_189 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_189', blank=True) # Field name made lowercase.
    var_190 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_190', blank=True) # Field name made lowercase.
    var_191 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_191', blank=True) # Field name made lowercase.
    var_192 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_192', blank=True) # Field name made lowercase.
    var_193 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_193', blank=True) # Field name made lowercase.
    var_194 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_194', blank=True) # Field name made lowercase.
    var_195 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_195', blank=True) # Field name made lowercase.
    var_196 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_196', blank=True) # Field name made lowercase.
    var_197 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_197', blank=True) # Field name made lowercase.
    var_198 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_198', blank=True) # Field name made lowercase.
    var_199 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_199', blank=True) # Field name made lowercase.
    var_200 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_200', blank=True) # Field name made lowercase.
    var_201 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_201', blank=True) # Field name made lowercase.
    var_202 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_202', blank=True) # Field name made lowercase.
    var_203 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_203', blank=True) # Field name made lowercase.
    var_204 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_204', blank=True) # Field name made lowercase.
    var_205 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_205', blank=True) # Field name made lowercase.
    var_206 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_206', blank=True) # Field name made lowercase.
    var_207 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_207', blank=True) # Field name made lowercase.
    var_208 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_208', blank=True) # Field name made lowercase.
    var_209 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_209', blank=True) # Field name made lowercase.
    var_210 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_210', blank=True) # Field name made lowercase.
    var_211 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_211', blank=True) # Field name made lowercase.
    var_212 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_212', blank=True) # Field name made lowercase.
    var_213 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_213', blank=True) # Field name made lowercase.
    var_214 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_214', blank=True) # Field name made lowercase.
    var_215 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_215', blank=True) # Field name made lowercase.
    var_216 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_216', blank=True) # Field name made lowercase.
    var_217 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_217', blank=True) # Field name made lowercase.
    var_218 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_218', blank=True) # Field name made lowercase.
    var_219 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_219', blank=True) # Field name made lowercase.
    var_220 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_220', blank=True) # Field name made lowercase.
    var_221 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_221', blank=True) # Field name made lowercase.
    var_222 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_222', blank=True) # Field name made lowercase.
    var_223 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_223', blank=True) # Field name made lowercase.
    var_224 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_224', blank=True) # Field name made lowercase.
    var_225 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_225', blank=True) # Field name made lowercase.
    var_226 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_226', blank=True) # Field name made lowercase.
    var_227 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_227', blank=True) # Field name made lowercase.
    var_228 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_228', blank=True) # Field name made lowercase.
    var_229 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_229', blank=True) # Field name made lowercase.
    var_230 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_230', blank=True) # Field name made lowercase.
    var_231 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_231', blank=True) # Field name made lowercase.
    var_232 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_232', blank=True) # Field name made lowercase.
    var_233 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_233', blank=True) # Field name made lowercase.
    var_234 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_234', blank=True) # Field name made lowercase.
    var_235 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_235', blank=True) # Field name made lowercase.
    var_236 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_236', blank=True) # Field name made lowercase.
    var_237 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_237', blank=True) # Field name made lowercase.
    var_238 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_238', blank=True) # Field name made lowercase.
    var_239 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_239', blank=True) # Field name made lowercase.
    var_240 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_240', blank=True) # Field name made lowercase.
    var_241 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_241', blank=True) # Field name made lowercase.
    var_242 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_242', blank=True) # Field name made lowercase.
    var_243 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_243', blank=True) # Field name made lowercase.
    var_244 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_244', blank=True) # Field name made lowercase.
    var_245 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_245', blank=True) # Field name made lowercase.
    var_246 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_246', blank=True) # Field name made lowercase.
    var_247 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_247', blank=True) # Field name made lowercase.
    var_248 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_248', blank=True) # Field name made lowercase.
    var_249 = models.DecimalField(decimal_places=0, null=True, max_digits=6, db_column='VAR_249', blank=True) # Field name made lowercase.
    var_250 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_250', blank=True) # Field name made lowercase.
    var_251 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_251', blank=True) # Field name made lowercase.
    var_252 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_252', blank=True) # Field name made lowercase.
    var_253 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_253', blank=True) # Field name made lowercase.
    var_254 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_254', blank=True) # Field name made lowercase.
    var_255 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_255', blank=True) # Field name made lowercase.
    var_256 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_256', blank=True) # Field name made lowercase.
    var_257 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_257', blank=True) # Field name made lowercase.
    var_258 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_258', blank=True) # Field name made lowercase.
    var_259 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_259', blank=True) # Field name made lowercase.
    var_260 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_260', blank=True) # Field name made lowercase.
    var_261 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_261', blank=True) # Field name made lowercase.
    var_262 = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VAR_262', blank=True) # Field name made lowercase.
    var_263 = models.FloatField(null=True, db_column='VAR_263', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'pool_collection_data_1'

class PoolCollections(models.Model):
#    collection_name = models.CharField(max_length=1200, primary_key=True, db_column='COLLECTION_NAME') # Field name made lowercase.
    collection_name = models.CharField(db_column='COLLECTION_NAME', primary_key=True, max_length=255)  # Field name made lowercase.
    data_table_name = models.CharField(max_length=1200, db_column='DATA_TABLE_NAME', blank=True) # Field name made lowercase.
    links_table_name = models.CharField(max_length=1200, db_column='LINKS_TABLE_NAME', blank=True) # Field name made lowercase.
    records_written = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='RECORDS_WRITTEN', blank=True) # Field name made lowercase.
    records_deleted = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='RECORDS_DELETED', blank=True) # Field name made lowercase.
    child_collection_name = models.CharField(max_length=1200, db_column='CHILD_COLLECTION_NAME', blank=True) # Field name made lowercase.
    foreign_key_name = models.CharField(max_length=1200, db_column='FOREIGN_KEY_NAME', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'pool_collections'

class PoolCollectionsDesc(models.Model):
#    collection_name = models.CharField(max_length=1200, primary_key=True, db_column='COLLECTION_NAME') # Field name made lowercase.
    collection_name = models.CharField(max_length=255, primary_key=True, db_column='COLLECTION_NAME')  # Field name made lowercase.
    variable_name = models.CharField(max_length=1200, db_column='VARIABLE_NAME', blank=True) # Field name made lowercase.
    variable_type = models.CharField(max_length=1200, db_column='VARIABLE_TYPE', blank=True) # Field name made lowercase.
    variable_maximum_size = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VARIABLE_MAXIMUM_SIZE', blank=True) # Field name made lowercase.
    variable_size_is_fixed = models.CharField(max_length=15, db_column='VARIABLE_SIZE_IS_FIXED', blank=True) # Field name made lowercase.
    variable_position = models.DecimalField(decimal_places=0, null=True, max_digits=11, db_column='VARIABLE_POSITION', blank=True) # Field name made lowercase.
    variable_annotation = models.CharField(max_length=12000, db_column='VARIABLE_ANNOTATION', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'pool_collections_desc'

class ProdsysComm(models.Model):
    comm_task = models.BigIntegerField(primary_key=True, db_column='COMM_TASK') # Field name made lowercase.
    comm_meta = models.BigIntegerField(null=True, db_column='COMM_META', blank=True) # Field name made lowercase.
    comm_owner = models.CharField(max_length=48, db_column='COMM_OWNER', blank=True) # Field name made lowercase.
    comm_cmd = models.CharField(max_length=768, db_column='COMM_CMD', blank=True) # Field name made lowercase.
    comm_ts = models.BigIntegerField(null=True, db_column='COMM_TS', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'prodsys_comm'

class Productiondatasets(models.Model):
#    name = models.CharField(max_length=360, primary_key=True, db_column='NAME') # Field name made lowercase.
    name = models.CharField(max_length=255, primary_key=True, db_column='NAME')  # Field name made lowercase.
    version = models.IntegerField(null=True, db_column='VERSION', blank=True) # Field name made lowercase.
    vuid = models.CharField(max_length=120, db_column='VUID') # Field name made lowercase.
    files = models.IntegerField(null=True, db_column='FILES', blank=True) # Field name made lowercase.
    gb = models.IntegerField(null=True, db_column='GB', blank=True) # Field name made lowercase.
    events = models.IntegerField(null=True, db_column='EVENTS', blank=True) # Field name made lowercase.
    site = models.CharField(max_length=30, db_column='SITE', blank=True) # Field name made lowercase.
    sw_release = models.CharField(max_length=60, db_column='SW_RELEASE', blank=True) # Field name made lowercase.
    geometry = models.CharField(max_length=60, db_column='GEOMETRY', blank=True) # Field name made lowercase.
    jobid = models.IntegerField(null=True, db_column='JOBID', blank=True) # Field name made lowercase.
    pandaid = models.IntegerField(null=True, db_column='PANDAID', blank=True) # Field name made lowercase.
    prodtime = models.DateTimeField(null=True, db_column='PRODTIME', blank=True) # Field name made lowercase.
    timestamp = models.IntegerField(null=True, db_column='TIMESTAMP', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'productiondatasets'

class Proxykey(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    dn = models.CharField(max_length=300, db_column='DN') # Field name made lowercase.
    credname = models.CharField(max_length=120, db_column='CREDNAME') # Field name made lowercase.
    created = models.DateTimeField(db_column='CREATED') # Field name made lowercase.
    expires = models.DateTimeField(db_column='EXPIRES') # Field name made lowercase.
    origin = models.CharField(max_length=240, db_column='ORIGIN') # Field name made lowercase.
    myproxy = models.CharField(max_length=240, db_column='MYPROXY') # Field name made lowercase.
    class Meta:
        db_table = u'proxykey'

class Redirect(models.Model):
#    service = models.CharField(max_length=90, db_column='SERVICE') # Field name made lowercase.
#    type = models.CharField(max_length=90, db_column='TYPE') # Field name made lowercase.
#    site = models.CharField(max_length=90, db_column='SITE') # Field name made lowercase.
#    description = models.CharField(max_length=360, db_column='DESCRIPTION') # Field name made lowercase.
#    url = models.CharField(max_length=750, primary_key=True, db_column='URL') # Field name made lowercase.
#    testurl = models.CharField(max_length=750, db_column='TESTURL', blank=True) # Field name made lowercase.
#    response = models.CharField(max_length=90, db_column='RESPONSE') # Field name made lowercase.
#    aliveresponse = models.CharField(max_length=90, db_column='ALIVERESPONSE') # Field name made lowercase.
#    responsetime = models.IntegerField(null=True, db_column='RESPONSETIME', blank=True) # Field name made lowercase.
#    rank = models.IntegerField(null=True, db_column='RANK', blank=True) # Field name made lowercase.
#    performance = models.IntegerField(null=True, db_column='PERFORMANCE', blank=True) # Field name made lowercase.
#    status = models.CharField(max_length=90, db_column='STATUS') # Field name made lowercase.
#    log = models.CharField(max_length=750, db_column='LOG', blank=True) # Field name made lowercase.
#    statustime = models.DateTimeField(db_column='STATUSTIME') # Field name made lowercase.
#    usetime = models.DateTimeField(db_column='USETIME') # Field name made lowercase.
    service = models.CharField(db_column='SERVICE', max_length=30)  # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=30)  # Field name made lowercase.
    site = models.CharField(db_column='SITE', max_length=30)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=120)  # Field name made lowercase.
    url = models.CharField(db_column='URL', primary_key=True, max_length=250)  # Field name made lowercase.
    testurl = models.CharField(db_column='TESTURL', max_length=250, blank=True)  # Field name made lowercase.
    response = models.CharField(db_column='RESPONSE', max_length=30)  # Field name made lowercase.
    aliveresponse = models.CharField(db_column='ALIVERESPONSE', max_length=30)  # Field name made lowercase.
    responsetime = models.IntegerField(db_column='RESPONSETIME', blank=True, null=True)  # Field name made lowercase.
    rank = models.IntegerField(db_column='RANK', blank=True, null=True)  # Field name made lowercase.
    performance = models.IntegerField(db_column='PERFORMANCE', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=30)  # Field name made lowercase.
    log = models.CharField(db_column='LOG', max_length=250, blank=True)  # Field name made lowercase.
    statustime = models.DateTimeField(db_column='STATUSTIME') # Field name made lowercase.
    usetime = models.DateTimeField(db_column='USETIME') # Field name made lowercase.
    class Meta:
        db_table = u'redirect'

class Savedpages(models.Model):
    name = models.CharField(max_length=90, primary_key=True, db_column='NAME') # Field name made lowercase.
    flag = models.CharField(max_length=60, primary_key=True, db_column='FLAG') # Field name made lowercase.
    hours = models.IntegerField(primary_key=True, db_column='HOURS') # Field name made lowercase.
    html = models.TextField(db_column='HTML') # Field name made lowercase.
    lastmod = models.DateTimeField(null=True, db_column='LASTMOD', blank=True) # Field name made lowercase.
    interval = models.IntegerField(null=True, db_column='INTERVAL', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'savedpages'


class SchedconfigOld(models.Model):
    name = models.CharField(max_length=180, db_column='NAME') # Field name made lowercase.
    nickname = models.CharField(max_length=180, primary_key=True, db_column='NICKNAME') # Field name made lowercase.
    queue = models.CharField(max_length=180, db_column='QUEUE', blank=True) # Field name made lowercase.
    localqueue = models.CharField(max_length=60, db_column='LOCALQUEUE', blank=True) # Field name made lowercase.
    system = models.CharField(max_length=180, db_column='SYSTEM') # Field name made lowercase.
    sysconfig = models.CharField(max_length=60, db_column='SYSCONFIG', blank=True) # Field name made lowercase.
    environ = models.CharField(max_length=750, db_column='ENVIRON', blank=True) # Field name made lowercase.
    gatekeeper = models.CharField(max_length=120, db_column='GATEKEEPER', blank=True) # Field name made lowercase.
    jobmanager = models.CharField(max_length=240, db_column='JOBMANAGER', blank=True) # Field name made lowercase.
    se = models.CharField(max_length=750, db_column='SE', blank=True) # Field name made lowercase.
    ddm = models.CharField(max_length=360, db_column='DDM', blank=True) # Field name made lowercase.
    jdladd = models.CharField(max_length=1500, db_column='JDLADD', blank=True) # Field name made lowercase.
    globusadd = models.CharField(max_length=300, db_column='GLOBUSADD', blank=True) # Field name made lowercase.
    jdl = models.CharField(max_length=180, db_column='JDL', blank=True) # Field name made lowercase.
    jdltxt = models.CharField(max_length=1500, db_column='JDLTXT', blank=True) # Field name made lowercase.
    version = models.CharField(max_length=180, db_column='VERSION', blank=True) # Field name made lowercase.
    site = models.CharField(max_length=180, db_column='SITE') # Field name made lowercase.
    region = models.CharField(max_length=180, db_column='REGION', blank=True) # Field name made lowercase.
    gstat = models.CharField(max_length=180, db_column='GSTAT', blank=True) # Field name made lowercase.
    tags = models.CharField(max_length=600, db_column='TAGS', blank=True) # Field name made lowercase.
    cmd = models.CharField(max_length=600, db_column='CMD', blank=True) # Field name made lowercase.
    lastmod = models.DateTimeField(db_column='LASTMOD') # Field name made lowercase.
    errinfo = models.CharField(max_length=240, db_column='ERRINFO', blank=True) # Field name made lowercase.
    nqueue = models.IntegerField(db_column='NQUEUE') # Field name made lowercase.
#    comment_ = models.CharField(max_length=1500, db_column='COMMENT_', blank=True) # Field name made lowercase.
    comment_field = models.CharField(max_length=1500, db_column='COMMENT_', blank=True)  # Field name made lowercase.
    appdir = models.CharField(max_length=300, db_column='APPDIR', blank=True) # Field name made lowercase.
    datadir = models.CharField(max_length=240, db_column='DATADIR', blank=True) # Field name made lowercase.
    tmpdir = models.CharField(max_length=240, db_column='TMPDIR', blank=True) # Field name made lowercase.
    wntmpdir = models.CharField(max_length=240, db_column='WNTMPDIR', blank=True) # Field name made lowercase.
    dq2url = models.CharField(max_length=240, db_column='DQ2URL', blank=True) # Field name made lowercase.
    special_par = models.CharField(max_length=240, db_column='SPECIAL_PAR', blank=True) # Field name made lowercase.
    python_path = models.CharField(max_length=240, db_column='PYTHON_PATH', blank=True) # Field name made lowercase.
    nodes = models.IntegerField(db_column='NODES') # Field name made lowercase.
    status = models.CharField(max_length=30, db_column='STATUS', blank=True) # Field name made lowercase.
    copytool = models.CharField(max_length=240, db_column='COPYTOOL', blank=True) # Field name made lowercase.
    copysetup = models.CharField(max_length=600, db_column='COPYSETUP', blank=True) # Field name made lowercase.
    releases = models.CharField(max_length=1500, db_column='RELEASES', blank=True) # Field name made lowercase.
    sepath = models.CharField(max_length=450, db_column='SEPATH', blank=True) # Field name made lowercase.
    envsetup = models.CharField(max_length=600, db_column='ENVSETUP', blank=True) # Field name made lowercase.
    copyprefix = models.CharField(max_length=480, db_column='COPYPREFIX', blank=True) # Field name made lowercase.
    lfcpath = models.CharField(max_length=240, db_column='LFCPATH', blank=True) # Field name made lowercase.
    seopt = models.CharField(max_length=900, db_column='SEOPT', blank=True) # Field name made lowercase.
    sein = models.CharField(max_length=180, db_column='SEIN', blank=True) # Field name made lowercase.
    seinopt = models.CharField(max_length=180, db_column='SEINOPT', blank=True) # Field name made lowercase.
    lfchost = models.CharField(max_length=240, db_column='LFCHOST', blank=True) # Field name made lowercase.
    cloud = models.CharField(max_length=180, db_column='CLOUD', blank=True) # Field name made lowercase.
    siteid = models.CharField(max_length=180, db_column='SITEID', blank=True) # Field name made lowercase.
    proxy = models.CharField(max_length=240, db_column='PROXY', blank=True) # Field name made lowercase.
    retry = models.CharField(max_length=30, db_column='RETRY', blank=True) # Field name made lowercase.
    queuehours = models.IntegerField(db_column='QUEUEHOURS') # Field name made lowercase.
    envsetupin = models.CharField(max_length=600, db_column='ENVSETUPIN', blank=True) # Field name made lowercase.
    copytoolin = models.CharField(max_length=540, db_column='COPYTOOLIN', blank=True) # Field name made lowercase.
    copysetupin = models.CharField(max_length=600, db_column='COPYSETUPIN', blank=True) # Field name made lowercase.
    seprodpath = models.CharField(max_length=600, db_column='SEPRODPATH', blank=True) # Field name made lowercase.
    lfcprodpath = models.CharField(max_length=240, db_column='LFCPRODPATH', blank=True) # Field name made lowercase.
    copyprefixin = models.CharField(max_length=240, db_column='COPYPREFIXIN', blank=True) # Field name made lowercase.
    recoverdir = models.CharField(max_length=240, db_column='RECOVERDIR', blank=True) # Field name made lowercase.
    memory = models.IntegerField(db_column='MEMORY') # Field name made lowercase.
    maxtime = models.IntegerField(db_column='MAXTIME') # Field name made lowercase.
    space = models.IntegerField(db_column='SPACE') # Field name made lowercase.
    tspace = models.DateTimeField(db_column='TSPACE') # Field name made lowercase.
    cmtconfig = models.CharField(max_length=750, db_column='CMTCONFIG', blank=True) # Field name made lowercase.
    setokens = models.CharField(max_length=240, db_column='SETOKENS', blank=True) # Field name made lowercase.
    glexec = models.CharField(max_length=30, db_column='GLEXEC', blank=True) # Field name made lowercase.
    priorityoffset = models.CharField(max_length=180, db_column='PRIORITYOFFSET', blank=True) # Field name made lowercase.
    allowedgroups = models.CharField(max_length=300, db_column='ALLOWEDGROUPS', blank=True) # Field name made lowercase.
    defaulttoken = models.CharField(max_length=300, db_column='DEFAULTTOKEN', blank=True) # Field name made lowercase.
    pcache = models.CharField(max_length=300, db_column='PCACHE', blank=True) # Field name made lowercase.
    validatedreleases = models.CharField(max_length=1500, db_column='VALIDATEDRELEASES', blank=True) # Field name made lowercase.
    accesscontrol = models.CharField(max_length=60, db_column='ACCESSCONTROL', blank=True) # Field name made lowercase.
    dn = models.CharField(max_length=300, db_column='DN', blank=True) # Field name made lowercase.
    email = models.CharField(max_length=180, db_column='EMAIL', blank=True) # Field name made lowercase.
    allowednode = models.CharField(max_length=240, db_column='ALLOWEDNODE', blank=True) # Field name made lowercase.
    maxinputsize = models.IntegerField(null=True, db_column='MAXINPUTSIZE', blank=True) # Field name made lowercase.
    timefloor = models.IntegerField(null=True, db_column='TIMEFLOOR', blank=True) # Field name made lowercase.
    depthboost = models.IntegerField(null=True, db_column='DEPTHBOOST', blank=True) # Field name made lowercase.
    idlepilotsupression = models.IntegerField(null=True, db_column='IDLEPILOTSUPRESSION', blank=True) # Field name made lowercase.
    pilotlimit = models.IntegerField(null=True, db_column='PILOTLIMIT', blank=True) # Field name made lowercase.
    transferringlimit = models.IntegerField(null=True, db_column='TRANSFERRINGLIMIT', blank=True) # Field name made lowercase.
    cachedse = models.IntegerField(null=True, db_column='CACHEDSE', blank=True) # Field name made lowercase.
    corecount = models.IntegerField(null=True, db_column='CORECOUNT', blank=True) # Field name made lowercase.
    countrygroup = models.CharField(max_length=192, db_column='COUNTRYGROUP', blank=True) # Field name made lowercase.
    availablecpu = models.CharField(max_length=192, db_column='AVAILABLECPU', blank=True) # Field name made lowercase.
    availablestorage = models.CharField(max_length=192, db_column='AVAILABLESTORAGE', blank=True) # Field name made lowercase.
    pledgedcpu = models.CharField(max_length=192, db_column='PLEDGEDCPU', blank=True) # Field name made lowercase.
    pledgedstorage = models.CharField(max_length=192, db_column='PLEDGEDSTORAGE', blank=True) # Field name made lowercase.
    last_status = models.CharField(max_length=768, db_column='LAST_STATUS', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'schedconfig_old'

class Servicelist(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    name = models.CharField(max_length=180, db_column='NAME') # Field name made lowercase.
    host = models.CharField(max_length=300, db_column='HOST', blank=True) # Field name made lowercase.
    pid = models.IntegerField(null=True, db_column='PID', blank=True) # Field name made lowercase.
    userid = models.CharField(max_length=120, db_column='USERID', blank=True) # Field name made lowercase.
    type = models.CharField(max_length=90, db_column='TYPE', blank=True) # Field name made lowercase.
    grp = models.CharField(max_length=60, db_column='GRP', blank=True) # Field name made lowercase.
    description = models.CharField(max_length=600, db_column='DESCRIPTION', blank=True) # Field name made lowercase.
    url = models.CharField(max_length=600, db_column='URL', blank=True) # Field name made lowercase.
    testurl = models.CharField(max_length=600, db_column='TESTURL', blank=True) # Field name made lowercase.
    response = models.CharField(max_length=600, db_column='RESPONSE', blank=True) # Field name made lowercase.
    tresponse = models.IntegerField(null=True, db_column='TRESPONSE', blank=True) # Field name made lowercase.
    tstart = models.DateTimeField(db_column='TSTART') # Field name made lowercase.
    tstop = models.DateTimeField(db_column='TSTOP') # Field name made lowercase.
    tcheck = models.DateTimeField(db_column='TCHECK') # Field name made lowercase.
    cyclesec = models.IntegerField(null=True, db_column='CYCLESEC', blank=True) # Field name made lowercase.
    status = models.CharField(max_length=60, db_column='STATUS') # Field name made lowercase.
    lastmod = models.DateTimeField(db_column='LASTMOD') # Field name made lowercase.
    config = models.CharField(max_length=600, db_column='CONFIG', blank=True) # Field name made lowercase.
    message = models.CharField(max_length=12000, db_column='MESSAGE', blank=True) # Field name made lowercase.
    restartcmd = models.CharField(max_length=12000, db_column='RESTARTCMD', blank=True) # Field name made lowercase.
    doaction = models.CharField(max_length=12000, db_column='DOACTION', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'servicelist'

class Siteaccess(models.Model):
    id = models.BigIntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    dn = models.CharField(max_length=300, db_column='DN', blank=True) # Field name made lowercase.
    pandasite = models.CharField(max_length=300, db_column='PANDASITE', blank=True) # Field name made lowercase.
    poffset = models.BigIntegerField(db_column='POFFSET') # Field name made lowercase.
    rights = models.CharField(max_length=90, db_column='RIGHTS', blank=True) # Field name made lowercase.
    status = models.CharField(max_length=60, db_column='STATUS', blank=True) # Field name made lowercase.
    workinggroups = models.CharField(max_length=300, db_column='WORKINGGROUPS', blank=True) # Field name made lowercase.
    created = models.DateTimeField(null=True, db_column='CREATED', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'siteaccess'

class Sitedata(models.Model):
    site = models.CharField(max_length=90, primary_key=True, db_column='SITE') # Field name made lowercase.
    flag = models.CharField(max_length=60, primary_key=True, db_column='FLAG') # Field name made lowercase.
    hours = models.IntegerField(primary_key=True, db_column='HOURS') # Field name made lowercase.
    nwn = models.IntegerField(null=True, db_column='NWN', blank=True) # Field name made lowercase.
    memmin = models.IntegerField(null=True, db_column='MEMMIN', blank=True) # Field name made lowercase.
    memmax = models.IntegerField(null=True, db_column='MEMMAX', blank=True) # Field name made lowercase.
    si2000min = models.IntegerField(null=True, db_column='SI2000MIN', blank=True) # Field name made lowercase.
    si2000max = models.IntegerField(null=True, db_column='SI2000MAX', blank=True) # Field name made lowercase.
    os = models.CharField(max_length=90, db_column='OS', blank=True) # Field name made lowercase.
    space = models.CharField(max_length=90, db_column='SPACE', blank=True) # Field name made lowercase.
    minjobs = models.IntegerField(null=True, db_column='MINJOBS', blank=True) # Field name made lowercase.
    maxjobs = models.IntegerField(null=True, db_column='MAXJOBS', blank=True) # Field name made lowercase.
    laststart = models.DateTimeField(null=True, db_column='LASTSTART', blank=True) # Field name made lowercase.
    lastend = models.DateTimeField(null=True, db_column='LASTEND', blank=True) # Field name made lowercase.
    lastfail = models.DateTimeField(null=True, db_column='LASTFAIL', blank=True) # Field name made lowercase.
    lastpilot = models.DateTimeField(null=True, db_column='LASTPILOT', blank=True) # Field name made lowercase.
    lastpid = models.IntegerField(null=True, db_column='LASTPID', blank=True) # Field name made lowercase.
    nstart = models.IntegerField(db_column='NSTART') # Field name made lowercase.
    finished = models.IntegerField(db_column='FINISHED') # Field name made lowercase.
    failed = models.IntegerField(db_column='FAILED') # Field name made lowercase.
    defined = models.IntegerField(db_column='DEFINED') # Field name made lowercase.
    assigned = models.IntegerField(db_column='ASSIGNED') # Field name made lowercase.
    waiting = models.IntegerField(db_column='WAITING') # Field name made lowercase.
    activated = models.IntegerField(db_column='ACTIVATED') # Field name made lowercase.
    holding = models.IntegerField(db_column='HOLDING') # Field name made lowercase.
    running = models.IntegerField(db_column='RUNNING') # Field name made lowercase.
    transferring = models.IntegerField(db_column='TRANSFERRING') # Field name made lowercase.
    getjob = models.IntegerField(db_column='GETJOB') # Field name made lowercase.
    updatejob = models.IntegerField(db_column='UPDATEJOB') # Field name made lowercase.
    lastmod = models.DateTimeField(db_column='LASTMOD') # Field name made lowercase.
    ncpu = models.IntegerField(null=True, db_column='NCPU', blank=True) # Field name made lowercase.
    nslot = models.IntegerField(null=True, db_column='NSLOT', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'sitedata'

class SitedataOld(models.Model):
    site = models.CharField(max_length=90, primary_key=True, db_column='SITE') # Field name made lowercase.
    flag = models.CharField(max_length=60, primary_key=True, db_column='FLAG') # Field name made lowercase.
    hours = models.IntegerField(primary_key=True, db_column='HOURS') # Field name made lowercase.
    nwn = models.IntegerField(null=True, db_column='NWN', blank=True) # Field name made lowercase.
    memmin = models.IntegerField(null=True, db_column='MEMMIN', blank=True) # Field name made lowercase.
    memmax = models.IntegerField(null=True, db_column='MEMMAX', blank=True) # Field name made lowercase.
    si2000min = models.IntegerField(null=True, db_column='SI2000MIN', blank=True) # Field name made lowercase.
    si2000max = models.IntegerField(null=True, db_column='SI2000MAX', blank=True) # Field name made lowercase.
    os = models.CharField(max_length=90, db_column='OS', blank=True) # Field name made lowercase.
    space = models.CharField(max_length=90, db_column='SPACE', blank=True) # Field name made lowercase.
    minjobs = models.IntegerField(null=True, db_column='MINJOBS', blank=True) # Field name made lowercase.
    maxjobs = models.IntegerField(null=True, db_column='MAXJOBS', blank=True) # Field name made lowercase.
    laststart = models.DateTimeField(null=True, db_column='LASTSTART', blank=True) # Field name made lowercase.
    lastend = models.DateTimeField(null=True, db_column='LASTEND', blank=True) # Field name made lowercase.
    lastfail = models.DateTimeField(null=True, db_column='LASTFAIL', blank=True) # Field name made lowercase.
    lastpilot = models.DateTimeField(null=True, db_column='LASTPILOT', blank=True) # Field name made lowercase.
    lastpid = models.IntegerField(null=True, db_column='LASTPID', blank=True) # Field name made lowercase.
    nstart = models.IntegerField(db_column='NSTART') # Field name made lowercase.
    finished = models.IntegerField(db_column='FINISHED') # Field name made lowercase.
    failed = models.IntegerField(db_column='FAILED') # Field name made lowercase.
    defined = models.IntegerField(db_column='DEFINED') # Field name made lowercase.
    assigned = models.IntegerField(db_column='ASSIGNED') # Field name made lowercase.
    waiting = models.IntegerField(db_column='WAITING') # Field name made lowercase.
    activated = models.IntegerField(db_column='ACTIVATED') # Field name made lowercase.
    holding = models.IntegerField(db_column='HOLDING') # Field name made lowercase.
    running = models.IntegerField(db_column='RUNNING') # Field name made lowercase.
    transferring = models.IntegerField(db_column='TRANSFERRING') # Field name made lowercase.
    getjob = models.IntegerField(db_column='GETJOB') # Field name made lowercase.
    updatejob = models.IntegerField(db_column='UPDATEJOB') # Field name made lowercase.
    lastmod = models.DateTimeField(db_column='LASTMOD') # Field name made lowercase.
    ncpu = models.IntegerField(null=True, db_column='NCPU', blank=True) # Field name made lowercase.
    nslot = models.IntegerField(null=True, db_column='NSLOT', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'sitedata_old'

class Siteddm(models.Model):
    name = models.CharField(max_length=180, primary_key=True, db_column='NAME') # Field name made lowercase.
    incmd = models.CharField(max_length=180, db_column='INCMD') # Field name made lowercase.
    inpath = models.CharField(max_length=600, db_column='INPATH', blank=True) # Field name made lowercase.
    inopts = models.CharField(max_length=180, db_column='INOPTS', blank=True) # Field name made lowercase.
    outcmd = models.CharField(max_length=180, db_column='OUTCMD') # Field name made lowercase.
    outopts = models.CharField(max_length=180, db_column='OUTOPTS', blank=True) # Field name made lowercase.
    outpath = models.CharField(max_length=600, db_column='OUTPATH') # Field name made lowercase.
    class Meta:
        db_table = u'siteddm'

class Sitehistory(models.Model):
    site = models.CharField(max_length=90, primary_key=True, db_column='SITE') # Field name made lowercase.
    flag = models.CharField(max_length=60, primary_key=True, db_column='FLAG') # Field name made lowercase.
    time = models.DateTimeField(primary_key=True, db_column='TIME') # Field name made lowercase.
    hours = models.IntegerField(primary_key=True, db_column='HOURS') # Field name made lowercase.
    nwn = models.IntegerField(null=True, db_column='NWN', blank=True) # Field name made lowercase.
    memmin = models.IntegerField(null=True, db_column='MEMMIN', blank=True) # Field name made lowercase.
    memmax = models.IntegerField(null=True, db_column='MEMMAX', blank=True) # Field name made lowercase.
    si2000min = models.IntegerField(null=True, db_column='SI2000MIN', blank=True) # Field name made lowercase.
    si2000max = models.IntegerField(null=True, db_column='SI2000MAX', blank=True) # Field name made lowercase.
    si2000a = models.IntegerField(null=True, db_column='SI2000A', blank=True) # Field name made lowercase.
    si2000p = models.IntegerField(null=True, db_column='SI2000P', blank=True) # Field name made lowercase.
    walla = models.IntegerField(null=True, db_column='WALLA', blank=True) # Field name made lowercase.
    wallp = models.IntegerField(null=True, db_column='WALLP', blank=True) # Field name made lowercase.
    os = models.CharField(max_length=90, db_column='OS') # Field name made lowercase.
    space = models.CharField(max_length=90, db_column='SPACE') # Field name made lowercase.
    minjobs = models.IntegerField(null=True, db_column='MINJOBS', blank=True) # Field name made lowercase.
    maxjobs = models.IntegerField(null=True, db_column='MAXJOBS', blank=True) # Field name made lowercase.
    laststart = models.DateTimeField(null=True, db_column='LASTSTART', blank=True) # Field name made lowercase.
    lastend = models.DateTimeField(null=True, db_column='LASTEND', blank=True) # Field name made lowercase.
    lastfail = models.DateTimeField(null=True, db_column='LASTFAIL', blank=True) # Field name made lowercase.
    lastpilot = models.DateTimeField(null=True, db_column='LASTPILOT', blank=True) # Field name made lowercase.
    lastpid = models.IntegerField(null=True, db_column='LASTPID', blank=True) # Field name made lowercase.
    nstart = models.IntegerField(db_column='NSTART') # Field name made lowercase.
    finished = models.IntegerField(db_column='FINISHED') # Field name made lowercase.
    failed = models.IntegerField(db_column='FAILED') # Field name made lowercase.
    defined = models.IntegerField(db_column='DEFINED') # Field name made lowercase.
    assigned = models.IntegerField(db_column='ASSIGNED') # Field name made lowercase.
    waiting = models.IntegerField(db_column='WAITING') # Field name made lowercase.
    activated = models.IntegerField(db_column='ACTIVATED') # Field name made lowercase.
    running = models.IntegerField(db_column='RUNNING') # Field name made lowercase.
    getjob = models.IntegerField(db_column='GETJOB') # Field name made lowercase.
    updatejob = models.IntegerField(db_column='UPDATEJOB') # Field name made lowercase.
    subtot = models.IntegerField(db_column='SUBTOT') # Field name made lowercase.
    subdef = models.IntegerField(db_column='SUBDEF') # Field name made lowercase.
    subdone = models.IntegerField(db_column='SUBDONE') # Field name made lowercase.
    filemods = models.IntegerField(db_column='FILEMODS') # Field name made lowercase.
    ncpu = models.IntegerField(null=True, db_column='NCPU', blank=True) # Field name made lowercase.
    nslot = models.IntegerField(null=True, db_column='NSLOT', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'sitehistory'

class Sitesinfo(models.Model):
#    name = models.CharField(max_length=360, primary_key=True, db_column='NAME') # Field name made lowercase.
#    nick = models.CharField(max_length=60, db_column='NICK') # Field name made lowercase.
#    contact = models.CharField(max_length=90, db_column='CONTACT', blank=True) # Field name made lowercase.
#    email = models.CharField(max_length=90, db_column='EMAIL', blank=True) # Field name made lowercase.
#    status = models.CharField(max_length=36, db_column='STATUS', blank=True) # Field name made lowercase.
#    lrc = models.CharField(max_length=360, db_column='LRC', blank=True) # Field name made lowercase.
#    gridcat = models.IntegerField(null=True, db_column='GRIDCAT', blank=True) # Field name made lowercase.
#    monalisa = models.CharField(max_length=60, db_column='MONALISA', blank=True) # Field name made lowercase.
#    computingsite = models.CharField(max_length=60, db_column='COMPUTINGSITE', blank=True) # Field name made lowercase.
#    mainsite = models.CharField(max_length=60, db_column='MAINSITE', blank=True) # Field name made lowercase.
#    home = models.CharField(max_length=360, db_column='HOME', blank=True) # Field name made lowercase.
#    ganglia = models.CharField(max_length=360, db_column='GANGLIA', blank=True) # Field name made lowercase.
#    goc = models.CharField(max_length=60, db_column='GOC', blank=True) # Field name made lowercase.
#    gocconfig = models.IntegerField(null=True, db_column='GOCCONFIG', blank=True) # Field name made lowercase.
#    prodsys = models.CharField(max_length=60, db_column='PRODSYS', blank=True) # Field name made lowercase.
#    dq2svc = models.CharField(max_length=60, db_column='DQ2SVC', blank=True) # Field name made lowercase.
#    usage = models.CharField(max_length=120, db_column='USAGE', blank=True) # Field name made lowercase.
#    updtime = models.IntegerField(null=True, db_column='UPDTIME', blank=True) # Field name made lowercase.
#    ndatasets = models.IntegerField(null=True, db_column='NDATASETS', blank=True) # Field name made lowercase.
#    nfiles = models.IntegerField(null=True, db_column='NFILES', blank=True) # Field name made lowercase.
#    timestamp = models.IntegerField(null=True, db_column='TIMESTAMP', blank=True) # Field name made lowercase.
    name = models.CharField(db_column='NAME', primary_key=True, max_length=120)  # Field name made lowercase.
    nick = models.CharField(db_column='NICK', max_length=20)  # Field name made lowercase.
    contact = models.CharField(db_column='CONTACT', max_length=30, blank=True)  # Field name made lowercase.
    email = models.CharField(db_column='EMAIL', max_length=30, blank=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=12, blank=True)  # Field name made lowercase.
    lrc = models.CharField(db_column='LRC', max_length=120, blank=True)  # Field name made lowercase.
    gridcat = models.IntegerField(db_column='GRIDCAT', blank=True, null=True)  # Field name made lowercase.
    monalisa = models.CharField(db_column='MONALISA', max_length=20, blank=True)  # Field name made lowercase.
    computingsite = models.CharField(db_column='COMPUTINGSITE', max_length=20, blank=True)  # Field name made lowercase.
    mainsite = models.CharField(db_column='MAINSITE', max_length=20, blank=True)  # Field name made lowercase.
    home = models.CharField(db_column='HOME', max_length=120, blank=True)  # Field name made lowercase.
    ganglia = models.CharField(db_column='GANGLIA', max_length=120, blank=True)  # Field name made lowercase.
    goc = models.CharField(db_column='GOC', max_length=20, blank=True)  # Field name made lowercase.
    gocconfig = models.IntegerField(db_column='GOCCONFIG', blank=True, null=True)  # Field name made lowercase.
    prodsys = models.CharField(db_column='PRODSYS', max_length=20, blank=True)  # Field name made lowercase.
    dq2svc = models.CharField(db_column='DQ2SVC', max_length=20, blank=True)  # Field name made lowercase.
    usage = models.CharField(db_column='USAGE', max_length=40, blank=True)  # Field name made lowercase.
    updtime = models.IntegerField(db_column='UPDTIME', blank=True, null=True)  # Field name made lowercase.
    ndatasets = models.IntegerField(db_column='NDATASETS', blank=True, null=True)  # Field name made lowercase.
    nfiles = models.IntegerField(db_column='NFILES', blank=True, null=True)  # Field name made lowercase.
    timestamp = models.IntegerField(db_column='TIMESTAMP', blank=True, null=True)  # Field name made lowercase.
    class Meta:
        db_table = u'sitesinfo'

class Sitestats(models.Model):
    cloud = models.CharField(max_length=30, primary_key=True, db_column='CLOUD') # Field name made lowercase.
    site = models.CharField(max_length=180, db_column='SITE', blank=True) # Field name made lowercase.
    at_time = models.DateTimeField(null=True, db_column='AT_TIME', blank=True) # Field name made lowercase.
    twidth = models.IntegerField(null=True, db_column='TWIDTH', blank=True) # Field name made lowercase.
    tjob = models.IntegerField(null=True, db_column='TJOB', blank=True) # Field name made lowercase.
    tgetjob = models.IntegerField(null=True, db_column='TGETJOB', blank=True) # Field name made lowercase.
    tstagein = models.IntegerField(null=True, db_column='TSTAGEIN', blank=True) # Field name made lowercase.
    trun = models.IntegerField(null=True, db_column='TRUN', blank=True) # Field name made lowercase.
    tstageout = models.IntegerField(null=True, db_column='TSTAGEOUT', blank=True) # Field name made lowercase.
    twait = models.IntegerField(null=True, db_column='TWAIT', blank=True) # Field name made lowercase.
    nusers = models.IntegerField(null=True, db_column='NUSERS', blank=True) # Field name made lowercase.
    nwn = models.IntegerField(null=True, db_column='NWN', blank=True) # Field name made lowercase.
    njobs = models.IntegerField(null=True, db_column='NJOBS', blank=True) # Field name made lowercase.
    nfinished = models.IntegerField(null=True, db_column='NFINISHED', blank=True) # Field name made lowercase.
    nfailed = models.IntegerField(null=True, db_column='NFAILED', blank=True) # Field name made lowercase.
    nfailapp = models.IntegerField(null=True, db_column='NFAILAPP', blank=True) # Field name made lowercase.
    nfailsys = models.IntegerField(null=True, db_column='NFAILSYS', blank=True) # Field name made lowercase.
    nfaildat = models.IntegerField(null=True, db_column='NFAILDAT', blank=True) # Field name made lowercase.
    ntimeout = models.IntegerField(null=True, db_column='NTIMEOUT', blank=True) # Field name made lowercase.
    efficiency = models.IntegerField(null=True, db_column='EFFICIENCY', blank=True) # Field name made lowercase.
    siteutil = models.IntegerField(null=True, db_column='SITEUTIL', blank=True) # Field name made lowercase.
    jobtype = models.CharField(max_length=90, db_column='JOBTYPE', blank=True) # Field name made lowercase.
    proctype = models.CharField(max_length=270, db_column='PROCTYPE', blank=True) # Field name made lowercase.
    username = models.CharField(max_length=270, db_column='USERNAME', blank=True) # Field name made lowercase.
    ngetjob = models.IntegerField(null=True, db_column='NGETJOB', blank=True) # Field name made lowercase.
    nupdatejob = models.IntegerField(null=True, db_column='NUPDATEJOB', blank=True) # Field name made lowercase.
    release = models.CharField(max_length=270, db_column='RELEASE', blank=True) # Field name made lowercase.
    nevents = models.BigIntegerField(null=True, db_column='NEVENTS', blank=True) # Field name made lowercase.
    spectype = models.CharField(max_length=270, db_column='SPECTYPE', blank=True) # Field name made lowercase.
    tsetup = models.IntegerField(null=True, db_column='TSETUP', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'sitestats'

class Submithosts(models.Model):
    name = models.CharField(max_length=180, db_column='NAME') # Field name made lowercase.
    nickname = models.CharField(max_length=60, db_column='NICKNAME') # Field name made lowercase.
    host = models.CharField(max_length=180, primary_key=True, db_column='HOST') # Field name made lowercase.
    system = models.CharField(max_length=180, db_column='SYSTEM') # Field name made lowercase.
    rundir = models.CharField(max_length=600, db_column='RUNDIR') # Field name made lowercase.
    runurl = models.CharField(max_length=600, db_column='RUNURL') # Field name made lowercase.
    jdltxt = models.CharField(max_length=12000, db_column='JDLTXT', blank=True) # Field name made lowercase.
    pilotqueue = models.CharField(max_length=60, db_column='PILOTQUEUE', blank=True) # Field name made lowercase.
    outurl = models.CharField(max_length=600, db_column='OUTURL', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'submithosts'

class Sysconfig(models.Model):
    name = models.CharField(max_length=180, primary_key=True, db_column='NAME') # Field name made lowercase.
    system = models.CharField(max_length=60, primary_key=True, db_column='SYSTEM') # Field name made lowercase.
    config = models.CharField(max_length=12000, db_column='CONFIG', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'sysconfig'

class TM4RegionsReplication(models.Model):
    tier2 = models.CharField(max_length=150, primary_key=True, db_column='TIER2') # Field name made lowercase.
    cloud = models.CharField(max_length=90, db_column='CLOUD') # Field name made lowercase.
    percentage = models.FloatField(null=True, db_column='PERCENTAGE', blank=True) # Field name made lowercase.
    tier1 = models.CharField(max_length=150, db_column='TIER1') # Field name made lowercase.
    nsubs = models.IntegerField(null=True, db_column='NSUBS', blank=True) # Field name made lowercase.
    subsoption = models.CharField(max_length=960, db_column='SUBSOPTION', blank=True) # Field name made lowercase.
    status = models.CharField(max_length=36, db_column='STATUS', blank=True) # Field name made lowercase.
    timestamp = models.IntegerField(null=True, db_column='TIMESTAMP', blank=True) # Field name made lowercase.
    stream_pattern = models.CharField(max_length=96, db_column='STREAM_PATTERN', blank=True) # Field name made lowercase.
    nreplicas = models.IntegerField(null=True, db_column='NREPLICAS', blank=True) # Field name made lowercase.
    nsubs_aod = models.IntegerField(null=True, db_column='NSUBS_AOD', blank=True) # Field name made lowercase.
    nsubs_dpd = models.IntegerField(null=True, db_column='NSUBS_DPD', blank=True) # Field name made lowercase.
    upd_flag = models.CharField(max_length=12, db_column='UPD_FLAG', blank=True) # Field name made lowercase.
    esd = models.IntegerField(null=True, db_column='ESD', blank=True) # Field name made lowercase.
    esd_subsoption = models.CharField(max_length=960, db_column='ESD_SUBSOPTION', blank=True) # Field name made lowercase.
    desd = models.IntegerField(null=True, db_column='DESD', blank=True) # Field name made lowercase.
    desd_subsoption = models.CharField(max_length=960, db_column='DESD_SUBSOPTION', blank=True) # Field name made lowercase.
    prim_flag = models.IntegerField(null=True, db_column='PRIM_FLAG', blank=True) # Field name made lowercase.
    t2group = models.BigIntegerField(null=True, db_column='T2GROUP', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u't_m4regions_replication'

class TTier2Groups(models.Model):
    name = models.CharField(max_length=36, primary_key=True, db_column='NAME') # Field name made lowercase.
    gid = models.BigIntegerField(null=True, db_column='GID', blank=True) # Field name made lowercase.
    ntup_share = models.BigIntegerField(null=True, db_column='NTUP_SHARE', blank=True) # Field name made lowercase.
    timestmap = models.BigIntegerField(null=True, db_column='TIMESTMAP', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u't_tier2_groups'

class Tablepart4Copying(models.Model):
    table_name = models.CharField(max_length=90, primary_key=True, db_column='TABLE_NAME') # Field name made lowercase.
    partition_name = models.CharField(max_length=90, primary_key=True, db_column='PARTITION_NAME') # Field name made lowercase.
    copied_to_arch = models.CharField(max_length=30, db_column='COPIED_TO_ARCH') # Field name made lowercase.
    copying_done_on = models.DateTimeField(null=True, db_column='COPYING_DONE_ON', blank=True) # Field name made lowercase.
    deleted_on = models.DateTimeField(null=True, db_column='DELETED_ON', blank=True) # Field name made lowercase.
    data_verif_passed = models.CharField(max_length=9, db_column='DATA_VERIF_PASSED', blank=True) # Field name made lowercase.
    data_verified_on = models.DateTimeField(null=True, db_column='DATA_VERIFIED_ON', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'tablepart4copying'

class Taginfo(models.Model):
    tag = models.CharField(max_length=90, primary_key=True, db_column='TAG') # Field name made lowercase.
    description = models.CharField(max_length=300, db_column='DESCRIPTION') # Field name made lowercase.
    nqueues = models.IntegerField(db_column='NQUEUES') # Field name made lowercase.
    queues = models.CharField(max_length=12000, db_column='QUEUES', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'taginfo'

class Tags(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    name = models.CharField(max_length=60, db_column='NAME') # Field name made lowercase.
    description = models.CharField(max_length=180, db_column='DESCRIPTION') # Field name made lowercase.
    ugid = models.IntegerField(null=True, db_column='UGID', blank=True) # Field name made lowercase.
    type = models.CharField(max_length=30, db_column='TYPE') # Field name made lowercase.
    itemid = models.IntegerField(null=True, db_column='ITEMID', blank=True) # Field name made lowercase.
    created = models.DateTimeField(db_column='CREATED') # Field name made lowercase.
    class Meta:
        db_table = u'tags'

class Transfercosts(models.Model):
#    sourcesite = models.CharField(max_length=768, primary_key=True, db_column='SOURCESITE') # Field name made lowercase.
#    destsite = models.CharField(max_length=768, primary_key=True, db_column='DESTSITE') # Field name made lowercase.
#    type = models.CharField(max_length=768, primary_key=True, db_column='TYPE') # Field name made lowercase.
#    status = models.CharField(max_length=192, db_column='STATUS', blank=True) # Field name made lowercase.
#    last_update = models.DateTimeField(null=True, db_column='LAST_UPDATE', blank=True) # Field name made lowercase.
#    cost = models.BigIntegerField(db_column='COST') # Field name made lowercase.
#    max_cost = models.BigIntegerField(null=True, db_column='MAX_COST', blank=True) # Field name made lowercase.
#    min_cost = models.BigIntegerField(null=True, db_column='MIN_COST', blank=True) # Field name made lowercase.
    sourcesite = models.CharField(db_column='SOURCESITE', max_length=256)  # Field name made lowercase.
    destsite = models.CharField(db_column='DESTSITE', max_length=256)  # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=256)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=64, blank=True)  # Field name made lowercase.
    last_update = models.DateTimeField(db_column='LAST_UPDATE', blank=True, null=True)  # Field name made lowercase.
    cost = models.BigIntegerField(db_column='COST') # Field name made lowercase.
    max_cost = models.BigIntegerField(db_column='MAX_COST', blank=True, null=True)  # Field name made lowercase.
    min_cost = models.BigIntegerField(db_column='MIN_COST', blank=True, null=True)  # Field name made lowercase.
    class Meta:
        db_table = u'transfercosts'

class TransfercostsHistory(models.Model):
#    sourcesite = models.CharField(max_length=768, primary_key=True, db_column='SOURCESITE') # Field name made lowercase.
    sourcesite = models.CharField(db_column='SOURCESITE', primary_key=True, max_length=255)  # Field name made lowercase.
    destsite = models.CharField(max_length=768, db_column='DESTSITE') # Field name made lowercase.
    type = models.CharField(max_length=768, db_column='TYPE', blank=True) # Field name made lowercase.
    status = models.CharField(max_length=192, db_column='STATUS', blank=True) # Field name made lowercase.
    last_update = models.DateTimeField(null=True, db_column='LAST_UPDATE', blank=True) # Field name made lowercase.
    cost = models.BigIntegerField(db_column='COST') # Field name made lowercase.
    max_cost = models.BigIntegerField(null=True, db_column='MAX_COST', blank=True) # Field name made lowercase.
    min_cost = models.BigIntegerField(null=True, db_column='MIN_COST', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'transfercosts_history'

class TriggersDebug(models.Model):
    when = models.DateTimeField(primary_key=True, db_column='WHEN') # Field name made lowercase.
    what = models.CharField(max_length=300, db_column='WHAT', blank=True) # Field name made lowercase.
    value = models.CharField(max_length=600, db_column='VALUE', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'triggers_debug'

class Usagereport(models.Model):
    entry = models.IntegerField(primary_key=True, db_column='ENTRY') # Field name made lowercase.
    flag = models.CharField(max_length=60, db_column='FLAG') # Field name made lowercase.
    hours = models.IntegerField(null=True, db_column='HOURS', blank=True) # Field name made lowercase.
    tstart = models.DateTimeField(null=True, db_column='TSTART', blank=True) # Field name made lowercase.
    tend = models.DateTimeField(null=True, db_column='TEND', blank=True) # Field name made lowercase.
    tinsert = models.DateTimeField(db_column='TINSERT') # Field name made lowercase.
    site = models.CharField(max_length=90, db_column='SITE') # Field name made lowercase.
    nwn = models.IntegerField(null=True, db_column='NWN', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'usagereport'

class Usercacheusage(models.Model):
    username = models.CharField(max_length=384, db_column='USERNAME') # Field name made lowercase.
#    filename = models.CharField(max_length=768, primary_key=True, db_column='FILENAME') # Field name made lowercase.
    filename = models.CharField(db_column='FILENAME', max_length=255, primary_key=True)  # Field name made lowercase.
    hostname = models.CharField(max_length=192, primary_key=True, db_column='HOSTNAME') # Field name made lowercase.
    creationtime = models.DateTimeField(primary_key=True, db_column='CREATIONTIME') # Field name made lowercase.
    modificationtime = models.DateTimeField(null=True, db_column='MODIFICATIONTIME', blank=True) # Field name made lowercase.
    filesize = models.BigIntegerField(null=True, db_column='FILESIZE', blank=True) # Field name made lowercase.
    checksum = models.CharField(max_length=108, db_column='CHECKSUM', blank=True) # Field name made lowercase.
    aliasname = models.CharField(max_length=768, db_column='ALIASNAME', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'usercacheusage'

class Users(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    name = models.CharField(max_length=180, db_column='NAME') # Field name made lowercase.
    dn = models.CharField(max_length=450, db_column='DN', blank=True) # Field name made lowercase.
    email = models.CharField(max_length=180, db_column='EMAIL', blank=True) # Field name made lowercase.
    url = models.CharField(max_length=300, db_column='URL', blank=True) # Field name made lowercase.
    location = models.CharField(max_length=180, db_column='LOCATION', blank=True) # Field name made lowercase.
    classa = models.CharField(max_length=90, db_column='CLASSA', blank=True) # Field name made lowercase.
    classp = models.CharField(max_length=90, db_column='CLASSP', blank=True) # Field name made lowercase.
    classxp = models.CharField(max_length=90, db_column='CLASSXP', blank=True) # Field name made lowercase.
    sitepref = models.CharField(max_length=180, db_column='SITEPREF', blank=True) # Field name made lowercase.
    gridpref = models.CharField(max_length=60, db_column='GRIDPREF', blank=True) # Field name made lowercase.
    queuepref = models.CharField(max_length=180, db_column='QUEUEPREF', blank=True) # Field name made lowercase.
    scriptcache = models.CharField(max_length=300, db_column='SCRIPTCACHE', blank=True) # Field name made lowercase.
    types = models.CharField(max_length=180, db_column='TYPES', blank=True) # Field name made lowercase.
    sites = models.CharField(max_length=750, db_column='SITES', blank=True) # Field name made lowercase.
    njobsa = models.IntegerField(null=True, db_column='NJOBSA', blank=True) # Field name made lowercase.
    njobsp = models.IntegerField(null=True, db_column='NJOBSP', blank=True) # Field name made lowercase.
    njobs1 = models.IntegerField(null=True, db_column='NJOBS1', blank=True) # Field name made lowercase.
    njobs7 = models.IntegerField(null=True, db_column='NJOBS7', blank=True) # Field name made lowercase.
    njobs30 = models.IntegerField(null=True, db_column='NJOBS30', blank=True) # Field name made lowercase.
    cpua1 = models.BigIntegerField(null=True, db_column='CPUA1', blank=True) # Field name made lowercase.
    cpua7 = models.BigIntegerField(null=True, db_column='CPUA7', blank=True) # Field name made lowercase.
    cpua30 = models.BigIntegerField(null=True, db_column='CPUA30', blank=True) # Field name made lowercase.
    cpup1 = models.BigIntegerField(null=True, db_column='CPUP1', blank=True) # Field name made lowercase.
    cpup7 = models.BigIntegerField(null=True, db_column='CPUP7', blank=True) # Field name made lowercase.
    cpup30 = models.BigIntegerField(null=True, db_column='CPUP30', blank=True) # Field name made lowercase.
    cpuxp1 = models.BigIntegerField(null=True, db_column='CPUXP1', blank=True) # Field name made lowercase.
    cpuxp7 = models.BigIntegerField(null=True, db_column='CPUXP7', blank=True) # Field name made lowercase.
    cpuxp30 = models.BigIntegerField(null=True, db_column='CPUXP30', blank=True) # Field name made lowercase.
    quotaa1 = models.BigIntegerField(null=True, db_column='QUOTAA1', blank=True) # Field name made lowercase.
    quotaa7 = models.BigIntegerField(null=True, db_column='QUOTAA7', blank=True) # Field name made lowercase.
    quotaa30 = models.BigIntegerField(null=True, db_column='QUOTAA30', blank=True) # Field name made lowercase.
    quotap1 = models.BigIntegerField(null=True, db_column='QUOTAP1', blank=True) # Field name made lowercase.
    quotap7 = models.BigIntegerField(null=True, db_column='QUOTAP7', blank=True) # Field name made lowercase.
    quotap30 = models.BigIntegerField(null=True, db_column='QUOTAP30', blank=True) # Field name made lowercase.
    quotaxp1 = models.BigIntegerField(null=True, db_column='QUOTAXP1', blank=True) # Field name made lowercase.
    quotaxp7 = models.BigIntegerField(null=True, db_column='QUOTAXP7', blank=True) # Field name made lowercase.
    quotaxp30 = models.BigIntegerField(null=True, db_column='QUOTAXP30', blank=True) # Field name made lowercase.
    space1 = models.IntegerField(null=True, db_column='SPACE1', blank=True) # Field name made lowercase.
    space7 = models.IntegerField(null=True, db_column='SPACE7', blank=True) # Field name made lowercase.
    space30 = models.IntegerField(null=True, db_column='SPACE30', blank=True) # Field name made lowercase.
    lastmod = models.DateTimeField(db_column='LASTMOD') # Field name made lowercase.
    firstjob = models.DateTimeField(db_column='FIRSTJOB') # Field name made lowercase.
    latestjob = models.DateTimeField(db_column='LATESTJOB') # Field name made lowercase.
    pagecache = models.TextField(db_column='PAGECACHE', blank=True) # Field name made lowercase.
    cachetime = models.DateTimeField(db_column='CACHETIME') # Field name made lowercase.
    ncurrent = models.IntegerField(db_column='NCURRENT') # Field name made lowercase.
    jobid = models.IntegerField(db_column='JOBID') # Field name made lowercase.
    status = models.CharField(max_length=60, db_column='STATUS', blank=True) # Field name made lowercase.
    vo = models.CharField(max_length=60, db_column='VO', blank=True) # Field name made lowercase.

    class Meta:
        db_table = u'users'
##FIXME: reenable this after proper dbproxies are introduced!###        db_table = u'"ATLAS_PANDAMETA"."USERS"'
        allColumns = COLUMNS['ActiveUsers-all']
        primaryColumns = [ 'name']
        secondaryColumns = []
        orderColumns = ORDER_COLUMNS['ActiveUsers-all']
        columnTitles = COL_TITLES['ActiveUsers-all']
        filterFields = FILTERS['ActiveUsers-all']


    def __str__(self):
        return 'User: ' + str(self.name) + '[' + str(self.status) + ']'



class UsersOld(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    name = models.CharField(max_length=180, db_column='NAME') # Field name made lowercase.
    dn = models.CharField(max_length=300, db_column='DN', blank=True) # Field name made lowercase.
    email = models.CharField(max_length=180, db_column='EMAIL', blank=True) # Field name made lowercase.
    url = models.CharField(max_length=300, db_column='URL', blank=True) # Field name made lowercase.
    location = models.CharField(max_length=180, db_column='LOCATION', blank=True) # Field name made lowercase.
    classa = models.CharField(max_length=90, db_column='CLASSA', blank=True) # Field name made lowercase.
    classp = models.CharField(max_length=90, db_column='CLASSP', blank=True) # Field name made lowercase.
    classxp = models.CharField(max_length=90, db_column='CLASSXP', blank=True) # Field name made lowercase.
    sitepref = models.CharField(max_length=180, db_column='SITEPREF', blank=True) # Field name made lowercase.
    gridpref = models.CharField(max_length=60, db_column='GRIDPREF', blank=True) # Field name made lowercase.
    queuepref = models.CharField(max_length=180, db_column='QUEUEPREF', blank=True) # Field name made lowercase.
    scriptcache = models.CharField(max_length=300, db_column='SCRIPTCACHE', blank=True) # Field name made lowercase.
    types = models.CharField(max_length=180, db_column='TYPES', blank=True) # Field name made lowercase.
    sites = models.CharField(max_length=750, db_column='SITES', blank=True) # Field name made lowercase.
    njobsa = models.IntegerField(null=True, db_column='NJOBSA', blank=True) # Field name made lowercase.
    njobsp = models.IntegerField(null=True, db_column='NJOBSP', blank=True) # Field name made lowercase.
    njobs1 = models.IntegerField(null=True, db_column='NJOBS1', blank=True) # Field name made lowercase.
    njobs7 = models.IntegerField(null=True, db_column='NJOBS7', blank=True) # Field name made lowercase.
    njobs30 = models.IntegerField(null=True, db_column='NJOBS30', blank=True) # Field name made lowercase.
    cpua1 = models.BigIntegerField(null=True, db_column='CPUA1', blank=True) # Field name made lowercase.
    cpua7 = models.BigIntegerField(null=True, db_column='CPUA7', blank=True) # Field name made lowercase.
    cpua30 = models.BigIntegerField(null=True, db_column='CPUA30', blank=True) # Field name made lowercase.
    cpup1 = models.BigIntegerField(null=True, db_column='CPUP1', blank=True) # Field name made lowercase.
    cpup7 = models.BigIntegerField(null=True, db_column='CPUP7', blank=True) # Field name made lowercase.
    cpup30 = models.BigIntegerField(null=True, db_column='CPUP30', blank=True) # Field name made lowercase.
    cpuxp1 = models.BigIntegerField(null=True, db_column='CPUXP1', blank=True) # Field name made lowercase.
    cpuxp7 = models.BigIntegerField(null=True, db_column='CPUXP7', blank=True) # Field name made lowercase.
    cpuxp30 = models.BigIntegerField(null=True, db_column='CPUXP30', blank=True) # Field name made lowercase.
    quotaa1 = models.BigIntegerField(null=True, db_column='QUOTAA1', blank=True) # Field name made lowercase.
    quotaa7 = models.BigIntegerField(null=True, db_column='QUOTAA7', blank=True) # Field name made lowercase.
    quotaa30 = models.BigIntegerField(null=True, db_column='QUOTAA30', blank=True) # Field name made lowercase.
    quotap1 = models.BigIntegerField(null=True, db_column='QUOTAP1', blank=True) # Field name made lowercase.
    quotap7 = models.BigIntegerField(null=True, db_column='QUOTAP7', blank=True) # Field name made lowercase.
    quotap30 = models.BigIntegerField(null=True, db_column='QUOTAP30', blank=True) # Field name made lowercase.
    quotaxp1 = models.BigIntegerField(null=True, db_column='QUOTAXP1', blank=True) # Field name made lowercase.
    quotaxp7 = models.BigIntegerField(null=True, db_column='QUOTAXP7', blank=True) # Field name made lowercase.
    quotaxp30 = models.BigIntegerField(null=True, db_column='QUOTAXP30', blank=True) # Field name made lowercase.
    space1 = models.IntegerField(null=True, db_column='SPACE1', blank=True) # Field name made lowercase.
    space7 = models.IntegerField(null=True, db_column='SPACE7', blank=True) # Field name made lowercase.
    space30 = models.IntegerField(null=True, db_column='SPACE30', blank=True) # Field name made lowercase.
    lastmod = models.DateTimeField(db_column='LASTMOD') # Field name made lowercase.
    firstjob = models.DateTimeField(db_column='FIRSTJOB') # Field name made lowercase.
    latestjob = models.DateTimeField(db_column='LATESTJOB') # Field name made lowercase.
    pagecache = models.TextField(db_column='PAGECACHE', blank=True) # Field name made lowercase.
    cachetime = models.DateTimeField(db_column='CACHETIME') # Field name made lowercase.
    ncurrent = models.IntegerField(db_column='NCURRENT') # Field name made lowercase.
    jobid = models.IntegerField(db_column='JOBID') # Field name made lowercase.
    status = models.CharField(max_length=60, db_column='STATUS', blank=True) # Field name made lowercase.
    vo = models.CharField(max_length=60, db_column='VO', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'users_old'

class Userstats(models.Model):
    name = models.CharField(max_length=180, primary_key=True, db_column='NAME') # Field name made lowercase.
    label = models.CharField(max_length=60, db_column='LABEL', blank=True) # Field name made lowercase.
    yr = models.IntegerField(primary_key=True, db_column='YR') # Field name made lowercase.
    mo = models.IntegerField(primary_key=True, db_column='MO') # Field name made lowercase.
    jobs = models.BigIntegerField(null=True, db_column='JOBS', blank=True) # Field name made lowercase.
    idlo = models.BigIntegerField(null=True, db_column='IDLO', blank=True) # Field name made lowercase.
    idhi = models.BigIntegerField(null=True, db_column='IDHI', blank=True) # Field name made lowercase.
    info = models.CharField(max_length=300, db_column='INFO', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'userstats'

class Usersubs(models.Model):
#    datasetname = models.CharField(max_length=765, primary_key=True, db_column='DATASETNAME') # Field name made lowercase.
    datasetname = models.CharField(max_length=255, primary_key=True, db_column='DATASETNAME')  # Field name made lowercase.
    site = models.CharField(max_length=192, primary_key=True, db_column='SITE') # Field name made lowercase.
    creationdate = models.DateTimeField(null=True, db_column='CREATIONDATE', blank=True) # Field name made lowercase.
    modificationdate = models.DateTimeField(null=True, db_column='MODIFICATIONDATE', blank=True) # Field name made lowercase.
    nused = models.IntegerField(null=True, db_column='NUSED', blank=True) # Field name made lowercase.
    state = models.CharField(max_length=90, db_column='STATE', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'usersubs'

class VoToSite(models.Model):
    site_name = models.CharField(max_length=96, primary_key=True, db_column='SITE_NAME') # Field name made lowercase.
    queue = models.CharField(max_length=192, primary_key=True, db_column='QUEUE') # Field name made lowercase.
    vo_name = models.CharField(max_length=96, primary_key=True, db_column='VO_NAME') # Field name made lowercase.
    class Meta:
        db_table = u'vo_to_site'

class Vorspassfail(models.Model):
    site_name = models.CharField(max_length=96, primary_key=True, db_column='SITE_NAME') # Field name made lowercase.
    passfail = models.CharField(max_length=12, db_column='PASSFAIL') # Field name made lowercase.
    last_checked = models.DateTimeField(null=True, db_column='LAST_CHECKED', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'vorspassfail'

class Wndata(models.Model):
    site = models.CharField(max_length=90, primary_key=True, db_column='SITE') # Field name made lowercase.
    wn = models.CharField(max_length=150, primary_key=True, db_column='WN') # Field name made lowercase.
    flag = models.CharField(max_length=60, primary_key=True, db_column='FLAG') # Field name made lowercase.
    hours = models.IntegerField(primary_key=True, db_column='HOURS') # Field name made lowercase.
    mem = models.IntegerField(null=True, db_column='MEM', blank=True) # Field name made lowercase.
    si2000 = models.IntegerField(null=True, db_column='SI2000', blank=True) # Field name made lowercase.
    os = models.CharField(max_length=90, db_column='OS', blank=True) # Field name made lowercase.
    space = models.CharField(max_length=90, db_column='SPACE', blank=True) # Field name made lowercase.
    maxjobs = models.IntegerField(null=True, db_column='MAXJOBS', blank=True) # Field name made lowercase.
    laststart = models.DateTimeField(null=True, db_column='LASTSTART', blank=True) # Field name made lowercase.
    lastend = models.DateTimeField(null=True, db_column='LASTEND', blank=True) # Field name made lowercase.
    lastfail = models.DateTimeField(null=True, db_column='LASTFAIL', blank=True) # Field name made lowercase.
    lastpilot = models.DateTimeField(null=True, db_column='LASTPILOT', blank=True) # Field name made lowercase.
    lastpid = models.IntegerField(null=True, db_column='LASTPID', blank=True) # Field name made lowercase.
    nstart = models.IntegerField(db_column='NSTART') # Field name made lowercase.
    finished = models.IntegerField(db_column='FINISHED') # Field name made lowercase.
    failed = models.IntegerField(db_column='FAILED') # Field name made lowercase.
    holding = models.IntegerField(db_column='HOLDING') # Field name made lowercase.
    running = models.IntegerField(db_column='RUNNING') # Field name made lowercase.
    transferring = models.IntegerField(db_column='TRANSFERRING') # Field name made lowercase.
    getjob = models.IntegerField(db_column='GETJOB') # Field name made lowercase.
    updatejob = models.IntegerField(db_column='UPDATEJOB') # Field name made lowercase.
    lastmod = models.DateTimeField(db_column='LASTMOD') # Field name made lowercase.
    ncpu = models.IntegerField(null=True, db_column='NCPU', blank=True) # Field name made lowercase.
    ncpucurrent = models.IntegerField(null=True, db_column='NCPUCURRENT', blank=True) # Field name made lowercase.
    nslot = models.IntegerField(null=True, db_column='NSLOT', blank=True) # Field name made lowercase.
    nslotcurrent = models.IntegerField(null=True, db_column='NSLOTCURRENT', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'wndata'

