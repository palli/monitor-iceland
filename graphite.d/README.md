graphite.d
==========

This directory contains misc scripts that collect data in print them out
in a graphite compatible form.

Every file in here should be able to run without parameters and print data to stdout in the form of:

METRIC_NAME	value	timestamp

Example:
```
# ./landspitali.py 
landspitali.birthNumbers 5 1374439387
landspitali.surgeries 2 1374439387
landspitali.dischargedNumbers 39 1374439387
landspitali.hospitalizedNumbers 39 1374439387
landspitali.atwork 306 1374439387
landspitali.patients-child 6 1374439387
landspitali.patients-er 25 1374439387
landspitali.patients-walk 27 1374439387
landspitali.patients-icu 6 1374439387
landspitali.patients-hotel 27 1374439387
landspitali.donors 0 1374439387
landspitali.patients-skilun 0 1374439387
landspitali.patients-heart2 0 1374439387
```
