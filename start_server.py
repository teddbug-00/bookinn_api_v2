import uvicorn
import http

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, use_colors=True)
    