##
# Copyright (c) 2012 Intel Corporation.
# 
# Redistribution and use in source and binary forms, with or without modification, 
# are permitted provided that the following conditions are met:
# 
# *Redistributions of works must retain the original copyright notice, this list 
# of conditions and the following disclaimer.
# *Redistributions in binary form must reproduce the original copyright notice, 
# this list of conditions and the following disclaimer in the documentation 
# and/or other materials provided with the distribution.
# *Neither the name of Intel Corporation nor the names of its contributors 
# may be used to endorse or promote products derived from this work without 
# specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY INTEL CORPORATION "AS IS" 
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
# ARE DISCLAIMED. IN NO EVENT SHALL INTEL CORPORATION BE LIABLE FOR ANY DIRECT, 
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, 
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, 
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY 
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING 
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, 
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.  
# 
# Authors:
#         Zhang, Zhiqiang <zhiqiang.zhang@intel.com> 
#


Summary: webapi test suite template
Name: webapi-testsuite-template
Version: 1.0.0
Release: 1
License: BSD
Group: System/Libraries
Source: %name-%version.tar.gz
#Requires: webapi-helper
#BuildRoot: %_topdir/%name-%version-buildroot

%description
This is webapi test suite template package


%prep
%setup -q

%build
./autogen
./configure --prefix=/usr
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

############## generate crx, wgt packge ####################
crx_installer="chromium-browser"
wgt_installer="wrt-installer"

cp -a $RPM_BUILD_ROOT  $RPM_BUILD_DIR/%name
cp -a manifest.json    $RPM_BUILD_DIR/%name
cp -a custom.png       $RPM_BUILD_DIR/%name

pre_dir=`pwd`
cd $RPM_BUILD_DIR/%name

cat > index.html << EOF
<!doctype html>
<head>
    <meta http-equiv="Refresh" content="1; url=opt/%name/testkit/web/index.html?testsuite=/usr/share/%name/tests.xml">
</head>
EOF

#create crx
if [[ %TYPE == "all" || %TYPE == "crx" ]]; then
    echo %TYPE
    which $crx_installer > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        export DISPLAY=:0
        cp -f $pre_dir/config.xml.crx ./config.xml
        $crx_installer --user-data-dir=/tmp  --pack-extension=../%name
        mv ../%name.crx  $RPM_BUILD_ROOT/opt/%name/
    fi
fi

#create zip
cp -f $pre_dir/config.xml.crx ./config.xml
cd $RPM_BUILD_DIR
zip -Drq %name-%version-%release.zip %name
cd $RPM_BUILD_DIR/%name

#create wgt
cp -f $pre_dir/config.xml.wgt ./config.xml
zip -rq $RPM_BUILD_ROOT/opt/%name/%name.wgt *

cd $pre_dir
rm -rf $RPM_BUILD_DIR/%name

#copy web runtime launcher wraper
#mkdir -p $RPM_BUILD_ROOT/usr/bin
#chmod 755 WRTLauncher
#cp -a WRTLauncher $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/opt/unpacked_crx/%name
########################## end ##############################


%clean
rm -rf $RPM_BUILD_ROOT

%files
/opt/%name
/usr/share/%name
#/usr/bin/WRTLauncher
/opt/unpacked_crx/%name

%changelog

%post
############## install/uninstall crx, wgt packge ####################
crx_installer="chromium-browser"
wgt_installer="wrt-installer"

which $crx_installer > /dev/null 2>&1
if [ $? -eq 0 ]; then
    crx_install_dir="/opt/unpacked_crx/%name"
    cd $crx_install_dir
    [ -e /opt/%name/%name.crx ] && unzip /opt/%name/%name.crx
    cd -
    #postpone crx installation, and install it before execute testing because the rpm is installed by root, and it can't install crx correctly
    #$crx_installer --user-data-dir=/tmp --load-extension=$crx_install_dir
fi

which $wgt_installer > /dev/null 2>&1
if [ $? -eq 0 ]; then
    [ -e /opt/%name/%name.wgt ] && $wgt_installer -i /opt/%name/%name.wgt
    wgt_install_dir="/opt/apps/org.tizen.`wrt-launcher -l | tail -n 1 | grep %name | awk '{ print $2 }'`"
    echo $wgt_install_dir/res/src/
fi


%postun
crx_installer="chromium-browser"
wgt_installer="wrt-installer"

which $wgt_installer > /dev/null 2>&1
if [ $? -eq 0 ]; then
    $wgt_installer -un %name
fi

rm -rf /opt/unpacked_crx/%name
########################## end ##############################
