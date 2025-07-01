from fastapi import FastAPI
from router import router_

app = FastAPI()

app.include_router(router=router_,prefix="/api_test")



# uvicorn main:app --reload   
# uvicorn main:app --reload --port 8081