# versioner
Allows to increase or decrease software version number. 
Any position can be changed, also separator is customizable.
For example:
- need to increase version "1.0.3". 
Execute:
VersionParser.increase("1.0.3")
Result: "1.0.4"
- need to increase "0.3.5-alpha2":
Result: "0.3.5-alpha3"
- need to decrease first digit in "beta8-0.99":
Execute: 
VersionParser.decrease("beta8-0.99", pos=0)
Result: "beta7-0.99"
- need to increase by 3 pre-last digit of "great_release_4_0_1_RC" with "\_" as separator:
Execute:
VersionParser.increase("great_release_4_0_1_RC", separator="\_", pos=-2, value=3)
Result: "great_release_4_3_1_RC"
- finally, need to decrease number in additiona part of the version concatinated by "+", i.e. "1.2.3alpha6+component0.2.5":
Execute:
VersionParser.decrease("1.2.3alpha6+component0.2.5", section_separator="+", section=1)
Result: "1.2.3alpha6+component0.2.4"