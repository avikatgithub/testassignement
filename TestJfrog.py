#!/usr//bin/python3

import json
import os
import ssl
import operator
import requests
import sys
from artifactory import ArtifactoryPath


try:
    import requests.packages.urllib3 as urllib3
except ImportError:
    import urllib3

jfrogURL = sys.argv[1]
apiKey = sys.argv[2]
repoName = str(sys.argv[3])
artType = str(sys.argv[4])
limits = sys.argv[5]

print ("jfrogURL --> "+jfrogURL+"::: apiKey--> "+apiKey+"::repoName-->"+repoName+"::artType-->"+artType+":::limits-->"+limits)

def create_aql_text(*args):
    """
    Create AQL querty from string or list or dict arguments
    """
    aql_query_text = ""
    for arg in args:
        if isinstance(arg, dict):
            arg = "({})".format(json.dumps(arg))
        elif isinstance(arg, list):
            arg = "({})".format(json.dumps(arg)).replace("[", "").replace("]", "")
        aql_query_text += arg
    return aql_query_text

# API_KEY
#aql = ArtifactoryPath("https://"+jfrogURL+"/artifactory/api/search/aql", apikey=apiKey)
aql = ArtifactoryPath(
    "http://"+jfrogURL+"/artifactory/api/search/aql", apikey=apiKey)


args = ["items.find",
            {"$and":
                [
                    {
                        "repo":{"$eq": repoName},
                        "name": {"$match" : "*."+artType},
                        "stat.downloads":{"$gt": "0"}
                    }
                ]
            }
        ]

args1 = [".sort",
            {"$desc":
                [
                    "name"
                ]
            }
        ]

args2 = [".limit(2)"]

finalargs = args + args1 + args2

aql_query_text = create_aql_text(*finalargs)

print (aql_query_text)

# artifacts_list contains raw data (list of dict)
# Send query:
# items.find({"$and": [{"repo": {"$eq": "repo"}}, {"$or": [{"path": {"$match": "*path1"}}, {"path": {"$match": "*path2"}}]}]})
artifacts_list = aql.aql(*finalargs)


result = json.dumps(artifacts_list)



print ("Response Total data --->"+result)


