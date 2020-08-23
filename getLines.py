import base64

VALID_LEVEL = ["max", "min", "mix"]
VALID_TARGET = ["female", "male", "mix"]


def decode(b):
    return base64.b64decode(b.encode('ascii')).decode('UTF-8')


def getLines(config):

    linesFemale = []
    linesMale = []

    if config['level'] == "max" or config['level'] == "mix":
        with open("resources-max.txt", "r", encoding="utf-8") as resources:
            raw = resources.readlines()
            linesFemale += map(decode, raw)

    if config['level'] == "min" or config['level'] == "mix":
        with open("resources-min.txt", "r", encoding="utf-8") as resources:
            raw = resources.readlines()
            linesFemale += map(decode, raw)

    if config['target'] == "female":
        return linesFemale
    else:
        linesMale = [replaceF2M(s) for s in linesFemale]

        if config['target'] == "male":
            return linesMale
        else:
            return linesFemale + linesMale


replaceTable = [
    ['5aaI', '54i4'],
    ['8J+QtA==', '8J+RtA=='],
    ['8J+Qjg==', '8J+RtA=='],
    ['5q+N5Lqy', '54i25Lqy'],
    ['5q+N', '5YWs'],
    ['5L2g5ZCX', '5L2g54i5'],
    ['6YC8', '5bGM'],
    ['6Zi06YGT', '6IKb6Zeo'],
    ['5aSE5aWz', '5aSE55S3'],
    ['5aiY', '54i5'],
    ['5aW5', '5LuW']
]

for p in replaceTable:
    p[0] = decode(p[0])
    p[1] = decode(p[1])


def replaceF2M(s):
    r = s
    for replace in replaceTable:
        r = r.replace(*replace)
    return r
