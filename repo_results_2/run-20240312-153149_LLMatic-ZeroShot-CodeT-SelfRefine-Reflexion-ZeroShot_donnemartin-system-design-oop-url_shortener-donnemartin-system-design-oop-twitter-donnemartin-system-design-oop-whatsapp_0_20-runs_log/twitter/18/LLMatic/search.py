class Search:
	def __init__(self, users, posts):
		self.users = users
		self.posts = posts

	def search_users(self, keyword):
		return [user for user in self.users if keyword in user.username]

	def search_posts(self, keyword):
		return [post for post in self.posts if keyword in post.content]

	def filter_posts(self, filter_type, filter_value):
		if filter_type == 'hashtag':
			return [post for post in self.posts if f'#{filter_value}' in post.content]
		elif filter_type == 'user_mention':
			return [post for post in self.posts if f'@{filter_value}' in post.content]
		elif filter_type == 'trending_topic':
			return [post for post in self.posts if filter_value in post.content]
		else:
			return 'Invalid filter type'