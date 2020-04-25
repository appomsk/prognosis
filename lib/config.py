urls = '''
https://www.worldometers.info/coronavirus/
https://www.worldometers.info/coronavirus/country/us/
https://www.worldometers.info/coronavirus/country/spain/
https://www.worldometers.info/coronavirus/country/russia/
https://www.worldometers.info/coronavirus/country/czech-republic/
https://www.worldometers.info/coronavirus/country/sweden/
'''.split()

url_more = 'https://www.worldometers.info/coronavirus/worldwide-graphs/'

world_url = urls[0]
prefix_url = 'https://www.worldometers.info/coronavirus/country/'

cases = 'Cases'
active = 'Active'
deaths = 'Deaths'
dates = 'Dates'
fetcheddf_order = [dates, cases, active, deaths]

datadir = '../Data'

mkcol_diff = lambda col: col + 'D'
mkcol_p    = lambda col: col + '%'
mkcol_pp   = lambda col: col + '%%'
mkcol_avep = lambda col: col + 'Ave%'
mkcol_avepp  = lambda col: col + 'Ave%%'
mkcol_ave1 = lambda col: col + 'Ave1'
