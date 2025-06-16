import sqlite3

conn=sqlite3.connect('data.db')

cursor=conn.cursor()

# cursor.execute("DROP TABLE IF EXISTS videos")
cursor.execute('''
    CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            duration TEXT NOT NULL
    )
''')

def list_all():
        cursor.execute("SELECT * FROM videos")
        print("Id | Name | Duration")
        for row in cursor.fetchall():
            print(f"{row[0]} | {row[1]} | {row[2]}")

        
def add_video(name,duration):
    cursor.execute("INSERT INTO videos (name,duration) VALUES (?, ?)",(name ,duration))
    conn.commit()

    
def update_video(index,new_name,new_duration):
    if not new_name.strip():
        new_name="N|A"
    if not new_duration.strip():
        new_duration="N|A"
    cursor.execute("UPDATE videos SET name=?, duration=? WHERE id=?",(new_name,new_duration,index))
    conn.commit()

def delete_video(index):
    cursor.execute("DELETE FROM videos WHERE id=?",(index,))
    conn.commit()

def main():
    while True:
        print("------YOUTUBE MANGER------")
        print("1. List all videos")
        print("2. Add video")
        print("3. Update video")
        print("4. Delete video")
        print("5. EXIT the app")
        choice=input("enter your choice: ")
        match(choice):
            case '1':
                print("\n")
                print("loading videos..")
                list_all()
                print("\n")
                
            case '2':
                name=input("enter video name: ")
                duration=input("enter video duration: ")
                add_video(name,duration)
                print("video added successfully!")
            case '3':
                print("\n")
                list_all()
                print("\n")
                index=int(input("enter video ID to update :"))
                name=input("enter video name: ")
                duration=input("enter video duration: ")           
                update_video(index,name,duration)
                print("video updated successfully!")
                
            
            case '4':
                # list_all()
                index=int(input("enter video ID to delete :"))          
                delete_video(index)           
                print("video deleted successfully!")

            case '5':
                print("exiting the app..")
                conn.close()
                print("Done")
                exit()
            case _:
                print("INVALID INPUT!")
      
    
        
if __name__=="__main__":
    main()
    
