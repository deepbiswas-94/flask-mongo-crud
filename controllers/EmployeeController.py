from flask import request
from models.Employees import getEmployeesList,createEmployee,getSingleEmployee,attemptDeleteEmployee,updateEmployee
import pymongo,mongoengine
from email_validator import validate_email, EmailNotValidError
from controllers.BaseController import BaseController as base
class EmployeeController(base):    
    def employeeList():
        """ Getting a list Employees
            :Returns:
                - Returns result of list operation
            :Exceptions:
                - DuplicateKeyError : if any duplicates are found
        """        
        try:
            requestData = request.json    
            employeeList = getEmployeesList()
        except pymongo.errors.DuplicateKeyError:
            pass
        except Exception as e:
            return base.prepareResponse({"message": employeeList,"status":True})        
        finally:
            return base.prepareResponse({"data": employeeList,"status":True})        

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
                return base.prepareResponse({"message": 'Employee email invalid',"status":False})                    
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
                resp = base.prepareResponse({"message": 'Something went wrong',"status":False})                    
            else:
                resp = base.prepareResponse({"message": 'Employee update successful',"status":True})
            return resp          
        else:
            # Insert
            try:            
                status = createEmployee(requestData)
            except pymongo.errors.DuplicateKeyError:
                resp = base.prepareResponse({"message": 'Something went wrong',"status":False})  
            except KeyError:
                resp = base.prepareResponse({"message": 'Something went wrong',"status":False})  
            except mongoengine.errors.NotUniqueError:
                resp = base.prepareResponse({"message": 'This user already exists',"status":False})  
            else:        
                resp = base.prepareResponse({"message": 'Employee added successfully',"status":True})   
            return resp
        
    def deleteEmployee():
        """ Attempts to Delete an employee document
            :Returns:
                - Returns response according to operation status
        """                
        requestData = request.json
        try:
            employee = attemptDeleteEmployee(requestData)
            resp = base.prepareResponse({"message": 'Delete Successful',"status":True})  
        except:
            resp = base.prepareResponse({"message": 'Something went wrong',"status":False})  
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
            resp = base.prepareResponse({"message": 'Something went wrong',"status":False})  
            return resp       
        else:
            return base.prepareResponse({"data": employee,"status":True})  