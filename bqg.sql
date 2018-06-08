USE biquge;

-- auto-generated definition
CREATE TABLE novel_info
(
  id                 INT AUTO_INCREMENT
    PRIMARY KEY,
  novel_link         TEXT        NOT NULL,
  novel_id           VARCHAR(10) NOT NULL,
  novel_name         VARCHAR(15) NULL,
  novel_author       VARCHAR(10) NULL,
  novel_type         VARCHAR(10) NULL,
  novel_status       VARCHAR(10) NULL,
  novel_last_pubdate VARCHAR(10) NULL,
  novel_intro        TEXT        NULL,
  CONSTRAINT novel_info_id_uindex
  UNIQUE (id),
  CONSTRAINT novel_info_novel_id_uindex
  UNIQUE (novel_id)
);

-- auto-generated definition
CREATE TABLE chapter_info
(
  id              INT AUTO_INCREMENT
    PRIMARY KEY,
  chapter_id      INT         NOT NULL,
  novel_id        VARCHAR(10) NOT NULL,
  chapter_link    TEXT        NOT NULL,
  chapter_name    VARCHAR(50) NOT NULL,
  chapter_content LONGTEXT    NOT NULL,
  CONSTRAINT chapter_info_id_uindex
  UNIQUE (id),
  CONSTRAINT chapter_info_chapter_id_uindex
  UNIQUE (chapter_id)
);