from database.models import Task
from database.repo import session


def create_task(id,name,status):
    try:
        task=Task(task_id=id,task_name=name,task_status=status)
    except Exception as e:
        return f"Some thing wring witht he attributes {e}"
    try:
        session.add(task)
        session.commit()
        return "Successfully inserted into the Tak table"
    except Exception as e:
        session.rollback()
        return f"Failed to Insert into Tasks {e}"
        
def get_tasks():
    
    try:
        result=session.query(Task).all()
        
        
    except Exception as  e:
        return f"Some thing wrong wth query {e}"

    return result

def get_task_id(id):

    try:
        result=session.query(Task).filter_by(task_id=id).all()
        return result
    except Exception as e:
        return f"There is an issute with the query statement{e}"


def get_task_status(status):
    
    try:
        result=session.query(Task).filter_by(task_status=status).all()
        return result
    except Exception as e:
        return f"The returned has error {e}"