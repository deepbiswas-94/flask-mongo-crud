from flask import Blueprint
from controllers.EmployeeController import EmployeeController as emp

router = Blueprint('router',__name__,url_prefix='/employee')

router.route('list', methods=['GET'])(emp.employeeList)
router.route('addOrUpdate', methods=['POST'])(emp.addOrUpdate)
router.route('view', methods=['GET'])(emp.viewEmployee)
router.route('delete', methods=['POST'])(emp.deleteEmployee)