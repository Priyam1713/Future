"""Thin in-process adapters. Native outputs and errors are never rescored here."""
import contextlib,copy,importlib,io,json,sys,threading
from .common import ROOT,REGISTRY_HASH,PROFILE_HASH,LabError,bounded_json,digest,obj,sequence,nonempty,profile,code_sha
from .registry import capability
_CLI_LOCK=threading.RLock()
def invoke(request):
    profile();bounded_json(request)
    if not isinstance(request,dict):raise LabError('Invocation object required')
    entry=capability(request.get('technique_id'));command=request.get('operation');op=next((o for o in entry['operations'] if o['command']==command),None)
    if op is None:raise LabError('Operation is not registered for selected technique')
    obj(request,['technique_id','operation','input' if op['adapter']=='native_request' else 'arguments']);output=None;error=None;stdout='';stderr='';code=0
    if op['adapter']=='native_request':
        module,function=op['python_entry_point'].rsplit('.',1);fn=getattr(importlib.import_module(module),function)
        from ..__main__ import load_registry
        reg=load_registry()
        try:
            try:output=fn(copy.deepcopy(request['input']),reg)
            except Exception as exc:error=dict(type=type(exc).__name__,module=type(exc).__module__,message=str(exc));code=2
        finally:reg.close()
    else:
        args=sequence(request['arguments'],128)
        for value in args:nonempty(value,4096)
        if any(value=='--database' or value.startswith('--database=') or value=='--format' or value.startswith('--format=') for value in args):raise LabError('Lab legacy adapter owns database and JSON format options')
        from ..__main__ import main
        out=io.StringIO();err=io.StringIO()
        with _CLI_LOCK:
            previous=sys.argv;sys.argv=['future',command]+args
            try:
                with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):
                    try:main()
                    except SystemExit as exc:code=exc.code if isinstance(exc.code,int) else 2;error=dict(type='SystemExit',module='builtins',message=str(exc)) if code else None
                    except Exception as exc:error=dict(type=type(exc).__name__,module=type(exc).__module__,message=str(exc));code=2
            finally:sys.argv=previous
        stdout=out.getvalue();stderr=err.getvalue()
        if stdout.strip():
            try:output=json.loads(stdout)
            except ValueError:
                if not code:raise LabError('Native CLI did not return structured JSON')
    result=dict(schema_version=1,technique_id=entry['technique_id'],operation=command,adapter=op['adapter'],registry_sha256=REGISTRY_HASH,core_sha256=entry['core_sha256'],request_sha256=digest(request),execution_status='native_error' if error else 'returned',native_output=output,native_output_sha256=digest(output) if output is not None else None,native_error=error,native_exit_code=code,native_stdout=stdout if op['adapter']=='legacy_cli_inprocess' else None,native_stderr=stderr if op['adapter']=='legacy_cli_inprocess' else None,provenance=dict(core_release='core-v1.0.0',profile_identifiers=entry['profile_identifiers'],python_entry_point=op['python_entry_point'],sources=entry['sources']),limits=['Native unsupported states remain inside native_output.','This invocation is not empirical validation or a shared prediction score.'])
    result['lab_profile_sha256']=PROFILE_HASH;result['lab_code_sha256']=digest({p.relative_to(ROOT).as_posix():code_sha(p.relative_to(ROOT).as_posix()) for p in sorted((ROOT/'future/lab').glob('*.py'))})
    result['invocation_sha256']=digest(result);return result
def validate_request(request):
    r=invoke(request)
    return dict(status='native_completed' if r['native_error'] is None and r['native_exit_code']==0 else 'native_rejected',method='Validation through native offline execution; may cost the same as run.',invocation=r)
