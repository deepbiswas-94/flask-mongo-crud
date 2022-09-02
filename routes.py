from flask import Blueprint
from controllers.EmployeeController import employeeList,addOrUpdate,viewEmployee,deleteEmployee

router = Blueprint('router',__name__,url_prefix='/employee')

router.route('list', methods=['GET'])(employeeList)
router.route('addOrUpdate', methods=['POST'])(addOrUpdate)
router.route('view', methods=['GET'])(viewEmployee)
router.route('delete', methods=['POST'])(deleteEmployee)