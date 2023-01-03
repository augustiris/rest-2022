
--BOOK 1
DO $FN$
BEGIN
    FOR counter IN 1..42 LOOP
        EXECUTE $$ INSERT INTO library.book_copies(book_id, location_id)
            VALUES (1, 1) $$
            USING counter;
    END LOOP;
END;
$FN$;

DO $FN$
BEGIN
  FOR counter IN 1..2 LOOP
    EXECUTE $$ INSERT INTO library.book_copies(book_id, location_id)
        VALUES (1, 2); $$
        USING counter;
  END LOOP;
END;
$FN$;

--BOOK 2
DO $FN$
BEGIN
  FOR counter IN 1..5 LOOP
    EXECUTE $$ INSERT INTO library.book_copies(book_id, location_id)
        VALUES (2, 4); $$
        USING counter;
  END LOOP;
END;
$FN$;

--BOOK 3
DO $FN$
BEGIN
  FOR counter IN 1..2 LOOP
    EXECUTE $$ INSERT INTO library.book_copies(book_id, location_id)
        VALUES (3, 1); $$
        USING counter;
  END LOOP;
END;
$FN$;

DO $FN$
BEGIN
  FOR counter IN 1..7 LOOP
    EXECUTE $$ INSERT INTO library.book_copies(book_id, location_id)
        VALUES (3, 2); $$
        USING counter;
  END LOOP;
END;
$FN$;

DO $FN$
BEGIN
  FOR counter IN 1..3 LOOP
    EXECUTE $$ INSERT INTO library.book_copies(book_id, location_id)
        VALUES (3, 3); $$
        USING counter;
  END LOOP;
END;
$FN$;

--BOOK 4
DO $FN$
BEGIN
  FOR counter IN 1..7 LOOP
    EXECUTE $$ INSERT INTO library.book_copies(book_id, location_id)
        VALUES (4, 4); $$
        USING counter;
  END LOOP;
END;
$FN$;

--BOOK 5
DO $FN$
BEGIN
  FOR counter IN 1..3 LOOP
    EXECUTE $$ INSERT INTO library.book_copies(book_id, location_id)
        VALUES (5, 3); $$
        USING counter;
  END LOOP;
END;
$FN$;

--BOOK 1
DO $FN$
BEGIN
    FOR counter IN 1..6 LOOP
        EXECUTE $$ INSERT INTO library.book_copies(book_id, location_id)
            VALUES (6, 2) $$
            USING counter;
    END LOOP;
END;
$FN$;