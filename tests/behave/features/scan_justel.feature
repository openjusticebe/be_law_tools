Feature: scan_justel

  Scenario: Generate URLS for scanning engine
    Given a set of parameters
        | startDate  |  endDate   | interval |
        | 1990-01-01 | 1990-03-01 | month    |
      When I obtain the generator
        Then I can rotate through 3 valid urls
