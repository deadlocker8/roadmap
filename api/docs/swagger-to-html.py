#!/usr/bin/python

import yaml
import json
import sys
import re

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>%s</title>
  <link href="https://fonts.googleapis.com/css?family=Open+Sans:400,700|Source+Code+Pro:300,600|Titillium+Web:400,600,700" rel="stylesheet">
  <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.22.2/swagger-ui.css" >
  <style>
    html
    {
      box-sizing: border-box;
      overflow: -moz-scrollbars-vertical;
      overflow-y: scroll;
    }
    *,
    *:before,
    *:after
    {
      box-sizing: inherit;
    }

    body {
      margin:0;
      background: #fafafa;
    }
  </style>
</head>
<body>

<div id="swagger-ui"></div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.22.2/swagger-ui-bundle.js"> </script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.22.2/swagger-ui-standalone-preset.js"> </script>
<script>
window.onload = function() {

  var spec = %s;

  // Build a system
  const ui = SwaggerUIBundle({
    spec: spec,
    dom_id: '#swagger-ui',
    deepLinking: true,
    presets: [
      SwaggerUIBundle.presets.apis
    ]
  })

  window.ui = ui
}
</script>
</body>

</html>
"""

VERSION_PATTERN = r'"version": "\d+.\d+.\d+"'

if len(sys.argv) != 3:
    print('Invalid number of args')
    print('Usage: swagger-to-html.py source.yml destination.html')
    exit()

with open(sys.argv[1], "r") as inputFile:
    spec = yaml.load(inputFile, Loader=yaml.FullLoader)
    spec = json.dumps(spec)

    with open('../version.json', 'r') as f:
        VERSION = json.load(f)
    VERSION = VERSION['version']

    versionNameShort = VERSION['name'].replace('v', '')
    print('Setting version number to "{}"'.format(versionNameShort))
    spec = re.sub(VERSION_PATTERN, '"version": "{}"'.format(versionNameShort), spec, flags=re.S)

    spec = TEMPLATE % ("Roadmaps API", spec)
    with open(sys.argv[2], "w") as f:
        f.write(spec)
        print("DONE")
