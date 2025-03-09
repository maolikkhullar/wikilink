from flask_restful import Resource
from flask import request,jsonify
from flask_jwt_extended import jwt_required,get_jwt_identity
import wikipedia
from models.WikipediaDB import WikipediaDB
from datetime import datetime
from database import db


class Wikipedea(Resource):
    @jwt_required()
    def post(self,function):
        if function == 'search':
            search_keyword = request.form.get('search_keyword')
            list = request.form.get('list')
            response = self.search(search_keyword,list)
            return response
        
        elif function == 'article':
            title = request.form.get('title')
            response = self.get_article(title)
            return response
        
        elif function == 'save':
            title = request.form.get('title')
            url = request.form.get('url')
            response = self.save_favorite(title,url)
            return response
        
        elif function == 'list':
            response = self.get_favorites()
            return response
        
        elif function == 'delete':
            id = int(request.form.get('favourite_id'))
            print(id)
            response = self.delete_favorite(id)
            return response

    
    def search(self,search_keyword,result_num):
        if not search_keyword:
            return {'error': 'Search term is required'}, 400
        
        try:
            wikipedia.set_lang("en")
            results = wikipedia.search(search_keyword, results=result_num)
            return {
                'search_term': search_keyword,
                'results': [{'title': result} for result in results]
            }, 200
        except Exception as e:
            return {'error': str(e)}, 500
        
    def get_article(self, title):

        if not title:
            return {'error': 'Article title is required'}, 400
        
        requested_title = title.strip()
        try:

            page = wikipedia.page(requested_title, auto_suggest=False) # auto_suggest=False for exact matching, got error with input Food output Good

            # from modules.util.LLM import LLM
            # llm_instance = LLM()

            # categories = llm_instance.get_categories(page.content)
            
            return {'title': page.title,'summary': page.summary,'url': page.url , 'content':page.content}, 200
        
        except wikipedia.exceptions.DisambiguationError as e:

            options = e.options[:10]
            return {'error': f"'{requested_title}' may refer to multiple articles",'options': options}, 300
        
        except Exception as e:
            return {'error': str(e)}, 404
        
    
    def save_favorite(self,title,url):

        if not (title or url):
            return {'error': 'Title and URL are required'}, 400
        
        try:
            user_id = get_jwt_identity()

            existing_save = WikipediaDB.query.filter(WikipediaDB.title==title,WikipediaDB.url==url,WikipediaDB.user_id== user_id).first()

            if not existing_save:
                wiki_obj = WikipediaDB(
                    title=title,
                    url=url,
                    date_added=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    user_id = user_id
                )
                db.session.add(wiki_obj)
                db.session.commit()
                return {'message': 'Article saved to favorites'}, 201
            
            return {'message': 'Already saved'}, 400
        
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500
        
    def get_favorites(self):

        try:
            userid = get_jwt_identity()
            favorites = WikipediaDB.query.filter_by(user_id=userid).order_by(WikipediaDB.date_added.desc()).all()

            favourite_list = []
            for favorite in favorites:
                favorite_dict = favorite.to_dict()
                
                from modules.api.tags import Tags
                tags_obj = Tags()
                tags_response = tags_obj.get_tags(favorite.id)

                if tags_response and isinstance(tags_response, tuple):
                    tags_data = tags_response[0]
                    print(tags_data)
                    favorite_dict['tags'] = tags_data.get('tags', [])
                else:
                    favorite_dict['tags'] = []

                favourite_list.append(favorite_dict)

            return {'favorites': favourite_list}, 200
        
        except Exception as e:
            return {'error': str(e)}, 500
        
    def delete_favorite(self,id):
        try:
            favorite = WikipediaDB.query.get(id)
            if not favorite:
                return {'error': 'Favorite not found'}, 404
            
            db.session.delete(favorite)
            db.session.commit()
            return {'message': 'Favorite deleted'}, 200
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500
