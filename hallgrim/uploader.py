################################################################################
#
# This is the uploader. It simplifies the testing process immensely and  makes
# autoILIAS finally obsolete, since this system uses a proper Ilias
# implementation.
#
# The code is straight forward. You need to seed s couple of POST requests
# in the right order an then the items appear at the right place. Currently
# works for the Folder 'Sandkasten' of the test environment that ships
# with hallgrim. Ilias changes often so maybe the urls have to be updated.
#
# The simplest way was to intercept the html traffic with wireshark.
#
# Sadly this script adds some ugly dependencies like requests_toolbelt.
#
################################################################################

import os

import requests
from requests_toolbelt import MultipartEncoder
from lxml import html

__all__ = ['send_script']

# static data
host = "http://192.168.1.2/"
login = {"username" : "root", "password" : "homer", "cmd[showLogin]" : "Login"}
upload_url = host + "ilias/ilias.php?ref_id=65&cmd=post&cmdClass=ilobjquestionpoolgui&cmdNode=26:gb&baseClass=ilRepositoryGUI&fallbackCmd=upload&rtoken=fd2f3337a6d4ae0689b5163d6af186a9"
import_url = host + "ilias/ilias.php?ref_id=65&cmd=post&cmdClass=ilobjquestionpoolgui&cmdNode=26:gb&baseClass=ilRepositoryGUI&fallbackCmd=questions&rtoken=fd2f3337a6d4ae0689b5163d6af186a9"
confirm_url = host + "ilias/ilias.php?ref_id=65&cmd=post&cmdClass=ilobjquestionpoolgui&cmdNode=26:gb&baseClass=ilRepositoryGUI&rtoken=fd2f3337a6d4ae0689b5163d6af186a9"

import_data = {
    "cmd[importQuestions]" : "Import",
}

confirm_data = {
    "cmd[importVerifiedFile]" : "Import",
    "questions_only" : "1",
}


def send_script(filepath):
    file = MultipartEncoder(fields={
        'xmldoc': (
            os.path.basename(filepath),
            open(filepath, 'rb'),
            'text/xml'
        )
    })

    # session create and login
    session = requests.Session()
    r = session.post(host + "ilias/login.php", data=login)
    r = session.post(import_url, data=import_data)
    r = session.post(upload_url, data=file, headers={'Content-Type': file.content_type})
    r = session.post(confirm_url, data=confirm_data)

    return r.status_code == 500

