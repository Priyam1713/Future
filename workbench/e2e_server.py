"""Isolated browser-test server. Synthetic clock control never exists in production."""
import tempfile
import uvicorn
from fastapi import Request
from .api import create_app

def main():
    with tempfile.TemporaryDirectory(prefix='future-workbench-browser-') as directory:
        stamp=['2030-01-01T00:00:00Z'];app=create_app(directory,clock=lambda:stamp[0])
        @app.post('/__test__/clock')
        def advance(q:dict):stamp[0]=q['at'];return {'at':stamp[0]}
        uvicorn.run(app,host='127.0.0.1',port=8765,access_log=False)
if __name__=='__main__':main()
