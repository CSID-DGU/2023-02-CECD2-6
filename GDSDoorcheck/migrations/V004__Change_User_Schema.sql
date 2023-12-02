ALTER TABLE UsersKeywords DROP CONSTRAINT userskeywords_user_id_fkey;

DROP TABLE UsersKeywords;

ALTER TABLE Users ADD topics varchar;
ALTER TABLE Users ADD keywords varchar;