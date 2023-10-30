import { test, expect } from '@playwright/test';

test('Stress Testing', async ({ browser }) => {
  test.setTimeout(120000);
  const hostContext = await browser.newContext();
  var userPage = new Array();

  const hostpage = await hostContext.newPage();
  await hostpage.goto('https://votafun.onrender.com/');
  var join_room_url = "https://votafun.onrender.com/room/join/";

  await hostpage.getByText('CREATE ROOM').click();
  await hostpage.waitForURL('https://votafun.onrender.com/room/join/*');
  await hostpage.getByRole('textbox').fill('abc');
  await hostpage.getByRole('button').click();
  await hostpage.waitForURL('https://votafun.onrender.com/room/lobby/*');
  var url = hostpage.url();
  var split_url = url.split("/");
  join_room_url = join_room_url.concat(split_url[split_url.length-1]);

  for (let i=0; i<1; i++) {
    let userContext = await browser.newContext();
    userPage.push(await userContext.newPage());

    await userPage[i].goto(join_room_url);
    await userPage[i].getByRole('textbox').fill('ccc');
    await userPage[i].getByRole('button').click();
  }
  //
  // await hostpage.waitForTimeout(15000);
  await hostpage.locator('.tracking-widest').fill('50');
  await hostpage.waitForTimeout(10000);
  await hostpage.getByText('START ROOM').click();
  await hostpage.waitForURL('https://votafun.onrender.com/room/session/*');

  for (let i = 0; i < 5; i++) {
    await hostpage.locator('.btn-primary').click();
    await hostpage.waitForTimeout(20000);
  }

});
