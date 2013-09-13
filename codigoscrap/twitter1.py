import twitter 

#enter your consumer key,secret and access token secret,key in below function as parameters 

api=twitter.Api(consumer_key='MkYf8YeLhcMb1i96wyCK9A',consumer_secret='gE3xMrhlpnHHZAAN1v0SDzI6KsTcep1l35VFvlYaOc',access_token_key='14938655-jazKpLgtqywDVg8Yp3AEhjAwIcmIwUvG8GPdxhk7n',access_token_secret='d9WrNHmGK7IZsEkoPkcOhpbpJMKyLDgfpxKAjgbl7Y') 

#now using PostUpdate method of the api we can use to post an update on twitter account 

users = api.GetFriends()
for u in users:
	print u.name
#print [u.name for u in users]
#status = api.PostUpdate('programmed...') 
#print status.text 