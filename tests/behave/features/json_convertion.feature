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

  @debug
  Scenario: Convert a document into a JSON - debug mode
    Given justel uri "loi/2019/03/23/2019A40586/justel"
      When I extract unformatted data
      And I convert to dict
      And I load dict properties
        Then It contains at least 1800 entries
        And It contains the type "part" with reference "1" at position 0
        And It contains the type "book" with reference "1" at position 1
        And It contains the type "title" with reference "1" at position 2
        And It contains the type "article" with reference "1:1" at position 3
        #And It contains the type "chapter" with reference "1" at position 19
        #And It contains the type "chapter" with reference "3" at position 39
        #And It contains the type "article" with reference "1:27" at position 40
        And It contains the type "book" with reference "2" at position 57
        And It contains the type "book" with reference "3" at position 280
        And It contains the type "book" with reference "5" at position 467
        And It contains the type "subsection" with reference "3" at position 306
        And It contains the type "article" with reference "3:44" at position 342
        And It contains the type "book" with reference "7" at position 911
        #And It contains the type "article" with reference "7:24" at position 950
        #And It contains the type "subsection" with reference "1" at position 976
        #And It contains the type "article" with reference "7:53" at position 985
        #And It contains the type "article" with reference "7:56" at position 988
        #And It contains the type "section" with reference "2" at position 991
        #And It contains the type "article" with reference "7:58" at position 992
        #And It contains the type "article" with reference "7:59" at position 993
        #And It contains the type "section" with reference "3" at position 994
        #And It contains the type "article" with reference "7:60" at position 995
        #And It contains the type "article" with reference "7:62" at position 1000
        #And It contains the type "article" with reference "7:146" at position 1116
        ##And It contains the type "article" with reference "7:146 DROIT FUTUR" at position 1117
        #And It contains the type "article" with reference "7:146/1" at position 1119
        #And It contains the type "article" with reference "7:146/2" at position 1120
        #And It contains the type "subsection" with reference "1" at position 1130
        #And It contains the type "article" with reference "7:170" at position 1160
        #And It contains the type "article" with reference "7:199" at position 1200
        #And It contains the type "article" with reference "7:216" at position 1230
        And It contains the type "book" with reference "8" at position 1253
        And It contains the type "book" with reference "9" at position 1266
        And It contains the type "chapter" with reference "1" at position 1372
        And It contains the type "book" with reference "14" at position 1549
        #And It contains the type "article" with reference "14:36" at position 1600
        #And It contains the type "subsection" with reference "2" at position 1630
        #And It contains the type "article" with reference "14:63" at position 1635
        #And It contains the type "title" with reference "5" at position 1640
        #And It contains the type "chapter" with reference "1" at position 1641
        #And It contains the type "article" with reference "14:67" at position 1642
        #And It contains the type "article" with reference "14:71" at position 1650
        And It contains the type "book" with reference "15" at position 1666
        And It contains the type "book" with reference "16" at position 1722
        And It contains the type "book" with reference "17" at position 1780
        And It contains the type "book" with reference "18" at position 1794
        And It contains the type "chapter" with reference "3" at position 1802
        And the document "language" is "FR"

    Given justel uri "wet/2019/03/23/2019A40586/justel"
      When I extract unformatted data
      And I convert to dict
        Then the document "language" is "NL"

        # /!\ different than FR. Error in the source
        And It contains the type "subsection" with reference "2" at position 306
        # /!\ different than FR. Error in the source
        And It contains the type "article" with reference "3:43" at position 342
        # /!\ different than FR. Error in the source
        And It contains the type "chapter" with reference "I" at position 1372

        And It is equals to previously loaded properties

