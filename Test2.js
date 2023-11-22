// Import Puppeteer libraries for Chrome and Edge browsers
const puppeteerChrome = require('puppeteer');         // For Chrome
const puppeteerEdge = require('puppeteer-edge');      // For Edge

(async () => {
    // Define which browser to use: 'chrome' or 'edge'
    const browserChoice = 'chrome'; // Change this to 'edge' to use Microsoft Edge

    // Select the appropriate Puppeteer library based on the browser choice
    const puppeteer = browserChoice === 'chrome' ? puppeteerChrome : puppeteerEdge;

    // Launch the browser
    // Setting 'headless' to false opens a real browser window
    // 'defaultViewport: null' and '--start-maximized' maximize the window
    const browser = await puppeteer.launch({
        headless: false,               // Show the browser window
        defaultViewport: null,         // Use the maximum viewport size
        args: ['--start-maximized']    // Start with a maximized window
    });

    // Open a new page in the browser
    const page = await browser.newPage();

    // Navigate to the specified URL (Data USA's homepage in this case)
    await page.goto('https://datausa.io');
    console.log('Home page is opened'); // Log when the page is opened

    // Execute a custom script within the page for smooth scrolling
    await page.evaluate(() => {
        return new Promise((resolve, reject) => {
            var totalHeight = 0;
            var distance = 20; // Each scroll will move the page by 20 pixels
            var timer = setInterval(() => {
                var scrollHeight = document.body.scrollHeight; // Total scrollable height
                window.scrollBy(0, distance); // Scroll down by 'distance' pixels
                totalHeight += distance;

                // If the bottom is reached, stop scrolling
                if (totalHeight >= scrollHeight) {
                    clearInterval(timer);
                    resolve();
                }
            }, 20); // Do this every 20 milliseconds
        });
    });

    // Wait for 3 seconds
    await new Promise(resolve => setTimeout(resolve, 3000));

    // Navigate to the About page by clicking the link and wait for the navigation
    await Promise.all([
        page.waitForNavigation(),                        // Wait for the page to load
        page.click("a[href='/about']")                   // Click the 'About' link
    ]);
    console.log('About page is opened'); // Log when the About page is opened

    // Wait for another 3 seconds
    await new Promise(resolve => setTimeout(resolve, 3000));

    // Navigate to the Maps page
    await Promise.all([
        page.waitForNavigation(),                        // Wait for the page to load
        page.click("a[href='/map']")                     // Click the 'Maps' link
    ]);
    console.log('Maps page is opened'); // Log when the Maps page is opened

    // Check if the current URL is correct (i.e., the Maps page)
    const currentURL = await page.url();
    if (currentURL !== 'https://datausa.io/map') {
        console.log('Test failed: Did not navigate to Maps page');
    } else {
        console.log('Test passed: Navigated to Maps page');
    }

    // Wait for a manual action to close the browser
    // This long timeout allows you to see the results before the browser closes
    console.log("Press 'Ctrl + C' in the terminal to close the browser.");
    await new Promise(resolve => setTimeout(resolve, 1000000)); // Wait for a long time

    // Close the browser
    await browser.close();
})();
