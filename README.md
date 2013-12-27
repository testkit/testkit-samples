# Test Environment
- Ubuntu 12.04 (32bit/64bit)
- Python 2.7 +
- Already get the source code and install Testkit-Lite test Host 
  Lite repo url: https://github.com/testkit/testkit-lite

# Build and Run

- Web Test Suite:

   Prepare for building by running the following command:

       $ cd webapi-testsuite-template

   Build ZIP package by running the following command:

       $ ./pack.sh

   Unzip the package on the test machine by running the following command:

       $ unzip -o webapi-testsuite-template-<version>.zip -d /opt/usr/media/tct

   Install the package on the test machine, use TIZEN Target for instance:

       $ sdb shell "/opt/usr/media/tct/opt/webapi-testsuite-template/inst.sh"

   Run test cases by running the following command on host:

       $ testkit-lite -f device:/opt/usr/media/tct/opt/webapi-testsuite-template/tests.xml -e "WRTLauncher" -o webapi-testsuite-template.results.xml

- Core Test Suite:

  TBD
