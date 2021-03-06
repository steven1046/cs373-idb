__author__ = 'nicopelico'

from configuration.database import db
from utils.json_utils import  to_json


class Platform(db.Model):
    __tablename__ = "platforms"

    platform_id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(80))

    #Platform constructor
    def __init__(self, platform_id, platform):
        self.platform_id = platform_id
        self.platform = platform

    #Returns a representation of the platform
    def __repr__(self):
        return ""

    #Create a new platform object and commit it
    def create_platform(platform):
        new_platform = Platform(platform["genre_id"], platform["genre"])
        db.session.add(new_platform)
        db.session.commit()

    #Returns a json of the platform matching the platform id
    @to_json
    def find_by_id(platform_id):
        return Platform.query.filter_by(platform_id=platform_id).first()

    #Return a json of each platform in their own dictionary 
    def get_all_platforms():
        # want a way to just do a select *. query.all() was giving me problems
        return Platform.query.with_entities(Platform.platform_id, Platform.platform).all()





