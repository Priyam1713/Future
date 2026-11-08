"""One-command localhost launch; first setup needs package downloads."""
import argparse, importlib.util, subprocess, sys, shutil, os
from pathlib import Path

def main():
    p=argparse.ArgumentParser();p.add_argument('--no-build',action='store_true');p.add_argument('--port',type=int,default=8000);args=p.parse_args()
    root=Path(__file__).resolve().parents[1];web=root/'workbench/web'
    for mod in ['fastapi','uvicorn']:
        if importlib.util.find_spec(mod) is None:
            subprocess.run([sys.executable,'-m','pip','install','-r',str(root/'workbench/requirements.txt')],check=True);break
    if not args.no_build:
        npm=shutil.which('npm.cmd') or shutil.which('npm')
        if not npm:raise SystemExit('Node.js and npm are required for initial setup')
        if not (web/'node_modules').exists():subprocess.run([npm,'ci'],cwd=web,check=True)
        subprocess.run([npm,'run','build'],cwd=web,check=True)
    if not (web/'dist/index.html').exists():raise SystemExit('Frontend build is missing; omit --no-build')
    import uvicorn
    from .api import create_app
    print(f'Future Workbench: http://127.0.0.1:{args.port} (local data stays in FUTURE_WORKBENCH_HOME or ~/.future-workbench)')
    uvicorn.run(create_app(),host='127.0.0.1',port=args.port,access_log=False)
if __name__=='__main__':main()
