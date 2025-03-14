
from py2neo import Graph, Node, Relationship, NodeMatcher
from sqlalchemy import false, null


g = Graph("neo4j+s://533a5787.databases.neo4j.io", auth=("neo4j", "yFDQiYSLutuTv0-0KXQkdKDT6f3RJITRpT2lUn9B2pI"))
matcher = NodeMatcher(g)

# Start the transaction
tx = g.begin()
try:
    #Create the user node (does not check of node already exists!!)
    a = matcher.match("Person", device_id="0000000000001").first()
    if (a== None):

        a = Node("Person", device_id="0000000000001", user_name = "Andreas Kretz")
        tx.create(a)

        # check if node has been created if not raise exception to rollback transaction
        if(tx.exists(a) == False):
            raise (Exception) 

    # create the relationship (user)-[VISITED]-(Business)
    b = matcher.match("Business", business_id="0322120-04-001").first()

    propierties = {"scan_timestamp":"2022-01-01 12:55:55"}
    r = Relationship(a, "VISITED", b, **propierties)
    r.identity = None
    tx.create(r)
    
    # check if relationship has been created if not raise exception to rollback transaction
    if(tx.exists(r) == False):
        raise (Exception)

    # commit the transaction if everything was successful
    g.commit(tx)

except Exception as e:
    g.rollback(tx) # rollback the transaction on error
    print(e)




"""
Use queries in neo4j browser

MATCH (p:Person)
WHERE p.user_name = 'Andreas Kretz'
RETURN p
   
MATCH (b:Business)
WHERE b.business_id = '0322120-04-001'
RETURN b   

"""