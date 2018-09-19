# Make Datasets for LibInsight Ingest

Currently the only dataset we are transforming for ingest is circulation. Get the report from OCLC WMS under *Analytics-> Reports-> Circulation Reports-> Circulation Events Detail Report.

Run this report from the last date for which there is data in LibInsight until the present. Should probably develop a schedule like "First Friday of every month, the previous (or 2 ago, depending on OCLC's loading schedule) month's data gets loaded".

Report parameters should be dates, then under Circulation Event Type, limit to Check Out and Renew, otherwise it will count Check Ins, Removals, and all kinds of stuff that isn't what we're tracking.

The circulation script `circ_stats.py` defines a CLI that takes 2 paramaters, `--from_oclc` and `to_libinsight`, which state the path to the file from OCLC and where to save the file for LibInsight, respectively.

