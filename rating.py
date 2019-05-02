import json
import requests
from bs4 import BeautifulSoup

def try_float(text):
	try:
		r = float(text)
	except ValueError as e:
		return 0
	return r	

def try_int(text):
	try:
		r = int(text)
	except ValueError as e:
		return 0
	return r


def parse_kinopoisk(url):
	url = url + '?force-version=touch&source=desktop_footer'
	session = requests.Session()
	headers = requests.utils.default_headers()
	headers.update({
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
	})
	r = session.get(url, headers=headers)
	html = r.text
	soup = BeautifulSoup(html, "html.parser")
	trs = soup.select(".app-container .page .details-table__row")
	imdb = 0
	kinopoisk_rating = 0
	people_i = 0
	people_k = 0
	for tr in trs:
		tds = tr.select('.details-table__cell')
		if len(tds) > 1 and "IMDb" in tds[0].text:
			imdb = tds[1].text
			people_i = tds[2].text.replace(" ", "")	
			
	tdss = soup.select('.movie-rating__value')
	if len(tdss) > 0:
		kinopoisk_rating = tdss[0].text
	tt = soup.select('.movie-rating__count')
	if len(tt) > 0:
		people_k = tt[0].text.replace(" ", "")


	return {
		'IMDb': try_float(imdb),
		'kinopoisk': try_float(kinopoisk_rating),
		'people_k': try_int(people_k),
		'people_i': try_int(people_i),
	}




def parse_movies(city = 2): # Almaty by default
	url = 'http://m.kino.kz/index.htm?city=%d&sort=1' % city
	r = requests.get(url)
	html = r.text
	soup = BeautifulSoup(html, "html.parser")
	row = soup.select("body table tr:nth-of-type(3) td.stripe-body div a")[1:]
	movies = []
	for item in row:
		url = item['href']
		name = item.text
		d_url = 'http://kino.kz' + url.replace('.htm', '.asp')
        #код работает #список фильмов и их URL #список URL кинопоиск каждого фильма
		if "movie" in d_url:
			r = requests.get(d_url)
			html = r.text
			soup = BeautifulSoup(html, "html.parser")
			#get local rating
			rr = soup.select('div.star-rate-text b span')[1:]
			for item in rr:
				local_rating = item.text

			movie = {
				'Название': name,
				'url': url,
		
			}
			movie['IMDb'] = 0
			movie['kinopoisk'] = 0
			movie['people_k'] = 0
			movie['people_i'] = 0
			links = soup.select("div.detail_content table a")
			for item in links:
				k_url = item['href']
				if "kinopoisk" in k_url:
					data = parse_kinopoisk(k_url)
					movie['IMDb'] =  data['IMDb']
					movie['kinopoisk'] = data['kinopoisk']
					movie['people_k'] = data['people_k']
					movie['people_i'] = data['people_i']

	
				if movie['people_k'] > 10000:
					r1 = movie['kinopoisk'] *  (movie['people_k'] / (movie['people_k'] + 500))
				else:
					r1 = movie['kinopoisk']
				if movie['people_i'] > 10000:
					r2 = movie['IMDb'] *  ((movie['people_i'] + 500) / movie['people_i'])
				else:
					r2 = movie['IMDb']	

				movie['rating'] = (r1 + r2) /2
				movie['rating'] = int(movie['rating'] * 100) / 100
			


			movies.append(movie)
	#print(movies)
	return movies

	


if __name__ == "__main__":
	from operator import itemgetter
	movies = parse_movies()
	movies = sorted(movies, key=itemgetter('rating'), reverse=True)
	with open ("rating.json", "w", encoding = 'utf - 8') as file:
		data = json.dumps(movies, ensure_ascii = False)
		file.write(data)
	
	
	


					