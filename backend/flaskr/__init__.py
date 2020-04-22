import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    
    # @DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the 
    CORS(app, resources={'/': {'origins': '*'}})
    
    # @DONE: Use the after_request decorator to set Access-Control-Allow  
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response
    
    
    def paginate_questions(request, selection):
        page = request.args.get('page', 1, type=int)
        start =  (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
      
        books = [book.format() for book in selection]
        current_books = books[start:end]
      
        return current_books
        
    # @DONE: Create an endpoint to handle GET requests for all available categories.
    def generate_categories_dict():
        categories = Category.query.all()
        categories_dict = {}
        for each_category in categories:
            categories_dict[each_category.id] = each_category.type
        return categories_dict
    
    # curl -X GET http://127.0.0.1:5000/categories
    @app.route('/categories')
    def get_categories():
        return jsonify({'success': True, 'categories': generate_categories_dict()})
    
    
    '''
    @DONE: 
    Create an endpoint to handle GET requests for questions, 
    including pagination (every 10 questions). 
    This endpoint should return a list of questions, 
    number of total questions, current category, categories. 
    
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
    '''
    
    # curl -X GET http://127.0.0.1:5000/questions?page=2
    @app.route('/questions')  
    def get_questions():
        
        questions = Question.query.all()
        page_questions = paginate_questions(request, questions)
        
        categories_dict = generate_categories_dict()
        categories_list = [i for i in categories_dict.values()]
        
        if len(page_questions)==0:
            abort(404)
        
        return jsonify({'success':True, 
                        'questions': page_questions, 
                        'total_questions':len(questions),
                        'categories': categories_list,
                        'current_category':None})

    '''
    @DONE: 
    Create an endpoint to DELETE question using a question ID. 
    
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''
    
    # curl -X DELETE http://127.0.0.1:5000/questions/5
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                       Question.id == question_id).one_or_none()

            if question is None:
                abort(404)
            question.delete()

            return jsonify({
                "success": True,
                "deleted question": question_id})

        except:
            abort(422)       
    
    '''
    @TODO: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.
    
    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''
    
    # curl -X POST -H "Content-Type: application/json" -d '{"question":"what is your name?","answer":"Sid","category":"2","difficulty":"3"}' http://127.0.0.1:5000/questions
    # curl -X POST http://127.0.0.1:5000/questions?search=lake
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        search = request.args.get('search', None, type=str)
        
        if search != None:
            try:
                print ('######search term is  :', search)
                questions = Question.query.filter(Question.question.ilike(f'%{search}%')).all()
                if questions is None:
                    abort(404)
                
                page_questions = paginate_questions(request, questions)
                return jsonify({'success': True,
                                'questions': page_questions})
            
            
            except Exception as e:
                print (e)
                abort(422)
        else:
            try:
                n_question = body.get('question', None)
                n_answer = body.get('answer', None)
                n_category = body.get('category', None)
                n_difficulty = body.get('difficulty', None)
                question = Question(question = n_question, answer = n_answer, 
                         category = n_category, difficulty= n_difficulty)
                print (question)
                question.insert()
                return jsonify({
                    'success': True,
                    'created question': question.id})
            except Exception as e:
                print (e)
                abort(422) # unprocessible
    
    '''
    @DONE: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 
    
    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''

    
    '''
    @DONE: 
    Create a GET endpoint to get questions based on category. 
    
    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''
    
    # curl -X GET http://127.0.0.1:5000/categories/1/questions
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        try:
            questions = Question.query.filter(Question.category == category_id).all()
            questions = [i.format() for i in questions]
            return jsonify({'success':True,
                            'questions': questions,
                            'total_questions': len(questions),
                            'current_category': category_id})
        except Exception as e:
            print (e)
            abort(422)
    
    '''
    @TODO: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 
    
    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        try:
            body = request.get_json()

            previous_questions = body.get('previous_questions')
            quiz_category = body.get('quiz_category')['id']
            
            print ('quiz category is:', quiz_category, previous_questions)

            if (quiz_category == 0):
                questions = Question.query.all()
            else:
                questions = Question.query.filter(Question.category == quiz_category).all()

            # exclude previous questions
            questions = Question.query.filter(~Question.id.in_(previous_questions)).all()
            
            if(len(questions) > 0):
                question = questions[random.randint(0,len(questions))].format()
            else:
                question = None

            return jsonify({
                'success': True,
                'question': question})

        except:
            abort(422)
    
    '''
    @DONE: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False, 
            "error": 404,
            "message": "Not found"
            }), 404
    
    @app.errorhandler(422)
    def unprocessible(error):
        return jsonify({
            "success": False,
            'error': 422,
            'message': 'unprocessible'})
    
    return app

    