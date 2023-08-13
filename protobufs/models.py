import grpc
from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import hr_pb2
import hr_pb2_grpc

app = Flask(__name__)

# Define your SQLAlchemy model
Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    department = Column(String)
    title = Column(String)

# gRPC service implementation
class HRServiceServicer(hr_pb2_grpc.HRServiceServicer):
    def __init__(self, session):
        self.session = session

    def CreateEmployee(self, request, context):
        new_employee = Employee(
            name=request.name,
            email=request.email,
            department=request.department,
            title=request.title
        )
        self.session.add(new_employee)
        self.session.commit()
        return hr_pb2.EmployeeResponse(id=new_employee.id)

    def GetEmployee(self, request, context):
        employee = self.session.query(Employee).filter_by(id=request.id).first()
        if employee:
            return employee
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Employee not found!')
            return hr_pb2.Employee()

    def GetAllEmployees(self, request, context):
        employees = self.session.query(Employee).all()
        return hr_pb2.EmployeeList(employees=employees)

# Create a SQLAlchemy session
engine = create_engine('sqlite:///employees.db')
Session = sessionmaker(bind=engine)
session = Session()

# Create and add the gRPC service to the Flask app
def create_app():
    grpc_server = grpc.server(thread_pool=ThreadPoolExecutor())
    hr_pb2_grpc.add_HRServiceServicer_to_server(HRServiceServicer(session), grpc_server)
    grpc_server.add_insecure_port('[::]:50051')
    grpc_server.start()
    
    app.run(host='0.0.0.0', port=5000)  # Start the Flask app

if __name__ == '__main__':
    create_app()
