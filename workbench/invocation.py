"""Workbench compatibility for native ledger readers with a root argument."""
import copy, hashlib
from pathlib import Path
from future import lab, remote_viewing, prophetic_dreams
from future.lab.common import digest

def invoke(request):
    result=lab.invoke(request)
    error=result['native_error']
    # Frozen Lab passes Registry as positional argument two. These two readers
    # use that position for root, so file-backed reports need keyword dispatch.
    if request['technique_id'] not in (43,44) or not error or error['type']!='TypeError' or "not 'Registry'" not in error['message']:
        return result
    engine=remote_viewing if request['technique_id']==43 else prophetic_dreams
    from future.__main__ import load_registry
    registry=load_registry()
    try:
        try:
            output=engine.read(copy.deepcopy(request['input']),registry=registry)
            native_error=None
        except Exception as exc:
            output=None;native_error=dict(type=type(exc).__name__,module=type(exc).__module__,message=str(exc))
    finally:registry.close()
    result.update(adapter='workbench_native_keyword_registry',native_output=output,native_output_sha256=digest(output) if output is not None else None,native_error=native_error,native_exit_code=2 if native_error else 0,execution_status='native_error' if native_error else 'returned')
    result['workbench_adapter']=dict(id='ledger-keyword-registry-v1',code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),original_lab_error=error)
    result['invocation_sha256']=digest({k:v for k,v in result.items() if k!='invocation_sha256'})
    return result
