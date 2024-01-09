# 10.0.0.203
# 10.0.0.128
# Secret = V1T4L_3sr123
from pyrad.client import Client
from pyrad.dictionary import Dictionary
import pyrad.packet
from fastapi import APIRouter, FastAPI


router = APIRouter()

def connectRadius():
    srv = Client(server="10.0.0.203", secret=b"V1T4L_3sr123", dict=Dictionary("dictionary"))
    
    req = srv.CreateAuthPacket(code=pyrad.packet.AccessRequest,
                            User_Name="nelson.londono", NAS_Identifier="localhost")
    req["User-Password"] = req.PwCrypt("Luribe.3")

    try:
        print("Sending authentication request")
        reply = srv.SendPacket(req)
    except pyrad.client.Timeout:
        print("RADIUS server does not reply")

    if reply.code == pyrad.packet.AccessAccept:
        print("Access accepted")
    else:
        print("Access denied")

    print("Attributes returned by server:")
    for i in reply.keys():
        print("%s: %s" % (i, reply[i]))
    # srv = Client(server="10.0.0.203", secret=b"V1T4L_3sr123"
    #             ,dict=Dictionary("dictionary"))

    # # create request


    # # send request
    # reply = srv.SendPacket(req)

    # if reply.code == pyrad.packet.AccessAccept:
    #     print("access accepted")
    # else:
    #     print("access denied")

    # print("Attributes returned by server:")
    # for i in reply.keys():
    #     print("%s: %s" % (i, reply[i]))


@router.get("/test", 
    tags=["Conexión"],        
    summary="Método para verificar la conexión con la API",
)
async def test_API():
    connectRadius()
    return {
            "code":200,
            "message": "API connected successfully",
            "state": True,
            "data": {}
        } 


app = FastAPI(
    title="Prueba de Radius",
    version="v0.0.1",
    description="API de consultar datos de la base de datos de Nomina de ARUS"
)
app.include_router(router)