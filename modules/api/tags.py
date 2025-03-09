from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
from models.WikipediaDB import WikipediaDB
from database import db
from modules.util.LLM import LLM
from modules.api.wikipedia import Wikipedea

class Tags(Resource):

    @jwt_required()
    def post(self,function):
        if function=='autotag':
            article_id = request.form.get('article_id')
            response = self.autotag(article_id)
            return response
        
        elif function == 'add_custom_tags':
            article_id = request.form.get('article_id')
            tags = request.form.get('tags')  # Comma-separated
            response = self.add_custom_tags(article_id, tags)
            return response
        
        elif function == 'get_tags':
            article_id = request.form.get('article_id')
            response = self.get_tags(article_id)
            return response
    
    def autotag(self, article_id):
        try:

            llm_obj = LLM()
            wiki_obj = Wikipedea()

            title = WikipediaDB.query.with_entities(WikipediaDB.title).filter_by(id=article_id).scalar()

            if not title:
                return {"message": "Article not found"}, 404

            content = wiki_obj.get_article(title)[0]["content"]
            tags = llm_obj.get_categories(content)

            from models.Tags import Tags
            for tag in tags:
                existing_tag = Tags.query.filter_by(tag_name=tag,article_id=article_id).first()
                
                if not existing_tag:
                    new_tag = Tags(article_id=article_id, tag_name=tag)
                    db.session.add(new_tag)

            db.session.commit()

            return {
                "message": f"Following tags added successfully: {tags}"}, 200

        except Exception as e:
            db.session.rollback()
            return {"message": f"Error during autotagging: {str(e)}"}, 500
    
    def add_custom_tags(self, article_id, tags):

        if not tags:
            return {"message": "No tags provided"}, 400
        
        tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]

        if not tag_list:
            return {"message": "No valid tags provided"}, 400
        
        article = WikipediaDB.query.filter_by(id=article_id).first()
        if not article:
            return {"message": "Article not found"}, 404

        added_tags = []
        from models.Tags import Tags
        
        for tag in tag_list:
            existing_tag = Tags.query.filter_by(tag_name=tag, article_id=article_id).first()
            if not existing_tag:
                db.session.add(Tags(article_id=article_id, tag_name=tag))
                added_tags.append(tag)

        if added_tags:
            db.session.commit()
            return {"message": f"Following custom tags added successfully: {added_tags}"}, 200
        else:
            return {"message": "No new tags were added (tags may already exist)"}, 200
        
    def get_tags(self,article_id):
        try:

            title = WikipediaDB.query.with_entities(WikipediaDB.title).filter_by(id=article_id).scalar()

            if not title:
                return {"message": "Article not found"}, 404
            
            from models.Tags import Tags
            tags = Tags.query.filter_by(article_id=article_id).all()

            tag_list = [tag.tag_name for tag in tags]
                
            if not tag_list:
                return({"message":"No Tags present"},404)

            return {"tags": tag_list}, 200

        except Exception as e:
            db.session.rollback()
            return {"message": f"Error during autotagging: {str(e)}"}, 500


