import os,re,random,time,django,datetime
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web_scraping_api.settings")
django.setup()
from urllib.request import urlopen
from bs4 import BeautifulSoup
from scraping_app.models import Subject,Author,Article


def number_articles():
    """ Count the number of articles on the homepage """

    # Open the Techcrunch homepage and store the HTML content in the variable "content_homepage"
    link='https://beta.techcrunch.com'
    link_o=urlopen(link)
    page_html=link_o.read()
    link_o.close()
    content_homepage=BeautifulSoup(page_html,"html.parser")

    # Count the number of articles
    articles_search=content_homepage.findAll(class_="post-block__header")
    return len(articles_search)


def scrape(i):
    """ Scrape the Techcrunch homepage, Article page and Author Page to get the relevant data """

    # Regular expressions
    pattern_author = re.compile(r"[\n\t]+")
    pattern_article = re.compile(r"(\n|\xa0)+")
    pattern_article_2 = re.compile(r"\.{1}\b")

    # Open the Techcrunch homepage and store the HTML content in the variable "content_homepage"
    link='https://beta.techcrunch.com'
    link_o=urlopen(link)
    page_html=link_o.read()
    link_o.close()
    content_homepage=BeautifulSoup(page_html,"html.parser")

    article_dict={}

    # Find the article_link on the homepage, open the link and store its content in the variable "content_article_page"
    article_link=content_homepage.findAll(class_="post-block__header")[i].h2.a.get('href')
    article_link_open=urlopen(article_link)
    page_html_article=article_link_open.read()
    article_link_open.close()
    content_article_page=BeautifulSoup(page_html_article,"html.parser")

    # Subject's fields
    # Find the article's subject data
    article_subject_info=str(content_article_page.find(type="application/ld+json"))
    subject_info_beginning=article_subject_info.find("keywords")
    subject_info_end=article_subject_info.find("</script>")
    subject_info=article_subject_info[subject_info_beginning+11:subject_info_end-5]
    # Process "subject_info" to extract the "subject_name"
    subject_info=subject_info.replace('"','')
    subject=subject_info.split(',')[2].title()
    article_dict['subject_name']=subject

    # Author's fields
    # Find the author's name data
    author_info=content_homepage.findAll(class_="post-block__header")[i].div.div.span.a.text
    # Process "author_info" to extract the "author_name"
    article_dict['author_name']=re.sub(pattern_author,"",author_info)
    # Find the author_link on the homepage, open the link and store its content in the variable "content_author_page"
    author_link = content_homepage.findAll(class_="post-block__header")[i].div.div.span.a.get('href')
    try:
        author_link_open=urlopen(author_link)
        page_html_author=author_link_open.read()
        author_link_open.close()
        content_author_page=BeautifulSoup(page_html_author,"html.parser")
        # Extract "author_pic"
        author_pic_info = content_author_page.find(class_="author-profile__avatar").get('src')
        article_dict['author_pic'] = author_pic_info
    except:
        article_dict['author_pic'] = 'no picture'

    # Article's fields
    # Extract "article_title"
    article_dict['article_title']=content_article_page.find(class_="article__title").text
    # Extract "article_slug"
    article_dict['article_slug']=article_link[22:]
    # Extract "article_heroimage"
    try:
        article_dict['article_heroimage']=content_article_page.find(class_="article__featured-image").get('src')
    except:
        article_dict['article_heroimage']='no picture'
    # Extract "article_publishdate"
    article_dict['article_publishdate']=content_homepage.findAll(class_="post-block__header")[i].div.div.time.get('datetime')[0:10]
    # Extract "article_text"
    article_text_info=content_article_page.find(class_="article-content").text
    # article_dict['article_text']=re.sub(pattern_article_2,". ",re.sub(pattern_article,"",article_text_info))
    article_dict['article_text']=article_text_info

    # Return the article dictionary
    return article_dict


def store(article_dict):
    """ Store the data of article dictionary in database """

    # Check if the subject is already in the database and, if not, choose a color and store the subject
    if article_dict['subject_name'] not in map(str,Subject.objects.all()):
        subject_color="#%06x" % random.randint(0, 0xFFFFFF)
        while Subject.objects.filter(color=subject_color):
            subject_color="#%06x" % random.randint(0, 0xFFFFFF)
        subject = Subject(name=article_dict['subject_name'],
                          color=subject_color)
        subject.save()

    # Check if the author is already in the database and, if not, store it
    if article_dict['author_name'] not in map(str,Author.objects.all()):
        author=Author(name=article_dict['author_name'],
                      picture=article_dict['author_pic'])
        author.save()

    # Check if the article is already in the database and, if not, store it
    if article_dict['article_slug'] not in map(str,Article.objects.all()):
        article=Article(title=article_dict['article_title'],
                        slug=article_dict['article_slug'],
                        author=Author.objects.get(name=article_dict['author_name']),
                        subject=Subject.objects.get(name=article_dict['subject_name']),
                        hero_image=article_dict['article_heroimage'],
                        publish_date=article_dict['article_publishdate'],
                        text=article_dict['article_text'])
        article.save()


# Scrape and store the data every hour

print('\nStart: '+ str(datetime.datetime.now()))

for i in range(number_articles()):
    try:
        article_dict=scrape(i)
        store(article_dict)
    except:
        print('Error: '+ str(datetime.datetime.now()))
        
print('End: '+ str(datetime.datetime.now()))

