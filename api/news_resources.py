import datetime

from flask_restful import Resource, reqparse, abort

from flask import jsonify

from data import db_session
from data.news import News

parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('content', required=True)
parser.add_argument('date', required=True, type=str)
parser.add_argument('seem_for', required=True, type=str)
parser.add_argument('author_id', required=True, type=int)


def abort_if_news_not_found(news_id):
    session = db_session.create_session()
    news = session.query(News).get(news_id)
    if not news:
        abort(404, message=f"News {news_id} not found")


class NewsResource(Resource):
    def get(self, news_id):
        abort_if_news_not_found(news_id)
        session = db_session.create_session()
        news = session.query(News).get(news_id)
        return jsonify(
            {
                'news':
                    news.to_dict(
                        only=(
                            'title', 'content', 'date', 'user.surname', 'user.name', 'user.patronymic',
                            'user.status_id'))
            }
        )

    def delete(self, news_id):
        abort_if_news_not_found(news_id)
        session = db_session.create_session()
        news = session.query(News).get(news_id)
        session.delete(news)
        session.commit()
        return jsonify({'success': 'OK'})


class NewsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        news = session.query(News).all()
        return jsonify(
            {
                'news':
                    [item.to_dict(
                        only=(
                        'title', 'content', 'date', 'user.surname', 'user.name', 'user.patronymic', 'user.status_id'))
                        for item in news]
            }
        )

    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        news = News(
            title=args['title'],
            content=args['content'],
            author_id=args['author_id'],
            seem_for=args['seem_for'],
            date=datetime.datetime.strptime(args['date'], '%Y-%m-%d %H:%M:%S.%f')
        )
        db_sess.add(news)
        db_sess.commit()
        return jsonify({'success': 'OK'})
