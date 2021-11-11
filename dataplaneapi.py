from json import load
import requests
from requests.models import HTTPBasicAuth

load_balancer_link = 'http://36.255.69.28:5555/v2'
auth = HTTPBasicAuth('admin','adminpwd')
transaction_id = '670d07af-baa9-4040-bf9c-d29a7f12c593'
def get_configuration():
    config_link = '/services/haproxy/configuration/raw'
    url = load_balancer_link + config_link
    resp = requests.get(url,auth=auth)
    data = resp.json().get('data')
    print(data)

def get_transaction_list():
    config_link = '/services/haproxy/transactions'
    url = load_balancer_link + config_link
    resp = requests.get(url,auth=auth)
    data = resp.json()
    print(data)

def start_transaction():
    config_link = '/services/haproxy/transactions?version=1'
    url = load_balancer_link + config_link
    resp = requests.post(url,auth=auth)
    print(resp.status_code)
    print(resp.json())

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

get_configuration()
# start_transaction()
# get_transaction_list()
# add_backend()
# delete_backend('server1')
# add_server('server1','10.1.0.14',8000)
# add_frontend()
# add_bind('*',80)
# commit_transaction()