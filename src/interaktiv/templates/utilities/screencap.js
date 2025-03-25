const puppeteer = require('puppeteer');

async function checkBasicAuth(url) {
    const response = await fetch(url, {method: 'GET'});

    if (response.status === 401) {
        const authHeader = response.headers.get('www-authenticate');
        if (authHeader && authHeader.toLowerCase().includes('basic')) {
            return true;
        }
    }
    return false;
}

async function run(url, username, password, basic_auth_username, basic_auth_password) {
    const browser = await puppeteer.launch({args: ['--no-sandbox', '--disable-setuid-sandbox']});
    const page = await browser.newPage();

    const siteURL = new URL(url)

    await page.setViewport({width: 1920, height: 1080});

    if (await checkBasicAuth(siteURL.origin) && basic_auth_username && basic_auth_password) {
        await page.setExtraHTTPHeaders({
            'Authorization': `Basic ${Buffer.from(basic_auth_username + ':' + basic_auth_password).toString('base64')}`
        })
    }

    const response = await fetch(`${siteURL.origin}/++api++/@login`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({"login": username, "password": password})
    });

    const data = await response.json();
    const token = data.token;

    const cookies = response.headers.get('set-cookie');
    const __acCookie = cookies.split(';').find(cookie => cookie.trim().startsWith('__ac='));

    if (__acCookie) {
        await browser.setCookie({
            name: '__ac',
            value: __acCookie.split('=')[1],
            domain: siteURL.host,
            path: '/',
            sameSite: 'Lax',
        });
    }

    await browser.setCookie({
        name: 'auth_token',
        value: token,
        domain: siteURL.host,
        path: '/',
        secure: siteURL.origin.startsWith('https://'),
    });

    await page.goto(siteURL.href, {waitUntil: 'networkidle0'});

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