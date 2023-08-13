from concurrent import futures
import grpc
import hr_pb2
import hr_pb2_grpc
from flask import Flask, jsonify,Request
from models import Employee

app = Flask(__name__)
employees=[]
class HRServiceServicer(hr_pb2_grpc.HRServiceServicer):
    """Missing associated documentation comment in .proto file."""

    def CreateEmployee(self, request, context):
        

        employees.append(new_employee)
        new_employee=hr_pb2.Employee(
            id=len(employees) +1,
            name=request.name,
            email=request.email,
            department=request.department,
            title=request.title

        

        )

        employees.append(new_employee)
        employees.session.commit()
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')
    
    # def create_app():
    #     app.add_url_rule(
    #     "/CreateEmployee.HRServiceServicer().GET",
    #     view_func=HRServiceServicer().CreateEmployee,
    #     methods=["POST"]
    #     )
    #     return app
    


    def GetEmployee(self, request, context):
        """Missing associated documentation comment in .proto file."""
        for employee in employees:
            if employee.id == request.id:
                return employee
            
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details('Employee not found!')
        channel = grpc.insecure_channel("localhost:50051")
        stub = hr_pb2_grpc.HRServiceStub(channel)

        grpc_request = hr_pb2.GetEmployeeReuest(employee_id=request.employee.id)
        grpc_response = stub.GetEmployee(grpc_request)
        #raise NotImplementedError('Method not implemented!')
        return hr_pb2.GetEmployeeResponse(
            id = grpc_response.id,
            name = grpc_response.name,
            email =grpc_response.email,
            department = grpc_response.department
        )
    def GetAllEmployees(self,request,context):
        return hr_pb2.EmployeeList(employees.employee)
    
    
 # This class is part of an EXPERIMENTAL API.
class HRService(object):
    """Missing associated documentation comment in .proto file."""
    #@staticmethod
    # def create_app():
    #     app.add_url_rule(
    #         "/getemployee. HRServiceServicer().GET",
    #         view_func=HRServiceServicer().GetEmployee,
    #         methods=["GET"]
    #     )
    #     return app

    @staticmethod
    def GetEmployee(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        

        app.add_url_rule(
            "/getemployee. HRServiceServicer().GET",
            view_func=HRServiceServicer().GetEmployee,
            methods=["GET"]
        )
        return app
        return grpc.experimental.unary_unary(request, target, '/hr.HRService/GetEmployee',
            hr__pb2.GetEmployeeRequest.SerializeToString,
            hr__pb2.GetEmployeeResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateEmployee(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/hr.HRService/CreateEmployee',
            hr__pb2.CreateEmployeeRequest.SerializeToString,
            hr__pb2.CreateEmployeeResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)





def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    hr_pb2_grpc.add_HRServiceServicer_to_server(
        HRServiceServicer(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    # app = create_app()
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    serve()
