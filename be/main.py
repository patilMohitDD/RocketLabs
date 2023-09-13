from fastapi import FastAPI, Depends, HTTPException, Request
from database import Node, Rocket, get_db, sessionLocal
from fastapi.responses import JSONResponse
import json
from seed_database import seed_database

app = FastAPI()

@app.on_event("startup")
def on_startup():
    db = sessionLocal()
    result = db.query(Node).all()
    if not result:
        seed_database()

    
@app.get("/rocket/{rocket_id}")
async def root(rocket_id: int, db = Depends(get_db)):
    rocket = db.query(Rocket).filter(Rocket.id == rocket_id).first()
    if rocket is None:
        raise HTTPException(status_code=404, detail="Rocket not found")
    nodes = db.query(Node).filter(Node.rocket_id == rocket_id).all()
    response = {}
    
    for node in nodes:
        if not node.parent_id:
            response = get_dict(db, node, response)
    return response


@app.get("/rocket/{rocket_id}/{children:path}")
async def root(rocket_id: int, request: Request, children: str, db = Depends(get_db)):
    rocket = db.query(Rocket).filter(Rocket.id == rocket_id).first()
    if rocket is None:
        raise HTTPException(status_code=404, detail="Rocket not found")

    pathComponent = children.split("/")
    
    parent = None
    for element in pathComponent:
        nodes = db.query(Node).filter(Node.rocket_id == rocket_id, Node.name == element, Node.parent_id == parent).all()
        if not nodes:
            raise HTTPException(status_code=404, detail="Something wrong with URL elements")

        if not nodes[0].id:
            raise HTTPException(status_code=404, detail="Something wrong with " + element)
        parent = nodes[0].id

    response = {}
    for node in nodes:
        response = get_dict(db, node, response)

    return response

@app.post("/rocket/{rocket_id}/{children:path}")
async def root(rocket_id: int, request: Request, children: str, db = Depends(get_db)):
    rocket = db.query(Rocket).filter(Rocket.id == rocket_id).first()
    if not rocket:
        raise HTTPException(status_code=404, detail="Rocket not found")
        
    pathComponent = children.split("/")
    bodyDetails = await request.json()
    
    parent = None
    for element in pathComponent[:-1]:
        nodes = db.query(Node).filter(Node.rocket_id == rocket_id, Node.name == element, Node.parent_id == parent).all()

        if not nodes[0].id: raise HTTPException(status_code=404, detail="Something wrong with " + element)
        
        parent = nodes[0].id
    
    checkNode =  db.query(Node).filter(Node.rocket_id == rocket_id, Node.name == pathComponent[-1], Node.parent_id == nodes[0].id).all()
    if not checkNode:
        print("here")
        newNode = Node(name = pathComponent[-1], parent_id = nodes[0].id, rocket_id = rocket_id,value = None)
        db.add(newNode)
        db.commit()
        db.refresh(newNode)

        contenDetail = pathComponent[-1].upper() + " added in the Database"
        return JSONResponse(
            status_code=200, content = {"detail": contenDetail}
        )
    
    if (bodyDetails == {}):
         raise HTTPException(status_code=404, detail= pathComponent[-1].upper() + " Already Present in the Database ")


    parentId = checkNode[0].id
    put_dict(db, rocket_id, parentId, bodyDetails)
    # print(bodyDetails)
    return JSONResponse(
            status_code=200, content = {"details added": "SUCCESS"}
        )

    
def put_dict(db, rocketID, parentID, dictionary):
    for key, value in dictionary.items():
        if type(value) is not dict:
            newNode = Node(name = key, parent_id = parentID, rocket_id = rocketID, value = value)
            db.add(newNode)
            db.commit()
            db.refresh(newNode)
        else:
            newNode = Node(name = key, parent_id = parentID, rocket_id = rocketID, value = None)
            db.add(newNode)
            db.commit()
            db.refresh(newNode)

            newParentID = newNode.id
            put_dict(db, rocketID, newParentID, value)
            
    return

     
def get_dict(db, node, response):
    if node.value:
        response[node.name] = node.value
        return response
    else:
        response[node.name] = {}
        for child in node.children:
            response[node.name] = get_dict(db, child, response[node.name])

        return response