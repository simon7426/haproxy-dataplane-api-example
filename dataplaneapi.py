from json import load
import requests
from requests.models import HTTPBasicAuth
import os

load_balancer_link = 'http://36.255.68.245:5555/v2'
auth = HTTPBasicAuth('admin','adminpwd')
transaction_id = '34f3f8ba-6ffa-45ae-b878-8b8b5e6c3174'
def get_configuration():
    config_link = '/services/haproxy/configuration/raw'
    url = load_balancer_link + config_link
    resp = requests.get(url,auth=auth)
    version = resp.json().get('_version')
    print(version)
    data = resp.json().get('data')
    print(data)
    return {
        'version': version,
        'data': data
    }

def get_transaction_list():
    config_link = '/services/haproxy/transactions'
    url = load_balancer_link + config_link
    resp = requests.get(url,auth=auth)
    data = resp.json()
    print(data)

def start_transaction():
    version_no = get_configuration()['version']
    config_link = f'/services/haproxy/transactions?version={version_no}'
    url = load_balancer_link + config_link
    resp = requests.post(url,auth=auth)
    print(resp.status_code)
    print(resp.json())

def delete_transaction():
    config_link = f'/services/haproxy/transactions/{transaction_id}'
    url = load_balancer_link + config_link
    resp = requests.delete(url,auth=auth)
    print(resp.status_code)

def add_backend():
    config_link = '/services/haproxy/configuration/backends?'
    query_string = 'transaction_id='+transaction_id
    data = {
        'name': 'all_backend',
        'mode': 'http',
    }
    url = load_balancer_link + config_link + query_string
    resp = requests.post(url,json=data,auth=auth)
    print(resp.status_code)
    print(resp.json())

def delete_backend(backend_name):
    config_link = '/services/haproxy/configuration/backends/'
    query_string = 'transaction_id='+transaction_id
    url = load_balancer_link+config_link+backend_name + '?' + query_string
    resp = requests.delete(url,auth=auth)
    print(resp.status_code)

def add_server(server_name,server_ip,server_port):
    config_link = '/services/haproxy/configuration/servers'
    query_string = '?backend='+'all_backend'+'&'+'transaction_id='+transaction_id
    url = load_balancer_link + config_link + query_string
    data = {
        'name': server_name,
        'address': server_ip,
        'port': server_port
    }
    resp = requests.post(url,auth=auth,json=data)
    print(resp.status_code)
    print(resp.json())

def delete_server(server_name, backend_name):
    config_link = f'/services/haproxy/configuration/servers/{server_name}'
    query_string = f'?backend={backend_name}&transaction_id={transaction_id}'
    url = load_balancer_link + config_link + query_string
    resp = requests.delete(url,auth=auth)
    print(resp.status_code)
    # print(resp.json())

def add_frontend():
    config_link = '/services/haproxy/configuration/frontends'
    query_string = '?transaction_id='+transaction_id
    data = {
        'name': 'all_frontend',
        'mode': 'http',
        'default_backend': 'all_backend',
    }
    url = load_balancer_link + config_link + query_string
    resp = requests.post(url,json=data,auth=auth)
    print(resp.status_code)
    print(resp.json())

def add_bind(address,port):
    config_link = '/services/haproxy/configuration/binds'
    query_string = '?'+'frontend=all_frontend&'+'transaction_id='+transaction_id
    data = {
        "address": address,
        "name": "all_bind",
        "port": port
    }
    url = load_balancer_link + config_link + query_string
    resp = requests.post(url,auth=auth,json=data)
    print(resp.status_code)
    print(resp.json())

def commit_transaction():
    config_link = '/services/haproxy/transactions/'+transaction_id
    url = load_balancer_link + config_link
    resp = requests.put(url,auth=auth)
    print(resp.status_code)
    print(resp.json())

def get_all_transactions():
    url = load_balancer_link + '/services/haproxy/transactions'
    resp = requests.get(url, auth=auth)
    print(resp.status_code)
    print(resp.json())

def get_transactions(transaction_id):
    url = load_balancer_link + f'/services/haproxy/transactions/{transaction_id}'
    resp = requests.get(url, auth=auth)
    print(resp.status_code)
    print(resp.json())

def get_all_backends():
    url = load_balancer_link + f'/services/haproxy/configuration/backends'
    resp = requests.get(url,auth=auth)
    print(resp.status_code)
    print(resp.json())

def get_backend(backend_name):
    url = load_balancer_link + f'/services/haproxy/configuration/backends/{backend_name}'
    resp = requests.get(url,auth=auth)
    print(resp.status_code)
    print(resp.json())

def put_backend(backend_name):
    query_string = '?transaction_id='+transaction_id
    url = load_balancer_link + f'/services/haproxy/configuration/backends/{backend_name}' + query_string
    data = {
        "adv_check": "httpchk",
        "balance": {
            "algorithm": "roundrobin"
        },
        "httpchk_params": {
            "method": "GET",
            "uri": "/healthy",
            "version": "HTTP/1.1",
        },
        "mode": "http",
        "name": "all_backend",
    }
    resp = requests.put(url,auth=auth,json=data)
    print(resp.status_code)
    print(resp.json())

# get_all_transactions()
# get_transactions(transaction_id)
get_configuration()
# start_transaction()
# delete_transaction()
# get_transaction_list()
# get_all_backends()
# get_backend('all_backend')
# put_backend('all_backend')
# add_backend()
# delete_backend('server1')
# add_server('server5','10.1.0.21',3000)
# delete_server('server2','all_backend')
# add_frontend()
# add_bind('*',80)
# commit_transaction()