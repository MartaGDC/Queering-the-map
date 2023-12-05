USE queer_mysql;

-- Show the comments containing a certain word for a certain country
SELECT comment
FROM queer
WHERE country_name = "Spain" AND comment REGEXP '(?i)\\blove\\b';

-- Show the comments with the min or max snetiment of emotionality for a certain country
SELECT DISTINCT(comment)
FROM queer
WHERE sentiment = (
    SELECT MIN(sentiment)
    FROM queer
    WHERE country_name= 'Spain'
);