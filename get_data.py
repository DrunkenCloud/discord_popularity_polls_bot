import requests
import time
import csv

url = 'https://graphql.anilist.co'

queries = [
    {
        'query': '''
        query ($page: Int, $perPage: Int) {
            Page(page: $page, perPage: $perPage) {
                media(type: ANIME, sort: TRENDING_DESC) {
                    id,
                    favourites
                }
            }
        }
        ''',
        'total': 250,
        'type': 'Anime Trending'
    },
    {
        'query': '''
        query ($page: Int, $perPage: Int) {
            Page(page: $page, perPage: $perPage) {
                media(type: ANIME, sort: POPULARITY_DESC) {
                    id,
                    favourites
                }
            }
        }
        ''',
        'total': 500,
        'type': 'Anime Popularity'
    },
    {
        'query': '''
        query ($page: Int, $perPage: Int) {
            Page(page: $page, perPage: $perPage) {
                media(format: TV, sort: POPULARITY_DESC) {
                    id,
                    favourites
                }
            }
        }
        ''',
        'total': 500,
        'type': 'Anime Top TV'
    },
    {
        'query': '''
        query ($page: Int, $perPage: Int) {
            Page(page: $page, perPage: $perPage) {
                media(type: MANGA, sort: TRENDING_DESC) {
                    id,
                    favourites
                }
            }
        }
        ''',
        'total': 100,
        'type': 'Manga Trending'
    },
    {
        'query': '''
        query ($page: Int, $perPage: Int) {
            Page(page: $page, perPage: $perPage) {
                media(type: MANGA, sort: POPULARITY_DESC) {
                    id,
                    favourites
                }
            }
        }
        ''',
        'total': 250,
        'type': 'Manga Popularity'
    },
    {
        'query': '''
        query ($page: Int, $perPage: Int) {
            Page(page: $page, perPage: $perPage) {
                media(source: WEB_NOVEL, sort: POPULARITY_DESC) {
                    id,
                    favourites
                }
            }
        }
        ''',
        'total': 50,
        'type': 'Web Novel'
    },
    {
        'query': '''
        query ($page: Int, $perPage: Int) {
            Page(page: $page, perPage: $perPage) {
                media(source: VIDEO_GAME, sort: POPULARITY_DESC) {
                    id,
                    favourites
                }
            }
        }
        ''',
        'total': 30,
        'type': 'Video Game'
    }
]

def fetch_media(query, total, type_, media_ids):
    variables = {'page': 1, 'perPage': 50}
    pages = (total // variables['perPage'])
    if total < variables['perPage']:
        pages += 1
        variables['perPage'] = total
    
    for page in range(1, pages + 1):
        variables['page'] = page
        print(f"Page no. {page} for {type_}")
        while True:
            response = requests.post(url, json={'query': query, 'variables': variables})
            if response.status_code == 200:
                data = response.json()
                for i in data['data']['Page']['media']:
                    media_ids[i['id']] = i['favourites']
                break
            elif response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", 60))
                print(f"Rate limit exceeded. Retrying after {retry_after} seconds...")
                time.sleep(retry_after +    10)
            else:
                print(f"Failed to fetch data: {response.status_code}")
                print(response.text)
                break

def get_characters(media_id, favs_count, males, females, specials):
    query = '''
            query($med_id: Int, $count: Int) {
                Media(id: $med_id) {
                    title{
                        romaji
                    }
                    startDate {
                        year
                    }
                    characters(page: 1, perPage: $count, sort: [FAVOURITES_DESC]){
                        edges {
                            node {
                                id
                                name {
                                    full
                                }
                                image{
                                    large
                                }
                                favourites
                                gender
                            }
                        }
                    }
                }
            }
            '''
    char_count = 1
    while(favs_count != 0):
        char_count += 5
        favs_count = favs_count//10

    variables = {'med_id': media_id, 'count': char_count}
    while True:
            response = requests.post(url, json={'query': query, 'variables': variables})
            if response.status_code == 200:
                data = response.json()
                min_favs = 1000
                if(data['data']['Media']['startDate']['year'] and data['data']['Media']['startDate']['year'] > 2022):
                    min_favs = 100
                for i in data['data']['Media']['characters']['edges']:
                    if(i['node']['favourites'] < min_favs):
                        continue
                    if(i['node']['gender'] == "Male"):
                        males[i['node']['id']] = [i['node']['name']['full'], i['node']['favourites'], data['data']['Media']['title']['romaji'], i['node']['image']['large']]
                    elif(i['node']['gender'] == "Female"):
                        females[i['node']['id']] = [i['node']['name']['full'], i['node']['favourites'], data['data']['Media']['title']['romaji'], i['node']['image']['large']]
                    else:
                        specials[i['node']['id']] = [i['node']['name']['full'], i['node']['favourites'], data['data']['Media']['title']['romaji'], i['node']['image']['large']]
                break
            elif response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", 60))
                print(f"Rate limit exceeded. Retrying after  {retry_after} seconds...")
                time.sleep(retry_after + 5)
            else:
                print(f"Failed to fetch data: {response.status_code}")
                print(response.text)
                break

if __name__ == "__main__":
    media_ids = {}
    for query in queries:
        fetch_media(query['query'], query['total'], query['type'], media_ids)
    
    with open('final.txt', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for ids, favourites in media_ids.items():
            writer.writerow([ids, favourites])

    males = {}
    females = {}
    specials = {}

    with open('final.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        count = 1
        for row in csv_reader:
            print(f"On line: {count}")
            get_characters(int(row[0]), int(row[1]), males, females, specials)
            count += 1

    with open('db_male.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for ids, details in males.items():
            writer.writerow([ids, details[0], details[1]])

    with open('db_female.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for ids, details in females.items():
            writer.writerow([ids, details[0], details[1]])

    with open('db_special.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for ids, details in specials.items():
            writer.writerow([ids, details[0], details[1]])