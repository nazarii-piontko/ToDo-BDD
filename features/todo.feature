Feature: I should able to add/toggle/remove ToDo items

Background:
  Given open home page
  And wait until loading is done

Scenario: I should see welcome message on an empty site
  Then I should see welcome message

Scenario: Add ToDo items
  When I add ToDo item "ToDo #1"
  Then I should see ToDo items:
  """
  ToDo #1
  """
  When I add ToDo item "ToDo #2"
  Then I should see ToDo items:
  """
  ToDo #1
  ToDo #2
  """
  When I add ToDo item "ToDo #3"
  Then I should see ToDo items:
  """
  ToDo #1
  ToDo #2
  ToDo #3
  """

Scenario: Toggle ToDo item to done
  When I add ToDo items:
  """
  ToDo #1
  ToDo #2
  ToDo #3
  """
  And toggle ToDo item "ToDo #2" to done
  Then I should see ToDo item "ToDo #2" toggled as done

Scenario: Remove ToDo item
  When I add ToDo items:
  """
  ToDo #1
  ToDo #2
  ToDo #3
  """
  And remove ToDo item "ToDo #2"
  Then I should see ToDo items:
  """
  ToDo #1
  ToDo #3
  """
  When I remove ToDo item "ToDo #1"
  And remove ToDo item "ToDo #3"
  Then I should see welcome message
