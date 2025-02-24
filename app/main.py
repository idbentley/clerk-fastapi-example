import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from clerk_backend_api.jwks_helpers import (
    AuthenticateRequestOptions,
    authenticate_request,
    AuthStatus,
)
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    clerk_secret_key: str = os.getenv("CLERK_SECRET_KEY")
    clerk_authorized_parties: list[str] = [
        "http://localhost:5173",
    ]


settings = Settings()


app = FastAPI()


origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def authenticate(request: Request, call_next):
    request_state = authenticate_request(
        request,
        AuthenticateRequestOptions(
            secret_key=settings.clerk_secret_key,
            authorized_parties=settings.clerk_authorized_parties,
        ),
    )

    if request_state.status != AuthStatus.SIGNED_IN:
        request.state.verified_clerk_token = None
    else:
        request.state.verified_clerk_token = request_state.payload

    response = await call_next(request)

    return response


@app.get("/clerk_jwt")
async def clerk_jwt(request: Request):
    if request.state.verified_clerk_token is None:
        return {"userId": None}
    return {"userId": request.state.verified_clerk_token["sub"]}


@app.get("/gated_data")
async def gated_data(request: Request):
    gated_data = {"foo": "bar"}

    if request.state.verified_clerk_token is None:
        return {"message": "Unauthorized"}
    return gated_data
