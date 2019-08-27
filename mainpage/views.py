from django.shortcuts import render
import requests
import json
from django.http import Http404
from pathlib import Path

# Create your views here.


def home(request):
    baseurl = "https://api.datamuse.com/words"
    if request.method == "GET":
        query = "funny"
        params_dict = {"rel_rhy": query}
        params_dict["max"] = 5
        resp = requests.get(baseurl, params=params_dict)
        words = resp.json()
        return render(request, "index.html", {'words': words})
    elif request.method == "POST":
        query = request.POST.get("query")
        params_dict = {"rel_rhy": query}
        params_dict["max"] = 5

        Path('rhyme_box_cache.txt').touch()

        with open('rhyme_box_cache.txt') as json_file:
            try:
                data = json.load(json_file)
            except:
                data = {}
            res = data.get(query)
            write = False
            if res is None:
                res = requests.get(baseurl, params=params_dict).json()
                data[query] = res
                write = True
        if write:
            with open('rhyme_box_cache.txt', 'w') as json_file:
                json_file.write(json.dumps(data))

        return render(
            request, "index.html", {'query': query, 'words': res, 'from_cache': not write}
        )
