--
-- PostgreSQL database cluster dump
--

\restrict 7dCrzv3PHEfT0Bx4dkkWn9aCqk59QIMR395QTG0sQcVpb3Ur27XdIf6BlFbCF9G

SET default_transaction_read_only = off;

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

--
-- Roles
--

CREATE ROLE "Gaia";
ALTER ROLE "Gaia" WITH SUPERUSER INHERIT CREATEROLE CREATEDB LOGIN REPLICATION BYPASSRLS PASSWORD 'md5f5a248ee519951af70e716aec1c71b46';






\unrestrict 7dCrzv3PHEfT0Bx4dkkWn9aCqk59QIMR395QTG0sQcVpb3Ur27XdIf6BlFbCF9G

--
-- Databases
--

--
-- Database "template1" dump
--

\connect template1

--
-- PostgreSQL database dump
--

\restrict gdw71zzIZuQ8F1JBr3RbCcgCZp7W7WkoiJVP5L2cnde0sxqOvIAFo68Qud6gkJG

-- Dumped from database version 13.23 (Debian 13.23-1.pgdg13+1)
-- Dumped by pg_dump version 13.23 (Debian 13.23-1.pgdg13+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- PostgreSQL database dump complete
--

\unrestrict gdw71zzIZuQ8F1JBr3RbCcgCZp7W7WkoiJVP5L2cnde0sxqOvIAFo68Qud6gkJG

--
-- Database "chart_db" dump
--

--
-- PostgreSQL database dump
--

\restrict TAdn95nd48I3O12SECFcXcPK4rRsAQMq0an2C7yGUsO9euOvcwa8lHZjCbAFSzH

-- Dumped from database version 13.23 (Debian 13.23-1.pgdg13+1)
-- Dumped by pg_dump version 13.23 (Debian 13.23-1.pgdg13+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: chart_db; Type: DATABASE; Schema: -; Owner: Gaia
--

CREATE DATABASE chart_db WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'en_US.utf8';


ALTER DATABASE chart_db OWNER TO "Gaia";

\unrestrict TAdn95nd48I3O12SECFcXcPK4rRsAQMq0an2C7yGUsO9euOvcwa8lHZjCbAFSzH
\connect chart_db
\restrict TAdn95nd48I3O12SECFcXcPK4rRsAQMq0an2C7yGUsO9euOvcwa8lHZjCbAFSzH

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- PostgreSQL database dump complete
--

\unrestrict TAdn95nd48I3O12SECFcXcPK4rRsAQMq0an2C7yGUsO9euOvcwa8lHZjCbAFSzH

--
-- Database "postgres" dump
--

\connect postgres

--
-- PostgreSQL database dump
--

\restrict AmzIGGD3a3bxLEAZohMJ39yFFmHZjbnlVFmupixb65YaPB3nbMV5NxdcaACEED8

-- Dumped from database version 13.23 (Debian 13.23-1.pgdg13+1)
-- Dumped by pg_dump version 13.23 (Debian 13.23-1.pgdg13+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- PostgreSQL database dump complete
--

\unrestrict AmzIGGD3a3bxLEAZohMJ39yFFmHZjbnlVFmupixb65YaPB3nbMV5NxdcaACEED8

--
-- PostgreSQL database cluster dump complete
--

