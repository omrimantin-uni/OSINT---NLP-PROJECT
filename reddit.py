import praw

reddit = praw.Reddit(
    client_id='cj5WPnCz0zy3GkqjtVITfg',
    client_secret='hmFUQ8rmn13LD9An-AzzhMB4GtpwKA',
    user_agent='Project'
)

subreddit = reddit.subreddit("Cars")
cnt = 0
for submission in subreddit.top(limit=10000):
    cnt += 1
    if submission.is_self:
        print(submission.selftext)
print(cnt)
