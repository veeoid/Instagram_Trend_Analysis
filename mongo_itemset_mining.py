import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017')
db = client["project"]
posts_collection = db['Posts']
profiles_collection = db['Profiles']
locations_collection = db['Locations']

# Generate smaller dataset
temppost_pipline = [
    {"$limit": 2000000},
    {"$out": "tempPosts"}
]

result = posts_collection.aggregate(temppost_pipline)

tempposts_collection = db['tempPosts']

# Generate L1
l1_pipeline = [
    {"$group": {"_id": "$location_id", "freq": {"$sum": 1}}},
    {"$match": {"freq": {"$gt": 10}}},
    {"$project": {"_id": 0, "location_id": "$_id", "freq": 1}},
    {"$out": "L1"}
]
result_for_L1 = tempposts_collection.aggregate(l1_pipeline)
L1 = db["L1"]


def itemset_mining():

    # initialize variables for loop start with L1
    prev_level = "L1"
    level = 2
    num_frequent_itemsets = 1
    last_frequency = float('inf')
    iter = 2

    # Loop until there are no more items
    while num_frequent_itemsets > 0:
        # Generate pipeline for the current level
        current_level_collection = f"L{level}"
        pipeline = []

        # add pipeline stages for MongoDB aggregation
        for i in range(1, level + 1):
            pipeline.append({"$lookup": {
                "from": prev_level,
                "let": {f"location{i}": f"$location_id"},
                "pipeline": [
                    {"$match": {"$expr": {"$eq": [f"$$location{i}", f"$location_id"]}}},
                    {"$project": {"_id": 0}}
                ],
                "as": f"location{i}_match"
            }})

        pipeline.append(
            {"$addFields": {"match_count": {"$sum": [f"$location{i}_match.count" for i in range(1, level + 1)]}}})
        pipeline.append({"$match": {"match_count": {"$gte": 10}}})

        # execute pipeline
        current_level = db[current_level_collection]
        result = list(tempposts_collection.aggregate(pipeline))
        current_level.insert_many(result)

        # count the number of frequent itemsets
        num_frequent_itemsets = current_level.count_documents({})
        print(f"Number of frequent itemsets in {current_level_collection}: {num_frequent_itemsets}")

        # prepare for next iteration
        if num_frequent_itemsets != 0:
            prev_level = current_level_collection
            last_frequency = num_frequent_itemsets
            iter += 1
        else:
            pass

        # increment to the next level
        level += 1
    client.close()


def main():
    itemset_mining()


if __name__ == '__main__':
    main()
