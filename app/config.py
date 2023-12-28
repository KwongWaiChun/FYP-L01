from sshtunnel import SSHTunnelForwarder
import os

basedir = os.path.abspath(os.path.dirname(__file__))

def create_ssh_tunnel():
    ssh_host = 'ec2-23-20-58-240.compute-1.amazonaws.com'
    ssh_port = 22
    ssh_username = 'ec2-user'
    ssh_private_key = 'app/key/labsuser.pem'

    rds_host = 'fyp-auroracluster-3sojpv1iwlyb.cluster-c7aws6ioupad.us-east-1.rds.amazonaws.com'
    rds_port = 3306
    rds_username = 'admin'
    rds_password = 'admin123'
    rds_database = 'MyDatabase'

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
