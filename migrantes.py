from csv import writer
from searchtweets import ResultStream, gen_rule_payload, load_credentials, collect_results
from tweet_parser.getter_methods.tweet_geo import get_profile_location

## Authentication, search_tweets_fullarchive_dev or search_tweets_30_day_dev
premium_search_args = load_credentials(filename="./twitter_keys.yaml",
                 yaml_key="search_tweets_fullarchive_dev",
                 env_overwrite=False)

country_code = "mx"
out_file = "migrantes.csv"

rule = gen_rule_payload("(migrantes) place_country:"+country_code,
    results_per_call=100,
    from_date="2016-06-01",
    to_date="2017-06-01") # testing with a sandbox account

print(rule)

def fetch_tweets():

    tweets = collect_results(rule,
                         max_results=10,
                         result_stream_args=premium_search_args)

    with open(out_file, 'w') as out:
        csv = writer(out)

        row = ("user", "city/state", "country", "text", "created_at")
        csv.writerow(row)

        for tweet in tweets:
            place_name = ""

            place = tweet.get("place")
            if place != None:
                place_name = place["full_name"]
            
            print(tweet)
            row = (
                tweet.get("screen_name"),
                place_name,
                country_code,
                tweet.all_text,
                tweet.created_at_string ##tweet.created_at_datetime.strftime("%Y-%m-%d|%H:%M:%S")
            )
            
            values = [(value.encode('unicode') if hasattr(value, 'encode') else value) for value in row]
            csv.writerow(values)
    out.close()


fetch_tweets()

##print(tweets[0].get("place")["name"])
##tweet.retweeted_tweet
##print(len(tweets))