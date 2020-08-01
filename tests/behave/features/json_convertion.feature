Feature: json_convertion

  Scenario: Convert the Belgium corporate law into a JSON
    Given justel uri "loi/2019/03/23/2019A40586/justel"
      When I extract unformatted data
      And I convert to dict
      And I load dict properties
        Then It contains at least 1800 entries
        And It contains the type "part" with reference "1" at position 0
        And It contains the type "book" with reference "1" at position 1
        And It contains the type "title" with reference "1" at position 2
        And It contains the type "article" with reference "1:1" at position 3
        And the document "language" is "FR"

    Given justel uri "wet/2019/03/23/2019A40586/justel"
      When I extract unformatted data
      And I convert to dict
        Then the document "language" is "NL"
        And It is equals to previously loaded properties

      When I convert dict to tree
        Then there is 5 root children
        And the first children is of type "part"


  Scenario: Convert the Belgium constitution into a JSON
    Given justel uri "constitution/1994/02/17/1994021048/justel"
      When I extract unformatted data
      And I convert to dict
        Then the document "language" is "FR"
        And It contains at least 220 entries
        And It contains the type "title" with reference "I" at position 0
        And It contains the type "article" with reference "1" at position 1
        And It contains the type "article" with reference "182" at position 220
        And It contains the type "article" with reference "198" at position 238

      When I convert dict to tree
        Then there is 9 root children
        And the first children is of type "title"

