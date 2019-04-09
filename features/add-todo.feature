Feature: I should able to add todo items

Scenario: Add one todo
  When I open web page "/"
  Then I should see element with css selector "span.pulse" hidden