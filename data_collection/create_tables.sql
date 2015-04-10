-- companies, games, genres, platforms, game_genres, game_platforms

-- Table: companies

-- DROP TABLE companies;

CREATE TABLE companies
(
  company_id integer NOT NULL,
  name character varying,
  deck text,
  description text,
  image character varying,
  address character varying,
  city character varying,
  state character varying,
  country character varying,
  phone character varying,
  date_founded date,
  website character varying,
  CONSTRAINT pk_companies PRIMARY KEY (company_id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE companies
  OWNER TO "dataUser";


-- Table: games

-- DROP TABLE games;

CREATE TABLE games
(
  game_id integer NOT NULL,
  name character varying,
  image character varying,
  original_release_date date,
  deck text,
  description text,
  company_id integer NOT NULL,
  CONSTRAINT pk_games PRIMARY KEY (game_id),
  CONSTRAINT fk_company_id FOREIGN KEY (company_id)
      REFERENCES companies (company_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE games
  OWNER TO "dataUser";

-- Index: app.fki_company_id

-- DROP INDEX app.fki_company_id;

CREATE INDEX fki_company_id
  ON games
  USING btree
  (company_id);


-- Table: genres

-- DROP TABLE genres;

CREATE TABLE genres
(
  genre_id integer NOT NULL,
  genre character varying NOT NULL,
  CONSTRAINT pk_genres PRIMARY KEY (genre_id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE genres
  OWNER TO "dataUser";


-- Table: platforms

-- DROP TABLE platforms;

CREATE TABLE platforms
(
  platform_id integer NOT NULL,
  platform character varying NOT NULL,
  CONSTRAINT pk_platforms PRIMARY KEY (platform_id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE platforms
  OWNER TO "dataUser";


-- Table: game_genres

-- DROP TABLE game_genres;

CREATE TABLE game_genres
(
  game_id integer NOT NULL,
  genre_id integer NOT NULL,
  CONSTRAINT pk_game_genres PRIMARY KEY (game_id, genre_id),
  CONSTRAINT fk_game_id FOREIGN KEY (game_id)
      REFERENCES games (game_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT fk_genre_id FOREIGN KEY (genre_id)
      REFERENCES genres (genre_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE game_genres
  OWNER TO "dataUser";


-- Table: game_platforms

-- DROP TABLE game_platforms;

CREATE TABLE game_platforms
(
  game_id integer NOT NULL,
  platform_id integer NOT NULL,
  CONSTRAINT pk_game_platforms PRIMARY KEY (game_id, platform_id),
  CONSTRAINT fk_game_id FOREIGN KEY (game_id)
      REFERENCES games (game_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT fk_platform_id FOREIGN KEY (platform_id)
      REFERENCES platforms (platform_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE game_platforms
  OWNER TO "dataUser";

-- Table: jobs

-- DROP TABLE jobs;

CREATE TABLE jobs
(
  job_id character varying NOT NULL,
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
