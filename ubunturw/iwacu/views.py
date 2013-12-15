from django.shortcuts import render
from django.conf import settings
from smartmin.views import *
from .models import *
from django.forms import Form
import zipfile
import os
import polib
import json


class MixedEntryCRUDL(SmartCRUDL):
    model = MixedEntry
    actions = ('unzip', 'list', 'export')

    class Export(SmartCsvView):
        fields = ('source', 'place', 'msgid', 'fr_msgstr', 'rw_msgstr', 'msgctxt', 'msgid_plural', 'fr_msgstr_plural', 'rw_msgstr_plural')

        def get_source(self, obj):
            return obj.pofile.program_name

        def get_place(self, obj):
            return obj.occurrences


    class Unzip(SmartFormView):
        class UnzipForm(Form):
            zip_file = forms.FileField()
    
        form_class = UnzipForm
        fields = ('zip_file',)
        success_message = 'Successfully Added'
        success_url = "@iwacu.mixedentry_list"
        submit_button_name = "Upload and Update Entries"

        def form_valid(self, form):
            file_to_unzip = self.form.cleaned_data['zip_file']

            #zfile = zipfile.ZipFile(file_to_unzip)
            #zfile.extractall(settings.EXTRACT_DIRS)
            self.import_new_entries()

            return HttpResponseRedirect(self.get_success_url())

        def import_new_entries(self):
            for root, dirs, files in os.walk(settings.EXTRACT_DIRS):
                for some_file in files:
                    if some_file.endswith(".po"):
                        if os.path.normpath(os.path.join(os.path.join(root, some_file), "../..")).endswith("fr"):
                            polib_po = polib.pofile(os.path.join(root, some_file))
                            for e in polib_po:
                                occurrences = json.dumps(e.occurrences)
                                new_entry = MixedEntry.get_or_create(some_file, 
                                                                     e.msgid, 
                                                                     occurrences, 
                                                                     e.msgctxt, 
                                                                     e.msgid_plural)

                                msgstr_plural = json.dumps(e.msgstr_plural)
                                new_entry.add_french_terms(e.msgstr, msgstr_plural)

                        if os.path.normpath(os.path.join(os.path.join(root, some_file), "../..")).endswith("rw"):
                            polib_po = polib.pofile(os.path.join(root, some_file))
                            for e in polib_po:
                                occurrences = json.dumps(e.occurrences)
                                new_entry = MixedEntry.get_or_create(some_file, 
                                                                     e.msgid, 
                                                                     occurrences, 
                                                                     e.msgctxt, 
                                                                     e.msgid_plural)
                        
                                msgstr_plural = json.dumps(e.msgstr_plural)
                                new_entry.add_rwanda_terms(e.msgstr, msgstr_plural)
