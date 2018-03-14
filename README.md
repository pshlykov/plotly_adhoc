# plotly_adhoc
Repo for various charting scripts based on plotly

Contents: 
2018/02 plot_part_size_pg.py This script to generate a bar chart from a Postgres database showing size of partitions in a table,
        partitioned by day, into a offline html report and sends this report via email as an attachment.
        Partitions are expected to be named in format 'yyyy_mm_dd'

for Envelope -- don't forget this:
https://github.com/tomekwojcik/envelopes/issues/18

a workaround is here:
https://github.com/tomekwojcik/envelopes/issues/18#issuecomment-159093421

i.e. replace this
```
        if type_maj == 'text' and type_min in ('html', 'plain'):
            msg.attach(MIMEText(part[1], type_min, self._charset))
        else:
            msg.attach(part[1])
```

with this:

```
if type_maj == 'text' and type_min in ('html', 'plain') and\
            (isinstance(part[1], str) or isinstance(part[1], unicode)):
            msg.attach(MIMEText(part[1], type_min, self._charset))
        else:
            msg.attach(part[1])
```

in the line 291 of envelope.py 
