from flask import jsonify,request
from models.Employees import getEmployeesList,createEmployee,getSingleEmployee,attemptDeleteEmployee,updateEmployee
import pymongo,mongoengine
from email_validator import validate_email, EmailNotValidError

def employeeList():
    """ Getting a list Employees
        :Returns:
            - Returns result of list operation
        :Exceptions:
            - DuplicateKeyError : if any duplicates are found
    """        
    try:
        employeeList = getEmployeesList()
    except pymongo.errors.DuplicateKeyError:
        pass
    finally:
        return jsonify(employeeList),200

def validateEmail(function):            
    """ Validates an email
        :Returns:
            - Returns wrapped function if valid
        :Exceptions:
            - EmailNotValidError : if email found invalid
    """            
    def wrapper():
        requestData = request.json    
        try:
            validation = validate_email(requestData['email'], check_deliverability=True)            
            email = validation.email        
        except EmailNotValidError as e:
            resp = jsonify('Employee email invalid'), 200
            return resp                      
        else:        
            return function()
    return wrapper
    
@validateEmail
def addOrUpdate():
    """ Add or update employee document
        :Returns:
            - Returns response according to operation status
    """                
    requestData = request.json
    if 'employee_id' in requestData:
        # Update
        try:
            status = updateEmployee(requestData)
        except:
            resp = jsonify('Something went wrong'), 200
        else:
            resp = jsonify('Employee update Success'), 200
        return resp          
    else:
        # Insert
        try:            
            status = createEmployee(requestData)
        except pymongo.errors.DuplicateKeyError:
            resp = jsonify('Employee Insert failed'), 200
        except KeyError:
            resp = jsonify('Something went wrong'), 200
        except mongoengine.errors.NotUniqueError:
            resp = jsonify('This user already exists'), 200
        else:        
            resp = jsonify('Employee insert Success'), 200
        return resp
    
def deleteEmployee():
    """ Attempts to Delete an employee document
        :Returns:
            - Returns response according to operation status
    """                
    requestData = request.json
    try:
        employee = attemptDeleteEmployee(requestData)
        resp = jsonify('Employee delete Success'), 200
    except:
        resp = jsonify('Employee delete Failed'), 200
    return resp

def viewEmployee():
    """ Attempts to View an employee document
        :Returns:
            - Returns single employee details if successful
    """                    
    requestData = request.json
    try:
        employee = getSingleEmployee(requestData)
    except:
        resp = jsonify('Something went wrong'), 200
        return resp       
    else:
        return employee