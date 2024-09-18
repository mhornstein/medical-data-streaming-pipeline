import yaml

def load_config(config_file='config.yaml'):
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
        config['bootstrap_servers'] = f"{config['server_url']}:9092"
        config['schema_registry_url'] = f"http://{config['server_url']}:8081"
    return config

config = load_config()