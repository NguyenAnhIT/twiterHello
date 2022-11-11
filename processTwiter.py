import json
import random

import requests



class ProcessTwiter(object):
    def __init__(self):
        pass




    def processLikeTwiter(self,cookies,twiterID):
        cookie = cookies.split('||')[0]
        bearer = cookies.split('||')[1]
        csrfToken = cookies.split('||')[2].strip('\n')
        url = "https://twitter.com/i/api/graphql/lI07N6Otwv1PhnEgXILM7A/FavoriteTweet"

        payload = {"variables": {"tweet_id": f"{twiterID}"}}
        headers = {
            "cookie": cookie,
            "authority": "twitter.com",
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "authorization": bearer,
            "content-type": "application/json",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
            "x-csrf-token": csrfToken,
            "x-twitter-active-user": "yes",
            "x-twitter-auth-type": "OAuth2Session",
            "x-twitter-client-language": "en"
        }

        response = requests.request("POST", url, json=payload, headers=headers)
        print(response.text)


    def processReweetTwiter(self,cookies,twiterID):
        cookie = cookies.split('||')[0]
        bearer = cookies.split('||')[1]
        csrfToken = cookies.split('||')[2]
        url = "https://twitter.com/i/api/graphql/ojPdsZsimiJrUGLR1sjUtA/CreateRetweet"

        payload = {"variables": {
            "tweet_id": twiterID,
            "dark_request": False
        }}
        headers = {
            "cookie": cookie,
            "authority": "twitter.com",
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "authorization": bearer,
            "content-type": "application/json",
            "origin": "https://twitter.com",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
            "x-csrf-token": csrfToken,
            "x-twitter-active-user": "yes",
            "x-twitter-auth-type": "OAuth2Session",
            "x-twitter-client-language": "en"
        }

        response = requests.request("POST", url, json=payload, headers=headers)
        print(response.text)

    def processGetFollowingTwiter(self,cookies,countFriends,name):
        cookie = cookies.split('||')[0]
        bearer = cookies.split('||')[1]
        csrfToken = cookies.split('||')[2]
        meUID = self.processConvertNameToUID(name=name)
        print(meUID)

        url = "https://twitter.com/i/api/graphql/9rGM7YNDYuiqd0Cb0ZwLJw/Following"

        querystring = {
            "variables": "{\"userId\":\"%s\",\"count\":50,\"includePromotedContent\":false,\"withSuperFollowsUserFields\":true,\"withDownvotePerspective\":false,\"withReactionsMetadata\":false,\"withReactionsPerspective\":false,\"withSuperFollowsTweetFields\":true}"%(meUID),
            "features": "{\"responsive_web_twitter_blue_verified_badge_is_enabled\":false,\"verified_phone_label_enabled\":false,\"responsive_web_graphql_timeline_navigation_enabled\":true,\"unified_cards_ad_metadata_container_dynamic_card_content_query_enabled\":true,\"tweetypie_unmention_optimization_enabled\":true,\"responsive_web_uc_gql_enabled\":true,\"vibe_api_enabled\":true,\"responsive_web_edit_tweet_api_enabled\":true,\"graphql_is_translatable_rweb_tweet_is_translatable_enabled\":true,\"standardized_nudges_misinfo\":true,\"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled\":false,\"interactive_text_enabled\":true,\"responsive_web_text_conversations_enabled\":false,\"responsive_web_enhance_cards_enabled\":true}"}
        headers = {
            "cookie": cookie,
            "authority": "twitter.com",
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "authorization": bearer,
            "content-type": "application/json",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
            "x-csrf-token": csrfToken,
            "x-twitter-active-user": "yes",
            "x-twitter-auth-type": "OAuth2Session",
            "x-twitter-client-language": "en"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        data = json.loads(response.text)
        datas = data['data']['user']['result']['timeline']['timeline']['instructions'][3]['entries']
        listFollowing = []
        try:
            for item in datas:
                listFollowing.append(item['content']['itemContent']['user_results']['result']['legacy']['screen_name'])
        except:
            pass
        rdListFollowing = []
        while True:
            item = listFollowing[random.randint(0, len(listFollowing) - 1)]
            if item not in rdListFollowing:
                rdListFollowing.append(item)

            if len(rdListFollowing) > int(countFriends)-1:
                break
        print(rdListFollowing)
        return rdListFollowing



    def processCommentTwiter(self,cookies,twiterID,countFriends):
        cookie = cookies.split('||')[0]
        bearer = cookies.split('||')[1]
        csrfToken = cookies.split('||')[2]
        name = cookies.split('||')[3]

        listFollowing = self.processGetFollowingTwiter(cookies,countFriends,name=name)
        text = ''
        for item in listFollowing:
            text += f'@{item} '


        url = "https://twitter.com/i/api/graphql/znCBT5T-VuJFVKmKvj2RVQ/CreateTweet"

        payload = {
            "variables": {
                "tweet_text": text,
                "reply": {
                    "in_reply_to_tweet_id": twiterID,
                    "exclude_reply_user_ids": []
                },
                "media": {
                    "media_entities": [],
                    "possibly_sensitive": False
                },
                "withDownvotePerspective": False,
                "withReactionsMetadata": False,
                "withReactionsPerspective": False,
                "withSuperFollowsTweetFields": True,
                "withSuperFollowsUserFields": True,
                "semantic_annotation_ids": [],
                "dark_request": False
            },
            "features": {
                "tweetypie_unmention_optimization_enabled": True,
                "responsive_web_uc_gql_enabled": True,
                "vibe_api_enabled": True,
                "responsive_web_edit_tweet_api_enabled": True,
                "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                "interactive_text_enabled": True,
                "responsive_web_text_conversations_enabled": False,
                "responsive_web_twitter_blue_verified_badge_is_enabled": False,
                "verified_phone_label_enabled": False,
                "standardized_nudges_misinfo": True,
                "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": False,
                "responsive_web_graphql_timeline_navigation_enabled": True,
                "responsive_web_enhance_cards_enabled": True
            },
            "queryId": "znCBT5T-VuJFVKmKvj2RVQ"
        }
        headers = {
            "cookie": cookie,
            "authority": "twitter.com",
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "authorization": bearer,
            "content-type": "application/json",
            "origin": "https://twitter.com",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
            "x-csrf-token": csrfToken,
            "x-twitter-active-user": "yes",
            "x-twitter-auth-type": "OAuth2Session",
            "x-twitter-client-language": "en"
        }

        response = requests.request("POST", url, json=payload, headers=headers)

        print(response.text)

    def processGetUIDTwiter(self,screen_name):
        url = "https://tweeterid.com/ajax.php"

        payload = f"input=%40{screen_name}"
        headers = {
            "authority": "tweeterid.com",
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://tweeterid.com",
            "referer": "https://tweeterid.com/",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }

        response = requests.request("POST", url, data=payload, headers=headers)
        print(response.text)
        return response.text.strip('\n')


    def processFollowTwiter(self,cookies,screen_name):
        cookie = cookies.split('||')[0]
        bearer = cookies.split('||')[1]
        csrfToken = cookies.split('||')[2]
        uid = self.processGetUIDTwiter(screen_name.strip('@'))
        print(uid)
        url = "https://twitter.com/i/api/1.1/friendships/create.json"

        payload = f"include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&include_ext_has_nft_avatar=1&skip_status=1&user_id={uid}"
        headers = {
            "cookie":cookie ,
            "authority": "twitter.com",
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "authorization": bearer,
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://twitter.com",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
            "x-csrf-token": csrfToken,
            "x-twitter-active-user": "yes",
            "x-twitter-auth-type": "OAuth2Session",
            "x-twitter-client-language": "en"
        }

        response = requests.request("POST", url, data=payload, headers=headers)

        print(response.text)



    def processConvertNameToUID(self,name):
        url = "https://twitter.com/i/api/graphql/ofhhyYpXnuekADBgD0KKtw/ProfileSpotlightsQuery"
        payload = {
            "variables": {"screen_name": f"{name}"}
        }
        headers = {
            "cookie": """guest_id_marketing=v1%3A166118860951229126; guest_id_ads=v1%3A166118860951229126; personalization_id="v1_3pST+R9K9rzUflj0/4zzWg=="; guest_id=v1%3A166118860951229126; _ga=GA1.2.378656298.1661188611; _gid=GA1.2.218239602.1667921699; external_referer=8e8t2xd8A2w%3D|0|F8C7rVpldvGNltGxuH%2ByoRY%2FzjrflHIZH061f%2B5OiIwP17ZTz34ZGg%3D%3D; g_state={"i_l":0}; kdt=B7IwVDir2buH3jC9pKuGHkwjVqtJ9YJppLRgJMfC; auth_token=d714eddacc12848b0e3712d06bb988316fe1f7ae; ct0=493680f3c7c0e3b00c6d0bfd8be31668b9033466db440dc19d92c2ae463b1570bc218a5ff81416c594bab12d9ce66de74311d198857a19dcd6c7d480d2db0540991ec445151ef89054ac75cb6ed5d082; twid=u%3D1590005007201742849""",
            "authority": "twitter.com",
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
            "content-type": "application/json",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
            "x-csrf-token": "493680f3c7c0e3b00c6d0bfd8be31668b9033466db440dc19d92c2ae463b1570bc218a5ff81416c594bab12d9ce66de74311d198857a19dcd6c7d480d2db0540991ec445151ef89054ac75cb6ed5d082",
            "x-twitter-active-user": "yes",
            "x-twitter-auth-type": "OAuth2Session",
            "x-twitter-client-language": "en"
        }

        response = requests.request("GET", url, headers=headers, json=payload)
        data = json.loads(response.text)
        rest_id = data['data']['user_result_by_screen_name']['result']['rest_id']
        return rest_id

# guest_id_marketing=v1%3A166118860951229126; guest_id_ads=v1%3A166118860951229126; personalization_id="v1_3pST+R9K9rzUflj0/4zzWg=="; guest_id=v1%3A166118860951229126; _ga=GA1.2.378656298.1661188611; _gid=GA1.2.218239602.1667921699; external_referer=8e8t2xd8A2w%3D|0|F8C7rVpldvGNltGxuH%2ByoRY%2FzjrflHIZH061f%2B5OiIwP17ZTz34ZGg%3D%3D; g_state={"i_l":0}; kdt=B7IwVDir2buH3jC9pKuGHkwjVqtJ9YJppLRgJMfC; auth_token=d714eddacc12848b0e3712d06bb988316fe1f7ae; ct0=493680f3c7c0e3b00c6d0bfd8be31668b9033466db440dc19d92c2ae463b1570bc218a5ff81416c594bab12d9ce66de74311d198857a19dcd6c7d480d2db0540991ec445151ef89054ac75cb6ed5d082; twid=u%3D1590005007201742849