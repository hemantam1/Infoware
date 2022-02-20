The E-commerce scraper files consists of python scripts that scrap the files from ecommerce websites including Amazon, Bigbasket, Dmart, Grofers, and Jiomart.

There are 2 different sets of files:
  1. Product Scraper scripts: These are used for scraping products across various pincodes. The pincodes and the items are present in the Required files directory which can be
                              modified as per requirement.
  2. Offers and Combos scripts: These are for a generalized purpose of scraping deals via the E-commerce websites. They have been optimized for faster execution.
                                No other inputs are required, and can be setup to run on a server once the headless mode configuration is made.

All of the scripts work on basically the same selected libraries that are present in python:
  1. Selenium: It handles the automation of opening, interacting with the webelements and closing the chrome browser.
  2. BeautifulSoup: It handles the navigation and scraping of the webpages.
  3. Pandas: For storing of scrapped data.
  4. CSV: Used to transfer the stored data to csv files.
  5. Concurrent: It handles the speeding up of the scraping by handling multiple instances of the chrome. The number of "workers" can be set as per requirement.
  6. re: Used to define regular Expressions which are then used for various purposes during the execution of the scripts.
  7. Warnings: To supress unecessary cluttering of the console.
  8. Datetime: This module is used to get the current time and also to track the timing of execution of the scripts.
  9. time: Used to tell the execution to stop while the webpages are loaded into view or to give time to functions to scrap the data.
For the Offers and Combos file, the functions and the main files have been separated for easier understanding and keeping the code clean.
