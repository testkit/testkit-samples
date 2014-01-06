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

name=$(basename $(pwd))
main_version="1.0.0"
release="1"
version="$main_version-$release"
appname=$(echo $name|sed 's/-/_/g')

# set value "1" if this suite need to sign,otherwise set "0" #
sign="0"

# set value "1" if this suite need to keep src_file,otherwise set "0" #
src_file="0"

# specified files to be kept in whitelist #
whitelist="
inst.sh
tests.xml
COPYING
LICENSE.Apache-2.0
LICENSE.CC-BY-3.0
NOTICE
mediasrc"
