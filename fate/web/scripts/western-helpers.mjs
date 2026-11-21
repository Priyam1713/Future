export async function fillBirth(page, origin = "http://127.0.0.1:8010") {
  await page.goto(`${origin}/#western`);
  await page.getByLabel("Date of birth", { exact: true }).fill("1990-07-15");
  await page.getByLabel("Recorded birth time").fill("14:30:00");
  await page.getByLabel("Birth city", { exact: true }).fill("London GB");
  await page.getByRole("button", { name: "Find city", exact: true }).click();
  await page
    .getByRole("button", { name: /^London · GB/ })
    .first()
    .click();
  await page
    .getByLabel("I’ve checked the coordinates and timezone for my birthplace.")
    .check();
}

export async function turnInstrument(page) {
  const slider=page.getByRole('slider',{name:'Turn the instrument'});
  await slider.scrollIntoViewIfNeeded();
  const b=await slider.boundingBox();
  await page.mouse.move(b.x+b.width*.5,b.y+b.height*.5);
  await page.mouse.down();
  for(const fraction of [.58,.66,.74,.82,.74,.66,.58,.5]){
    await page.mouse.move(b.x+b.width*fraction,b.y+b.height*.5,{steps:3});
    await page.waitForTimeout(90);
  }
  await page.mouse.up();
  await page.getByRole('button',{name:'Align Ascendant',exact:true}).click();
}
