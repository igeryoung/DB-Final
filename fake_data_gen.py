import random
from faker import Faker
import pandas as pd

# Initialize Faker
fake = Faker()

# Number of mock records
num_records = 5000

# Generate mock data
data = []
for i in range(num_records):
    artist = {
        "artist_id": i+12,
        "artist_name": fake.name(),
        "total_played": random.randint(0, 1000000),
        "bio": fake.text(max_nb_chars=200),
        "email": fake.email()+str(i),
        "password": fake.password(length=15),
        "debut_date": fake.date_between(start_date='-30y', end_date='today'),
        "cash": random.randint(0, 100000),
        "follow_num": random.randint(0, 1000000)
    }
    data.append(artist)

# Convert to DataFrame
df = pd.DataFrame(data)

# Save to CSV without headers
df.to_csv('mock_artist_data.csv', index=False, header=False)

print("Mock data generated and saved to 'mock_artist_data.csv' without headers.")
