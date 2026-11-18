import {test,expect} from '@playwright/test';
test('Gemini is offered in all 54 flows and requires consent and reviewed native input',async({page,request})=>{
 const registry=await(await request.get('/api/registry')).json();await page.goto('/');
 for(const engine of registry.entries){await page.locator('.engine-card').filter({has:page.getByRole('heading',{name:engine.name,exact:true})}).click();await expect(page.getByText('Get input help from Gemini',{exact:true})).toBeVisible();await page.locator('nav').getByRole('button',{name:'Explore',exact:true}).click()}
 const detail=await(await request.get('/api/techniques/4')).json();
 await page.locator('.engine-card').filter({has:page.getByRole('heading',{name:detail.capability.name,exact:true})}).click();
 await page.getByText('Get input help from Gemini',{exact:true}).click();
 await page.getByLabel('Gemini assistance text',{exact:true}).fill('Synthetic test facts');
 await expect(page.getByRole('button',{name:'Prepare with Gemini',exact:true})).toBeDisabled();
 await page.getByText('I permit sending this selected content to Google for Gemini processing',{exact:true}).click();
 await page.route('**/api/ai/assist',route=>route.fulfill({json:{request:detail.sample,missing_information:[],validation:{native_error:null},provenance:{model:'mock'}}}));
 await page.getByRole('button',{name:'Prepare with Gemini',exact:true}).click();
 await expect(page.getByRole('button',{name:'Use reviewed Gemini inputs',exact:true})).toBeDisabled();
 await page.getByText('I reviewed all fields; no observations or evidence were invented',{exact:true}).click();
 await page.getByRole('button',{name:'Use reviewed Gemini inputs',exact:true}).click();
 await page.getByRole('button',{name:'Run technique',exact:true}).click();
 await expect(page.locator('.results .badge').filter({hasText:'returned'})).toBeVisible();
 await expect(page.getByText('Explain this result with Gemini',{exact:true})).toBeVisible();
});
