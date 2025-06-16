from pymongo import MongoClient
from bson import ObjectId

client=MongoClient("mongodb+srv://youtubepy:rohitgiri123@cluster0.857hrwi.mongodb.net/")
#not a good idea to include id and password in a code file

db=client["ytmanger"]
video_collection=db["db_videos"]
print(video_collection)

def list_videos():
    for video in video_collection.find():
        print(f"ID {video['_id']}, Name:{video['name']} Duration:{video['duration']}")

def add_video(name,time):
    video_collection.insert_one({"name": name, "duration": time})

def update_video(index,u_name,u_time):
    video_collection.update_one(
            {'_id':ObjectId(index)},
            {"$set":{"name":u_name , "duration":u_time}}
                            )

def delete(index):
    video_collection.delete_one({"_id":ObjectId(index)})

def main(): 
    while True:
        print("\n ------Youtuber Videos Manager------")
        print("1. list all videos")
        print("2. add new video")
        print("3. update video")
        print("4. delete video")
        print("5. exit the app!")
        choice=input("enter your choice: ")
        if(choice=='1'):
            list_videos()
        elif(choice=='2'):
            name=input("enter video name: ")
            time=input("enter video duration: ")
            add_video(name,time)
        elif(choice=='3'):
            index=input("enter video id to update: ")
            u_name=input("enter new video name: ")
            u_time=input("enter new video duration: ")
            update_video(index,u_name,u_time)
        elif (choice=='4'):
            index=input("enter video id to delete: ")
            delete(index)
        else:
            print("please enter a valid choice!")
        
if __name__=="__main__":
    main()
