import yaml

def load_config():
    with open("config.yml", "r") as config_file:
        try:
            return yaml.safe_load(config_file)
        except yaml.YAMLError as exc:
            print(exc)

def flatten_forwards(forwards):
    result = {}
    for path, target in forwards.items():
        
        if isinstance(target, dict):
            for subpath, subtarget in flatten_forwards(target).items():
                result["/".join([path, subpath])] = subtarget
        else:
            result[path] = target

    return result

def generate_forward(path, target):
    return f"""
        location = /{path} {{
            return 301 {target};
        }}
    """

def generate_nginx_config(config):
    return f"""
events {{
    worker_connections  {config.get("connections", 1024)}; 
}}

http {{
    include mime.types;
    default_type application/octet-stream;
    sendfile on;

    server {{
        listen 80;
        listen [::]:80;

        server_name {config.get("server_name")};

        location /
        {{
            root /etc/nginx/html;
            index index.html;
        }}

        {"\n".join(generate_forward(path, target) for path, target in flatten_forwards(config.get("forwards", [])).items())}
    }}
}}
        """

print(generate_nginx_config(load_config()))
