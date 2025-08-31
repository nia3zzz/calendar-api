from dotenv import load_dotenv

# load the .env variables into runtime environment
load_dotenv()

from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from db.engine import get_db
from sqlalchemy.orm import Session
from routes.auth_routes import auth_routes
import jwt
from lib.assign_jwt import secret_key
import strawberry
from strawberry.fastapi import GraphQLRouter


v1 = FastAPI()


# initialize the health check of graphql
@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello World"


schema = strawberry.Schema(Query)

graphql_app = GraphQLRouter(schema)


# define a auth middleware for every route except signup, login and the healthcheck
@v1.middleware("http")
async def AuthenticationMiddleware(request: Request, call_next):
    # check if its the allowed routes
    if request.url.path != "/api/v1/graphql":
        return await call_next(request)

    # check for the cookie
    hold_cookie = request.cookies.get("Access_Cookie")

    if hold_cookie == None:
        return JSONResponse(
            status_code=401,
            content={"staus": "error", "message": "Unauthorized, login first."},
        )

    # decode the jwt from the cookie and attach the user id in request object
    try:
        payload = jwt.decode(hold_cookie, str(secret_key), algorithms=["HS256"])

        request.state.user_id = payload.get("user_id")
        return await call_next(request)
    except (jwt.InvalidTokenError, jwt.ExpiredSignatureError):
        return JSONResponse(
            status_code=401,
            content={"staus": "error", "message": "Unauthorized, login first."},
        )
    except:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": "Something went wrong."},
        )


# include auth routes
v1.include_router(router=auth_routes, prefix="/api/v1/auth")

# include the graphql route
v1.include_router(graphql_app, prefix="/api/v1/graphql", tags=["GraphQl"])


# health check route
@v1.get("/", tags=["Health Check"])
def read_root(db: Session = Depends(get_db)):
    try:
        print("Database Session: ", db)

    finally:
        return {
            "Health": "Check",
        }
