import {test,expect} from '@playwright/test';
import {readFileSync} from 'node:fs';
const cases=JSON.parse(readFileSync('../tests/dedicated-inputs.json','utf8'));
test('all 43 dedicated forms prepare and run user inputs without sample loading',async({page,request})=>{
 test.setTimeout(300000);
 const registry=await (await request.get('/api/registry')).json();
 await page.goto('/');
 for(const [key,answers] of Object.entries(cases) as [string,Record<string,any>][]){
  const engine=registry.entries.find((e:any)=>e.technique_id===Number(key));
  const detail=await (await request.get(`/api/techniques/${key}`)).json();
  await page.locator('.engine-card').filter({has:page.getByRole('heading',{name:engine.name,exact:true})}).click();
  await expect(page.getByRole('heading',{name:detail.dedicated.title,exact:true})).toBeVisible();
  for(const field of detail.dedicated.fields){
   if(!(field.key in answers))continue;
   const input=page.getByLabel(field.label,{exact:true});const value=answers[field.key];
   if(field.type==='images')await input.setInputFiles(value.map((v:string,i:number)=>({name:`target${i}.png`,mimeType:'image/png',buffer:Buffer.from(v.split(',').pop()!,'base64')})));
   else if(field.type==='select')await input.selectOption(value);
   else await input.fill(value);
  }
  const preparation=page.waitForResponse(r=>r.url().endsWith('/api/intake/dedicated'));
  await page.getByRole('button',{name:'Prepare these inputs',exact:true}).click();
  const prepared=await preparation;expect(prepared.status(),`prepare #${key}: ${await prepared.text()}`).toBe(200);
  const execution=page.waitForResponse(r=>r.url().endsWith('/api/sessions')&&r.request().method()==='POST');
  await page.getByRole('button',{name:'Run technique',exact:true}).click();
  const response=await execution;expect(response.status(),`run #${key}`).toBe(200);
  const session=await response.json();expect(session.result.native_error,`native #${key}`).toBeNull();
  await expect(page.locator('.results .badge').filter({hasText:'returned'})).toBeVisible();
  if(key==='50')await page.screenshot({path:'../screenshots/dedicated-circuit-result.png'});
  await page.locator('nav').getByRole('button',{name:'Explore',exact:true}).click();
 }
});

