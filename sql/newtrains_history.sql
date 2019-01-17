-- Drop table

-- DROP TABLE public.newtrains_history

CREATE TABLE public.newtrains_history (
	id serial NOT NULL,
	route varchar(12) NOT NULL,
	car varchar(7) NOT NULL,
	seen_start timestamp NOT NULL,
	seen_end timestamp NULL,
	CONSTRAINT newtrains_history_pk PRIMARY KEY (id)
);

