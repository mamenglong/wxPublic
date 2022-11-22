import os
import sys
import yaml
import argparse
import subprocess
import signal

parser = argparse.ArgumentParser()
parser.add_argument('--cfg', type=str, default='../config_test.yaml')
args = parser.parse_args()

def send_dd_now(env):
    print("running...")
    subprocess.run([f"{sys.executable}", "ddApi.py"], env=env)
    return


def signal_handler(signum, frame):
    print("\n程序结束！")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
    with open(args.cfg, "r", encoding="utf-8") as fd:
        config = yaml.safe_load(fd)
    config['USER_ID'] = '\n'.join(config['USER_ID'])

    if type(config['BIRTHDAY']) is list:
        config['BIRTHDAY'] = '\n'.join(config['BIRTHDAY'])
    else:
        config['BIRTHDAY'] = config['BIRTHDAY']
    config['DD_ACCESS_TOKEN'] = '\n'.join(config['DD_ACCESS_TOKEN'])
    config['DD_SIGN_SECRET'] = '\n'.join(config['DD_SIGN_SECRET'])
    env = {**os.environ, **config}
    print("开始运行，等待定时触发...")
    send_dd_now(env)

