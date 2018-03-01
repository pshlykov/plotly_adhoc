# plotly_adhoc
Repo for various charting scripts based on plotly

Contents: 
2018/02 plot_part_size_pg.py This script to generate a bar chart from a Postgres database showing size of partitions in a table,
        partitioned by day, into a offline html report and sends this report via email as an attachment.
        Partitions are expected to be named in format 'yyyy_mm_dd'
