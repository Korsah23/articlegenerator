from flask import Flask, render_template,request
import openai
openai.api_key = "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"
import requests,os



app = Flask(__name__)

# Enable debug mode
app.debug = True

# Set the FLASK_ENV environment variable to development
os.environ['FLASK_DEBUG'] = 'development'


@app.route('/',methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        title=request.form['title']
        keyword = request.form['keyword']
        introduction = generate_intro(title)
        body = generate_body(title)
        conclusion = generate_conclusion(title)
        photos = generate_photos(keyword)
        videoId = generate_video(title)
        #return f'intro:{introduction} body:{body} conclusion:{conclusion}'
        return render_template('article.html',title=title.upper(),introduction=introduction,body=body,conclusion=conclusion,photos=photos,videoId=videoId)
        
    else:
        return render_template('index.html')




def generate_intro(title):
  response = openai.Completion.create(
    model = 'text-davinci-002',
    prompt = 'Write a blog post introduction paragraph on the topic. ' + title +"with length of at least 100 words",
    max_tokens = 200,
    temperature = 0.6
  )

  retrieve_intro = response.choices[0].text

  return retrieve_intro


def generate_body(title):
  response = openai.Completion.create(
    model = 'text-davinci-002',
    prompt = f'Write a 5-paragraphed blog post body on the topic {title}', 
    max_tokens = 4000,
    temperature = 0.6
  )

  retrieve_body = response.choices[0].text

  return retrieve_body

def generate_conclusion(title):
  response = openai.Completion.create(
    model = 'text-davinci-002',
    prompt = 'Write a blog post conclusionon the topic. ' + title, 
    max_tokens = 4000,
    temperature = 0.6
  )

  retrieve_conclusion = response.choices[0].text

  return retrieve_conclusion

def generate_photos(keyword):

    # Set the authorization headers
    headers = {
    'Authorization': 'Bearer 563492ad6f91700001000001b0f216a1d8904366a249d46acf112cd5',
    'Content-Type': 'application/json'
    }
    # Set the API endpoint URL
    api_url = f'https://api.pexels.com/v1/search?query={keyword}'
    # Make the GET request
    response = requests.get(api_url, headers=headers)
    photos_list = []
    # Check the status code
    if response.status_code == 200:
        # Process the response data
        data = response.json()
        photos = data['photos']
        if len(photos) == 0:
          photos_list.append("https://images.pexels.com/photos/806408/pexels-photo-806408.jpeg?auto=compress&cs=tinysrgb&w=600")
          return photos_list
          
        elif len(photos) < 3:
          for i in range(0,len(photos)):
            photos_list.append(photos[i]["src"]["original"])
          return photos_list
          
        else:  
          for i in range(0,3):
          #photos[i]["url"]
            photos_list.append(photos[i]["src"]["original"])
          return photos_list
        
    else:
        print(f'Error: {response.status_code}')


import requests


# Set the API endpoint URL
def generate_video(title):
  endpoint = 'https://www.googleapis.com/youtube/v3/search'
  params = {
  'part': 'snippet',
  'q': f'{title}',
  'type': 'video',
  'key': 'AIzaSyB-RJgEYkn5lzsDzovPDADPtC_Wmz6dllA'
    }

    # Send the GET request
  response = requests.get(endpoint, params=params)



    # Check the status code
  if response.status_code == 200:
    # Process the response data
    data = response.json()
    return data['items'][0]['id']['videoId']
  else:
    return f'Error: {response.status_code}'


    



if __name__ == '__main__':
    app.run()