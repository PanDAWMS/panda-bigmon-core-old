"""
topology.models -- for Schedconfig and other topology-related objects

"""

from django.db import models
# Create your models here.
class Schedconfig(models.Model):
    name = models.CharField(max_length=180, db_column='NAME')  # Field name made lowercase.
    nickname = models.CharField(max_length=180, primary_key=True, db_column='NICKNAME')  # Field name made lowercase.
    queue = models.CharField(max_length=180, db_column='QUEUE', blank=True)  # Field name made lowercase.
    localqueue = models.CharField(max_length=60, db_column='LOCALQUEUE', blank=True)  # Field name made lowercase.
    system = models.CharField(max_length=180, db_column='SYSTEM')  # Field name made lowercase.
    sysconfig = models.CharField(max_length=60, db_column='SYSCONFIG', blank=True)  # Field name made lowercase.
    environ = models.CharField(max_length=750, db_column='ENVIRON', blank=True)  # Field name made lowercase.
    gatekeeper = models.CharField(max_length=120, db_column='GATEKEEPER', blank=True)  # Field name made lowercase.
    jobmanager = models.CharField(max_length=240, db_column='JOBMANAGER', blank=True)  # Field name made lowercase.
    se = models.CharField(max_length=1200, db_column='SE', blank=True)  # Field name made lowercase.
    ddm = models.CharField(max_length=360, db_column='DDM', blank=True)  # Field name made lowercase.
    jdladd = models.CharField(max_length=1500, db_column='JDLADD', blank=True)  # Field name made lowercase.
    globusadd = models.CharField(max_length=300, db_column='GLOBUSADD', blank=True)  # Field name made lowercase.
    jdl = models.CharField(max_length=180, db_column='JDL', blank=True)  # Field name made lowercase.
    jdltxt = models.CharField(max_length=1500, db_column='JDLTXT', blank=True)  # Field name made lowercase.
    version = models.CharField(max_length=180, db_column='VERSION', blank=True)  # Field name made lowercase.
    site = models.CharField(max_length=180, db_column='SITE')  # Field name made lowercase.
    region = models.CharField(max_length=180, db_column='REGION', blank=True)  # Field name made lowercase.
    gstat = models.CharField(max_length=180, db_column='GSTAT', blank=True)  # Field name made lowercase.
    tags = models.CharField(max_length=600, db_column='TAGS', blank=True)  # Field name made lowercase.
    cmd = models.CharField(max_length=600, db_column='CMD', blank=True)  # Field name made lowercase.
    lastmod = models.DateTimeField(db_column='LASTMOD')  # Field name made lowercase.
    errinfo = models.CharField(max_length=240, db_column='ERRINFO', blank=True)  # Field name made lowercase.
    nqueue = models.IntegerField(db_column='NQUEUE')  # Field name made lowercase.
    comment_ = models.CharField(max_length=1500, db_column='COMMENT_', blank=True)  # Field name made lowercase.
    appdir = models.CharField(max_length=1500, db_column='APPDIR', blank=True)  # Field name made lowercase.
    datadir = models.CharField(max_length=240, db_column='DATADIR', blank=True)  # Field name made lowercase.
    tmpdir = models.CharField(max_length=240, db_column='TMPDIR', blank=True)  # Field name made lowercase.
    wntmpdir = models.CharField(max_length=240, db_column='WNTMPDIR', blank=True)  # Field name made lowercase.
    dq2url = models.CharField(max_length=240, db_column='DQ2URL', blank=True)  # Field name made lowercase.
    special_par = models.CharField(max_length=240, db_column='SPECIAL_PAR', blank=True)  # Field name made lowercase.
    python_path = models.CharField(max_length=240, db_column='PYTHON_PATH', blank=True)  # Field name made lowercase.
    nodes = models.IntegerField(db_column='NODES')  # Field name made lowercase.
    status = models.CharField(max_length=30, db_column='STATUS', blank=True)  # Field name made lowercase.
    copytool = models.CharField(max_length=240, db_column='COPYTOOL', blank=True)  # Field name made lowercase.
    copysetup = models.CharField(max_length=600, db_column='COPYSETUP', blank=True)  # Field name made lowercase.
    releases = models.CharField(max_length=1500, db_column='RELEASES', blank=True)  # Field name made lowercase.
    sepath = models.CharField(max_length=1200, db_column='SEPATH', blank=True)  # Field name made lowercase.
    envsetup = models.CharField(max_length=600, db_column='ENVSETUP', blank=True)  # Field name made lowercase.
    copyprefix = models.CharField(max_length=480, db_column='COPYPREFIX', blank=True)  # Field name made lowercase.
    lfcpath = models.CharField(max_length=240, db_column='LFCPATH', blank=True)  # Field name made lowercase.
    seopt = models.CharField(max_length=1200, db_column='SEOPT', blank=True)  # Field name made lowercase.
    sein = models.CharField(max_length=1200, db_column='SEIN', blank=True)  # Field name made lowercase.
    seinopt = models.CharField(max_length=1200, db_column='SEINOPT', blank=True)  # Field name made lowercase.
    lfchost = models.CharField(max_length=240, db_column='LFCHOST', blank=True)  # Field name made lowercase.
    cloud = models.CharField(max_length=180, db_column='CLOUD', blank=True)  # Field name made lowercase.
    siteid = models.CharField(max_length=180, db_column='SITEID', blank=True)  # Field name made lowercase.
    proxy = models.CharField(max_length=240, db_column='PROXY', blank=True)  # Field name made lowercase.
    retry = models.CharField(max_length=30, db_column='RETRY', blank=True)  # Field name made lowercase.
    queuehours = models.IntegerField(db_column='QUEUEHOURS')  # Field name made lowercase.
    envsetupin = models.CharField(max_length=600, db_column='ENVSETUPIN', blank=True)  # Field name made lowercase.
    copytoolin = models.CharField(max_length=540, db_column='COPYTOOLIN', blank=True)  # Field name made lowercase.
    copysetupin = models.CharField(max_length=600, db_column='COPYSETUPIN', blank=True)  # Field name made lowercase.
    seprodpath = models.CharField(max_length=1200, db_column='SEPRODPATH', blank=True)  # Field name made lowercase.
    lfcprodpath = models.CharField(max_length=240, db_column='LFCPRODPATH', blank=True)  # Field name made lowercase.
    copyprefixin = models.CharField(max_length=1080, db_column='COPYPREFIXIN', blank=True)  # Field name made lowercase.
    recoverdir = models.CharField(max_length=240, db_column='RECOVERDIR', blank=True)  # Field name made lowercase.
    memory = models.IntegerField(db_column='MEMORY')  # Field name made lowercase.
    maxtime = models.IntegerField(db_column='MAXTIME')  # Field name made lowercase.
    space = models.IntegerField(db_column='SPACE')  # Field name made lowercase.
    tspace = models.DateTimeField(db_column='TSPACE')  # Field name made lowercase.
    cmtconfig = models.CharField(max_length=750, db_column='CMTCONFIG', blank=True)  # Field name made lowercase.
    setokens = models.CharField(max_length=240, db_column='SETOKENS', blank=True)  # Field name made lowercase.
    glexec = models.CharField(max_length=30, db_column='GLEXEC', blank=True)  # Field name made lowercase.
    priorityoffset = models.CharField(max_length=180, db_column='PRIORITYOFFSET', blank=True)  # Field name made lowercase.
    allowedgroups = models.CharField(max_length=300, db_column='ALLOWEDGROUPS', blank=True)  # Field name made lowercase.
    defaulttoken = models.CharField(max_length=300, db_column='DEFAULTTOKEN', blank=True)  # Field name made lowercase.
    pcache = models.CharField(max_length=300, db_column='PCACHE', blank=True)  # Field name made lowercase.
    validatedreleases = models.CharField(max_length=1500, db_column='VALIDATEDRELEASES', blank=True)  # Field name made lowercase.
    accesscontrol = models.CharField(max_length=60, db_column='ACCESSCONTROL', blank=True)  # Field name made lowercase.
    dn = models.CharField(max_length=300, db_column='DN', blank=True)  # Field name made lowercase.
    email = models.CharField(max_length=180, db_column='EMAIL', blank=True)  # Field name made lowercase.
    allowednode = models.CharField(max_length=240, db_column='ALLOWEDNODE', blank=True)  # Field name made lowercase.
    maxinputsize = models.IntegerField(null=True, db_column='MAXINPUTSIZE', blank=True)  # Field name made lowercase.
    timefloor = models.IntegerField(null=True, db_column='TIMEFLOOR', blank=True)  # Field name made lowercase.
    depthboost = models.IntegerField(null=True, db_column='DEPTHBOOST', blank=True)  # Field name made lowercase.
    idlepilotsupression = models.IntegerField(null=True, db_column='IDLEPILOTSUPRESSION', blank=True)  # Field name made lowercase.
    pilotlimit = models.IntegerField(null=True, db_column='PILOTLIMIT', blank=True)  # Field name made lowercase.
    transferringlimit = models.IntegerField(null=True, db_column='TRANSFERRINGLIMIT', blank=True)  # Field name made lowercase.
    cachedse = models.IntegerField(null=True, db_column='CACHEDSE', blank=True)  # Field name made lowercase.
    corecount = models.IntegerField(null=True, db_column='CORECOUNT', blank=True)  # Field name made lowercase.
    countrygroup = models.CharField(max_length=192, db_column='COUNTRYGROUP', blank=True)  # Field name made lowercase.
    availablecpu = models.CharField(max_length=192, db_column='AVAILABLECPU', blank=True)  # Field name made lowercase.
    availablestorage = models.CharField(max_length=192, db_column='AVAILABLESTORAGE', blank=True)  # Field name made lowercase.
    pledgedcpu = models.CharField(max_length=192, db_column='PLEDGEDCPU', blank=True)  # Field name made lowercase.
    pledgedstorage = models.CharField(max_length=192, db_column='PLEDGEDSTORAGE', blank=True)  # Field name made lowercase.
    statusoverride = models.CharField(max_length=768, db_column='STATUSOVERRIDE', blank=True)  # Field name made lowercase.
    allowdirectaccess = models.CharField(max_length=30, db_column='ALLOWDIRECTACCESS', blank=True)  # Field name made lowercase.
    gocname = models.CharField(max_length=192, db_column='GOCNAME', blank=True)  # Field name made lowercase.
    tier = models.CharField(max_length=45, db_column='TIER', blank=True)  # Field name made lowercase.
    multicloud = models.CharField(max_length=192, db_column='MULTICLOUD', blank=True)  # Field name made lowercase.
    lfcregister = models.CharField(max_length=30, db_column='LFCREGISTER', blank=True)  # Field name made lowercase.
    stageinretry = models.IntegerField(null=True, db_column='STAGEINRETRY', blank=True)  # Field name made lowercase.
    stageoutretry = models.IntegerField(null=True, db_column='STAGEOUTRETRY', blank=True)  # Field name made lowercase.
    fairsharepolicy = models.CharField(max_length=1536, db_column='FAIRSHAREPOLICY', blank=True)  # Field name made lowercase.
    allowfax = models.CharField(max_length=192, db_column='ALLOWFAX', blank=True)  # Field name made lowercase.
    faxredirector = models.CharField(max_length=768, db_column='FAXREDIRECTOR', blank=True)  # Field name made lowercase.
    maxwdir = models.IntegerField(null=True, db_column='MAXWDIR', blank=True)  # Field name made lowercase.
    celist = models.CharField(max_length=12000, db_column='CELIST', blank=True)  # Field name made lowercase.
    minmemory = models.IntegerField(null=True, db_column='MINMEMORY', blank=True)  # Field name made lowercase.
    maxmemory = models.IntegerField(null=True, db_column='MAXMEMORY', blank=True)  # Field name made lowercase.
    mintime = models.IntegerField(null=True, db_column='MINTIME', blank=True)  # Field name made lowercase.

    def __str__(self):
        return 'Schedconfig:' + str(self.nickname)

    def getFields(self):
        return ["name", "nickname", "queue", "localqueue", "system", \
                "sysconfig", "environ", "gatekeeper", "jobmanager", "se", "ddm", \
                "jdladd", "globusadd", "jdl", "jdltxt", "version", "site", \
                "region", "gstat", "tags", "cmd", "lastmod", "errinfo", \
                "nqueue", "comment_", "appdir", "datadir", "tmpdir", "wntmpdir", \
                "dq2url", "special_par", "python_path", "nodes", "status", \
                "copytool", "copysetup", "releases", "sepath", "envsetup", \
                "copyprefix", "lfcpath", "seopt", "sein", "seinopt", "lfchost", \
                "cloud", "siteid", "proxy", "retry", "queuehours", "envsetupin", \
                "copytoolin", "copysetupin", "seprodpath", "lfcprodpath", \
                "copyprefixin", "recoverdir", "memory", "maxtime", "space", \
                "tspace", "cmtconfig", "setokens", "glexec", "priorityoffset", \
                "allowedgroups", "defaulttoken", "pcache", "validatedreleases", \
                "accesscontrol", "dn", "email", "allowednode", "maxinputsize", \
                 "timefloor", "depthboost", "idlepilotsupression", "pilotlimit", \
                 "transferringlimit", "cachedse", "corecount", "countrygroup", \
                 "availablecpu", "availablestorage", "pledgedcpu", \
                 "pledgedstorage", "statusoverride", "allowdirectaccess", \
                 "gocname", "tier", "multicloud", "lfcregister", "stageinretry", \
                 "stageoutretry", "fairsharepolicy", "allowfax", "faxredirector", \
                 "maxwdir", "celist", "minmemory", "maxmemory", "mintime"]

    def getValuesList(self):
        repre = []
        for field in self._meta.fields:
#            print field.name
#        for field in self.getFields():
#            repre.append((field, self.__dict__[field]))
            repre.append((field.name, field))
        return repre

    class Meta:
        db_table = u'schedconfig'


class Schedinstance(models.Model):
    name = models.CharField(max_length=180, db_column='NAME')  # Field name made lowercase.
    nickname = models.CharField(max_length=180, primary_key=True, db_column='NICKNAME')  # Field name made lowercase.
    pandasite = models.CharField(max_length=180, primary_key=True, db_column='PANDASITE')  # Field name made lowercase.
    nqueue = models.IntegerField(db_column='NQUEUE')  # Field name made lowercase.
    nqueued = models.IntegerField(db_column='NQUEUED')  # Field name made lowercase.
    nrunning = models.IntegerField(db_column='NRUNNING')  # Field name made lowercase.
    nfinished = models.IntegerField(db_column='NFINISHED')  # Field name made lowercase.
    nfailed = models.IntegerField(db_column='NFAILED')  # Field name made lowercase.
    naborted = models.IntegerField(db_column='NABORTED')  # Field name made lowercase.
    njobs = models.IntegerField(db_column='NJOBS')  # Field name made lowercase.
    tvalid = models.DateTimeField(db_column='TVALID')  # Field name made lowercase.
    lastmod = models.DateTimeField(db_column='LASTMOD')  # Field name made lowercase.
    errinfo = models.CharField(max_length=450, db_column='ERRINFO', blank=True)  # Field name made lowercase.
    ndone = models.IntegerField(db_column='NDONE')  # Field name made lowercase.
    totrunt = models.IntegerField(db_column='TOTRUNT')  # Field name made lowercase.
    comment_ = models.CharField(max_length=1500, db_column='COMMENT_', blank=True)  # Field name made lowercase.
    class Meta:
        db_table = u'schedinstance'

