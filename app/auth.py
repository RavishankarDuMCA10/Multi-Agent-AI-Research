from fastapi import Request, HTTPException


async def require_api_key(request: Request):
    config = request.app.state.config
    if not config.api_key:
        return  # No API key required if not set in config
    key = request.headers.get("X-API-Key", "")
    if key != config.api_key:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
