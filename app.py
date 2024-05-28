from flask import Flask, jsonify, render_template
import etcd3

app = Flask(__name__)

@app.route('/etcd', methods=['GET'])
def get_etcd_data():
    etcd = etcd3.client(host='192.168.0.175', port=2379)  # replace with your etcd server details
    all_data = {}
    for value, metadata in etcd.get_all():
        all_data[metadata.key.decode('utf-8')] = value.decode('utf-8')
    return render_template('index.html', data=all_data)

if __name__ == '__main__':
    app.run(debug=True)