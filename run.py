from app import app
from gevent import pywsgi
from kubernetes import client, config

config.load_kube_config()
api_client = client.ApiClient()
namespace = "staging"
secret_name = "tls_cred"
v1 = client.CoreV1Api(api_client)
secret = v1.read_namespaced_secret(name=secret_name, namespace=namespace)
data = secret.data

tls_crt = data["tls.crt"]
tls_key = data["tls.key"]

if __name__ == '__main__':
    http_server = pywsgi.WSGIServer(('0.0.0.0', 443), app, keyfile=tls_key, certfile=tls_crt)
    http_server.serve_forever()
