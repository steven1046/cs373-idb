-- companies, games, genres, platforms, game_genres, game_platforms

-- Table: app.companies

-- DROP TABLE app.companies;

CREATE TABLE app.companies
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
ALTER TABLE app.companies
  OWNER TO "dataUser";


-- Table: app.games

-- DROP TABLE app.games;

CREATE TABLE app.games
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
      REFERENCES app.companies (company_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE app.games
  OWNER TO "dataUser";

-- Index: app.fki_company_id

-- DROP INDEX app.fki_company_id;

CREATE INDEX fki_company_id
  ON app.games
  USING btree
  (company_id);


-- Table: app.genres

-- DROP TABLE app.genres;

CREATE TABLE app.genres
(
  genre_id integer NOT NULL,
  genre character varying NOT NULL,
  CONSTRAINT pk_genres PRIMARY KEY (genre_id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE app.genres
  OWNER TO "dataUser";


-- Table: app.platforms

-- DROP TABLE app.platforms;

CREATE TABLE app.platforms
(
  platform_id integer NOT NULL,
  platform character varying NOT NULL,
  CONSTRAINT pk_platforms PRIMARY KEY (platform_id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE app.platforms
  OWNER TO "dataUser";


-- Table: app.game_genres

-- DROP TABLE app.game_genres;

CREATE TABLE app.game_genres
(
  game_id integer NOT NULL,
  genre_id integer NOT NULL,
  CONSTRAINT pk_game_genres PRIMARY KEY (game_id, genre_id),
  CONSTRAINT fk_game_id FOREIGN KEY (game_id)
      REFERENCES app.games (game_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT fk_genre_id FOREIGN KEY (genre_id)
      REFERENCES app.genres (genre_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE app.game_genres
  OWNER TO "dataUser";


-- Table: app.game_platforms

-- DROP TABLE app.game_platforms;

CREATE TABLE app.game_platforms
(
  game_id integer NOT NULL,
  platform_id integer NOT NULL,
  CONSTRAINT pk_game_platforms PRIMARY KEY (game_id, platform_id),
  CONSTRAINT fk_game_id FOREIGN KEY (game_id)
      REFERENCES app.games (game_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT fk_platform_id FOREIGN KEY (platform_id)
      REFERENCES app.platforms (platform_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE app.game_platforms
  OWNER TO "dataUser";
