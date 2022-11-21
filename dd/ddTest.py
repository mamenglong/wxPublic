import os
import sys
import yaml
import argparse
import subprocess
import signal

parser = argparse.ArgumentParser()
parser.add_argument('--cfg', type=str, default='../config_test.yaml')
args = parser.parse_args()


def send(env):
    print("running send ...")
    subprocess.run([f"{sys.executable}", "ddApi.py"], env=env)


def signal_handler(signum, frame):
    print("\n程序结束！")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
    with open(args.cfg, "r", encoding="utf-8") as fd:
        config = yaml.safe_load(fd)
    env = {**os.environ, **config}
    print("开始运行...")
    send(env)
