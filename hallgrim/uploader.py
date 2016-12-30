################################################################################
#
# This is the uploader. It simplifies the testing process immensely and makes
# autoILIAS finally obsolete, since this system uses a proper Ilias
# implementation.
#
# The code is straight forward. You need to seed s couple of POST requests in
# the right order an then the items appear at the right place. Currently works
# for the Folder 'Sandkasten' of the test environment that ships with hallgrim.
# Ilias changes often so maybe the urls have to be updated.
#
# The simplest way was to intercept the html traffic with wireshark.
#
# Sadly this script adds some ugly dependencies like requests_toolbelt.
#
################################################################################

import os

import requests
from .MultipartEncoder import MultipartEncoder

__all__ = ['send_script']

# static data
login_url = "ilias/login.php"
upload_url = "ilias/ilias.php?ref_id=67&cmd=post&cmdClass=ilobjquestionpoolgui&cmdNode=26:gb&baseClass=ilRepositoryGUI&fallbackCmd=upload&rtoken=%s"
import_url = "ilias/ilias.php?ref_id=67&cmd=post&cmdClass=ilobjquestionpoolgui&cmdNode=26:gb&baseClass=ilRepositoryGUI&fallbackCmd=questions&rtoken=%s"
confirm_url = "ilias/ilias.php?ref_id=67&cmd=post&cmdClass=ilobjquestionpoolgui&cmdNode=26:gb&baseClass=ilRepositoryGUI&rtoken=%s"

import_data = {
    "cmd[importQuestions]": "Import",
}

confirm_data = {
    "cmd[importVerifiedFile]": "Import",
    "questions_only": "1",
}


def send_script(filepath, host, user, password, rtoken):
    login = {"username": user, "password": password, "cmd[showLogin]": "Login"}

    file = MultipartEncoder(fields={
        'xmldoc': (
            os.path.basename(filepath),
            open(filepath, 'rb'),
            'text/xml'
        )
    })
    header = {'Content-Type': file.content_type}

    # session create and login
    session = requests.Session()
    r = session.post(host + login_url, data=login)
    r = session.post(host + (import_url % rtoken), data=import_data)
    r = session.post(host + (upload_url % rtoken), data=file, headers=header)
    r = session.post(host + (confirm_url % rtoken), data=confirm_data)

    return r.status_code == 500
