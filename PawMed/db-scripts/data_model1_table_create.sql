CREATE TABLE public.patient (
    id integer NOT NULL,
    name text NOT NULL,
    surname text NOT NULL,
    registration_date timestamp with time zone NOT NULL,
    age integer NOT NULL,
    phone_number text NOT NULL,
    birth_date timestamp with time zone NOT NULL,
    city text NOT NULL,
    zip_code integer NOT NULL,
    gender char NOT NULL,
    personid integer NOT NULL,
    PRIMARY KEY (id)
);


CREATE TABLE public.visit (
    id integer NOT NULL,
    doctor integer NOT NULL,
    patient integer NOT NULL,
    date timestamp with time zone NOT NULL,
    room integer NOT NULL,
    remarks text NOT NULL,
    diagnosis text NOT NULL,
    medical_interview text NOT NULL,
    examination text NOT NULL,
    recommendation text NOT NULL,
    PRIMARY KEY (id)
);

CREATE INDEX ON public.visit
    (doctor);
CREATE INDEX ON public.visit
    (patient);


CREATE TABLE public.prescription (
    id integer NOT NULL,
    visit integer NOT NULL,
    date_of_issue timestamp with time zone NOT NULL,
    expiration_date timestamp with time zone NOT NULL,
    remarks text NOT NULL,
    PRIMARY KEY (id)
);

CREATE INDEX ON public.prescription
    (visit);


CREATE TABLE public.doctor (
    id integer NOT NULL,
    name text NOT NULL,
    surname text NOT NULL,
    room integer NOT NULL,
    phone_number text NOT NULL,
    PRIMARY KEY (id)
);


CREATE TABLE public.specialization (
    id integer NOT NULL,
    name text NOT NULL,
    PRIMARY KEY (id)
);


CREATE TABLE public.test (
    id integer NOT NULL,
    type text NOT NULL,
    execution_date timestamp with time zone NOT NULL,
    executive integer NOT NULL,
    remarks text NOT NULL,
    laboratory_room integer NOT NULL,
    visit integer NOT NULL,
    PRIMARY KEY (id)
);

CREATE INDEX ON public.test
    (executive);
CREATE INDEX ON public.test
    (laboratory_room);
CREATE INDEX ON public.test
    (visit);


CREATE TABLE public.laboratory (
    id integer NOT NULL,
    room integer NOT NULL,
    type text NOT NULL,
    PRIMARY KEY (id)
);


CREATE TABLE public.technician (
    id integer NOT NULL,
    name text NOT NULL,
    surname text NOT NULL,
    PRIMARY KEY (id)
);


CREATE TABLE public.doctor_specialization (
    id integer NOT NULL,
    doctorid integer NOT NULL,
    specialization integer NOT NULL,
    PRIMARY KEY (id)
);

CREATE INDEX ON public.doctor_specialization
    (doctorid);
CREATE INDEX ON public.doctor_specialization
    (specialization);


ALTER TABLE public.visit ADD CONSTRAINT FK_visit__doctor FOREIGN KEY (doctor) REFERENCES public.doctor(id);
ALTER TABLE public.visit ADD CONSTRAINT FK_visit__patient FOREIGN KEY (patient) REFERENCES public.patient(id);
ALTER TABLE public.prescription ADD CONSTRAINT FK_prescription__visit FOREIGN KEY (visit) REFERENCES public.visit(id);
ALTER TABLE public.test ADD CONSTRAINT FK_test__executive FOREIGN KEY (executive) REFERENCES public.technician(id);
ALTER TABLE public.test ADD CONSTRAINT FK_test__laboratory_room FOREIGN KEY (laboratory_room) REFERENCES public.laboratory(id);
ALTER TABLE public.test ADD CONSTRAINT FK_test__visit FOREIGN KEY (visit) REFERENCES public.visit(id);
ALTER TABLE public.doctor_specialization ADD CONSTRAINT FK_doctor_specialization__doctorid FOREIGN KEY (doctorid) REFERENCES public.doctor(id);
ALTER TABLE public.doctor_specialization ADD CONSTRAINT FK_doctor_specialization__specialization FOREIGN KEY (specialization) REFERENCES public.specialization(id);