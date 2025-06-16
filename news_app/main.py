import requests
api='ae7ea6c40b42431b81ab8dd069ca9ca2'
def fetchnewz():
    query=input("search: ")
    url=f"https://newsapi.org/v2/everything?q={query}&from=2025-04-22&sortBy=publishedAt&apiKey=ae7ea6c40b42431b81ab8dd069ca9ca2"

    responce=requests.get(url)
    data=responce.json()
    if "articles" in data and data.get("status") == "ok":
        
        
        article=data.get("articles",{})
        for i,a in enumerate(article):
            result=article[i]
            # print(result)
            title=result.get('title',{})
            link=result.get('url',{})
            print(f"{i}. Title: {title}\nRead More: {link}\n\n")
    else:
        print(f"there's no news abt {query}")
        
#calling function
fetchnewz()
    
    
    