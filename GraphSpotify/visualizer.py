import json

def visualize(data):
    # Uncomment below to make the JSON output human-readable
    #data["js"] = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
    js = json.dumps(data, separators=(',', ':'))
    js = "<script type=\"text/javascript\">data = " + js + "</script>"

    html = "&nbsp;"

    return js, html
