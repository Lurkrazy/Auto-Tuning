import json


def testDict():
    x = '{"label":18,"words":["realclearpolitics","-","election","2016","-","2016","republican","presidential","nomination","polls","year","state"]}'
    j = json.loads(x)
    print(j)
    print(type(j))