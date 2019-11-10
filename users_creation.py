import names
import pandas as pd

user_ids = []
chunksize = 10 ** 6

for chunk in pd.read_csv("data/ratings.csv", chunksize=chunksize):
    user_ids.extend(chunk.userId.unique())

def generate_users(ratings_dataset = user_ids):
    userIds = list(set(user_ids))
    randomNames = [names.get_first_name() for i in range(len(userIds))]
    user_ids_pd = pd.DataFrame(randomNames, index = userIds, columns = ["userNames"])
    user_ids_pd["password"] = "12345"
    user_ids_pd.to_csv("data/users.csv")

if __name__ == "__main__":
    generate_users()