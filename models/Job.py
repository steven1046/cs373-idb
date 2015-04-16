__author__ = 'Ruben Baeza'

from configuration.database import db
from utils.json_utils import to_json
from sqlalchemy import inspect
from models import Company


class Job(db.Model):
    __tablename__ = 'jobs'

    job_id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(80))
    url = db.Column(db.String(80))
    description = db.Column(db.Text)
    location = db.Column(db.String(80))
    company_name = db.Column(db.String(80))

    company_id = db.Column(db.Integer, db.ForeignKey("companies.company_id"))

    # Create a new job object
    def __init__(self, job_id, job_title, url, description, location, company_name, company_id):
        self.job_id = job_id
        self.job_title = job_title
        self.url = url
        self.description = description
        self.location = location
        self.company_name = company_name
        self.company_id = int(company_id)

    # Returns a dictionary representation of the model
    def __repr__(self):
        return str(self.to_dict())

    # Creates a dictionary of the model to_dict is called on
    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = str(getattr(self, column.name))
        return d


# Create a new job using the json sent in
def create_job(job):
    new_job = Job(job["job_id"], job["job_title"], job["url"], job["description"], job["location"], job["company_name"],
                  job["company_id"])
    db.session.add(new_job)
    db.session.commit()


#Returns a list of all the jobs in a json
@to_json
def find_all():
    return Job.query.all()


#Returns a json of the job model matching the job id passed in
@to_json
def find_by_id(job_id):
    return Job.query.filter_by(job_id=job_id).first()
