-- 03_spark_sql_analysis.sql
-- Milestone 4: Spark SQL Analytical Queries
-- Author: Jainil Modi

-- Note: Assumes DataFrame is registered as a temporary view named 'netflix_cleaned'

-- 1. Genre Distribution (Top 12)
SELECT genre_primary, COUNT(*) as title_count 
FROM netflix_cleaned 
GROUP BY genre_primary 
ORDER BY title_count DESC 
LIMIT 12;

-- 2. Year-over-Year Content Growth (2015-2021)
SELECT year_added, type, COUNT(*) as titles_added 
FROM netflix_cleaned 
WHERE year_added BETWEEN 2015 AND 2021 
GROUP BY year_added, type 
ORDER BY year_added ASC;

-- 3. Geographic Breakdown (Top 12 Countries, excluding 'Unknown')
SELECT country_primary, COUNT(*) as title_count 
FROM netflix_cleaned 
WHERE country_primary != 'Unknown' 
GROUP BY country_primary 
ORDER BY title_count DESC 
LIMIT 12;

-- 4. Rating Distribution (Movies vs TV Shows)
SELECT rating, type, COUNT(*) as count 
FROM netflix_cleaned 
GROUP BY rating, type 
ORDER BY count DESC;

-- 5. Content Type Split
SELECT type, COUNT(*) as total, ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM netflix_cleaned), 1) as percentage 
FROM netflix_cleaned 
GROUP BY type;

-- 6. Genre-Year Cross-Tabulation (2016-2021)
SELECT genre_primary, year_added, COUNT(*) as titles_added
FROM netflix_cleaned
WHERE year_added BETWEEN 2016 AND 2021
GROUP BY genre_primary, year_added
ORDER BY genre_primary, year_added;
