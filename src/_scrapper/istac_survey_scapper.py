import re
from tqdm import tqdm

from bs4 import BeautifulSoup
from request_handler import fetch_page_content
import pandas as pd

def scrap_datasets(href):
    if "multidatasetId" in href:
        return scrap_multidataset(href)
    else:
        return []

def scrap_multidataset(href):
    multidataset = []
    
    content = fetch_page_content(href)

    if not content:
        return []
    soup = BeautifulSoup(content, 'html.parser')
    dataset_anchors = soup.find_all('a', class_='multidataset-link')
    
    # Procesar datasets con progreso
    for anchor in tqdm(dataset_anchors, desc="Procesando datasets", leave=False, disable=len(dataset_anchors)<=1):
        dataset_title = re.sub(r'\s+', ' ', anchor['title']).strip()
        dataset_href = anchor['href']
        
        multidataset.append((dataset_title, dataset_href))
    
    return multidataset

def convert_to_dataframe(survey_data):
    # Extract the single survey title
    survey_title = survey_data.get("title", "No title")
    
    survey_multidatasets = survey_data.get("survey", [])
    
    # Create DataFrame with dataset information only
    rows = []
    for multidataset in survey_multidatasets:
        multidataset_title = multidataset.get("title", "No title")
        multidataset_href = multidataset.get("href", "No href")
        if multidataset.get("datasets"):
            # If dataset has sub-datasets, create one row per sub-dataset
            for dataset_title, dataset_href in multidataset["datasets"]:
                rows.append({
                    "multidataset_title": multidataset_title,
                    "multidataset_href": multidataset_href,
                    "dataset_title": dataset_title,
                    "dataset_href": dataset_href
                })
    
    df = pd.DataFrame(rows)

    return survey_title, df

def istac_survey_scrapper(soup):
    # Lógica específica para el scrapping de ISTAC_SURVEY
    items = soup.find_all("li")
    
    survey_list = []
    
    # Filtrar items que empiezan con número
    filtered_items = [item for item in items if re.match(r'^\d+', re.sub(r'\s+', ' ', item.get_text()).strip())]
    
    # Procesar surveys con progreso
    for item in tqdm(filtered_items, desc="Procesando surveys", leave=False): 
        
        # Filtrar por contenido que comienza con un número
        li_title = re.sub(r'\s+', ' ', item.get_text()).strip()
        url = item.find_all("a")
        href = url[0]['href'] if url else None
        
        datasets = scrap_datasets(href) if href else []
        
        survey_list.append({
            "title": li_title, # Título del item
            "href": href, # URL del item
            "datasets": datasets # [(dataset_title, dataset_href), ...]
        })

    survey_data = {"title": soup.title.string if soup.title else "No title", "survey": survey_list}

    return convert_to_dataframe(survey_data)