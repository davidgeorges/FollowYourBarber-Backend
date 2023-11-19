from django.contrib.auth.hashers import make_password, check_password

class PasswordManager :

    __password_error = " "

    # Hash the password
    def create_hash_password(self,password) :
        return make_password(password)

    # Check if two password match
    def verify_password(self,plain_password, hashed_password) :
        return check_password(plain_password, hashed_password)

    def set_password_error(self, error_message) :
        self.__password_error = error_message

    def get_password_error(self) :
        return self.__password_error

password_manager = PasswordManager()
