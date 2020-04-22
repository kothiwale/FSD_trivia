# Full Stack API Final Project

## Full Stack Trivia

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a  webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out. 

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others. 

# Installing Dependencies and Running the Program

Please take a look at README.md in frontend and backend folder for installing dependencies

# Endpoints

The applicaton would be run locally and would be available at http://127.0.0.1:5000

## GET /categories

This endpoint returns the list of all question categories

curl -X GET http://127.0.0.1:5000/categories

Attributes: categories
Parameters: None
Response: 

{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}

## GET /questions

This endpoint returns the list of all question categories

curl -X GET http://127.0.0.1:5000/questions?page=2

Attributes: questions
Parameters: page
Response: 

{
  "categories": [
    "Science", 
    "Art", 
    "Geography", 
    "History", 
    "Entertainment", 
    "Sports"
  ], 
  "current_category": null, 
  "questions": [
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }, 
  ], 
  "success": true, 
  "total_questions": 39
}


## DELETE /questions/<int:question_id>

This endpoint deletes a question
curl -X DELETE http://127.0.0.1:5000/questions/5

Attributes: /questions/<int:question_id>
parameters: None
Response:
{
  "deleted question": 10, 
  "success": true
}

## POST /questions

This endpoint can create as well as search a question

curl -X POST -H "Content-Type: application/json" -d '{"question":"what is your name?","answer":"Sid","category":"2","difficulty":"3"}' http://127.0.0.1:5000/questions
curl -X POST http://127.0.0.1:5000/questions?search=lake

Attributes: question, answer, category, difficulty
Parameters: search term
Response:
{
  "created question": 62, 
  "success": true
}

## GET /categories/<int:category_id>/questions

This endpoint gets all the questions from the specified category

curl -X GET http://127.0.0.1:5000/categories/1/questions

Attributes: /categories/<int:category_id>/questions
Parameters: None
Response:

{
  "current_category": 1, 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "sid", 
      "category": 1, 
      "difficulty": 5, 
      "id": 38, 
      "question": "What is my name?"
    }, 
 
    {
      "answer": "sid", 
      "category": 1, 
      "difficulty": 5, 
      "id": 60, 
      "question": "What is my name?"
    }
  ], 
  "success": true, 
  "total_questions": 16
}

## POST /quizzes

This endpoint simulates a game

curl -X POST -H 'Content-Type: application/json' -d '{"previous_questions" : [1, 2], "quiz_category" : {"id" : "3"}} http://127.0.0.1:5000/quizzes 

Response:
{
  "question": {
    "answer": "One", 
    "category": 2, 
    "difficulty": 4, 
    "id": 18, 
    "question": "How many paintings did Van Gogh sell in his lifetime?"
  }, 
  "success": true
}


# The following ERROR types are implemented for all above endpoints:

## 404

{
"success": False, 
"error": 404,
"message": "Not found"
}

## 422

{
"success": False, 
"error": 422,
"message": "unprocessible"
}

# Credits

The project has been conducted as part of Udacity Full Stack Developer Nanodegree program. The code base has been provided by Udacity.