Feature: scan_justel

  Scenario: Generate URLS for scanning engine
    Given a set of parameters
        | startDate  |  endDate   | interval |
        | 1990-01-01 | 1990-03-01 | month    |
      When I obtain the generator
        Then I can rotate through 3 valid urls


  Scenario: Discriminate between valid and invalid pages
    Given some urls
        | url                                              | result | links |
        | http://www.ejustice.just.fgov.be/eli/loi/1800    | False  | 0     |
        | http://www.ejustice.just.fgov.be/eli/loi/1800/02 | False  | 0     |
        | http://www.ejustice.just.fgov.be/eli/loi/1900    | True   | 6     |
      When I feed them to the scanner
        Then I obtain the expected results
        And I obtain the expected link count
