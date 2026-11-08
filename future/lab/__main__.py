"""Offline Python-first Lab CLI, separate from all frozen native CLI interfaces."""
import argparse,json,sys
from pathlib import Path
from .common import LabError,load_input
from . import list_techniques,capability,invoke,validate_request
from .experiments import create,forecast,resolve,persist
from .evaluation import evaluate,compare,markdown
from .reference import noaa_reference
def read_file(path):
    if Path(path).stat().st_size>2097152:raise LabError('Lab request file exceeds2MiB')
    return load_input(path)
def main():
    parser=argparse.ArgumentParser(description='Future Lab v1: native discovery and honest offline experiments');sub=parser.add_subparsers(dest='command',required=True)
    def command(name):
        p=sub.add_parser(name);p.add_argument('--format',choices=['json','markdown'],default='json');return p
    command('list');p=command('inspect');p.add_argument('technique_id',type=int)
    for name in ['run','validate']:
        p=command(name);p.add_argument('request')
    p=command('create');p.add_argument('plan');p.add_argument('--parent')
    p=command('forecast');p.add_argument('ledger');p.add_argument('--at',required=True)
    p=command('resolve');p.add_argument('ledger');p.add_argument('outcome');p.add_argument('--at',required=True)
    p=command('evaluate');p.add_argument('ledger')
    p=command('compare');p.add_argument('reports',nargs='+')
    p=command('persist');p.add_argument('ledger');p.add_argument('directory')
    command('noaa-reference');args=parser.parse_args();code=0
    if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8',newline='\n')
    try:
        if args.command=='list':result=list_techniques()
        elif args.command=='inspect':result=capability(args.technique_id)
        elif args.command=='run':
            result=invoke(read_file(args.request));code=2 if result['native_error'] is not None or result['native_exit_code'] else 0
        elif args.command=='validate':
            result=validate_request(read_file(args.request));code=2 if result['status']=='native_rejected' else 0
        elif args.command=='create':result=create(read_file(args.plan),read_file(args.parent) if args.parent else None)
        elif args.command=='forecast':result=forecast(read_file(args.ledger),args.at)
        elif args.command=='resolve':result=resolve(read_file(args.ledger),read_file(args.outcome),args.at)
        elif args.command=='evaluate':result=evaluate(read_file(args.ledger))
        elif args.command=='compare':result=compare([read_file(p) for p in args.reports])
        elif args.command=='persist':result=dict(snapshot_path=persist(args.directory,read_file(args.ledger)))
        else:result=noaa_reference()
        out=dict(status='accepted' if code==0 else 'native_rejected',task=args.command,result=result)
    except (ValueError,TypeError,KeyError,OSError,OverflowError,ArithmeticError) as exc:
        code=2;out=dict(status='rejected',task=args.command,error=dict(type=type(exc).__name__,message=str(exc)),result=None)
    print(markdown(out) if args.format=='markdown' else json.dumps(out,indent=2,ensure_ascii=False,allow_nan=False))
    if code:raise SystemExit(code)
if __name__=='__main__':main()
