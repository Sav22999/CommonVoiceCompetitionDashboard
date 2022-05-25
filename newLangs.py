import datetime
import json

import LangListSpeech
import requests

HTML1 = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
<p>
"""

HTML2 = """
</p>
</body>
</html>
"""

if __name__ == "__main__":
    reqData1 = requests.get("https://www.saveriomorelli.com/api/common-voice-android/v2/languages").content

    fromServer = json.loads(reqData1)
    allLanguages = []
    for lang in fromServer["languages"]:
        l = {}
        l[fromServer["languages"][lang]["english"]] = lang
        allLanguages.append(l)

    # print(allLanguages)

    tf = open("LangListSpeech.py", "w")
    json.dump(allLanguages, tf)
    tf.close()

    f = open("LangListSpeech.py", 'r+')
    lines = f.readlines()  # read old content
    f.seek(0)  # go back to the beginning of the file
    f.write("langs = ")  # write new content at the beginning
    for line in lines:  # write old content after new
        f.write(line)
    f.close()

    reqData2 = requests.get("https://commonvoice.mozilla.org/api/v1/languages_all").content

    fromServer = json.loads(reqData2)
    # print(j)
    allLanguagesFromMozilla = list()
    for lang in fromServer:
        if(lang["is_contributable"]==1):
            allLanguagesFromMozilla.append(lang["name"])
    allLanguagesFromMozilla.sort()

    # print(allLanguagesFromMozilla)

    tempSavedLanguages = list()
    for temp in allLanguages:
        tempSavedLanguages.append(temp[list(temp.keys())[0]])
    tempSavedLanguages.sort()

    # print(tempSavedLanguages)

    newLanguages = list()
    wrongLanguages = list()

    for k in allLanguagesFromMozilla:
        # print(k.values())
        # print(k.keys())
        # a = k.values()
        if k not in tempSavedLanguages:
            newLanguages.append(k)

    for w in tempSavedLanguages:
        if w not in allLanguagesFromMozilla:
            wrongLanguages.append(w)

    # print(newLanguages)

    with open("website/index.html", "w") as f:
        f.write(HTML1)

        if len(newLanguages) > 0:
            f.write("<p>New languages to add</p>")
            f.write(str(newLanguages))
            f.write("<p></p>")
            '''for i in newLanguages:
                c = fromServer["launched"]'''

            # for e in c:
            #     if e[""]
            #     print(e)
            # for j in c:
            # print(j)
            # c = reqData
            # print(c)
        else:
            # print("probably no new languages added")
            f.write("<p>No new languages to add</p>")

        if len(wrongLanguages) > 0:
            f.write("<hr><p>There could be wrong languages</p>")
            f.write(str(wrongLanguages))
            f.write("<p></p>")
            f.write(str(allLanguagesFromMozilla))

        now = datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        date_time = now.strftime("%d.%m.%y %H:%M")

        f.write(f"\n\n<p>Last updated: {date_time}</p>")
        f.write(HTML2)

    # langCode = list(langArray.values())[0]
    # langName = list(langArray.keys())[0]
