Feature: ProjectSelection

Scenario: Student selects an available project
Given User is already logged in as a student
And User is already on project selection page
When User selects an available project
Then Project selection is finally accepted

Scenario: Student selects an unavailable project
Given User is already logged in as a student
And User is already on project selection page
When User selects an unavailable project
Then Project selection is finally denied