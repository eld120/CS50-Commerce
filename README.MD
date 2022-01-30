# CS50w Commerce
Revisiting an old homework assignment.

## Abey?
Taking inspiration from the largest auction website that I know of, this assignment was my first introduction to django and 3rd party packages. This project does not aim to reproduce all of ebay's functionality but does intend to generally allow any user to view content and for authenticated users to create or interact with auctions.

### Challenges
- Moving logic from views to models in an effort to reuse code functionality.
    - This required quite a bit of digging into Django's documentation as well as seeking out more in depth tutorials.
- Minimizing SQL queries and caching
    - I've been aware of the benefits of caching since I made my first Flask app which queried an external API for each row of user data (unique transaction). I was not aware of more advanced SQL queries that could have returned distinct data in fewer queries and I did not have a caching solution at the time. Even today I have yet to utilize caching in this django project but this remains the first optimization I would look to (caching db queries and potentially commonly requested rendered results).
    - I've also heard that cache invalidation is hard. #TODO

### Current objectives:
- establish a mobile first responsive UI (not started)
- establish a CI/CD pipeline using Github Actions (not started)
- maintain PEP8 coding standards using pre-commit (done)
- achieve and maintain 100% unit test coverage for all of my code (in progress)
- learn Pytest best practices (in progress)

### Notable Technologies used with Django
- django-debug-toolbar
- django-environ
- pylint
- mypy
- flake8
- isort
- pre-commit
- black
- factory-boy
- faker
- pytest
