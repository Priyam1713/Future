import {useState} from 'react';
import {Button} from './components/ui/button';
export function DedicatedIntake({id,spec,onPrepared}:{id:number,spec:any,onPrepared:(r:any)=>void}){
 const [answers,setAnswers]=useState<Record<string,string>>(()=>Object.fromEntries(spec.fields.map((f:any)=>[f.key,f.default]))),[error,setError]=useState(''),[busy,setBusy]=useState(false);
 async function prepare(){setBusy(true);setError('');try{const response=await fetch('/api/intake/dedicated',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({technique_id:id,answers})});const result=await response.json();if(!response.ok)throw Error(result.error);onPrepared(result.request)}catch(e){setError(String(e))}finally{setBusy(false)}}
 return <section><h2>{spec.title}</h2><p>{spec.description}</p>{spec.fields.map((field:any)=><label className="field" key={field.key}><span>{field.label}</span><select disabled={busy} value={answers[field.key]} onChange={e=>setAnswers({...answers,[field.key]:e.target.value})}><option value="" disabled>Choose an option</option>{field.choices.map((v:string)=><option key={v} value={v}>{v.replaceAll('_',' ')}</option>)}</select></label>)}{error&&<p role="alert" className="error">{error}</p>}<Button disabled={busy} onClick={prepare}>Prepare these inputs</Button></section>
}
