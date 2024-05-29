from flask import Flask, render_template
import etcd3
import json

app = Flask(__name__)

def get_status(data):
    filestatusToken = "FileStatus"
    successfulltoken = "SuccessfullyTransfered"
    checksomeDifferenttoken = "CheckSumDifferent"
    filesizeToken = "FileSizeDifferent"
    nameToken = "Name"
    statuses = {}
    for key, value in data.items():
        if isinstance(value, dict):
            for file_key, file_value in value.items():
                filepath = file_value["Name"]
                if filestatusToken in file_value:
                    if file_value[filestatusToken] == successfulltoken:
                        statuses[filepath] = 'green'
                    elif file_value[filestatusToken] in [checksomeDifferenttoken, filesizeToken]:
                        statuses[filepath] = 'yellow'
                    else:
                        statuses[filepath] = 'red'
    return statuses

@app.route('/etcd', methods=['GET'])
def get_etcd_data():
    host = "192.168.0.175"
    port=2379
    etcd = etcd3.client(host=host, port=port)
    all_data = {}
    for value, metadata in etcd.get_all():
        key = metadata.key.decode('utf-8')
        value = json.loads(value.decode('utf-8'))
        all_data.update(get_status(value))
    return render_template('index.html', data=all_data)

if __name__ == '__main__':
    app.run(debug=True)