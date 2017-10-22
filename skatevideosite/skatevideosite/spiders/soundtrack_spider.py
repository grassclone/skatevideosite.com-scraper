import scrapy


class SoundtrackSpider(scrapy.Spider):
    name = 'soundtrack'
    urls = []
    base_url = 'http://www.skatevideosite.com/index.php?page=skatevideos&sort=rating&p='
    for x in range(1, 18): # crawls one page less then whats on second param
        urls.append(base_url + str(x))
        
    start_urls = urls
    def parse(self, response):
    # follow links to video pages
        for href in response.xpath("//table[2]//td/a/@href[not(contains(., '#online'))]").extract():
            print(response.follow(href, self.parse))
            yield response.follow(href, self.parse_soundtrack)
    #iterate over soundtrack
    def parse_soundtrack(self, response):
        video_title = response.xpath("//html/body/div[3]/div/div/h1/text()").extract()
        print(video_title)
        print("---------------------------------")
        # get song and artist. we need to split it into two strings.
        for capsule in response.xpath("/html/body//table//td/text()[contains(., '-')]").extract():
            yield {
            'artist': capsule.split("-")[0],
            'song':   capsule.split("-")[1],
            'video': video_title 
            }

