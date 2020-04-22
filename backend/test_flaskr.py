import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_v4"
        self.database_path = "postgresql://postgres:abcde@localhost:5432/trivia_v4"
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
        self.test_question = Question(question = 'What is my name?',
                     answer = 'sid',
                     difficulty = 5,
                     category = 1)
        self.json_question = {'question' :'What is my name?',
                     'answer' : 'sid',
                     'difficulty' : 5,
                     'category' : 1}
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        
        self.assertGreater(len(data['categories']), 1)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        
    def test_get_questions(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)
        
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        self.assertGreater(len(data['categories']), 1)
        self.assertTrue(data['categories'], True)
        self.assertGreater(data['total_questions'], 0)
        
    def test_get_questions_404_abort(self):
        res = self.client().get('/questions?page=10')
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
    
    def test_delete_question(self):
        new_question = self.test_question
        new_question.insert()
        
        res = self.client().delete(f'/questions/{new_question.id}')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(Question.query.filter(Question.id == new_question.id).first(), None)
        
    def test_create_question(self):
        res = self.client().post('/questions', json=self.json_question)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        
    def test_search_questions(self):
        res = self.client().post('/questions?search=lake')
        data = json.loads(res.data)

        self.assertTrue(len(data['questions']) > 0)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        
    def test_get_questions_by_category(self):
        res = self.client().get('/categories/5/questions')
        data = json.loads(res.data)

        # test assertions
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertGreater(data['total_questions'],0)
        
    def test_play_quiz(self):
        res = self.client().post('/quizzes', json={'previous_questions': [10,11,12],
                                                   'quiz_category': {'id': 1,}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        
        
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()