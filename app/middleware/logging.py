import time
import logging
from fastapi import Request

log = logging.getLogger("app.request")


async def logging_middleware(request: Request, call_next):
	
	start = time.time()
	response = await call_next(request)
	duration = (time.time() - start) * 1000
	log.info("%s %s -> %s (%.2fms)", request.method, request.url.path, response.status_code, duration)

	return response
