import json
import psycopg2
import os, re
import plotly.offline as offline
import plotly.graph_objs as plgo
from envelopes import Envelope

with open('config.json') as conf:
    parms = json.load(conf)

conf.close()

conn_str = "dbname={0} host={1} port={2} user={3} password={4}"\
           .format(parms["database_name"], parms["host_name"], parms["port_number"],\
           parms["username"], parms["password"])

try:
    conn = psycopg2.connect(conn_str)
except:
    print("Error connecting to the database")
    exit(1)

sql = """select right(relname,10), pg_total_relation_size(oid)/1024/1024/1024::float
         from pg_class
         where relname like 'meter_channel_reading_2%'
         and reltype<>0
         /*order by 1*/"""

cur = conn.cursor()
cur.execute(sql)
rows = cur.fetchall()

plot_data = {}
for row in rows:
    plot_data[row[0]] = row[1]

cur.close()
conn.close()

plot_data_x = sorted(plot_data.keys())
plot_data_y = []

for itm in plot_data_x:
    plot_data_y.append(plot_data[itm])

graph = plgo.Bar(x=plot_data_x, y=plot_data_y)
data = [graph]
layout = plgo.Layout(title='Partition size (Gib)')

fig = plgo.Figure(data=data, layout=layout)
rep_file_name = offline.plot(fig)


envelope = Envelope(from_addr = (u'no-reply@mailserver.com'),
                      to_addr = (parms["email_to"]),
                      subject = u'Daily partitions size bar chart',
                    text_body = u'Please open the attachment to explore the graph'
                   )

envelope.add_attachment(re.sub('file:///','/',rep_file_name,1))
envelope.send(parms["smtp_relay"])

exit(0)