from pymongo import MongoClient
from urllib.parse import quote_plus
import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from tkinter import ttk
from bson.objectid import ObjectId

fname = quote_plus('dbadmin')
password = quote_plus('dbImp!14@2')
uri = 'mongodb://%s:%s@78.38.35.219:27017/' % (fname, password)
client = MongoClient(uri)

db = client['G2']

collection = db['activity']

########################################################

def insert_document():
    publish_date = publish_date_entry.get()
    description = description_entry.get()
    user_id = user_id_combobox.get()
    fname = fname_entry.get()
    lname = lname_entry.get()
    tag_id = tag_id_combobox.get()
    tag_title = tag_title_entry.get()
    relatedpart = relatedpart_entry.get()
    description_doc = description_doc_entry.get()
    repository_doc = repository_doc_entry.get()
    start_at = start_at_entry.get()
    end_at = end_at_entry.get()
    description_media = description_media_entry.get()
    repository_media = repository_media_entry.get()

    user = {'user_id': user_id, 'fname': fname, 'lname': lname}
    tag = {'tag_id': tag_id, 'title': tag_title}
    document_link = {'relatedpart': relatedpart, 'description': description_doc, 'repository': repository_doc}
    media_link = {'start_at': start_at, 'end_at': end_at, 'description': description_media, 'repository': repository_media}
    
    new_document = {'publish_date': publish_date,
                    'description': description,
                    'user': [user],
                    'tag': [tag],
                    'document_link': [document_link],
                    'media_link': [media_link]}
    
    result = collection.insert_one(new_document)
    
    messagebox.showinfo('Successful Operation', 'New document successfully inserted. Document ID: ' + str(result.inserted_id))
#################################################################################
def delete_document():
    doc_id = doc_id_combobox.get()
    result = collection.delete_one({'_id': ObjectId(doc_id)})

    if result.deleted_count > 0:
        messagebox.showinfo('Successful Operation', 'The document has been successfully deleted.')
    else:
        messagebox.showinfo('Unsuccessful Operation', 'No document found with the specified criteria.')

################################################################################

def get_user_activities():
    doc_id = doc_id_combobox.get()
    activity = collection.find_one({'_id': ObjectId(doc_id)})

    if not activity:
        messagebox.showinfo('Unsuccessful Operation', 'No activity found with the specified ID.')
        return

    activities_window = tk.Toplevel(window)
    activities_window.title("User Activities")

    activities_treeview = ttk.Treeview(activities_window, columns=
                                       ('Date', 'Description', 'First Name', 'Last Name', 'Tag'))
    activities_treeview.pack(fill=tk.BOTH, expand=True)

    activities_treeview.heading('#0', text='ID')
    activities_treeview.heading('Date', text='Date')
    activities_treeview.heading('Description', text='Description')
    activities_treeview.heading('First Name', text='First Name')
    activities_treeview.heading('Last Name', text='Last Name')
    activities_treeview.heading('Tag', text='Tag')

    doc_id = str(activity['_id'])
    publish_date = activity['publish_date']
    description = activity['description']
    fname = activity['user'][0]['fname']
    lname = activity['user'][0]['lname']
    tag_title = activity['tag'][0]['title']

    activities_treeview.insert('', 'end', text=doc_id, values=(publish_date, description, fname, lname, tag_title))

#########################################################################

def update_document():
    user_id = user_id_combobox.get()
    new_publish_date = publish_date_entry.get()
    new_description = description_entry.get()
    new_user_id = user_id_combobox.get()
    new_fname = fname_entry.get()
    new_lname = lname_entry.get()
    new_tag_id = tag_id_combobox.get()
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
    
    result = collection.update_many(update_query, update_values)
    
    if result.modified_count > 0:
        messagebox.showinfo('Successful Operation', 'Number of updated documents: ' + str(result.modified_count))
    else:
        messagebox.showinfo('Unsuccessful Operation', 'No document found with the specified criteria.')

window = tk.Tk()
window.title("DataBase Connector")
window.geometry("330x500")

publish_date_label = tk.Label(window, text="date:")
publish_date_entry = DateEntry(window)

description_label = tk.Label(window, text="description:")
description_entry = tk.Entry(window)

user_label = tk.Label(window, text="user :")

user_id_label = tk.Label(window, text="user id:")

users_collection = db['user']
user = users_collection.distinct('_id')

user_id_combobox = ttk.Combobox(window, values=user)
user_id_combobox.set("select")
user_id_combobox.grid(row=3, column=1, padx=20)

fname_label = tk.Label(window, text="first name:")
fname_entry = tk.Entry(window)

lname_label = tk.Label(window, text="last name:")
lname_entry = tk.Entry(window)

tag_label = tk.Label(window, text="tag :")

tag_id_label = tk.Label(window, text="tag id:")

tags_collection = db['tag']
tag = tags_collection.distinct('_id')

tag_id_combobox = ttk.Combobox(window, values=tag)
tag_id_combobox.set("select")
tag_id_combobox.grid(row=3, column=1, padx=20)

tag_title_label = tk.Label(window, text="tag title:")
tag_title_entry = tk.Entry(window)

document_link_label = tk.Label(window, text="document link:")

relatedpart_label = tk.Label(window, text="related part:")
relatedpart_entry = tk.Entry(window)

description_doc_label = tk.Label(window, text="description:")
description_doc_entry = tk.Entry(window)

repository_doc_label = tk.Label(window, text="repository:")
repository_doc_entry = tk.Entry(window)

media_link_label= tk.Label(window, text="media link:")

start_at_label = tk.Label(window, text="start at:")
start_at_entry = tk.Entry(window)

end_at_label = tk.Label(window, text="end at:")
end_at_entry = tk.Entry(window)

description_media_label = tk.Label(window, text="description:")
description_media_entry = tk.Entry(window)

repository_media_label = tk.Label(window, text="repository:")
repository_media_entry = tk.Entry(window)

doc_id_label = tk.Label(window, text="doc id:")

docs_collection = db['activity']
doc = docs_collection.distinct('_id')

doc_id_combobox = ttk.Combobox(window, values=doc)
doc_id_combobox.set("select")
doc_id_combobox.grid(row=3, column=1, padx=20)

#############################################################
publish_date_label.grid(row=0, column=0, padx=20, sticky="w")
publish_date_entry.grid(row=0, column=1, padx=20)

description_label.grid(row=1, column=0, padx=20, sticky="w")
description_entry.grid(row=1, column=1, padx=20)

user_label.grid(row=2, column=0, padx=20, sticky="w") 

user_id_label.grid(row=3, column=0, padx=36, sticky="w") 
user_id_combobox.grid(row=3, column=0, padx=36, sticky="w")
user_id_combobox.grid(row=3, column=1, padx=20)

fname_label.grid(row=4, column=0, padx=36, sticky="w")
fname_entry.grid(row=4, column=1, padx=20)

lname_label.grid(row=5, column=0, padx=36, sticky="w")
lname_entry.grid(row=5, column=1, padx=20)

tag_label.grid(row=6, column=0, padx=20, sticky="w") 

tag_id_label.grid(row=7, column=0, padx=36, sticky="w") 
tag_id_combobox.grid(row=7, column=0, padx=36, sticky="w")
tag_id_combobox.grid(row=7, column=1, padx=20)

tag_title_label.grid(row=8, column=0,padx=36, sticky="w")
tag_title_entry.grid(row=8, column=1, padx=20)

document_link_label.grid(row=9, column=0, padx=20, sticky="w") 

relatedpart_label.grid(row=10, column=0, padx=36, sticky="w")
relatedpart_entry.grid(row=10, column=1, padx=20)

description_doc_label.grid(row=11, column=0,padx=36 , sticky="w")
description_doc_entry.grid(row=11, column=1, padx=20)

repository_doc_label.grid(row=12, column=0,padx=36 , sticky="w")
repository_doc_entry.grid(row=12, column=1, padx=20)

media_link_label.grid(row=13, column=0, padx=20, sticky="w") 

start_at_label.grid(row=14, column=0,padx=36 , sticky="w")
start_at_entry.grid(row=14, column=1, padx=20)

end_at_label.grid(row=15, column=0,padx=36 , sticky="w")
end_at_entry.grid(row=15, column=1, padx=20)

description_media_label.grid(row=16, padx=36 , column=0, sticky="w")
description_media_entry.grid(row=16, column=1, padx=20)

repository_media_label.grid(row=17, column=0,padx=36 , sticky="w")
repository_media_entry.grid(row=17, column=1, padx=20)

doc_id_label.grid(row=19, column=0, padx=36, pady=10, sticky="w") 
doc_id_combobox.grid(row=19, column=0, padx=36, pady=10, sticky="w")
doc_id_combobox.grid(row=19, column=1, padx=20, pady=10)

########################################################################

button_frame = tk.Frame(window)
button_frame.grid(row=21, column=0, columnspan=2, pady=10)

submit_button = tk.Button(button_frame, text="insert", command=insert_document)
delete_button = tk.Button(button_frame, text="delete", command=delete_document)
show_activities_button = tk.Button(button_frame, text="select", command=get_user_activities)
update_button = tk.Button(button_frame, text="update", command=update_document)

submit_button.grid(row=0, column=0, padx=10, pady=20)
delete_button.grid(row=0, column=1, padx=10, pady=20)
show_activities_button.grid(row=0, column=2, padx=10, pady=20)
update_button.grid(row=0, column=3, padx=10, pady=20)

window.mainloop()
