#!/usr/bin/env python
from django.http import HttpResponse
import os
import json

def ProjectList(request):

    data = "{\n"
    first = True

    for root, dirs, files in os.walk("./projects/"):
        for file in files:
            if file.endswith(".cxml"):
                if first == False:
                    data += ",\n"
                else:
                    first = False
                data += "\t\"" + file + "\": \"" + os.path.join(root, file).replace("\\", "/") + "\""
    
    data += "\n}"
    return HttpResponse(data, content_type="application/json")