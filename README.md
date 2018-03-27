## Web scraper for AWS Lambda

I implemented a site scraper for the Rutgers eSuds website in Python using Beautiful Soup. I deployed the scraper on the AWS Lambda platform to get the number of machines 'In Use' every five minutes.

See the Rutgers eSuds website [here](http://rutgers.esuds.net/).

Along with the SEED club at Rutgers University, we used this data to create an energy saving implementation plan and entered the proposal into the Rutgers Energy Institute 2018 Energy Contest.

I used this helpful [tutorial](https://andypi.co.uk/2016/07/20/using-aws-lambda-to-run-python-scripts-instead-of-local-cron/) to set up the Lambda function.