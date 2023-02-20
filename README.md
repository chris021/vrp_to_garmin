# vrp_to_garmin
This is a collosal hack I threw together to get the NZ Visual Reporting Points into a Garmin G3X.

The CAA only publishes these in a programatically useless PDF format.  To use this script, you must
first manually download the PDF from **aip.net.nz**, as you must accept the aeropath license agreement.

The PDF can then be found under `AIR-NAVIGATION-REGISTER` -> `1.06 - Visual Reporting Points (VRP)`.

Place this PDF in the same file as the script (the filename is hardcoded because I'm just that
lazy).  The Garmin waypoint file will be output to STDOUT.

The import has yet to be tested, so let me know if it works for you.
