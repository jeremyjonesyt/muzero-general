def scale_model_width(multiplier):
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    config['hidden_channels'] = int(config['hidden_channels'] * multiplier)
    with open('config.yaml', 'w') as f:
        yaml.dump(config, f)
