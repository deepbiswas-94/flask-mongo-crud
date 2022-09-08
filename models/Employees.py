from flask_mongoengine import MongoEngine
from flask import jsonify,Flask
import datetime
from flask_bcrypt import Bcrypt

db = MongoEngine()
appBcrypt = Flask(__name__)
bcryptObj = Bcrypt(appBcrypt)

class Employees(db.Document):
    employee_id = db.IntField()
    name = db.StringField(required=True)
    email = db.StringField(required=True,unique=True)
    password = db.StringField(required=True)
    date_modified = db.DateTimeField(default=datetime.datetime.utcnow)
    
def getEmployeesList():
    """ Getting a list of employees
        >>> Employees.objects()
        :Returns:
            - Return list of employees
    """     
    employees = Employees.objects()
    return employees    

def hashPassword(function):
    """ Generate Hash for a password
        Modifies the normal password to hashed password
    """         
    def wrapper(*args, **kwargs):
        password = args[0]['password']
        args[0]['password'] = bcryptObj.generate_password_hash(password)
        return function(*args, **kwargs)
    return wrapper

@hashPassword
def createEmployee(data):
    """ Insert a Employee document 
        :Parameters:
            - `data`:Dictionary containing insert data
        :Returns:
            - Returns result of insert operation
    """    
    newEmployeeId = getEmployeeCount() + 1
    newEmployee = Employees(name=data['name'],email=data['email'],password=data['password'],employee_id=newEmployeeId)
    status = newEmployee.save(validate=True)
    return status

def getSingleEmployee(data):
    """ Get details of a single employee
        :Parameters:
            - `data`:Dictionary containing employee_id
        :Returns:
            - Returns detail of the employee
    """        
    employees = Employees.objects.get_or_404(employee_id=data['employee_id'])
    return employees 

def getEmployeeCount():
    """ Getting number of employees
        :Returns:
            - Returns Number of employees
    """        
    count = Employees.objects().count()
    return count

def attemptDeleteEmployee(data):
    """ Delete a Employee document 
        :Parameters:
            - `data`:Dictionary containing employee_id
        :Returns:
            - Return ID if the delete was successful
    """            
    employee = Employees.objects.get_or_404(employee_id=data['employee_id'])
    employee.delete()
    return str(employee.id)

def updateEmployee(data):
    """ Update Single a Employee document 
        :Parameters:
            - `data`:Dictionary containing update data
        :Returns:
            - Return employee ID if successful
    """    
    employees = Employees.objects.get_or_404(employee_id=data['employee_id'])
    employees.update(**data)
    return str(employees.id)
