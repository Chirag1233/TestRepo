import etcd3
import json


keyName = "job3"
host = "192.168.0.175"
port=2379
etcd_key = "/edgeXray/TransferRequest/file_transfer_17169539551985740"
filesToken = "files"

etcd = etcd3.client(host=host, port=port) 
etcd.r