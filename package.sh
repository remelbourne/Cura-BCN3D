#!/usr/bin/env bash

set -e
set -u

# This script is to package the Cura package for Windows/Linux and Mac OS X
# This script should run under Linux and Mac OS X, as well as Windows with Cygwin.

#############################
# CONFIGURATION
#############################

##Select the build target
BUILD_TARGET=win32

##Do we need to create the final archive
ARCHIVE_FOR_DISTRIBUTION=1
##Which version name are we appending to the final archive
export BUILD_NAME=0.1.2
TARGET_DIR=Cura-BCN3D-${BUILD_NAME}-${BUILD_TARGET}

##Which CuraEngine to use
if [ -z ${CURA_ENGINE_REPO:-} ]; then
	CURA_ENGINE_REPO="https://github.com/Ultimaker/CuraEngine.git"
fi
if [ -z ${CURA_ENGINE_REPO_PUSHURL:-} ]; then
	CURA_ENGINE_REPO_PUSHURL="git@github.com:Ultimaker/CuraEngine.git"
fi
if [ -z ${CURA_ENGINE_BRANCH:-} ]; then
	CURA_ENGINE_BRANCH="legacy"
fi

JOBS=${JOBS:-3}

#############################
# Support functions
#############################
function checkTool
{
	if [ -z "`which $1`" ]; then
		echo "The $1 command must be somewhere in your \$PATH."
		echo "Fix your \$PATH or install $2"
		exit 1
	fi
}

function downloadURL
{
	filename=`basename "$1"`
	echo "Checking for $filename"
	if [ ! -f "$filename" ]; then
		echo "Downloading $1"
		curl -L -O "$1"
		if [ $? != 0 ]; then
			echo "Failed to download $1"
			exit 1
		fi
	fi
}

function extract
{
	echo "Extracting $*"
	echo "7z x -y $*" >> log.txt
	7z x -y $* >> log.txt
	if [ $? != 0 ]; then
        echo "Failed to extract $*"
        exit 1
	fi
}

function gitClone
{
	echo "Cloning $1 into $3"
	echo "  with push URL $2"
	if [ -d $3 ]; then
		cd $3
		git clean -dfx
		git reset --hard
		git pull
		cd -
	else
		if [ ! -z "${4-}" ]; then
			git clone $1 $3 --branch $4
		else
			git clone $1 $3
		fi
		git config remote.origin.pushurl "$2"
	fi
}

#############################
# Actual build script
#############################

if [ "$BUILD_TARGET" = "none" ]; then
	echo "You need to specify a build target with:"
	echo "$0 win32"
	echo "$0 debian_i386"
	echo "$0 debian_amd64"
	echo "$0 debian_armhf"
	echo "$0 darwin"
	echo "$0 freebsd"
	echo "$0 fedora                         # current   system"
	echo "$0 fedora \"mock_config_file\" ...  # different system(s)"
	exit 0
fi

if [ -z `which make` ]; then
	MAKE=mingw32-make
else
	MAKE=make
fi

# Change working directory to the directory the script is in
# http://stackoverflow.com/a/246128
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

checkTool git "git: http://git-scm.com/"
checkTool curl "curl: http://curl.haxx.se/"
if [ $BUILD_TARGET = "win32" ]; then
	checkTool avr-gcc "avr-gcc: http://winavr.sourceforge.net/ "
	#Check if we have 7zip, needed to extract and packup a bunch of packages for windows.
	checkTool 7z "7zip: http://www.7-zip.org/"
	checkTool $MAKE "mingw: http://www.mingw.org/"
fi
#For building under MacOS we need gnutar instead of tar
if [ -z `which tar` ]; then
	TAR=tar
else
	TAR=gnutar
fi

#############################
# Build the required firmwares arduino-1.0.1
#############################

if [ -d "C:/Arduino" ]; then
	ARDUINO_PATH=C:/Arduino
	ARDUINO_VERSION=105
elif [ -d "/Applications/Arduino.app/Contents/Resources/Java" ]; then
	ARDUINO_PATH=/Applications/Arduino.app/Contents/Resources/Java
	ARDUINO_VERSION=$(defaults read /Applications/Arduino.app/Contents/Info.plist CFBundleGetInfoString | sed -e 's/\.//g')
	PATH=$PATH:/Applications/Arduino.app/Contents/Resources/Java/hardware/tools/avr/bin/
else
	ARDUINO_PATH=/usr/share/arduino
	ARDUINO_VERSION=105
fi


if [ ! -d "$ARDUINO_PATH" ]; then
 echo "Arduino path '$ARDUINO_PATH' doesn't exist"
  exit 1
fi

#############################
# Build the packages
#############################
	
if [ $BUILD_TARGET = "win32" ]; then
		CXX=g++
fi
    


#add Cura
mkdir -p ${TARGET_DIR}/Cura ${TARGET_DIR}/resources ${TARGET_DIR}/plugins ${TARGET_DIR}/python
cp -a Cura/* ${TARGET_DIR}/Cura
cp -a resources/* ${TARGET_DIR}/resources
cp -a plugins/* ${TARGET_DIR}/plugins
cp -a python/* ${TARGET_DIR}/python
#Add cura version file
echo $BUILD_NAME > ${TARGET_DIR}/Cura/version

#add script files
if [ $BUILD_TARGET = "win32" ]; then
    cp -a scripts/${BUILD_TARGET}/*.bat ${TARGET_DIR}/
    cp CuraEngine/build/CuraEngine.exe ${TARGET_DIR}
	cp libgcc_s_sjlj-1.dll ${TARGET_DIR}
    cp libwinpthread-1.dll ${TARGET_DIR}
    cp libstdc++-6.dll ${TARGET_DIR}
fi

#package the result
if (( ${ARCHIVE_FOR_DISTRIBUTION} )); then
	if [ $BUILD_TARGET = "win32" ]; then
		#rm ${TARGET_DIR}.zip
		#cd ${TARGET_DIR}
		#7z a ../${TARGET_DIR}.zip *
		#cd ..		
		if [ -f '/c//NSIS/makensis.exe' ]; then
			echo "segundo"
			rm -rf scripts/win32/dist
			mv "`pwd`/${TARGET_DIR}" scripts/win32/dist
			'/c/NSIS/makensis.exe' -DVERSION=${BUILD_NAME} 'scripts/win32/installer.nsi' >> log.txt
            if [ $? != 0 ]; then echo "Failed to package NSIS installer"; exit 1; fi
			mv scripts/win32/Cura-BCN3D-${BUILD_NAME}.exe ./
		fi
	else
		echo "Archiving to ${TARGET_DIR}.tar.gz"
		$TAR cfp - ${TARGET_DIR} | gzip --best -c > ${TARGET_DIR}.tar.gz
	fi
else
	echo "Installed into ${TARGET_DIR}"
fi