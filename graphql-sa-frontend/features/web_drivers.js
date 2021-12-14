const { Builder, By, Capabilities, Key, until, } = require('selenium-webdriver');
require("chromedriver");
// driver setup
const capabilities = Capabilities.chrome();
capabilities.set('chromeOptions', { "w3c": false });
const driver = new Builder().withCapabilities(capabilities).build();

module.exports.driver = driver;
module.exports.until = until;
module.exports.By = By;

