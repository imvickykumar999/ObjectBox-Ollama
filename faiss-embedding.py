import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import os
import json
import ollama
from objectbox import *

# Step 1: Extract URLs from the Sitemap
sitemap_url = 'https://blogforge.pythonanywhere.com/sitemap.xml'

# Step 2: Fetch Meta Descriptions
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
SCRAPED_DATA_FILE = 'scraped_data.json'

def fetch_meta_descriptions():
    if os.path.exists(SCRAPED_DATA_FILE):
        with open(SCRAPED_DATA_FILE, "r") as file:
            return json.load(file)
    
    response = requests.get(sitemap_url)
    sitemap_xml = response.content
    root = ET.fromstring(sitemap_xml)
    namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls = [url.find('ns:loc', namespace).text for url in root.findall('ns:url', namespace)]
    
    data = {}
    for url in urls:
        try:
            page_response = requests.get(url, headers=headers)
            if page_response.status_code == 200:
                soup = BeautifulSoup(page_response.text, 'html.parser')
                blog_details = soup.find(class_="blog-details")
                
                if blog_details:
                    data[url] = blog_details.get_text(strip=True)
                else:
                    description_tag = soup.find('meta', attrs={'name': 'description'})
                    data[url] = description_tag['content'] if description_tag and 'content' in description_tag.attrs else 'No meta description found'
            else:
                data[url] = f'Error: {page_response.status_code}'
                
            print(data[url])
        except Exception as e:
            data[url] = f'Error fetching {url}: {str(e)}'
    
    with open(SCRAPED_DATA_FILE, "w") as file:
        json.dump(data, file)
    
    return data

documents = list(set(fetch_meta_descriptions().values()))

# Define the entity class first
@Entity()
class DocumentEmbedding:
    id = Id()
    document = String()
    embedding = Float32Vector(index=HnswIndex(
        dimensions=1024,
        distance_type=VectorDistanceType.COSINE
    ))

# Create the model and add the entity
model = Model()
model.entity(DocumentEmbedding)

# Do not remove DB files to allow reuse across runs
store = Store(model=model, directory="objectbox")
box = store.box(DocumentEmbedding)

# Check if embeddings need to be created
if box.count() == 0:
    print("Documents to embed: ", len(documents))
    # store each document in a vector embedding database
    for i, d in enumerate(documents):
        response = ollama.embeddings(model="mxbai-embed-large", prompt=d)
        embedding = response["embedding"]
        box.put(DocumentEmbedding(document=d, embedding=embedding))
        print(f"Document {i + 1} embedded")
else:
    print("Reusing existing embeddings from database.")

# Continuous chatting loop
while True:
    prompt = input("\n> ")
    if prompt.lower() == 'exit':
        break
    if not prompt.strip():
        continue  # Skip empty inputs
    
    # generate an embedding for the prompt and retrieve the most relevant doc
    response = ollama.embeddings(
        prompt=prompt,
        model="mxbai-embed-large"
    )
    
    query = box.query(
        DocumentEmbedding.embedding.nearest_neighbor(response["embedding"], 1)
    ).build()
    
    results = query.find_with_scores()
    if results:
        data = results[0][0].document
        #print(f"Data most relevant to \"{prompt}\" : {data}")
        print("Generating the response now...\n\n")
        
        # generate a response combining the prompt and data we retrieved
        output = ollama.generate(
            model="llama3",
            prompt=f"Using this data: {data}. Respond to this prompt: {prompt}"
        )
        
        print(output['response'])
    else:
        print("No relevant data found.")
