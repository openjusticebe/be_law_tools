Feature: extract_data

  Scenario: Obtain meta data from a document
    Given justel uri "loi/1999/01/10/1999009159/justel"
      When I download the document
      And I extract meta data
        Then I find a document number
        And the document "number" is "1999009159"
        And the document "source" is "JUSTICE"
        And it updated 3 other documents
