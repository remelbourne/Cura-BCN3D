"""
The version utility module is used to get the current Cura version, and check for updates.
It can also see if we are running a development build of Cura.
"""
__copyright__ = "Copyright (C) 2013 David Braam - Released under terms of the AGPLv3 License"

import os
import re
import sys
import urllib
import urllib2
import platform
import subprocess
import zipfile
import wx

try:
    from xml.etree import cElementTree as ElementTree
except:
    from xml.etree import ElementTree

from Cura.util import resources

def getVersion(getGitVersion = True):
    gitPath = os.path.abspath(os.path.join(os.path.split(os.path.abspath(__file__))[0], "../.."))
    if hasattr(sys, 'frozen'):
        versionFile = os.path.normpath(os.path.join(resources.resourceBasePath, "version"))
    else:
        versionFile = os.path.abspath(os.path.join(os.path.split(os.path.abspath(__file__))[0], "../version"))

    if getGitVersion:
        try:
            gitProcess = subprocess.Popen(args = "git show -s --pretty=format:%H", shell = True, cwd = gitPath, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            (stdoutdata, stderrdata) = gitProcess.communicate()

            if gitProcess.returncode == 0:
                return stdoutdata
        except:
            pass

    gitHeadFile = gitPath + "/.git/refs/heads/SteamEngine"
    if os.path.isfile(gitHeadFile):
        if not getGitVersion:
            return "dev"
        f = open(gitHeadFile, "r")
        version = f.readline()
        f.close()
        return version.strip()
    if os.path.exists(versionFile):
        f = open(versionFile, "r")
        version = f.readline()
        f.close()
        return version.strip()
    versionFile = os.path.abspath(os.path.join(os.path.split(os.path.abspath(__file__))[0], "../../version"))
    if os.path.exists(versionFile):
        f = open(versionFile, "r")
        version = f.readline()
        f.close()
        return version.strip()
    return "UNKNOWN" #No idea what the version is. TODO:Tell the user.

def isDevVersion():
    gitPath = os.path.abspath(os.path.join(os.path.split(os.path.abspath(__file__))[0], "../../.git"))
    hgPath  = os.path.abspath(os.path.join(os.path.split(os.path.abspath(__file__))[0], "../../.hg"))
    return os.path.exists(gitPath) or os.path.exists(hgPath)

# Get the latest version of firmware which is found in the bcn3d github website
def getLatestVersion():
    base_url = 'https://github.com/BCN3D/BCN3D-Firmware/archive/'

    url = 'https://github.com/BCN3D/BCN3D-Firmware/releases/'
    urlContent = urllib2.urlopen(url)
    data = urlContent.read()

    versionMatch = re.search(r'([\d.]+)\.(zip)', data)

    if not versionMatch:
        sys.exit('Couldn\'t find the Latest Version!')

    version = versionMatch.group(1)
    print 'The latest firmware version available is: ',version
    mychoice = wx.MessageBox(_("The latest firmware version available is: " + version + "\nWant to download the new version?"), _("New Version"), wx.YES_NO)

    if mychoice == wx.NO:
        print 'Hemos escogido no seguir'
        return None
    else:
        isDownloaded = downloadLatestVersion(version, base_url)
        if isDownloaded == None:
            return None
        elif isDownloaded != None:
            return not None

def downloadLatestVersion(version,base_url):

    version_url = base_url + version + '.zip'

    if sys.platform.startswith('win'):
        os.chdir(os.path.expanduser('~') + '\Documents')
        dir = 'Cura-BCN3D'
        if not os.path.exists(dir):
            home = os.path.expanduser('~')
            os.chdir(home + '\Documents')
            os.mkdir(dir)
    elif sys.platform.startswith('darwin'):
        os.chdir(os.path.expanduser('~') + '/Documents')
        dir = 'Cura-BCN3D'
        if not os.path.exists(dir):
            home = os.path.expanduser('~')
            os.chdir(home + '/Documents')
            os.mkdir(dir)

    myVar = firmwareAlreadyInstalled(version)

    if myVar != None:
        print 'Downloading Version... ',version
        urllib.urlretrieve(version_url, os.path.join(dir, version + '.zip'))
        print 'Done downloading!'

        print 'Inflating files...'
        os.chdir('Cura-BCN3D')
        with zipfile.ZipFile(version + '.zip') as z:
            z.extractall()
        print 'Done unziping the files!'

        if sys.platform == 'Windows':
            os.chdir(os.path.expanduser('~') + '\Documents')
        elif sys.platform == 'darwin':
            os.chdir(os.path.expanduser('~') + '/Documents')
        return not None

    elif myVar == None:
        return None

def firmwareAlreadyInstalled(version):

    if sys.platform == 'Windows':
        os.path.expanduser('~') + '\Documents\Versions'
    elif sys.platform == 'darwin':
        os.chdir(os.path.expanduser('~') + '/Documents')

    fname = version + '.zip'
    yes = fname in os.listdir('Cura-BCN3D')

    if yes == True:
        print 'Repositories up to date!'
        wx.MessageBox(_("Repositories up to date!"), _("Repository Information"), wx.OK)
        return None
    else:
        return not None
###### Until here what we have written

def checkForNewerVersion():
    if isDevVersion():
        return None
    try:
        updateBaseURL = 'http://software.ultimaker.com'
        localVersion = map(int, getVersion(False).split('.'))
        while len(localVersion) < 3:
            localVersion += [1]
        latestFile = urllib2.urlopen("%s/latest.xml" % (updateBaseURL))
        latestXml = latestFile.read()
        latestFile.close()
        xmlTree = ElementTree.fromstring(latestXml)
        for release in xmlTree.iter('release'):
            os = str(release.attrib['os'])
            version = [int(release.attrib['major']), int(release.attrib['minor']), int(release.attrib['revision'])]
            filename = release.find("filename").text
            if platform.system() == os:
                if version > localVersion:
                    return "%s/current/%s" % (updateBaseURL, filename)
    except:
        #print sys.exc_info()
        return None
    return None

if __name__ == '__main__':
    print(getVersion())
