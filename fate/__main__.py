"""python -m fate [--no-build] [--port 8010]."""
import argparse
import shutil
import subprocess
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--no-build', action='store_true')
    parser.add_argument('--port', type=int, default=8010)
    args = parser.parse_args()
    web = Path(__file__).parent / 'web'
    if not args.no_build:
        npm = shutil.which('npm.cmd') or shutil.which('npm')
        if not npm:
            raise SystemExit('Node.js and npm are required for the first build.')
        if not (web / 'node_modules').exists():
            subprocess.run([npm, 'ci'], cwd=web, check=True)
        subprocess.run([npm, 'run', 'build'], cwd=web, check=True)
    if not (web / 'dist/index.html').exists():
        raise SystemExit('Frontend missing: run python -m fate without --no-build.')
    from .api import create_app
    import uvicorn
    print(f'FATE: http://127.0.0.1:{args.port}')
    uvicorn.run(create_app(), host='127.0.0.1', port=args.port, access_log=False)


if __name__ == '__main__':
    main()
