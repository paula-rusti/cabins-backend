from faker import Faker
import itertools

fake = Faker()


# Define a custom function to generate increasing ids
def generate_ids(prefix, start=1):
    for i in itertools.count(start):
        yield f"{prefix}{i}"


# Generate sample user data with increasing ids
users = []
for id in generate_ids('user_', start=1000):
    user = {
        'id': id,
        'username': fake.user_name(),
        'email': fake.email(),
        'password': fake.password(),
    }
    users.append(user)

# Generate sample cabin data with increasing ids
cabins = []
for id in generate_ids('cabin_', start=2000):
    cabin = {
        'id': id,
        'name': fake.company(),
        'description': fake.text(),
        'price_per_night': fake.pydecimal(left_digits=2, right_digits=2, positive=True),
    }
    cabins.append(cabin)

# Generate sample booking data with increasing ids
bookings = []
for user_id in [user['id'] for user in users]:
    for cabin_id in [cabin['id'] for cabin in cabins]:
        booking = {
            'id': next(generate_ids('booking_', start=3000)),
            'user_id': user_id,
            'cabin_id': cabin_id,
            'check_in_date': fake.date_between(start_date='-1y', end_date='+1y'),
            'check_out_date': fake.date_between(start_date='-1y', end_date='+1y'),
        }
        bookings.append(booking)

# Generate sample review data with increasing ids
reviews = []
for booking_id in [booking['id'] for booking in bookings]:
    review = {
        'id': next(generate_ids('review_', start=4000)),
        'booking_id': booking_id,
        'rating': fake.random_int(min=1, max=5),
        'comment': fake.text(),
    }
    reviews.append(review)
