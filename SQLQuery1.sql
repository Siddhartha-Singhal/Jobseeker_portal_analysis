/*
                 INSIGHTS GENERATION
*/
--------------------------------------------------------------------------
-- What percentage of users complete profile submission?
select count(case when prf_submitted = 'Y' then 1 end) as Completed_Profile,
	cast(100.0 *
		(sum(case when prf_submitted = 'Y' then 1.0 else 0 end) / count(*))
		as decimal(5, 2))
		as percent_complete_profile_submission
from Preprocessed_DataJobSeeker;
/*
Result: 44.26%, 44261 users
*/

-----------------------------------------------------------------------------

-- How many users complete registration within the same day?
select count(*) as Users_completed_registration
from Preprocessed_DataJobSeeker
where clean_insertdate = clean_final_submittion_date;
/*
Result: 46819 users completed their registration within the same day
*/

----------------------------------------------------------------------------
/**/
-- What is the most used password sending mode?
select pwd_sent_mode, count(*) as most_used_pwd_sent_mode
from Preprocessed_DataJobSeeker
group by pwd_sent_mode
order by most_used_pwd_sent_mode desc;
/*
Result: Most used passwords are the ones that are provided by auto-suggest for the user
*/

------------------------------------------------------------------------------

-- What % of users go through all stages: register → login → submit form -> verified?
select	count(*) as User_completed_all_stages
from Preprocessed_DataJobSeeker
where clean_insertdate is not null
	  and has_logged_in is not null
	  and prf_submitted is not null
	  and is_verified = 1;

select	cast(100.0 *
			 sum(case when clean_insertdate is not null and has_logged_in is not null and prf_submitted is not null and is_verified = 1 then 1.0 else 0 end) /
			 count(*)
			 as decimal(5, 2)) 
		     as User_completed_all_stages
from Preprocessed_DataJobSeeker;
/*
Result: 70.43% of users go through all stages
The result is based on the fact if we cosider that 1 means the users has verified his phoneNo
*/

-----------------------------------------------------------------------------
/**/
-- What are the most common IP addresses?
select 
       js_request_ip_address, count(*) as ip_address_used
from Preprocessed_DataJobSeeker
group by js_request_ip_address
order by ip_address_used desc;
/*
Result: 110.172.191.34, 148.172.191.34, 182.71.124.30, 122.15.44.21 and 221.135.243.110
*/

-------------------------------------------------------------------------------------
/**/
-- Check for repeated or suspicious email activity in our job seeker database?
select sum(case when js_email is null then 1 else 0 end)
from Preprocessed_DataJobSeeker

SELECT
    js_email,
    COUNT(*) AS total_records,
    COUNT(DISTINCT js_unique_id) AS distinct_users
FROM Preprocessed_DataJobSeeker
WHERE js_email IS NOT NULL
GROUP BY js_email
HAVING COUNT(DISTINCT js_unique_id) = 1
ORDER BY distinct_users DESC, total_records DESC;
/*
Result: - Over 3,000 duplicate email entries were found in our 100,000-row dataset,
        indicating significant data redundancy. This suggests possible bot activity, 
		test accounts, or user re-registrations
		- Over 10,000 emails are missing as well
        - 49,000 unique emails with unique emails
        -41,000 duplicate usage
*/

---------------------------------------------------------------------------------------
/**/
select js_phoneNo, count(*) as records
from Preprocessed_DataJobSeeker
group by js_phoneNo
order by records desc

select sum(case when js_phoneNo is null then 1 else 0 end)
from Preprocessed_DataJobSeeker

SELECT TOP 30
    js_phoneNo,
    COUNT(*) AS total_records,
    COUNT(DISTINCT js_unique_id) AS distinct_users
FROM Preprocessed_DataJobSeeker
WHERE js_phoneNo IS NOT NULL
GROUP BY js_phoneNo
HAVING COUNT(DISTINCT js_unique_id) > 1
ORDER BY distinct_users DESC, total_records DESC;
/* 
Result - There are 20 records where same phone no is used by 2 different people
*/

--------------------------------------------------------
/**/
select js_unique_id, count(distinct js_name) as name, count(distinct js_email) as email, count(distinct js_phoneNo) as phoneNo
from Preprocessed_DataJobSeeker
group by js_unique_id
/*
Result - There are certain issues with the email column and it should not be used for analysis
*/

------------------------------------------------------------

select COUNT(*) as noOfIndividualsVerifiedPhoneNo
from Preprocessed_DataJobSeeker
where is_verified = 1
/*
Result - We can conclude that 6394 (1) users have their phoneNo verified and 93606 (0) users have not verified their phoneNo
*/

------------------------------------------------------------
/**/
select is_verified, satyapan_done, count(*)
from Preprocessed_DataJobSeeker
group by is_verified, satyapan_done

------------------------------------------------------------------

SELECT 
    cast(round(1.0 * COUNT(DISTINCT js_unique_id) / COUNT(DISTINCT clean_request_date), 0) as int) AS avg_users_per_day
FROM Preprocessed_DataJobSeeker
WHERE clean_request_date IS NOT NULL;

-------------------------------------------------------------------------

-- Step 1: Get distinct user count and total records per email
WITH EmailUserCounts AS (
    SELECT 
        js_email,
        COUNT(*) AS total_records,
        COUNT(DISTINCT js_unique_id) AS distinct_users
    FROM Preprocessed_DataJobSeeker
    WHERE js_email IS NOT NULL
    GROUP BY js_email
)

-- Step 2: Bin emails and summarize
SELECT 
    distinct_user_bin,
    COUNT(*) AS total_emails_in_bin,
    SUM(total_records) AS total_records_in_bin
FROM (
    SELECT 
        js_email,
        total_records,
        distinct_users,
        CASE 
            WHEN distinct_users > 1000 THEN 'More than 1000'
            WHEN distinct_users BETWEEN 500 AND 1000 THEN '500 to 1000'
            WHEN distinct_users BETWEEN 100 AND 499 THEN '100 to 499'
            WHEN distinct_users BETWEEN 2 AND 99 THEN '2 to 99'
            ELSE 'Exactly 1'
        END AS distinct_user_bin
    FROM EmailUserCounts
) AS BinnedData
GROUP BY distinct_user_bin
ORDER BY 
    CASE 
        WHEN distinct_user_bin = 'More than 1000' THEN 1
        WHEN distinct_user_bin = '500 to 1000' THEN 2
        WHEN distinct_user_bin = '100 to 499' THEN 3
        ELSE 4
    END;

------------------------------------------------------

SELECT 
    COUNT(DISTINCT js_email) AS verified_email_count
FROM Preprocessed_DataJobSeeker
WHERE js_email IS NOT NULL
  AND is_verified = 1;

SELECT 
    COUNT(*) AS total_verified
FROM Preprocessed_DataJobSeeker
WHERE is_verified = 1;


select count(*) as Total_Registrations
from Preprocessed_DataJobSeeker

select count(*) as Users_completed_registration
from Preprocessed_DataJobSeeker
where clean_insertdate <> clean_final_submittion_date;
