Feature: I should able to add todo items

Scenario: Add one todo
  When I open home page
  And wait for 2 seconds
  Then I should see element c"span.pulse" visible