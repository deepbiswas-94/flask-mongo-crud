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
    employees = Employees.objects()
    return jsonify(employees), 200    

def hashPassword(function):
    def wrapper(*args, **kwargs):
        password = args[0]['password']
        args[0]['password'] = bcryptObj.generate_password_hash(password)
        return function(*args, **kwargs)
    return wrapper

@hashPassword
def createEmployee(data):
    newEmployeeId = getEmployeeCount() + 1
    newEmployee = Employees(name=data['name'],email=data['email'],password=data['password'],employee_id=newEmployeeId)
    status = newEmployee.save(validate=True)
    return jsonify(status), 200

def getSingleEmployee(data):
    employees = Employees.objects.get_or_404(employee_id=data['employee_id'])
    return jsonify(employees), 200    

def getEmployeeCount():
    count = Employees.objects().count()
    return count

def deleteEmployee(data):
    employee = Employees.objects.get_or_404(employee_id=data['employee_id'])
    employee.delete()
    return jsonify(str(employee.id)), 200

def updateEmployee(data):
    employees = Employees.objects.get_or_404(employee_id=data['employee_id'])
    employees.update(**data)
    return jsonify(str(employees.id)), 200