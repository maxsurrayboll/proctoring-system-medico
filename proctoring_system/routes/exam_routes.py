from flask import Blueprint, request, jsonify, session
from models import db
from models.log_model import ExamLog
from utils.detection import detect_multiple_faces
import os

exam_bp = Blueprint('exam', __name__)

suspicion_scores = {}

if not os.path.exists('frames'):
    os.makedirs('frames')

@exam_bp.route('/log_event', methods=['POST'])
def log_event():
    if 'user_id' not in session:
        return jsonify({'error': 'No autenticado'}), 401

    user_id = session['user_id']
    data = request.get_json()

    event_type = data.get('event_type')
    details = data.get('details', '')

    score_map = {
        "tab_switch": 3,
        "window_blur": 2
    }

    score = score_map.get(event_type, 1)

    suspicion_scores[user_id] = suspicion_scores.get(user_id, 0) + score

    log = ExamLog(
        user_id=user_id,
        event_type=event_type,
        details=details,
        severity=score
    )

    db.session.add(log)
    db.session.commit()

    return jsonify({
        'status': 'ok',
        'risk_score': suspicion_scores[user_id]
    })


@exam_bp.route('/upload_frame', methods=['POST'])
def upload_frame():
    if 'user_id' not in session:
        return jsonify({'error': 'No autenticado'}), 401

    user_id = session['user_id']

    if 'frame' not in request.files:
        return jsonify({'error': 'No se envió imagen'}), 400

    file = request.files['frame']

    path = f'frames/user_{user_id}.png'
    file.save(path)

    faces = detect_multiple_faces(path)

    if faces > 1:
        suspicion_scores[user_id] = suspicion_scores.get(user_id, 0) + 5

        log = ExamLog(
            user_id=user_id,
            event_type="multiple_faces",
            details=f"{faces} personas detectadas",
            severity=5
        )

        db.session.add(log)
        db.session.commit()

        return jsonify({
            'alert': 'MULTIPLE_PERSONS_DETECTED',
            'faces': faces,
            'risk_score': suspicion_scores[user_id]
        })

    return jsonify({
        'status': 'ok',
        'faces': faces
    })