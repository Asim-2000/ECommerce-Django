from E_Commerce.models.User import User


class Customer(User):

    def create_Customer(self, firstname, lastname, email, password, contact_number):
        self.firstname = self.set_name(firstname)
        self.lastname = self.set_name(lastname)
        self.email = email
        self.password = password
        self.username = self.generate_username(email)
        self.set_contact_number(contact_number)
        self.verified = False
        self.encrypted_id = self.get_random_string()
        self.save()
