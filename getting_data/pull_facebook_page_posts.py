from urllib.request import urlopen
import time
import sys
import datetime
import json

def request_until_succeed(url):
    success = False
    while not success:
        try:
            response = urlopen(url)
            if response.getcode() == 200:
                success = True
        except Exception as e:
            print(e)
            time.sleep(5)
            print("Error for URL %s: %s" % (url, datetime.datetime.now()))
    return response.read()

def build_facebook_api_url(page_id='', page_name='', access_token='', fields=['posts.limit(100)']):
    identifier = page_id if page_id else page_name
    if not identifier:
        raise ValueError('At least one of page_id and page_name is required')
    field_names = ','.join(fields)
    base = "https://graph.facebook.com/v2.11"
    node = "/" + identifier + "?fields=%s" % field_names
    parameters = "&access_token=%s" % access_token
    url = base + node + parameters
    return url

def get_posts_from_response(feed_data):
    posts = list()
    for post in feed_data:
        message = post.get('message', '')
        if message:
            posts.append(message)
    print('%d posts found' % len(posts))
    print(posts[0].split('\n')[0])
    return posts

def get_facebook_feed(page_id='', page_name='', access_token=''):
    if not access_token:
        raise ValueError('Valid access_token is required')
    current_url = build_facebook_api_url(page_id=page_id, page_name=page_name, access_token=access_token, fields=['posts.limit(100)'])
    posts = list()
    i = 0
    while current_url:
        json_response = request_until_succeed(current_url)
        data = json.loads(json_response)
        if not i: # first pass, initial page has one extra step: 'feed' field
            feed_label = 'posts' if 'posts' in data else 'feed'
            data = data[feed_label]
        posts += get_posts_from_response(data['data'])
        current_url = data['paging'].get('next', '')
        print('Got data part %d from page...' % i)
        i += 1
    return posts

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Usage: python3 <this_script> <access_token> <page_name> <output_json>')
        sys.exit()
    # page_id = '776807699062251'
    # page_name = 'UniversityOfChicagoSecrets'
    access_token, page_name, output_json = sys.argv[1:4]
    posts = get_facebook_feed(page_name=page_name, access_token=access_token)
    print('%d posts found in total!' % len(posts))
    with open(output_json, 'w') as f:
        json.dump(posts, f)
    print('Dumped to JSON file')
