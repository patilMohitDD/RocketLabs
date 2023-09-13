from database import Node, Rocket, get_db, sessionLocal
from fastapi import Depends

def seed_database():
    db = sessionLocal()
    # Create a ROCKET
    rocket = Rocket(name = "Adtiya L -4")
    db.add(rocket)
    db.commit()
    db.refresh(rocket)

    # Creating Height
    height = Node(name = "Height", rocket_id = rocket.id, parent_id = None, value = 18.000)
    db.add(height)
    db.commit()

    # Creating Height
    mass = Node(name = "Mass", rocket_id = rocket.id, parent_id = None, value = 12000.00)
    db.add(mass)
    db.commit()


    # Creating Stage1 {}
    stage1 = Node(name = "Stage1", rocket_id = rocket.id, parent_id = None, value = None)
    db.add(stage1)
    db.commit()
    db.refresh(stage1)

    # Creating Stage1 -> Engine1
    Engine1 = Node(name = "Engine1", rocket_id = rocket.id, parent_id = stage1.id, value = None)
    db.add(Engine1)
    db.commit()
    db.refresh(Engine1)

    # Creating Stage1 -> Engine2
    Engine2 = Node(name = "Engine2", rocket_id = rocket.id, parent_id = stage1.id, value = None)
    db.add(Engine2)
    db.commit()
    db.refresh(Engine2)

    
    # Creating Stage1 -> Engine3
    Engine3 = Node(name = "Engine3", rocket_id = rocket.id, parent_id = stage1.id, value = None)
    db.add(Engine3)
    db.commit()
    db.refresh(Engine3)

    # Creating Stage1 -> Engine1 -> Thrust
    Thrust = Node(name = "Thrust", rocket_id = rocket.id, parent_id = Engine1.id, value = 9.493)
    db.add(Thrust)
    db.commit()

    # Creating Stage1 -> Engine1 -> ISP
    ISP = Node(name = "ISP", rocket_id = rocket.id, parent_id = Engine1.id, value = 9.493)
    db.add(ISP)
    db.commit()

    # Creating Stage1 -> Engine2 -> Thrust
    Thrust = Node(name = "Thrust", rocket_id = rocket.id, parent_id = Engine2.id, value = 9.413)
    db.add(Thrust)
    db.commit()

    # Creating Stage1 -> Engine2 -> ISP
    ISP = Node(name = "ISP", rocket_id = rocket.id, parent_id = Engine2.id, value = 11.632)
    db.add(ISP)
    db.commit()

    # Creating Stage1 -> Engine3 -> Thrust
    Thrust = Node(name = "Thrust", rocket_id = rocket.id, parent_id = Engine3.id, value = 9.899)
    db.add(Thrust)
    db.commit()

    # Creating Stage1 -> Engine3 -> ISP
    ISP = Node(name = "ISP", rocket_id = rocket.id, parent_id = Engine3.id, value = 12.551)
    db.add(ISP)
    db.commit()


    # Creating Stage2 {}
    stage2 = Node(name = "Stage2", rocket_id = rocket.id, parent_id = None, value = None)
    db.add(stage2)
    db.commit()
    db.refresh(stage2)

    # Creating Stage2 -> Engine1
    Engine1 = Node(name = "Engine1", rocket_id = rocket.id, parent_id = stage2.id, value = None)
    db.add(Engine1)
    db.commit()
    db.refresh(Engine1)
    

    # Creating Stage2 -> Engine1 -> Thrust
    Thrust = Node(name = "Thrust", rocket_id = rocket.id, parent_id = Engine1.id, value = 1.622)
    db.add(Thrust)
    db.commit()

    # Creating Stage2s -> Engine2 -> ISP
    ISP = Node(name = "ISP", rocket_id = rocket.id, parent_id = Engine1.id, value = 15.110)
    db.add(ISP)
    db.commit()


    # db.refresh()
    db.close()
    

if __name__ == "__main__":
    seed_database()