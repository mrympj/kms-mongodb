from pymongo import MongoClient
from urllib.parse import quote_plus
import tkinter as tk
from tkinter import messagebox

def connect_to_tag():
    fname = quote_plus('dbadmin')
    password = quote_plus('dbImp!14@2')
    client = MongoClient('mongodb://%s:%s@78.38.35.219:27017/' % (fname, password))
    db = client['tag']
    collection = db['tag_collection']
    messagebox.showinfo('اتصال', 'به دیتابیس Tag متصل شد!')

def connect_to_user():
    fname = quote_plus('dbadmin')
    password = quote_plus('dbImp!14@2')
    client = MongoClient('mongodb://%s:%s@78.38.35.219:27017/' % (fname, password))
    db = client['user']
    collection = db['user_collection']
    messagebox.showinfo('اتصال', 'به دیتابیس User متصل شد!')

def connect_to_activity():
    fname = quote_plus('dbadmin')
    password = quote_plus('dbImp!14@2')
    client = MongoClient('mongodb://%s:%s@78.38.35.219:27017/' % (fname, password))
    db = client['activity']
    collection = db['activity_collection']
    messagebox.showinfo('اتصال', 'به دیتابیس Activity متصل شد!')

def insert_document():
    #publish_date = datetime.now()
    publish_date = publish_date_entry.get()
    description = description_entry.get()
    user_id = user_id_entry.get()
    fname = fname_entry.get()
    lname = lname_entry.get()
    tag_id = tag_id_entry.get()
    tag_title = tag_title_entry.get()
    relatedpart = relatedpart_entry.get()
    description_doc = description_doc_entry.get()
    repository_doc = repository_doc_entry.get()
    start_at = start_at_entry.get()
    end_at = end_at_entry.get()
    description_media = description_media_entry.get()
    repository_media = repository_media_entry.get()

    user = {'user_id': user_id, ' fname': fname, 'lname': lname}
    tag = {'tag_id': tag_id, 'title': tag_title}
    document_link = {'relatedpart': relatedpart, 'description': description_doc, 'repository': repository_doc}
    media_link = {'start_at': start_at, 'end_at': end_at, 'description': description_media, 'repository': repository_media}
    
    new_document = {'publish_date': publish_date,
                    'description': description,
                    'user': [user],
                    'tag': [tag],
                    'document_link': [document_link],
                    'media_link': [media_link]}
    
    result = connect_to_activity.collection.insert_one(new_document)
    
    messagebox.showinfo('عملیات موفق', 'سند جدید با موفقیت درج شد. ID سند: ' + str(result.inserted_id))

def delete_document():
    user_id = user_id_entry.get()
    result = connect_to_activity.collection.delete_many({'user.user_id': user_id})
    
    if result.deleted_count > 0:
        messagebox.showinfo('عملیات موفق', 'تعداد سند‌های حذف شده: ' + str(result.deleted_count))
    else:
        messagebox.showinfo('عملیات ناموفق', 'هیچ سندی با این مشخصات یافت نشد.')


def get_user_activities():
    user_id = user_id_entry.get()
    activities = list(connect_to_activity.collection.find({'user.user_id': user_id}))
    
    count = len(activities)
    
    if count == 0:
        messagebox.showinfo('عملیات ناموفق', 'فعالیتی برای کاربر با شناسه مورد نظر یافت نشد.')
        return
    
    activities_window = tk.Toplevel(window)
    activities_window.title("فعالیت‌های کاربر")
    
    activities_listbox = tk.Listbox(activities_window)
    activities_listbox.pack(fill=tk.BOTH, expand=True)
    
    for activity in activities:
        description = activity['description']
        publish_date = activity['publish_date']
        fname = activity['fname']
        lname = activity['lname']
        tag_title = activity['tag_title']
        activities_listbox.insert(tk.END, f"تاریخ: {publish_date} | توضیحات: {description} | نام: {fname} | نام خانوادگی: {lname} | موضوع: {tag_title}")


def update_document():
    user_id = user_id_entry.get()
    new_publish_date = publish_date_entry.get()
    new_description = description_entry.get()
    new_user_id = user_id_entry.get()
    new_fname = fname_entry.get()
    new_lname = lname_entry.get()
    new_tag_id = tag_id_entry.get()
    new_tag_title = tag_title_entry.get()
    new_relatedpart = relatedpart_entry.get()
    new_description_doc = description_doc_entry.get()
    new_repository_doc = repository_doc_entry.get()
    new_start_at = start_at_entry.get()
    new_end_at = end_at_entry.get()
    new_description_media = description_media_entry.get()
    new_repository_media = repository_media_entry.get()

    update_query = {'user.user_id': user_id}
    update_values = {'$set': {
        'publish_date': new_publish_date,
        'description': new_description,
        'user.$[].user_id': new_user_id,
        'user.$[].fname': new_fname,
        'user.$[].lname': new_lname,
        'tag.$[].tag_id': new_tag_id,
        'tag.$[].title': new_tag_title,
        'document_link.$[].relatedpart': new_relatedpart,
        'document_link.$[].description': new_description_doc,
        'document_link.$[].repository': new_repository_doc,
        'media_link.$[].start_at': new_start_at,
        'media_link.$[].end_at': new_end_at,
        'media_link.$[].description': new_description_media,
        'media_link.$[].repository': new_repository_media
    }}
    
    result = connect_to_activity.collection.update_many(update_query, update_values)
    
    if result.modified_count > 0:
        messagebox.showinfo('عملیات موفق', 'تعداد سند‌های به‌روزرسانی شده: ' + str(result.modified_count))
    else:
        messagebox.showinfo('عملیات ناموفق', 'هیچ سندی با این مشخصات یافت نشد.')



# ساخت پنجره
window = tk.Tk()
window.title("ارسال داده به دیتابیس")
window.geometry("500x800")

# ساخت دو باکس متنی
publish_date_label = tk.Label(window, text="date:")
publish_date_label.pack()
publish_date_entry = tk.Entry(window)
publish_date_entry.pack()

description_label = tk.Label(window, text="description:")
description_label.pack()
description_entry = tk.Entry(window)
description_entry.pack()

user_id_label = tk.Label(window, text="user_id:")
user_id_label.pack()
user_id_entry = tk.Entry(window)
user_id_entry.pack()

fname_label = tk.Label(window, text="first name:")
fname_label.pack()
fname_entry = tk.Entry(window)
fname_entry.pack()

lname_label = tk.Label(window, text="last name:")
lname_label.pack()
lname_entry = tk.Entry(window)
lname_entry.pack()

tag_id_label = tk.Label(window, text="tag id:")
tag_id_label.pack()
tag_id_entry = tk.Entry(window)
tag_id_entry.pack()

tag_title_label = tk.Label(window, text="tag title:")
tag_title_label.pack()
tag_title_entry = tk.Entry(window)
tag_title_entry.pack()

relatedpart_label = tk.Label(window, text="related part:")
relatedpart_label.pack()
relatedpart_entry = tk.Entry(window)
relatedpart_entry.pack()

description_doc_label = tk.Label(window, text="description:")
description_doc_label.pack()
description_doc_entry = tk.Entry(window)
description_doc_entry.pack()

repository_doc_label = tk.Label(window, text="repository:")
repository_doc_label.pack()
repository_doc_entry = tk.Entry(window)
repository_doc_entry.pack()

start_at_label = tk.Label(window, text="start at:")
start_at_label.pack()
start_at_entry = tk.Entry(window)
start_at_entry.pack()

end_at_label = tk.Label(window, text="end at:")
end_at_label.pack()
end_at_entry = tk.Entry(window)
end_at_entry.pack()

description_media_label = tk.Label(window, text="description:")
description_media_label.pack()
description_media_entry = tk.Entry(window)
description_media_entry.pack()

repository_media_label = tk.Label(window, text="repository:")
repository_media_label.pack()
repository_media_entry = tk.Entry(window)
repository_media_entry.pack()

submit_button = tk.Button(window, text="insert", command=insert_document)
submit_button.pack()

delete_button = tk.Button(window, text="delete", command=delete_document)
delete_button.pack()

show_activities_button = tk.Button(window, text="select", command=get_user_activities)
show_activities_button.pack()

update_button = tk.Button(window, text="update", command=update_document)
update_button.pack()

# اضافه کردن دکمه‌ها
connect_to_tag_button = tk.Button(window, text="اتصال به دیتابیس Tag", command=connect_to_tag)
connect_to_tag_button.pack()

connect_to_user_button = tk.Button(window, text="اتصال به دیتابیس User", command=connect_to_user)
connect_to_user_button.pack()

connect_to_activity_button = tk.Button(window, text="اتصال به دیتابیس Activity", command=connect_to_activity)
connect_to_activity_button.pack()

# نمایش پنجره
window.mainloop()
