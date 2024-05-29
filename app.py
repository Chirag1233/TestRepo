from flask import Flask, render_template_string
from json2html import *
import etcd3
import json

app = Flask(__name__)

@app.route('/etcd', methods=['GET'])
def get_etcd_data():
    host = "192.168.0.175"
    port=2379
    etcd = etcd3.client(host=host, port=port)
    all_data = {}
    for value, metadata in etcd.get_all():
        key = metadata.key.decode('utf-8')
        value = json.loads(value.decode('utf-8'))
        all_data[key] = value
    html = json2html.convert(json = all_data)
    return render_template_string('<html><body>{}</body></html>'.format(html))

if __name__ == '__main__':
    app.run(debug=True)