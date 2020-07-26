Feature: json_convertion

  Scenario: Convert a document into a JSON
    Given justel uri "loi/2019/03/23/2019A40586/justel"
      When I extract unformatted data
      And I convert to dict
        Then It contains at least 1800 entries
        And It contains the type "part" with reference "1" at position 0
        And It contains the type "book" with reference "1" at position 1
        And It contains the type "title" with reference "1" at position 2
        And It contains the type "article" with reference "1:1" at position 3
        And the document "language" is "FR"

      When I convert dict to tree
        Then there is 5 root children
        And the first children is of type "part"


    Given justel uri "wet/2019/03/23/2019A40586/justel"
      When I extract unformatted data
      And I convert to dict
        Then the document "language" is "NL"
        And It contains at least 1800 entries
        And It contains the type "part" with reference "1" at position 0
        And It contains the type "book" with reference "1" at position 1
        And It contains the type "title" with reference "1" at position 2
        And It contains the type "article" with reference "1:1" at position 3

