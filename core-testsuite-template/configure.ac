AC_PREREQ(2.63)
AC_INIT(core-testsuite-template, 1.0.0, name@company.com)

#AC_CONFIG_SRCDIR(src/main.c)
AM_INIT_AUTOMAKE(core-testsuite-template, 1.0.0)

AC_PROG_CC
AC_ISC_POSIX

AC_PROG_LN_S
AC_PROG_MAKE_SET
AC_PROG_GCC_TRADITIONAL
AM_PROG_CC_C_O


CFLAGS="$CFLAGS -g -Wall -Werror -Wno-format"

PROVIDER_SUBDIRS="test"
AC_SUBST(PROVIDER_SUBDIRS)


TEST_BIN_DIR="/opt/${PACKAGE}-${VERSION}"
AC_SUBST(TEST_BIN_DIR)

XML_DATA_DIR="${datadir}${PACKAGE}"
AC_SUBST(XML_DATA_DIR)

AC_CONFIG_FILES([
Makefile
src/Makefile
])

AC_OUTPUT

echo ""
echo "tts-example-test  ${VERSION} has been configured as follows: "
echo "---------------------------------------------------"
echo "Source code location:   ${srcdir}"
echo "Compiler:               ${CC}"
echo "Providers:              ${PROVIDER_SUBDIRS}"
echo ""
