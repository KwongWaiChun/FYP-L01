from sshtunnel import SSHTunnelForwarder
import os
from kubernetes import client, config

basedir = os.path.abspath(os.path.dirname(__file__))

def create_ssh_tunnel():
    # Load the Kubernetes configuration
    config.load_kube_config()

    # Create a Kubernetes client
    api_client = client.ApiClient()

    # Specify the namespace and secret name
    namespace = "staging"
    secret_name = "ssh-tunnel"

    # Retrieve the secret
    v1 = client.CoreV1Api(api_client)
    secret = v1.read_namespaced_secret(name=secret_name, namespace=namespace)

    # Access the data from the secret
    data = secret.data

    # Extract the values from the secret data
    ssh_host = data["ssh_host"]
    ssh_username = data["ssh_username"]
    ssh_private_key = data["ssh_private_key"]
    rds_host = data["rds_host"]
    rds_username = data["rds_username"]
    rds_password = data["rds_password"]
    rds_database = data["rds_database"]

    server = SSHTunnelForwarder(
        (ssh_host, ssh_port),
        ssh_username=ssh_username,
        ssh_pkey=ssh_private_key,
        remote_bind_address=(rds_host, rds_port),
    )
    server.start()
    connection_url = f"mysql+pymysql://{rds_username}:{rds_password}@127.0.0.1:{server.local_bind_port}/{rds_database}"
    return connection_url

class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI") or create_ssh_tunnel() or \
        'sqlite:///'+os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
