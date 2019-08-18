#!/usr//bin/python3

# ==================================================================
#
# @Author Avik Paul
# Created to solve below problem.
#
# Problem Statement: Find the most popular and the 2nd most popular jar file (artifact) in a
# maven repository. The most popular artifact will be the one with highest number of downloads.
# In addition, to build and deploy this solution, create a robust CI/CD pipeline via Jenkins or other
# CI tool.
# ==================================================================

import json
import sys
from artifactory import ArtifactoryPath


jfrogURL = sys.argv[1]
apiKey = sys.argv[2]
repoName = str(sys.argv[3])
artType = str(sys.argv[4])
limits = str(sys.argv[5])

print ("jfrogURL --> "+jfrogURL+"::: apiKey--> "+apiKey+"::repoName-->"+repoName+"::artType-->"+artType+":::limits-->"+limits)

def create_aql_text(*args):
    """
    Create AQL query from string or list or dict arguments
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
aql = ArtifactoryPath(
    "http://"+jfrogURL+"/artifactory/api/search/aql", apikey=apiKey)

#Forming Arguments for search.
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

args2 = [".limit("+limits+")"]

finalargs = args + args1 + args2

#This is just to check whether Query is forming correctly or not.
aql_query_text = create_aql_text(*finalargs)

print ("Generated AQL query --> "+aql_query_text)

# artifacts_list contains raw data (list of dict)
# Send query:
# items.find({"$and": [{"repo": {"$eq": "repo"}}, {"$or": [{"path": {"$match": "*path1"}}, {"path": {"$match": "*path2"}}]}]})
artifacts_list = aql.aql(*finalargs)


result = json.dumps(artifacts_list)



print ("Most Popupar Download Based on Search Criteria--->"+result)
