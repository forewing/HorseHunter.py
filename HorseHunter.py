import argparse
import os
import random
import signal
import sys
import time
import atexit

import pyperclip

from getLines import getLines

global targetDict
global levelDict


targetDict = {
    "female": "令堂",
    "male": "令尊",
    "mix": "混合",
}

levelDict = {
    "max": "火力全开",
    "min": "口吐芬芳",
    "mix": "混合",
}


def parseArgs():
    def helpDict(d):
        return ", ".join([
            k+"="+d[k] for k in d
        ])
    parser = argparse.ArgumentParser(description='自动向剪贴板刷新金句，让你不再饱受欺凌')

    parser.add_argument('--target', '-t', dest='target',  choices=["female", "male", "mix"], default="female",
                        help='设置辱骂对象, '+helpDict(targetDict)+'. 默认 female')
    parser.add_argument('--level', '-l', dest='level',  choices=["max", "min", "mix"], default="max",
                        help='设置辱骂等级, '+helpDict(levelDict)+'. 默认 max')
    parser.add_argument('--interval', '-i', dest='interval', type=float, default=0.1,
                        help='设置刷新间隔(s). 默认 0.1')

    args = parser.parse_args()

    if args.interval < 0:
        raise argparse.ArgumentTypeError("assert: INTERVAL >= 0")

    config = {}
    config["target"] = args.target
    config["level"] = args.level
    config["interval"] = args.interval

    return config


def clearClip():
    pyperclip.copy("")


if __name__ == "__main__":
    atexit.register(clearClip)

    path = getattr(sys, '_MEIPASS', os.getcwd())
    os.chdir(path)

    print("本软件仅限用于自卫反击，向网络暴力说不！！")

    config = parseArgs()

    lines = getLines(config)

    print("辱骂对象：" + targetDict[config["target"]])
    print("辱骂等级：" + levelDict[config["level"]])
    print(f"候选金句：{len(lines)}")
    print(f"刷新间隔：{config['interval']}s")

    startTime = time.time()
    outputLinesCount = 0

    def signal_handler(signal, frame):
        endTime = time.time()
        print(f"本次使用时间：{round(endTime-startTime, 1)}s")
        print(f"共问候对面：{outputLinesCount} 次")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    print("持续输出中...")
    while True:
        outputLinesCount += 1
        pyperclip.copy(random.choice(lines))
        time.sleep(config["interval"])
