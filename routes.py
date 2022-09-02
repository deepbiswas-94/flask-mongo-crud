from flask import Blueprint
from controllers.EmployeeController import index,addOrUpdate,view,delete

router = Blueprint('router',__name__,url_prefix='/employee')

router.route('list', methods=['GET'])(index)
router.route('addOrUpdate', methods=['POST'])(addOrUpdate)
router.route('view', methods=['GET'])(view)
router.route('delete', methods=['POST'])(delete)