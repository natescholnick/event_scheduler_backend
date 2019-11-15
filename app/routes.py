from app import app, db
from flask import request, jsonify
from app.models import Event

@app.route('/')
def index():
    return 'Wubba whatever'


@app.route('/api/save', methods=['POST'])
def save():
    try:
        title = request.headers.get('title')
        day = request.headers.get('day')
        month = request.headers.get('month')
        year = request.headers.get('year')
        notes = request.headers.get('notes', '')

        if not title or not day or not month or not year:
            return jsonify({'code' : 306, 'message' : 'Information missing.'})

        event = Event(title=title, year=year, month=month, day=day, notes=notes)

        db.session.add(event)
        db.session.commit()

        return jsonify({'code' : 200, 'message' : 'Event saved.'})

    except:
        return jsonify({
            'code' : 305,
            'message' : 'Something went wrong.'
        })



@app.route('/api/retrieve', methods=['GET'])
def retrieve():
    try:
        day = request.headers.get('day')
        month = request.headers.get('month')
        year = request.headers.get('year')

        results = []

        if not year:
            return jsonify({'code' : 302, 'message' : 'Invalid year'})
        elif day and not month:
            return jsonify({'code' : 303, 'message' : 'Invalid month'})
        elif year and not month and not day:
            results = Event.query.filter_by(year=year).all()
        elif year and month and not day:
            results = Event.query.filter_by(year=year, month=month).all()
        elif year and month and day:
            results = Event.query.filter_by(year=year, month=month, day=day).all()
        else:
            return jsonify({'code' : 304, 'message' : 'Something went wrong.'})

        if not results:
            return jsonify({'code' : 200, 'message' : 'No events scheduled.'})

        events = []
        for result in results:
            events.append({
                'event_id' : result.event_id,
                'title' : result.title,
                'day' : result.day,
                'month' : result.month,
                'year' : result.year,
                'notes' : result.notes
            })

        return jsonify({'code' : 200, 'message' : 'Events retrieved.', 'events' : events})


    except:
        return jsonify({
            'code' : 301,
            'message' : 'Something went wrong.'
        })


@app.route('/api/delete', methods=['DELETE'])
def delete():
    try:
        event_id = request.headers.get('event_id')

        event = Event.query.filter_by(event_id=event_id).first()

        if not event:
            return jsonify({'code' : 308, 'message' : 'Event not found.'})

        title = event.title
        db.session.delete(event)
        db.session.commit()
        return jsonify({'code' : 200, 'message' : f'Event {title} was deleted.'})

    except:
        return jsonify({
            'code' : 307,
            'message' : 'Something went wrong.'
        })
