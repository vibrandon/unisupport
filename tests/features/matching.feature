Feature: Matching 
  As a student I want to match my preferred professional.

  Scenario: student match a professional positive test
    Given a student whose id is <student_id>
    When the student chooses a professional whose id is <professional_id> as his preferred professional 
    Then his preferred professional id is <professional_id>
    Examples: 
      | student_id | professional_id |
      | 1          | 2               |
      | 3          | 5               |

  Scenario: No professional id provided negative test 
    Given a student 
    When the student does not provide a professional id 
    Then the system return false
    Examples: 
      | student_id | 
      |            | 