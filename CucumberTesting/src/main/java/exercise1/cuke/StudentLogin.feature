Feature: StudentLogin

Scenario: Student logs in successfully
Given User is not yet logged in as student
And User navigated to student login
When User logs in as an existing student
Then User is finally logged in as a student

Scenario: Student logs in unsuccessfully
Given User is not yet logged in as student
And User navigated to student login
When User logs in as a fake student
Then User is not logged in as a student