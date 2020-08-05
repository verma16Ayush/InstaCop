import instaloader


def login_self(bot):
    username = input("Enter your username:\n$> ")
    password = input("Enter your password:\n$> ")
    bot.login(username, password)
    profile = instaloader.Profile.from_username(bot.context, username)
    return profile


def get_follow_info(profile):
    followers = [x for x in profile.get_followers()]
    followings = [x for x in profile.get_followees()]
    return followers, followings


def write_to_file(profile_list, file):
    for user_profile in profile_list:
        username = user_profile.username
        name = user_profile.full_name
        user_follower = user_profile.followers
        user_following = user_profile.followees
        private_account = user_profile.is_private
        verified = user_profile.is_verified
        bio = user_profile.biography
        file.write(
            (':\n\t'
             + "Username: {}"
             + '\n\t'
             + "followers: {}"
             + '\n\t'
             + "following: {}"
             + '\n\t'
             + "private account: {}"
             + '\n\t'
             + "verified: {}").format(
                username, user_follower, user_following, private_account, verified
            )
        )
        file.write("\n\n")


def find_desperate_influencers(followers, followings, mode='reasonable'):
    desparados = list()
    for following in followings:
        filter_type = {'strict': True, 'reasonable': following.is_verified, 'moderate': following.followers > 10000,
                       'kind': following.followers > 1000}
        try:
            followers.index(following)
        except ValueError as e:
            if filter_type:
                print("{} does not follow you back".format(following.username))
                desparados.append(following)
                continue

    return desparados


def drive():
    il = instaloader.Instaloader()
    profile = login_self(il)
    followers, followings = get_follow_info(profile)
    sav_in_file = input("Do you want to save Follower/Following details in a file?(y/n)\n$> ").casefold()
    if sav_in_file == 'y':
        followers_file = open("followers.txt", '+a')
        write_to_file(followers, followers_file)
        followings_file = open("following.txt", '+a')
        write_to_file(followings, followings_file)
        followers_file.close()
        followings_file.close()

    desperados = find_desperate_influencers(followers, followings, mode='strict')
    sav_in_file = input("\n\nDo you want to save these desperate influencers details to a file(y/n)\n$>").casefold()
    if sav_in_file == 'y':
        desperados_file = open("jerks.txt", '+a')
        write_to_file(desperados, desperados_file)
        desperados_file.close()

# if __name__ == '__main__()':


drive()