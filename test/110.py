import datetime
import requests

url = "https://fms.treas.gov/fmsweb/viewDTSFiles?dir=a&fname="
r = requests.get("https://www.fms.treas.gov/fmsweb/viewDTSFiles?dir=w&fname=13011400.txt")

print r.text #this is why it prints the URL, but scraper below still needs debugging

def generate_dates(start_date, end_date):
    dates = []
    td = datetime.timedelta(hours=24)
    current_date = start_date
    while current_date <= end_date:
        #datestring = str(current_date.year)[-2:] + str(current_date.month) + str(current_date.day) #+ '00.txt'
        datestring = current_date.strftime(format='%y%m%d') + '00.txt'
        #print datestring
        current_date += td
        dates.append(datestring)
    return dates

start_date = datetime.date(2005, 1, 1)
end_date = datetime.date(2012, 12, 31)

fnames = generate_dates(start_date, end_date)
#print fnames

urls = [url+fname for fname in fnames]
for url in urls:
    dataRequest = requests.get(url)

    localFile = open(url, 'w')
    localFile.write(dataRequest.txt)
    localFile.close()
    dataRequest.close()




#print urls

#for url in urls:
	#if fails then 00 -> 01 and if 01 fails then 02



