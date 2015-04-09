CREATE TABLE jobs
(
  company_id integer NOT NULL,
  cmpny_name character varying,
  job_id integer NOT NULL,
  job_title character varying,
  description text,
  location character varying,
  url character varying,
  CONSTRAINT pk_jobs PRIMARY KEY (job_id),
  CONSTRAINT fk_company_id FOREIGN KEY (company_id)
    REFERENCES companies (company_id) MATCH SIMPLE
    ON UPDATE NO ACTION ON DELETE NO ACTION

)

WITH(
  OIDS=FALSE
);
ALTER TABLE jobs
  OWNER TO "dataUser";