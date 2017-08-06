import argparse
from battleground import site_runner

def go():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--config',type=str,default="config/basic_config.json")
    args = parser.parse_args()
    site_runner.start_session(args.config)

if __name__ == "__main__":
    go()
