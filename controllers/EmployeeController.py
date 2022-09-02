from flask import jsonify,request
from models.Employees import getEmployeesList,createEmployee,getSingleEmployee,deleteEmployee,updateEmployee
import pymongo,mongoengine
from email_validator import validate_email, EmailNotValidError

def index():
    try:
        employeeList = getEmployeesList()
    except pymongo.errors.DuplicateKeyError:
        pass
    finally:
        return employeeList

def validateEmail(function):            
    def wrapper():
        requestData = request.json    
        try:
            validation = validate_email(requestData['email'], check_deliverability=True)            
            email = validation.email        
        except EmailNotValidError as e:
            resp = jsonify('Employee email invalid')
            resp.status = 200   
            return resp                      
        else:        
            return function()
    return wrapper
    
@validateEmail
def addOrUpdate():
    requestData = request.json
    if 'employee_id' in requestData:
        # Update
        try:
            status = updateEmployee(requestData)
        except:
            resp = jsonify('Something went wrong')
            resp.status = 200   
        else:
            resp = jsonify('Employee update Success')
            resp.status = 200  
        return resp          
    else:
        # Insert
        try:            
            status = createEmployee(requestData)
        except pymongo.errors.DuplicateKeyError:
            resp = jsonify('Employee Insert failed')
            resp.status = 200             
        except KeyError:
            resp = jsonify('Something went wrong')
            resp.status = 200          
        except mongoengine.errors.NotUniqueError:
            resp = jsonify('This user already exists')
            resp.status = 200              
        else:        
            resp = jsonify('Employee insert Success')
            resp.status = 200             
        return resp
    
def delete():
    requestData = request.json
    try:
        employee = deleteEmployee(requestData)
        resp = jsonify('Employee delete Success')
        resp.status = 200         
    except:
        resp = jsonify('Employee delete Failed')
        resp.status = 200         
    return resp

def view():
    requestData = request.json
    try:
        employee = getSingleEmployee(requestData)
    except:
        resp = jsonify('Something went wrong')
        resp.status = 200  
        return resp       
    else:
        return employee