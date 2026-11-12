"""Install the pinned, local-only Windows vision runtime outside the repository."""
import hashlib,json,os,subprocess,time,urllib.request,zipfile
from pathlib import Path
HOME=Path.home()/'.future-workbench-vision'
VERSION='0.40.16'
SHA='50fcf5ad54277f2fa5d173ebfc93bcb017adbc0c9ef2314daabc96ca9e6aa64e'
MODEL='qwen3-vl:4b-instruct-q4_K_M'
def main():
    HOME.mkdir(exist_ok=True);archive=HOME/'runtime.zip';runtime=HOME/'runtime';exe=runtime/'ollama.exe'
    if not exe.exists():
        if not archive.exists():
            print('Downloading pinned Ollama runtime (1.6 GB)',flush=True)
            urllib.request.urlretrieve(f'https://github.com/ollama/ollama/releases/download/v{VERSION}/ollama-windows-amd64.zip',archive)
        if hashlib.file_digest(archive.open('rb'),'sha256').hexdigest()!=SHA:raise ValueError('Runtime checksum mismatch')
        runtime.mkdir(exist_ok=True)
        with zipfile.ZipFile(archive) as z:
            for n in z.namelist():
                if not (runtime/n).resolve().is_relative_to(runtime.resolve()):raise ValueError('Unsafe archive path')
            z.extractall(runtime)
    env=dict(os.environ,OLLAMA_HOST='127.0.0.1:11435',OLLAMA_MODELS=str(HOME/'models'),OLLAMA_NO_CLOUD='1')
    log=(HOME/'runtime.log').open('ab')
    server=subprocess.Popen([str(exe),'serve'],env=env,stdout=log,stderr=log,creationflags=subprocess.CREATE_NO_WINDOW)
    try:
        for _ in range(60):
            try:urllib.request.urlopen('http://127.0.0.1:11435/api/version',timeout=2);break
            except OSError:time.sleep(1)
        subprocess.run([str(exe),'pull',MODEL],env=env,check=True)
        tags=json.load(urllib.request.urlopen('http://127.0.0.1:11435/api/tags'))
        (HOME/'installation.json').write_text(json.dumps(dict(runtime_version=VERSION,runtime_sha256=SHA,models=tags['models']),indent=2),encoding='utf-8')
        print('Local vision model installed and digest recorded.',flush=True)
    finally:server.terminate();server.wait(timeout=30);log.close()
if __name__=='__main__':main()
