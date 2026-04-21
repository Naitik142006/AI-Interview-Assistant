# app.py
from flask import Flask, render_template, request, session, redirect, url_for
import random
from datetime import datetime
from utils.ai_interview import AIInterviewer
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

# Validate configuration on startup
Config.validate()

# Create a SINGLE instance of AIInterviewer (persistent across requests)
ai_interviewer = AIInterviewer()

@app.route("/")
def home():
    session.clear()
    # Reset the AI interviewer for a new session
    ai_interviewer.reset_session()
    return render_template("index.html")

@app.route("/start_interview", methods=["POST"])
def start_interview():
    student_name = request.form.get("student_name", "Candidate")
    experience_level = request.form.get("experience_level", "medium")
    focus_areas = request.form.getlist("focus_areas")
    
    if not focus_areas:
        focus_areas = ["Arrays", "Linked Lists", "Sorting", "Greedy"]
    
    num_selected = len(focus_areas)
    
    if num_selected <= 5:
        max_questions = min(num_selected * 2, 15)
    elif num_selected <= 10:
        max_questions = min(num_selected + 3, 15)
    else:
        max_questions = min(num_selected, 15)
    
    max_questions = max(max_questions, 5)
    
    session['student_name'] = student_name
    session['experience_level'] = experience_level
    session['focus_areas'] = focus_areas
    session['questions_asked'] = []
    session['answers_given'] = []
    session['question_count'] = 0
    session['max_questions'] = max_questions
    
    question_schedule = []
    for i in range(max_questions):
        topic_index = i % len(focus_areas)
        question_schedule.append(focus_areas[topic_index])
    random.shuffle(question_schedule)
    session['question_schedule'] = question_schedule
    
    session['current_topic'] = question_schedule[0]
    
    # Use the persistent AI interviewer
    question = ai_interviewer.generate_question(
        topic=session['current_topic'],
        difficulty=experience_level,
        previous_questions=session['questions_asked']
    )
    
    session['current_question'] = question
    session['questions_asked'].append(question)
    
    return render_template("interview.html",
                         question=question,
                         question_num=1,
                         total=session['max_questions'],
                         student_name=student_name,
                         topic=session['current_topic'],
                         total_topics_selected=len(focus_areas))

@app.route("/analyze", methods=["POST"])
def analyze():
    question = request.form["question"]
    answer = request.form["answer"]
    
    analysis = ai_interviewer.analyze_answer(question, answer, session.get('current_topic', 'General'))
    
    if 'knowledge_score' in analysis:
        analysis['knowledge_score'] = min(max(analysis['knowledge_score'], 0), 100)
    if 'clarity_score' in analysis:
        analysis['clarity_score'] = min(max(analysis['clarity_score'], 0), 100)
    if 'confidence_score' in analysis:
        analysis['confidence_score'] = min(max(analysis['confidence_score'], 0), 100)
    
    session['answers_given'].append({
        'question': question,
        'answer': answer,
        'analysis': analysis,
        'topic': session.get('current_topic'),
        'timestamp': datetime.now().isoformat()
    })
    
    session['question_count'] += 1
    
    if session['question_count'] >= session['max_questions']:
        return redirect(url_for('summary'))
    
    question_schedule = session.get('question_schedule', [])
    if session['question_count'] < len(question_schedule):
        next_topic = question_schedule[session['question_count']]
    else:
        focus_areas = session.get('focus_areas', [])
        next_index = session['question_count'] % len(focus_areas)
        next_topic = focus_areas[next_index]
    
    session['current_topic'] = next_topic
    
    followup = None
    if analysis.get('knowledge_score', 0) > 40:
        followup = ai_interviewer.generate_followup(question, answer, next_topic)
    
    # Use the persistent AI interviewer
    next_question = ai_interviewer.generate_question(
        topic=next_topic,
        difficulty=session.get('experience_level', 'medium'),
        previous_questions=session['questions_asked']
    )
    
    session['current_question'] = next_question
    session['questions_asked'].append(next_question)
    
    return render_template("interview_with_feedback.html",
                         result=analysis,
                         question=question,
                         answer=answer,
                         followup=followup,
                         next_question=next_question,
                         next_topic=next_topic,
                         question_num=session['question_count'] + 1,
                         total=session['max_questions'])

@app.route("/summary")
def summary():
    answers = session.get('answers_given', [])
    if not answers:
        return redirect('/')
    
    # Generate model answers for each question
    for answer in answers:
        model_answer = ai_interviewer.generate_model_answer(answer['question'], answer.get('topic', 'General'))
        answer['model_answer'] = model_answer
    
    total_knowledge = 0
    total_clarity = 0
    total_confidence = 0
    
    for answer in answers:
        knowledge = min(max(answer['analysis'].get('knowledge_score', 0), 0), 100)
        clarity = min(max(answer['analysis'].get('clarity_score', 0), 0), 100)
        confidence = min(max(answer['analysis'].get('confidence_score', 0), 0), 100)
        
        total_knowledge += knowledge
        total_clarity += clarity
        total_confidence += confidence
    
    num = len(answers)
    
    avg_knowledge = (total_knowledge / num) if num > 0 else 0
    avg_clarity = (total_clarity / num) if num > 0 else 0
    avg_confidence = (total_confidence / num) if num > 0 else 0
    
    overall = (avg_knowledge + avg_clarity + avg_confidence) / 3
    overall = min(max(overall, 0), 100)
    
    overall_score = {
        'knowledge': round(avg_knowledge, 1),
        'clarity': round(avg_clarity, 1),
        'confidence': round(avg_confidence, 1),
        'overall': round(overall, 1)
    }
    
    return render_template("summary.html",
                         answers=answers,
                         student_name=session.get('student_name', 'Candidate'),
                         overall_score=overall_score)

if __name__ == "__main__":
    debug_mode = app.config['FLASK_ENV'] == 'development'
    print("\n" + "="*50)
    print("🚀 AI Interview Assistant Starting...")
    print("="*50)
    if debug_mode:
        print("⚠️  Running in DEVELOPMENT mode")
        print("🔧 Debug mode enabled")
    else:
        print("✅ Running in PRODUCTION mode")
    print(f"📝 API Key loaded: {'Yes' if Config.GROQ_API_KEY else 'No'}")
    print("="*50)
    app.run(debug=debug_mode, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))