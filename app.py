from flask import Flask, render_template
import etcd3
import json

app = Flask(__name__)

def get_status(data):
    filestatusToken = "FileStatus"
    successfulltoken = "SuccessfullyTransfered"
    checksomeDifferenttoken = "CheckSumDifferent"
    filesizeToken = "FileSizeDifferent"
    for key, value in data.items():
        if isinstance(value, dict):
            return get_status(value)
        elif key == filestatusToken:
            if value == successfulltoken:
                return 'green'
            elif value == checksomeDifferenttoken or value == filesizeToken:
                return 'yellow'
            else:
                return 'red'
    return 'red'

@app.route('/etcd', methods=['GET'])
def get_etcd_data():
    host = "192.168.0.175"
    port=2379
    etcd = etcd3.client(host=host, port=port)
    all_data = {}
    for value, metadata in etcd.get_all():
        key = metadata.key.decode('utf-8')
        value = json.loads(value.decode('utf-8'))
        all_data[key] = get_status(value)
    return render_template('index.html', data=all_data)

if __name__ == '__main__':
    app.run(debug=True)