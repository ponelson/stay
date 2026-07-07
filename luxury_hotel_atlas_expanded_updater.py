#!/usr/bin/env python3
"""
Luxury Hotel Atlas expanded updater starter.

Purpose:
- Keep the HTML atlas current without hand-editing embedded JavaScript.
- Refresh official directory pages where static HTML is available.
- Export a clean CSV/JSON that can be imported through the atlas Update Tools tab.

Install:
  python3 -m pip install requests beautifulsoup4 pandas lxml

Usage:
  python3 luxury_hotel_atlas_expanded_updater.py luxury_hotel_atlas_expanded_data.csv

Notes:
- Some hotel groups render locations client-side or behind anti-bot systems. Those require a saved HTML export, sitemap, or Playwright scraper.
- The script is intentionally conservative: it appends candidate rows with source URLs and does not delete your curated rows automatically.
"""
import sys, re, json, urllib.parse
from pathlib import Path
import pandas as pd
import requests
from bs4 import BeautifulSoup

SOURCES = {
    'Aman':'https://www.aman.com/hotels-and-resorts',
    'Belmond':'https://www.belmond.com/hotels',
    'Rosewood':'https://www.rosewoodhotels.com/en/luxury-hotels-and-resorts',
    'Four Seasons':'https://www.fourseasons.com/find_a_hotel_or_resort/',
    'COMO':'https://www.comohotels.com/destinations',
    'Auberge':'https://auberge.com/resorts/',
    'Explora':'https://www.explora.com/destinations/',
    'Singita':'https://singita.com/lodges/',
    'Capella':'https://capellahotels.com/en',
    '&Beyond':'https://www.andbeyond.com/our-lodges/',
    'EDITION':'https://www.editionhotels.com/destinations/',
    'Hoshino Resorts':'https://hoshinoresorts.com/en/hotels/',
    'Rocco Forte':'https://www.roccofortehotels.com/',
    'Zannier':'https://www.zannierhotels.com/',
    'The Chedi / GHM':'https://www.ghmhotels.com/en/our-hotels/',
    'Shangri-La Group':'https://www.shangri-la.com/find-a-hotel/',
    'Jumeirah':'https://www.jumeirah.com/en/stay',
    'Taj / IHCL':'https://www.tajhotels.com/en-in/hotels',
    'Relais & Châteaux':'https://www.relaischateaux.com/us/sitemap/',
}

def maps_url(name, country=''):
    return 'https://www.google.com/maps/search/?api=1&query='+urllib.parse.quote_plus(name+' '+country)

def fetch(url):
    r=requests.get(url,headers={'User-Agent':'Mozilla/5.0 luxury-hotel-atlas-updater'},timeout=35)
    r.raise_for_status(); return r.text

def generic_extract(brand,url):
    html=fetch(url)
    soup=BeautifulSoup(html,'lxml')
    text='\n'.join(s.strip() for s in soup.stripped_strings)
    candidates=[]
    # HTML directory pages often expose hotel names in headings/links.
    for tag in soup.find_all(['h1','h2','h3','h4','a']):
        s=' '.join(tag.get_text(' ',strip=True).split())
        if len(s)<4 or len(s)>90: continue
        if any(stop in s.lower() for stop in ['book now','discover','sign in','privacy','contact','offers','destinations','residences']): continue
        if brand.lower().split()[0] in s.lower() or any(w in s for w in ['Hotel','Resort','Lodge','Camp','Palace','House','Inn','Ryokan','EDITION','Shangri-La','Jumeirah','Taj','Chedi','Capella','COMO','Auberge','Rosewood','HOSHINOYA','KAI ']):
            candidates.append(s)
    # Dedupe preserving order
    seen=set(); rows=[]
    for s in candidates:
        k=s.lower()
        if k in seen: continue
        seen.add(k)
        rows.append({'brand':brand,'name':s,'country':'','city':'','region':'Imported / classify','subregion':'','lat':0,'lng':0,'status':'Imported / verify current','kind':'Hotel / resort','note':'Imported from official directory; classify and geocode before relying on it.','art':False,'url':url,'maps':maps_url(s),'nycDirect':False,'source':'Official directory updater'})
    return rows

def main(path):
    df=pd.read_csv(path).fillna('') if Path(path).exists() else pd.DataFrame()
    added=[]
    for brand,url in SOURCES.items():
        try:
            rows=generic_extract(brand,url)
            print(f'{brand}: {len(rows)} candidates')
            added.extend(rows)
        except Exception as e:
            print(f'{brand}: skipped ({e})')
    if added:
        out=pd.concat([df,pd.DataFrame(added)],ignore_index=True)
        out['_key']=out['brand'].astype(str).str.lower().str.strip()+'|'+out['name'].astype(str).str.lower().str.strip()
        out=out.drop_duplicates('_key',keep='first').drop(columns=['_key'])
        csv_out=Path(path).with_name(Path(path).stem+'_refreshed.csv')
        json_out=Path(path).with_name(Path(path).stem+'_refreshed.json')
        out.to_csv(csv_out,index=False)
        json_out.write_text(json.dumps(out.to_dict(orient='records'),ensure_ascii=False,indent=2),encoding='utf-8')
        print('Wrote',csv_out,'and',json_out)

if __name__=='__main__':
    main(sys.argv[1] if len(sys.argv)>1 else 'luxury_hotel_atlas_expanded_data.csv')
