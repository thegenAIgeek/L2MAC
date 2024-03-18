from dataclasses import dataclass, field

@dataclass
class User:
	id: str
	email: str
	password: str
	profile_picture: str = field(default=None)
	status_message: str = field(default=None)
	blocked_contacts: list = field(default_factory=list)

	def update_profile(self, data):
		self.profile_picture = data.get('profile_picture', self.profile_picture)
		self.status_message = data.get('status_message', self.status_message)

	def block_contact(self, contact_id):
		self.blocked_contacts.append(contact_id)

	def to_dict(self):
		return {
			'id': self.id,
			'email': self.email,
			'profile_picture': self.profile_picture,
			'status_message': self.status_message,
			'blocked_contacts': self.blocked_contacts
		}