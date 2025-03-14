from py2neo import Graph

import pprint

# create connection
g = Graph("neo4j+s://533a5787.databases.neo4j.io", auth=("neo4j", "yFDQiYSLutuTv0-0KXQkdKDT6f3RJITRpT2lUn9B2pI"))

# [Example 1]

# Find where Gilbert went and which zip code the business is in
# Using :ISLOCATED only shows the zip (directional + relation specified)
result = g.run("MATCH (p:Person)-[VISITED]-(Business)-[:ISLOCATED]-(Zip)\
                WHERE p.user_name = 'Gilbert Harris'\
                RETURN p,Business,Zip").data()
#pprint.pprint(result)
pprint.pprint(len(result))

### Same thing just with an arrow instead of naming the relationship
result = g.run("MATCH (p:Person)-->(Business)-->(Zip)\
                WHERE p.user_name = 'Gilbert Harris'\
                RETURN p,Business,Zip").data()
#pprint.pprint(result)
pprint.pprint(len(result))

### Matches more, because the zip doesnt have a direction
# Go to AuraDB query UI
result = g.run("MATCH (p:Person)--(Business)--(Zip)\
                WHERE p.user_name = 'Gilbert Harris'\
                RETURN p,Business,Zip").data()
#pprint.pprint(result)
pprint.pprint(len(result))



# [Example 2]
### Find everyone who went to a Bank using a regex
### Play around with the relation and see different results try (-- or <-- or --> ) and expore the results
result = g.run("MATCH (Business)-[vis:VISITED]-(Person)\
                WHERE Business.business_name =~ '.*Bank.*'\
                RETURN Business,Person").data()
#pprint.pprint(result)
pprint.pprint(len(result))

### Find everyone who visited a bank on Jan 3rd
result = g.run("MATCH (p:Person)-[vis:VISITED]-(b:Business)\
                WHERE vis.scan_timestamp =~ '2022-01-03.*' \
                AND b.business_name =~ '.*Bank.*'\
                RETURN b, p").data()
#pprint.pprint(result)
pprint.pprint(len(result))
