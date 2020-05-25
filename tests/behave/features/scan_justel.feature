Feature: scan_justel

  Scenario: Generate URLS for scanning engine
    Given a set of parameters
        | startDate  |  endDate   | interval |
        | 1990-01-01 | 1990-03-01 | month    |
      When I obtain the generator
        Then I can rotate through 3 valid urls


  Scenario: Discriminate between valid and invalid pages
    Given some page urls
        | url                                              | result | links |
        | http://www.ejustice.just.fgov.be/eli/loi/1800    | False  | 0     |
        | http://www.ejustice.just.fgov.be/eli/loi/1800/02 | False  | 0     |
        | http://www.ejustice.just.fgov.be/eli/loi/1900    | True   | 6     |
      When I feed them to the page scanner
        Then I obtain the expected results
        And I obtain the expected link count

  Scenario: Discriminate between valid and invalid documents
    Given some document urls
        | url                                                                   | result | text_length |
        | http://www.ejustice.just.fgov.be/eli/loi/1900/05/16/2100051650/justel | False  | 0           |
        | http://www.ejustice.just.fgov.be/eli/loi/1950/02/11/1950021101/justel | False  | 0           |
        | http://www.ejustice.just.fgov.be/eli/loi/1900/05/16/2009000663/justel | False  | 0           |
        | http://www.ejustice.just.fgov.be/eli/loi/1980/02/29/1980022902/justel | False  | 0           |
        | http://www.ejustice.just.fgov.be/eli/loi/1804/03/21/2010000632/justel | False  | 0           |
        | http://www.ejustice.just.fgov.be/eli/loi/1900/05/16/1900051650/justel | True   | 23850       |
      When I feed them to the document scanner
        Then I obtain the expected results
        And I obtain the expected text length
