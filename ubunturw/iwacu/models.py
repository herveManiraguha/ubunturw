from django.db import models
from smartmin.models import SmartModel
from django.contrib.auth.models import User
from django.conf import settings

class PofileModel(SmartModel):
    program_name = models.CharField(max_length=128)

    @classmethod
    def get_or_create(cls, name):
        user = User.objects.get(pk=settings.ANONYMOUS_USER_ID)

        pofiles = cls.objects.filter(program_name=name)
        if pofiles:
            return pofiles[0]
        return cls.objects.create(program_name=name, 
                                  created_by=user, 
                                  modified_by=user)



class MixedEntry(SmartModel):
    pofile = models.ForeignKey(PofileModel)
    msgid = models.TextField()
    msgctxt = models.TextField()
    msgid_plural = models.TextField()
    fr_msgstr = models.TextField()
    rw_msgstr = models.TextField()
    fr_msgstr_plural = models.TextField()
    rw_msgstr_plural = models.TextField()
    occurrences = models.TextField()

    @classmethod
    def get_or_create(cls, program_name, msgid, occurrences, msgctxt='', msgid_plural=''):

        if not msgctxt:
            msgctxt = ""


        user = User.objects.get(pk=settings.ANONYMOUS_USER_ID)
        pofile = PofileModel.get_or_create(program_name)

        entries = cls.objects.filter(pofile=pofile, msgid=msgid, occurrences=occurrences)
        if entries:
            return entries[0]

        return cls.objects.create(pofile=pofile, 
                                  msgid=msgid, 
                                  occurrences=occurrences, 
                                  msgctxt=msgctxt, 
                                  msgid_plural=msgid_plural, 
                                  created_by=user, 
                                  modified_by=user)

    def add_french_terms(self, msgstr, msgstr_plural):
        self.fr_msgstr = msgstr
        self.fr_msgstr_plural = msgstr_plural
        self.save()

    def add_rwanda_terms(self, msgstr, msgstr_plural):
        self.rw_msgstr = msgstr
        self.rw_msgstr_plural = msgstr_plural
        self.save()
            

 
