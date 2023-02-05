# PrizeCard_2
This project try to solve a necessity of companies to offer a fidelity card to their customers at a low cost and traceability.

 The project has 2 fronts one for the companies and another one for the shoppers.

The Companies, at this moment, are allowed to register themselves and create new fidelity cards.

The Shoppers, at this moment, are allowed to register themselves and use the cards created by the companies, when retrieving the list of companies the list of cards to be used will be displayed based on the distance between the shopper and the company, for that we have used the Geopy library, to get their stamps the shoppers will have to take a picture of the receipt, the picture will be translate to text through the use of  Pytesseract library, we will then create a unique key concatenating the name of the company with date and time of the ticket, in this way we avoid the same receipt to be multiple times, after validate the receipt, and make sure it corresponds to the card the shopper is trying to get a stamp for, the new stamp will then be added.

# Technologies used

- Python | Django | Django-Rest-Framework
- Postgres
-  Libraries
    - Geopy
    - Pytesseract
    - Django-countries
    - Django-phonenumber-field
- Docker
- Git Action

Obs.: The project has been made using TDD approach and respecting PEP8.