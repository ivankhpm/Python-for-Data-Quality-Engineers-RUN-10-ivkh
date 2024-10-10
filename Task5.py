import datetime as dt


##Class for NewsFeed
class NewsFeed:
    def __init__(self):
        self.records = []

## to save all inputs
    def add_record(self, record):
        self.records.append(record)

## to add all inputs to file
    def publish_records(self):
        with open("news_feed.txt", "a") as file:
            for record in self.records:
                file.write(record.publish())



# Class for NEWS
class News:
    def __init__(self, text, city):
        self.text = text
        self.city = city
        self.date = dt.datetime.now().strftime('%d/%m/%Y %H.%M')

##publish news
    def publish(self):
        return f"----News -------------------------\n{self.text}\n{self.city}, {self.date}\n\n"



#Class for Private Ad
class PrivateAd:
    def __init__(self, text, expiration_date):
        self.text = text
        try:
            self.expiration_date = dt.datetime.strptime(expiration_date, '%d-%m-%Y').date()
        except ValueError:
            raise ValueError("Expiration Date should be in 'DD-MM-YYYY' format")
        self.days_left = self.calculate_days_left()

##Day left calculation
    def calculate_days_left(self):
        today = dt.datetime.now().date()
        ##expiration_date = dt.datetime.strptime(self.expiration_date, "%d-%m-%Y").date()
        return (self.expiration_date - today).days

##publish PrivateAd
    def publish(self):
        return f"----Private Ad -------------------\n{self.text}\nActual until: {self.expiration_date}, {self.days_left} days left\n\n"




#Class for custom class BirthNotification
class BirthNotification:
    def __init__(self, user_name, date_of_birth):
        self.user_name = user_name
        try:
            self.date_of_birth = dt.datetime.strptime(date_of_birth, '%d-%m-%Y').date()
        except ValueError:
            raise ValueError("Date of Birth should be in 'DD-MM-YYYY' format")
        self.date_of_birth = self.calculate_days_to_birthday()

    def calculate_days_to_birthday(self):
        today = dt.datetime.today().date()
        this_year_birthday = self.date_of_birth.replace(year=today.year)

        # in case bday already was in current year check next year for this person
        if this_year_birthday < today:
            this_year_birthday = this_year_birthday.replace(year=today.year + 1)

        return (this_year_birthday - today).days

##publish BirthNotification
    def publish(self):
        return f"----IT IS BIRTHDAY SOON! ---------\nUser {self.user_name} has bday in {self.date_of_birth} day(s)\n\n"




##### USAGE ######

def get_input():
    data_type = input("Select the data type (1 for News, 2 for Private Ad, 3 for Bday Notification): ")
    if data_type == "1":
        text = input("Enter the news text: ")
        city = input("Enter the city: ")
        return News(text, city)
    elif data_type == "2":
        text = input("Enter the ad text: ")
        expiration_date = input("Enter the expiration date (IMPORTANT!!! DD-MM-YYYY): ")
        return PrivateAd(text, expiration_date)
    elif data_type == "3":
        user = input("Enter the user name: ")
        date_of_birth = input("Enter the birthday date (IMPORTANT!!! DD-MM-YYYY): ")
        return BirthNotification(user, date_of_birth)
    else:
        print("Invalid data type")
        return None


def main():
    news_feed = NewsFeed()
    while True:
        record = get_input()
        if record:
            news_feed.add_record(record)
        cont = input("Do you want to add more records? (yes/no): ")
        if cont.lower() != "yes":
            break
    news_feed.publish_records()


if __name__ == "__main__":
    main()
