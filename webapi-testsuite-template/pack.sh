#!/bin/bash
#
# Authors:
#             Jing Wang <jing.j.wang@intel.com>
#             Huajun Li <huajun.li@intel.com>
#	      Yugang Fan <yugang.fan@intel.com>
#
# script create rpm package

#parse params
USAGE="Usage: ./pack.sh [-t <package type: all | crx | wgt | zip>]"

platforms=""
blacklists=""
if [ -d "resources" ]; then
    blacklists=`ls resources/blacklist.* | sed 's/resources\/blacklist.//g'`
fi
if [[ "$blacklists" != "" ]]; then
    platforms=`echo $blacklists | sed 's/ / \| /g' | sed 's/\ | default//g'`
fi

if [[ $1 == "-h" || $1 == "--help" ]]; then
    if [[ $platforms != "" ]]; then
        echo $USAGE "[-p "$platforms"]"
    else
        echo $USAGE
    fi
    echo "Create package with wgt and raw source by default"
    exit 1
fi

type="wgt"
platform="default"
while getopts t:p: o
do
    case "$o" in
    t) type=$OPTARG;;
    p) platform=$OPTARG;;
    *) echo $USAGE "[-p "$platforms"]"
       echo "Create package with wgt and raw source by default"
       exit 1;;
    esac
done

if [ -f "resources/blacklist.$platform" ]; then
    cp -f resources/blacklist.$platform  resources/blacklist.js
elif [[ $platform != "default" ]]; then
    echo "No such platform: $platform"
    exit 1
fi

echo "Create package with $type and raw source"
sleep 3

# parse spec required name
NAME=`grep "Name:" *.spec | awk '{print $2}'`
if [ -z "$NAME" ];then
	echo "Name not specified in spec file"
	exit 1
fi


# parse spec required version
VERSION=`grep "Version:" ${NAME}.spec | awk '{print $2}'`
if [ -z "$VERSION" ];then
	echo "Version not specified in spec file"
	exit 1
fi

SRC_ROOT=${PWD}
RPM_ROOT=/tmp/${NAME}_pack
ARCHIVE_TYPE=tar.gz 	#tar.gz2
ARCHIVE_OPTION=czvf  	#cjvf

# check precondition
check_precondition()
{
    which $1 > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "Error: no tool: $1"
        exit 1
    fi
}
check_precondition rpmbuild
check_precondition gcc
check_precondition make


# clean
echo "cleaning rpm workspace... >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
rm -rf $RPM_ROOT

# create workspace
echo "create rpm workspace... >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
mkdir -p $RPM_ROOT/RPMS $RPM_ROOT/SRPMS $RPM_ROOT/SPECS $RPM_ROOT/SOURCES $RPM_ROOT/BUILD $RPM_ROOT/src_tmp/$NAME-$VERSION

# prepare
echo "prepare workspace... >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
rm -rf *.rpm *.tar.bz2 *.tar.gz *.zip
cp -a $SRC_ROOT/* $RPM_ROOT/src_tmp/$NAME-$VERSION
# create Makefile in top src folder
#cp $SRC_ROOT/top_Makefile $RPM_ROOT/src_tmp/$NAME-$VERSION/Makefile
cp $PWD/${NAME}.spec $RPM_ROOT/SPECS
cd $RPM_ROOT/src_tmp
tar $ARCHIVE_OPTION $RPM_ROOT/SOURCES/$NAME-$VERSION.$ARCHIVE_TYPE $NAME-$VERSION
cd -

# build
echo "build from workspace... >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
cd  $RPM_ROOT/SPECS
rpmbuild -ba ${NAME}.spec --clean --define "_topdir $RPM_ROOT" --define="TYPE $type" --target=noarch
cd -

# copy packages
echo "copy from workspace... >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
echo "get packages......"
if [ $type == 'all' ]; then
	find $RPM_ROOT -name "$NAME*.zip" | grep -v debuginfo | xargs -n1 -I {} mv {} $PWD -f
	find $RPM_ROOT -name "$NAME*.rpm" | grep -v debuginfo | xargs -n1 -I {} mv {} $PWD -f
elif [ $type == 'zip' ]; then
	find $RPM_ROOT -name "$NAME*.zip" | grep -v debuginfo | xargs -n1 -I {} mv {} $PWD -f
	find $RPM_ROOT -name "$NAME*.src.rpm" | grep -v debuginfo | xargs -n1 -I {} mv {} $PWD -f
else
	find $RPM_ROOT -name "$NAME*.rpm" | grep -v debuginfo | xargs -n1 -I {} mv {} $PWD -f
fi

if [[ $platform != "" && $platform != "default" ]]; then
	cd $PWD
	for file in `ls *.zip`; do
	        new_name=`echo $file | sed "s/\.zip/\.$platform\.zip/g"`
                mv $file $new_name
        done
	for file in `ls *.rpm`; do
		new_name=`echo $file | sed "s/\.rpm/\.$platform\.rpm/g"`
                mv $file $new_name
        done
        cd -
fi

echo "get $NAME-$VERSION.$ARCHIVE_TYPE......"
mv $RPM_ROOT/SOURCES/$NAME-$VERSION.$ARCHIVE_TYPE $PWD -f

# clean
echo "cleaning workspace... >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
rm -rf $RPM_ROOT

# validate
echo "checking result... >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
if [ $type == 'all' ] || [ $type == 'zip' ]; then
	if [ -z "`ls | grep "\.rpm"`" ] || [ -z "`ls | grep "\.$ARCHIVE_TYPE"`" ] || [ -z "`ls | grep "\.zip"`" ];then
		echo "------------------------------ FAILED to build $NAME packages --------------------------"
		exit 1
	fi		
else
	if [ -z "`ls | grep "\.rpm"`" ] || [ -z "`ls | grep "\.$ARCHIVE_TYPE"`" ];then
		echo "------------------------------ FAILED to build $NAME packages --------------------------"
		exit 1
	fi
fi

echo "------------------------------ Done to build $NAME packages --------------------------"
ls *.rpm *.$ARCHIVE_TYPE *.zip 2>/dev/null
