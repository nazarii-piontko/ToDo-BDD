Feature: I should able to add/mark/remove todo items

Background:
  Given open home page
  And wait until loading disappear

Scenario: I should see welcome message on fresh site
  Then I should see welcome message

Scenario: Add one todo item
  When I add todo item "ToDo #1"
  Then I should see todo item "ToDo #1" in the list

Scenario: Mark todo item
  When I add todo items:
  """
  ToDo #1
  ToDo #2
  ToDo #3
  """
  And toggle todo item "ToDo #2" done
  Then I should see todo item "ToDo #2" toggled as done

Scenario: Remove todo item
  When I add todo items:
  """
  ToDo #1
  ToDo #2
  ToDo #3
  """
  And remove todo item "ToDo #2"
  Then I should see todo items:
  """
  ToDo #1
  ToDo #3
  """
  When I remove todo item "ToDo #1"
  And remove todo item "ToDo #3"
  Then I should see welcome message