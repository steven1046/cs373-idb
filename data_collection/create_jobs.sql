DROP TABLE jobs;

CREATE TABLE jobs
(
 job_id character varying,
 job_title character varying,
 url character varying,
 description text,
 location character varying,
 company_name character varying,
 company_id integer,
 CONSTRAINT pk_jobs PRIMARY KEY (job_id),
 CONSTRAINT fk_company_id FOREIGN KEY (company_id)
     REFERENCES companies (company_id) MATCH SIMPLE
     ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
 OIDS=FALSE
);
ALTER TABLE jobs
 OWNER TO "dataUser";