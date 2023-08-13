import grpc
import hr_pb2
import hr_pb2_grpc
from concurrent import futures
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///employees.db"
db = SQLAlchemy(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    department = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(50), nullable=False)

    #db.create_all()

# Your Employee model should be imported here if it's defined in "models.py"
# from models import Employee
class HRServiceServicer(hr_pb2_grpc.HRServiceServicer):
    def CreateEmployee(self, request, context):
        new_employee = hr_pb2.Employee(
    
            name=request.name,
            email=request.email,
            department=request.department,
            title=request.title
        )
        db.session.add(new_employee)
        db.session.commit()

        return hr_pb2.CreateEmployeeResponse(employee=self._employee_to_proto(new_employee))
    def GetEmployee(self, request, context):
        employee = Employee.query.get(request.id)
        if employee:
            return self._employee_to_proto(employee)
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details('Employee not found!')

    def GetAllEmployees(self, request, context):
        employees = Employee.query.all()
        employee_protos = [self._employee_to_proto(employee) for employee in employees]
        return hr_pb2.EmployeeList(employees=employee_protos)

    @staticmethod
    def _employee_to_proto(employee):
        return hr_pb2.Employee(
            id=employee.id,
            name=employee.name,
            email=employee.email,
            department=employee.department,
            title=employee.title
        )

    
@app.route("/CreateEmployee", methods=["POST"])
def create_employee():
    channel = grpc.insecure_channel("localhost:50051")
    stub = hr_pb2_grpc.HRServiceStub(channel)
    
    grpc_request = hr_pb2.CreateEmployeeRequest(
        name=request.json["name"],
        email=request.json["email"],
        department=request.json["department"],
        title=request.json["title"]
    )
    grpc_response = stub.CreateEmployee(grpc_request)
    
    return jsonify({
        "message": "Employee created successfully",
        "employee": {
            "id": grpc_response.employee.id,
            "name": grpc_response.employee.name,
            "email": grpc_response.employee.email,
            "department": grpc_response.employee.department,
            "title": grpc_response.employee.title
        }
    })

# Add other routes for GetEmployee and GetAllEmployees as similar patterns
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    hr_pb2_grpc.add_HRServiceServicer_to_server(
        HRServiceServicer(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()

    app.run(host="0.0.0.0", port=5000)
app.debug =True
if __name__ == "__main__":
    serve()
