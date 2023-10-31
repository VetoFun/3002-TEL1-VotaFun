import { test, expect } from '@playwright/test';
test.describe.configure({mode: 'serial'})

test('Room creation', async ({ browser }) => {
  test.slow();
  const hostContext = await browser.newContext({ permissions: ["clipboard-read", "clipboard-write"] });
  const hostpage = await hostContext.newPage();

  await hostpage.goto('https://votafun.onrender.com/');
  await hostpage.locator('[class="btn btn-primary h-fit w-full py-3 text-lg hover:scale-105"]').click();
  await hostpage.waitForURL('https://votafun.onrender.com/room/join/*');
  await hostpage.getByRole('textbox').fill('Lloyd');
  await hostpage.getByRole('button').click();
  await hostpage.waitForURL('https://votafun.onrender.com/room/lobby/*');

  // checks if participant list contain Lloyd
  await expect(hostpage.locator('[class="flex flex-1 justify-between"]').nth(0)).toContainText('Lloyd');
  await expect(hostpage.locator('[class="btn btn-secondary text-lg"]')).toBeVisible();

  await hostpage.locator('[class="tooltip ml-2 rounded-md bg-accent p-3 px-4 transition-transform hover:scale-105 hover:cursor-pointer"]').click();

  // checks there is only one host
  await expect(hostpage.getByTestId("crown-icon")).toHaveCount(1);

  // checks if "Select Location" and "Select Activity" are present
  await expect(hostpage.locator('[class="select select-bordered select-error w-full text-lg"]')).toHaveCount(2);

  // checks if we can join the same room
  let room_url = await hostpage.evaluate("navigator.clipboard.readText()")
  let current_url = hostpage.url();
  let current_url_split = current_url.split('/');
  expect(room_url).toContain(current_url_split[current_url_split.length-1]);
});

test('Join room', async ({ browser }) => {
  test.slow();
  const hostContext = await browser.newContext({ permissions: ["clipboard-read", "clipboard-write"] });
  const hostpage = await hostContext.newPage();

  await hostpage.goto('https://votafun.onrender.com/');
  await hostpage.locator('[class="btn btn-primary h-fit w-full py-3 text-lg hover:scale-105"]').click();
  await hostpage.waitForURL('https://votafun.onrender.com/room/join/*');
  await hostpage.getByRole('textbox').fill('Lloyd');
  await hostpage.getByRole('button').click();
  await hostpage.waitForURL('https://votafun.onrender.com/room/lobby/*');

  await hostpage.locator('[class="tooltip ml-2 rounded-md bg-accent p-3 px-4 transition-transform hover:scale-105 hover:cursor-pointer"]').click();
  let room_url = await hostpage.evaluate("navigator.clipboard.readText()")

  const participantContext = await browser.newContext({ permissions: ["clipboard-read", "clipboard-write"] });
  const participantPage = await participantContext.newPage();

  await participantPage.goto(room_url);
  await participantPage.getByRole('textbox').fill('Charles');
  await participantPage.getByRole('button').click();
  await participantPage.waitForURL('https://votafun.onrender.com/room/lobby/*');

  // checks if there is only one host
  await expect(participantPage.locator('[class="group flex w-full gap-4 px-4 py-3 align-middle transition-colors hover:bg-accent group-hover:text-neutral"]').nth(0).getByTestId("crown-icon")).toHaveCount(1);
  await expect(participantPage.locator('[class="group flex w-full gap-4 px-4 py-3 align-middle transition-colors hover:bg-accent group-hover:text-neutral"]').nth(1).getByTestId("crown-icon")).toHaveCount(0);
  // check if room has 2 participants and they are rendered correctly
  await expect(participantPage.locator('[class="flex flex-1 justify-between"]')).toHaveCount(2);
  await expect(participantPage.locator('[class="flex flex-1 justify-between"]').nth(1)).toContainText("Charles");
  await expect(hostpage.locator('[class="flex flex-1 justify-between"]').nth(1)).toContainText("Charles");

  // checks if participant can see "thinking"
  await expect(participantPage.locator('[class="flex-1 rounded-md bg-accent py-2 text-center font-light leading-normal text-accent-content"]').nth(0)).toContainText("thinking");
  await expect(participantPage.locator('[class="flex-1 rounded-md bg-accent py-2 text-center font-light leading-normal text-accent-content"]').nth(1)).toContainText("thinking");
});

test('Kick user', async ({ browser }) => {
  test.slow();
  const hostContext = await browser.newContext({ permissions: ["clipboard-read", "clipboard-write"] });
  const hostpage = await hostContext.newPage();

  await hostpage.goto('https://votafun.onrender.com/');
  await hostpage.locator('[class="btn btn-primary h-fit w-full py-3 text-lg hover:scale-105"]').click();
  await hostpage.waitForURL('https://votafun.onrender.com/room/join/*');
  await hostpage.getByRole('textbox').fill('Lloyd');
  await hostpage.getByRole('button').click();
  await hostpage.waitForURL('https://votafun.onrender.com/room/lobby/*');

  await hostpage.locator('[class="tooltip ml-2 rounded-md bg-accent p-3 px-4 transition-transform hover:scale-105 hover:cursor-pointer"]').click();
  let room_url = await hostpage.evaluate("navigator.clipboard.readText()")

  const participantContext = await browser.newContext({ permissions: ["clipboard-read", "clipboard-write"] });
  const participantPage = await participantContext.newPage();

  await participantPage.goto(room_url);
  await participantPage.getByRole('textbox').fill('Charles');
  await participantPage.getByRole('button').click();
  await participantPage.waitForURL('https://votafun.onrender.com/room/lobby/*');

  await hostpage.getByTestId("kick-button").nth(0).click();
  await participantPage.waitForURL('https://votafun.onrender.com/room/lobby/*');

  // check if the participant is shown the return to home page
  await expect(participantPage.locator('[class="text-lg font-bold"]')).toContainText("You are not in a room!");
  await expect(participantPage.locator('[class="py-4"]')).toContainText("You will be returned to the home page");
  await expect(participantPage.locator('[class="btn btn-neutral"]')).toBeVisible();

  // checks if participant is returned to the home page
  await participantPage.locator('[class="btn btn-neutral"]').click();
  expect(participantPage.url()).toBe('https://votafun.onrender.com/');
});

test('Vote options', async ({ browser }) => {
  test.slow();
  const hostContext = await browser.newContext({ permissions: ["clipboard-read", "clipboard-write"] });
  const hostpage = await hostContext.newPage();

  await hostpage.goto('https://votafun.onrender.com/');
  await hostpage.locator('[class="btn btn-primary h-fit w-full py-3 text-lg hover:scale-105"]').click();
  await hostpage.waitForURL('https://votafun.onrender.com/room/join/*');
  await hostpage.getByRole('textbox').fill('Lloyd');
  await hostpage.getByRole('button').click();
  await hostpage.waitForURL('https://votafun.onrender.com/room/lobby/*');

  // starts the room
  await hostpage.getByRole('button').nth(0).click();
  await hostpage.waitForURL('https://votafun.onrender.com/room/session/*');

  // click on the first option
  await hostpage.getByRole('button').nth(0).click();

  // check if all options are still clickable
  await expect(hostpage.getByRole('button').nth(0)).toHaveAttribute("disabled");
  await expect(hostpage.getByRole('button').nth(1)).toHaveAttribute("disabled");
  await expect(hostpage.getByRole('button').nth(2)).toHaveAttribute("disabled");
  await expect(hostpage.getByRole('button').nth(3)).toHaveAttribute("disabled");
});

test('Set room properties', async ({ browser }) => {
  test.slow();
  const hostContext = await browser.newContext({ permissions: ["clipboard-read", "clipboard-write"] });
  const hostpage = await hostContext.newPage();

  await hostpage.goto('https://votafun.onrender.com/');
  await hostpage.locator('[class="btn btn-primary h-fit w-full py-3 text-lg hover:scale-105"]').click();
  await hostpage.waitForURL('https://votafun.onrender.com/room/join/*');
  await hostpage.getByRole('textbox').fill('Lloyd');
  await hostpage.getByRole('button').click();
  await hostpage.waitForURL('https://votafun.onrender.com/room/lobby/*');

  await hostpage.locator('[class="tooltip ml-2 rounded-md bg-accent p-3 px-4 transition-transform hover:scale-105 hover:cursor-pointer"]').click();
  let room_url = await hostpage.evaluate("navigator.clipboard.readText()")

  const participantContext = await browser.newContext({ permissions: ["clipboard-read", "clipboard-write"] });
  const participantPage = await participantContext.newPage();

  await participantPage.goto(room_url);
  await participantPage.getByRole('textbox').fill('Charles');
  await participantPage.getByRole('button').click();
  await participantPage.waitForURL('https://votafun.onrender.com/room/lobby/*');
});
