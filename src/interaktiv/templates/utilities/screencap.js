const puppeteer = require('puppeteer');

async function run(url, username, password) {
    const browser = await puppeteer.launch({args: ['--no-sandbox', '--disable-setuid-sandbox']});
    const page = await browser.newPage();

    await page.setViewport({width: 1920, height: 1080});

    const response = await fetch('http://localhost:3000/++api++/@login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ "login": username, "password": password })
    });

    const data = await response.json();
    const token = data.token;

    await page.setCookie({ name: 'auth_token', value: token, domain: 'localhost', path: '/' });

    await page.goto(url, {waitUntil: 'networkidle0'});

    await page.waitForSelector('.gdpr-privacy-banner-button', {timeout: 5000});
    await page.click('.gdpr-privacy-banner-button');

    const screenshot = await page.screenshot({encoding: 'base64', type: 'jpeg', quality: '50', fromSurface: true})

    await browser.close();
    return screenshot
}

if (process.argv.length <= 4) {
    console.error('Expected at least one argument!');
    process.exit(1);
}

//noinspection JSIgnoredPromiseFromCall
run(process.argv[2], process.argv[3], process.argv[4])
    .then(function (path) {
        console.log(path);
        process.exit(0);
    })
    .catch(function (e) {
        console.error(e.message);
        process.exit(1);
    });