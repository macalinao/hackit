--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner:
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner:
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: Comments; Type: TABLE; Schema: public; Owner: hackit; Tablespace:
--

CREATE TABLE "Comments" (
    id integer NOT NULL,
    votes integer,
    comment text,
    fb_id text,
    post_id integer NOT NULL,
    fb_user_id text,
    fb_user_name text,
    "time" integer
);


ALTER TABLE public."Comments" OWNER TO hackit;

--
-- Name: Comments_id_seq; Type: SEQUENCE; Schema: public; Owner: hackit
--

CREATE SEQUENCE "Comments_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Comments_id_seq" OWNER TO hackit;

--
-- Name: Comments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hackit
--

ALTER SEQUENCE "Comments_id_seq" OWNED BY "Comments".id;


--
-- Name: Groups; Type: TABLE; Schema: public; Owner: hackit; Tablespace:
--

CREATE TABLE "Groups" (
    g_id integer NOT NULL,
    fb_id text,
    name text
);


ALTER TABLE public."Groups" OWNER TO hackit;

--
-- Name: Groups_id_seq; Type: SEQUENCE; Schema: public; Owner: hackit
--

CREATE SEQUENCE "Groups_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Groups_id_seq" OWNER TO hackit;

--
-- Name: Groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hackit
--

ALTER SEQUENCE "Groups_id_seq" OWNED BY "Groups".g_id;


--
-- Name: Posts; Type: TABLE; Schema: public; Owner: hackit; Tablespace:
--

CREATE TABLE "Posts" (
    id integer NOT NULL,
    fb_id text,
    title text,
    full_post text,
    link text,
    likes integer,
    comments integer,
    active integer,
    original_url text,
    group_id text,
    fb_user_id text,
    fb_user_name text,
    "time" integer
);


ALTER TABLE public."Posts" OWNER TO hackit;

--
-- Name: Posts_id_seq; Type: SEQUENCE; Schema: public; Owner: hackit
--

CREATE SEQUENCE "Posts_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Posts_id_seq" OWNER TO hackit;

--
-- Name: Posts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hackit
--

ALTER SEQUENCE "Posts_id_seq" OWNED BY "Posts".id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: hackit
--

ALTER TABLE ONLY "Comments" ALTER COLUMN id SET DEFAULT nextval('"Comments_id_seq"'::regclass);


--
-- Name: g_id; Type: DEFAULT; Schema: public; Owner: hackit
--

ALTER TABLE ONLY "Groups" ALTER COLUMN g_id SET DEFAULT nextval('"Groups_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: hackit
--

ALTER TABLE ONLY "Posts" ALTER COLUMN id SET DEFAULT nextval('"Posts_id_seq"'::regclass);


--
-- Name: Comments_pkey; Type: CONSTRAINT; Schema: public; Owner: hackit; Tablespace:
--

ALTER TABLE ONLY "Comments"
    ADD CONSTRAINT "Comments_pkey" PRIMARY KEY (id);


--
-- Name: Posts_pkey; Type: CONSTRAINT; Schema: public; Owner: hackit; Tablespace:
--

ALTER TABLE ONLY "Posts"
    ADD CONSTRAINT "Posts_pkey" PRIMARY KEY (id);


--
-- Name: public; Type: ACL; Schema: -; Owner: hackit
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM hackit;
GRANT ALL ON SCHEMA public TO hackit;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

