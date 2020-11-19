# Mission-to-Mars

# Data Analytics Week 10 Challenge

## Objectives
The goals of this challenge are to:

* Use BeautifulSoup and Splinter to automate a web browser and scrape high-resolution images.
* Use a MongoDB database to store data from the web scrape.
* Update the web application and Flask to display the data from the web scrape.
* Use Bootstrap to style the web app.


## Resources

Python 3.7.7<br>
Jupyter Notebook<br>
Modules/Libraries:  splinter, BeautifulSoup, pandas, datetime<br>
VS Code (.py, .html, .css files)<br>
MongoDB<br>
Flask<br>
Bootstrap 3<br>

## Analysis

The web scrape is performed in the functions written in the python script:  [scraping.py](scraping.py).
Output is pushed to a browser with Flask, with the app routes being set up in the python script [app.py](app.py).
The app routes in the app.py script calls the scraping.py script which contains the code that is doing the heavy lifting.
Data is stored in a MongoDB, where it is retrieved to display on the browser through a locally hosted Flask instance.
The page is set up and formatted with the html file:  [index.html](templates/index.html).  This file uses Bootstrap 3 components to clean up the display and add responsive image types to allow for optimized viewing across various devices.  For the challenge, I have added the 4 hemisphere images as clickable thumbnails.  I have also set up the scraping route with an html index to add a home button to return to the main page once the scraping is complete. 

### Obstacles and Challenges

1. Throughout the weekly modules I encountered some errors that I was able to debug myself.  The chromedriver was not present in the directory where the python interpreter was looking.  Attention to detail and review of the error codes were crucial to overcoming this obstacle.  
2. Looping through the list of dictionaries held in the MongoDB was a challenge.  I understand that my code could be refactored to include these loops.  Considering there are only 4 items I have manually accessed each dictionary by the index list and key.  
3. Creating the clickable thumbnails was a bit of a challenge.  Finally, it occured to me that the data source url would have an exmaple that I could use for guidance on the syntax.  My app still lacks home buttons on the landing pages of the image thumbnails.  Next steps could be creating index html pages for each of the 4 images.
