from tkinter import Tk, messagebox, StringVar
import psycopg2
import tkinter.ttk as ttk
from time import sleep
from threading import Thread


def db_connect():
    conn = psycopg2.connect(
        host="172.18.17.236",
        database="g2",
        user="g2",
        password="123456",
        options="-c search_path=dbo,kms"
    )
    return conn


def tab_info():
    global selected_id
    global table_name
    global table_data
    index = nb.index(nb.select())
    if index == 0:
        selected_id = document_link_id_entry.get()
        table_name = 'document_link'
        table_data = {
            'related_part': document_link_related_part_entry.get(),
            'description': document_link_description_entry.get(),
            'main_id': document_link_main_id_entry.get(),
            'repository_id': document_link_repository_id_entry.get(),
        }
    if index == 1:
        selected_id = main_id_entry.get()
        table_name = 'main'
        table_data = {
            'title': main_title_entry.get(),
            'publish_date': main_publish_date_entry.get(),
            'description': main_description_entry.get(),
            'user_id': main_user_id_entry.get(),
            'tree_id': main_tree_id_entry.get(),
        }
    if index == 2:
        selected_id = media_link_id_entry.get()
        table_name = 'media_link'
        table_data = {
            'start_at': media_link_start_time_entry.get(),
            'end_at': media_link_end_time_entry.get(),
            'description': media_link_description_entry.get(),
            'media_id': media_link_main_id_entry.get(),
            'repository_id': media_link_repository_id_entry.get(),
        }
    if index == 3:
        selected_id = position_id_entry.get()
        table_name = 'position'
        table_data = {
            'title': position_title_entry.get(),
            'description': position_description_entry.get(),
        }
    if index == 4:
        selected_id = position_link_id_entry.get()
        table_name = 'position_link'
        table_data = {
            'appointment_date': position_link_apointment_date_entry.get(),
            'dismissal_date': position_link_dismissal_date_entry.get(),
            'user_id': position_link_user_id_entry.get(),
            'position_id': position_link_position_id_entry.get(),
        }
    if index == 5:
        selected_id = repository_id_entry.get()
        table_name = 'repository'
        table_data = {
            'name': repository_name_entry.get(),
            'type': repository_type_entry.get(),
            'url': repository_url_entry.get(),
            'description': repository_description_entry.get(),
        }
    if index == 6:
        selected_id = tag_id_entry.get()
        table_name = 'tag'
        table_data = {
            'title': tag_title_entry.get(),
            'publish_date': tag_publish_date_entry.get(),
            'description': tag_description_entry.get(),
        }
    if index == 7:
        selected_id = tag_link_id_entry.get()
        table_name = 'tag_link'
        table_data = {
            'main_id': tag_link_main_id_entry.get(),
            'tag_id': tag_link_tag_id_entry.get(),
        }
    if index == 8:
        selected_id = tree_id_entry.get()
        table_name = 'tree'
        table_data = {
            'title': tag_title_entry.get(),
            'code': tree_code_entry.get(),
            'root_code': tree_code_entry.get(),
        }
    if index == 9:
        selected_id = user_id_entry.get()
        table_name = 'user'
        table_data = {
            'first_name': user_first_name_entry.get(),
            'last_name': user_last_name_entry.get(),
            'national_code': user_national_code_entry.get(),
            'phone_number': user_phone_entry.get(),
            'username': user_username_entry.get(),
            'password': user_password_entry.get(),
            'evidence': user_evidence_entry.get(),
            'email': user_email_entry.get(),
        }


def insert_data():
    try:
        tab_info()
        conn = db_connect()

        values = str(list(table_data.values()))
        values = values.replace('\'\'', 'null')
        values = selected_id + ", " + values[1:-1]

        keys = table_name + "_id"
        for item in list(table_data.keys()):
            keys = keys + ", " + item

        cur = conn.cursor()
        cur.execute(f"INSERT INTO {table_name} ({keys}) VALUES ({values})")
        conn.commit()
        cur.close()
        MASSAGE_TEXT.set("Data inserted successfully")
    except:
        MASSAGE_TEXT.set("Failed to insert data")
    Thread(target=reset_status).start()


def select_data():
    try:
        tab_info()
        conn = db_connect()

        cur = conn.cursor()
        cur.execute("SELECT * FROM "+ table_name)
        rows = cur.fetchall()
        cur.close()
        MASSAGE_TEXT.set("Data selected successfully")
        messagebox.showinfo("Data", str(rows))
    except:
        MASSAGE_TEXT.set("Failed to select data")
    Thread(target=reset_status).start()


def update_data():
    try:
        tab_info()
        conn = db_connect()

        query=''
        for key, value in table_data.items():
            query = query +", "+ key +" = '"+ value +"'"
        query = query[2:]
        query = query.replace('\'\'', 'null')
        
        cur = conn.cursor()
        cur.execute(f"UPDATE {table_name} SET {query} WHERE {table_name}_id = {selected_id}")
        conn.commit()
        cur.close()
        MASSAGE_TEXT.set("Data updated successfully")
    except:
        MASSAGE_TEXT.set("Failed to update data")
    Thread(target=reset_status).start()


def delete_data():
    try:
        tab_info()
        conn = db_connect()

        cur = conn.cursor()
        cur.execute(f"DELETE FROM {table_name} WHERE {table_name}_id = {selected_id}")
        conn.commit()
        cur.close()
        MASSAGE_TEXT.set("Data deleted successfully")
    except:
        MASSAGE_TEXT.set("Failed to delete data")
    Thread(target=reset_status).start()


def exe_query():
    try:
        tab_info()
        conn = db_connect()

        is_select = False
        cur = conn.cursor()
        query = query_entry.get()
        cur.execute(query)
        try:
            rows = cur.fetchall()
            is_select = True
        except:
            pass
        cur.close()
        MASSAGE_TEXT.set("The query executed successfully")
        if is_select:
            messagebox.showinfo("Data", str(rows))
    except:
        MASSAGE_TEXT.set("Failed to execute query")
    Thread(target=reset_status).start()


table_list = {
    'Document Link': 'document_link',
    'Main': 'main',
    'Media Link': 'media_link',
    'Position': 'position',
    'Position Link': 'position_link',
    'Repository': 'repository',
    'Tag': 'tag',
    'Tag Link': 'tag_link',
    'Tree': 'tree',
    'User': 'user'
}


window = Tk()
window.title("SQL Database")

window.minsize(630, 0)

style = ttk.Style()
style.theme_use('clam')
style.configure('TLabel', font=('Helvetica', 11), padding=5)
style.configure("Info.TLabel", font=('Helvetica', 9), foreground='#8a8475')
style.configure('TEntry', font=('Helvetica', 12), padding=5)

def reset_status():
    sleep(4)
    MASSAGE_TEXT.set("...")
MASSAGE_TEXT = StringVar(window, "...")
LAST_ROW = 0

nb = ttk.Notebook(window, padding=5)

for key, value in table_list.items():

    tab = ttk.Frame(nb, padding=5)
    
    if key=='Document Link':
        document_link_id_label = ttk.Label(tab, text="ID")
        document_link_id_label.grid(row=0, column=0, sticky='w', pady=2)
        document_link_id_entry = ttk.Entry(tab)
        document_link_id_entry.grid(row=0, column=1, pady=2)
        ttk.Label(tab, text="Integer", style='Info.TLabel').grid(row=0, column=2)
        ttk.Label(tab, text="*", style='Info.TLabel').grid(row=0, column=3)

        document_link_related_part_label = ttk.Label(tab, text="Related Part")
        document_link_related_part_label.grid(row=1, column=0, sticky='w', pady=2)
        document_link_related_part_entry = ttk.Entry(tab)
        document_link_related_part_entry.grid(row=1, column=1, pady=2)
        ttk.Label(tab, text="String", style='Info.TLabel').grid(row=1, column=2)
        ttk.Label(tab, text="*", style='Info.TLabel').grid(row=1, column=3)

        document_link_description_label = ttk.Label(tab, text="Description")
        document_link_description_label.grid(row=2, column=0, sticky='w', pady=2)
        document_link_description_entry = ttk.Entry(tab)
        document_link_description_entry.grid(row=2, column=1, pady=2)
        ttk.Label(tab, text="String", style='Info.TLabel').grid(row=2, column=2)

        document_link_main_id_label = ttk.Label(tab, text="Main ID")
        document_link_main_id_label.grid(row=3, column=0, sticky='w', pady=2)
        document_link_main_id_entry = ttk.Entry(tab)
        document_link_main_id_entry.grid(row=3, column=1, pady=2)
        ttk.Label(tab, text="Integer", style='Info.TLabel').grid(row=3, column=2)
        ttk.Label(tab, text="*", style='Info.TLabel').grid(row=3, column=3)

        document_link_repository_id_label = ttk.Label(tab, text="Repository ID")
        document_link_repository_id_label.grid(row=4, column=0, sticky='w', pady=2)
        document_link_repository_id_entry = ttk.Entry(tab)
        document_link_repository_id_entry.grid(row=4, column=1, pady=2)
        ttk.Label(tab, text="Integer", style='Info.TLabel').grid(row=4, column=2)
        ttk.Label(tab, text="*", style='Info.TLabel').grid(row=4, column=3)
    
    if key=='Main':
        main_id_label = ttk.Label(tab, text="ID")
        main_id_label.grid(row=0, column=0, sticky='w', pady=2)
        main_id_entry = ttk.Entry(tab)
        main_id_entry.grid(row=0, column=1, pady=2)
        ttk.Label(tab, text="Integer", style='Info.TLabel').grid(row=0, column=2)
        ttk.Label(tab, text="*", style='Info.TLabel').grid(row=0, column=3)

        main_title_label = ttk.Label(tab, text="Title")
        main_title_label.grid(row=1, column=0, sticky='w', pady=2)
        main_title_entry = ttk.Entry(tab)
        main_title_entry.grid(row=1, column=1, pady=2)
        ttk.Label(tab, text="String", style='Info.TLabel').grid(row=1, column=2)
        ttk.Label(tab, text="*", style='Info.TLabel').grid(row=1, column=3)

        main_publish_date_label = ttk.Label(tab, text="Publish Date")
        main_publish_date_label.grid(row=2, column=0, sticky='w', pady=2)
        main_publish_date_entry = ttk.Entry(tab)
        main_publish_date_entry.grid(row=2, column=1, pady=2)
        ttk.Label(tab, text="Date", style='Info.TLabel').grid(row=2, column=2)
        ttk.Label(tab, text="*", style='Info.TLabel').grid(row=2, column=3)

        main_description_label = ttk.Label(tab, text="Description")
        main_description_label.grid(row=3, column=0, sticky='w', pady=2)
        main_description_entry = ttk.Entry(tab)
        main_description_entry.grid(row=3, column=1, pady=2)
        ttk.Label(tab, text="String", style='Info.TLabel').grid(row=3, column=2)

        main_user_id_label = ttk.Label(tab, text="User ID")
        main_user_id_label.grid(row=4, column=0, sticky='w', pady=2)
        main_user_id_entry = ttk.Entry(tab)
        main_user_id_entry.grid(row=4, column=1, pady=2)
        ttk.Label(tab, text="Integer", style='Info.TLabel').grid(row=4, column=2)
        ttk.Label(tab, text="*", style='Info.TLabel').grid(row=4, column=3)

        main_tree_id_label = ttk.Label(tab, text="Tree ID")
        main_tree_id_label.grid(row=5, column=0, sticky='w', pady=2)
        main_tree_id_entry = ttk.Entry(tab)
        main_tree_id_entry.grid(row=5, column=1, pady=2)
        ttk.Label(tab, text="Integer", style='Info.TLabel').grid(row=5, column=2)
        ttk.Label(tab, text="*", style='Info.TLabel').grid(row=5, column=3)

    if key=='Media Link':
        media_link_id_label = ttk.Label(tab, text="ID")
        media_link_id_label.grid(row=0, column=0, sticky='w', pady=2)
        media_link_id_entry = ttk.Entry(tab)
        media_link_id_entry.grid(row=0, column=1, pady=2)
        ttk.Label(tab, text="Integer", style='Info.TLabel').grid(row=0, column=2)
        ttk.Label(tab, text="*", style='Info.TLabel').grid(row=0, column=3)

        media_link_start_time_label = ttk.Label(tab, text="Start Time")
        media_link_start_time_label.grid(row=1, column=0, sticky='w', pady=2)
        media_link_start_time_entry = ttk.Entry(tab)
        media_link_start_time_entry.grid(row=1, column=1, pady=2)
        ttk.Label(tab, text="Time", style='Info.TLabel').grid(row=1, column=2)
        ttk.Label(tab, text="*", style='Info.TLabel').grid(row=1, column=3)

        media_link_end_time_label = ttk.Label(tab, text="End Time")
        media_link_end_time_label.grid(row=2, column=0, sticky='w', pady=2)
        media_link_end_time_entry = ttk.Entry(tab)
        media_link_end_time_entry.grid(row=2, column=1, pady=2)
        ttk.Label(tab, text="Time", style='Info.TLabel').grid(row=2, column=2)
        ttk.Label(tab, text="*", style='Info.TLabel').grid(row=2, column=3)
        
        media_link_description_label = ttk.Label(tab, text="Description")
        media_link_description_label.grid(row=3, column=0, sticky='w', pady=2)
        media_link_description_entry = ttk.Entry(tab)
        media_link_description_entry.grid(row=3, column=1, pady=2)
        ttk.Label(tab, text="String", style='Info.TLabel').grid(row=3, column=2)

        media_link_main_id_label = ttk.Label(tab, text="Main ID")
        media_link_main_id_label.grid(row=4, column=0, sticky='w', pady=2)
        media_link_main_id_entry = ttk.Entry(tab)
        media_link_main_id_entry.grid(row=4, column=1, pady=2)
        ttk.Label(tab, text="Integer", style='Info.TLabel').grid(row=4, column=2)
        ttk.Label(tab, text="*", style='Info.TLabel').grid(row=4, column=3)

        media_link_repository_id_label = ttk.Label(tab, text="Repository ID")
        media_link_repository_id_label.grid(row=5, column=0, sticky='w', pady=2)
        media_link_repository_id_entry = ttk.Entry(tab)
        media_link_repository_id_entry.grid(row=5, column=1, pady=2)
        ttk.Label(tab, text="Integer", style='Info.TLabel').grid(row=5, column=2)
        ttk.Label(tab, text="*", style='Info.TLabel').grid(row=5, column=3)

    if key=='Position':
        position_id_label = ttk.Label(tab, text="ID")
        position_id_label.grid(row=0, column=0, sticky='w', pady=2)
        position_id_entry = ttk.Entry(tab)
        position_id_entry.grid(row=0, column=1, pady=2)
        ttk.Label(tab, text="Integer", style='Info.TLabel').grid(row=0, column=2)
        ttk.Label(tab, text="*", style='Info.TLabel').grid(row=0, column=3)

        position_title_label = ttk.Label(tab, text="Title")
        position_title_label.grid(row=1, column=0, sticky='w', pady=2)
        position_title_entry = ttk.Entry(tab)
        position_title_entry.grid(row=1, column=1, pady=2)
        ttk.Label(tab, text="String", style='Info.TLabel').grid(row=1, column=2)
        ttk.Label(tab, text="*", style='Info.TLabel').grid(row=1, column=3)

        position_description_label = ttk.Label(tab, text="Description")
        position_description_label.grid(row=2, column=0, sticky='w', pady=2)
        position_description_entry = ttk.Entry(tab)
        position_description_entry.grid(row=2, column=1, pady=2)
        ttk.Label(tab, text="String", style='Info.TLabel').grid(row=2, column=2)

    if key=='Position Link':
        position_link_id_label = ttk.Label(tab, text="ID")
        position_link_id_label.grid(row=0, column=0, sticky='w', pady=2)
        position_link_id_entry = ttk.Entry(tab)
        position_link_id_entry.grid(row=0, column=1, pady=2)
        ttk.Label(tab, text="Integer", style='Info.TLabel').grid(row=0, column=2)
        ttk.Label(tab, text="*", style='Info.TLabel').grid(row=0, column=3)

        position_link_apointment_date_label = ttk.Label(tab, text="Appointment Date")
        position_link_apointment_date_label.grid(row=1, column=0, sticky='w', pady=2)
        position_link_apointment_date_entry = ttk.Entry(tab)
        position_link_apointment_date_entry.grid(row=1, column=1, pady=2)
        ttk.Label(tab, text="Date", style='Info.TLabel').grid(row=1, column=2)
        ttk.Label(tab, text="*", style='Info.TLabel').grid(row=1, column=3)

        position_link_dismissal_date_label = ttk.Label(tab, text="Dismissal Date")
        position_link_dismissal_date_label.grid(row=2, column=0, sticky='w', pady=2)
        position_link_dismissal_date_entry = ttk.Entry(tab)
        position_link_dismissal_date_entry.grid(row=2, column=1, pady=2)
        ttk.Label(tab, text="Date", style='Info.TLabel').grid(row=2, column=2)
        ttk.Label(tab, text="*", style='Info.TLabel').grid(row=2, column=3)

        position_link_user_id_label = ttk.Label(tab, text="User ID")
        position_link_user_id_label.grid(row=3, column=0, sticky='w', pady=2)
        position_link_user_id_entry = ttk.Entry(tab)
        position_link_user_id_entry.grid(row=3, column=1, pady=2)
        ttk.Label(tab, text="Integer", style='Info.TLabel').grid(row=3, column=2)
        ttk.Label(tab, text="*", style='Info.TLabel').grid(row=3, column=3)

        position_link_position_id_label = ttk.Label(tab, text="Position ID")
        position_link_position_id_label.grid(row=4, column=0, sticky='w', pady=2)
        position_link_position_id_entry = ttk.Entry(tab)
        position_link_position_id_entry.grid(row=4, column=1, pady=2)
        ttk.Label(tab, text="Integer", style='Info.TLabel').grid(row=4, column=2)
        ttk.Label(tab, text="*", style='Info.TLabel').grid(row=4, column=3)

    if key=='Repository':
        repository_id_label = ttk.Label(tab, text="ID")
        repository_id_label.grid(row=0, column=0, sticky='w', pady=2)
        repository_id_entry = ttk.Entry(tab)
        repository_id_entry.grid(row=0, column=1, pady=2)
        ttk.Label(tab, text="Integer", style='Info.TLabel').grid(row=0, column=2)
        ttk.Label(tab, text="*", style='Info.TLabel').grid(row=0, column=3)

        repository_name_label = ttk.Label(tab, text="Name")
        repository_name_label.grid(row=1, column=0, sticky='w', pady=2)
        repository_name_entry = ttk.Entry(tab)
        repository_name_entry.grid(row=1, column=1, pady=2)
        ttk.Label(tab, text="String", style='Info.TLabel').grid(row=1, column=2)
        ttk.Label(tab, text="*", style='Info.TLabel').grid(row=1, column=3)

        repository_type_label = ttk.Label(tab, text="Type")
        repository_type_label.grid(row=2, column=0, sticky='w', pady=2)
        repository_type_entry = ttk.Entry(tab)
        repository_type_entry.grid(row=2, column=1, pady=2)
        position_description_entry.grid(row=2, column=1, pady=2)
        ttk.Label(tab, text="String", style='Info.TLabel').grid(row=2, column=2)
        ttk.Label(tab, text="*", style='Info.TLabel').grid(row=2, column=3)

        repository_url_label = ttk.Label(tab, text="Url")
        repository_url_label.grid(row=3, column=0, sticky='w', pady=2)
        repository_url_entry = ttk.Entry(tab)
        repository_url_entry.grid(row=3, column=1, pady=2)
        ttk.Label(tab, text="String", style='Info.TLabel').grid(row=3, column=2)
        ttk.Label(tab, text="*", style='Info.TLabel').grid(row=3, column=3)
        
        repository_description_label = ttk.Label(tab, text="Description")
        repository_description_label.grid(row=4, column=0, sticky='w', pady=2)
        repository_description_entry = ttk.Entry(tab)
        repository_description_entry.grid(row=4, column=1, pady=2)
        ttk.Label(tab, text="String", style='Info.TLabel').grid(row=4, column=2)

    if key=='Tag':
        tag_id_label = ttk.Label(tab, text="ID")
        tag_id_label.grid(row=0, column=0, sticky='w', pady=2)
        tag_id_entry = ttk.Entry(tab)
        tag_id_entry.grid(row=0, column=1, pady=2)
        ttk.Label(tab, text="Integer", style='Info.TLabel').grid(row=0, column=2)
        ttk.Label(tab, text="*", style='Info.TLabel').grid(row=0, column=3)

        tag_title_label = ttk.Label(tab, text="Title")
        tag_title_label.grid(row=1, column=0, sticky='w', pady=2)
        tag_title_entry = ttk.Entry(tab)
        tag_title_entry.grid(row=1, column=1, pady=2)
        ttk.Label(tab, text="String", style='Info.TLabel').grid(row=1, column=2)
        ttk.Label(tab, text="*", style='Info.TLabel').grid(row=1, column=3)

        tag_publish_date_label = ttk.Label(tab, text="Publish Date")
        tag_publish_date_label.grid(row=2, column=0, sticky='w', pady=2)
        tag_publish_date_entry = ttk.Entry(tab)
        tag_publish_date_entry.grid(row=2, column=1, pady=2)
        ttk.Label(tab, text="String", style='Info.TLabel').grid(row=2, column=2)

        tag_description_label = ttk.Label(tab, text="Description")
        tag_description_label.grid(row=3, column=0, sticky='w', pady=2)
        tag_description_entry = ttk.Entry(tab)
        tag_description_entry.grid(row=3, column=1, pady=2)
        ttk.Label(tab, text="String", style='Info.TLabel').grid(row=3, column=2)

    if key=='Tag Link':
        tag_link_id_label = ttk.Label(tab, text="ID")
        tag_link_id_label.grid(row=0, column=0, sticky='w', pady=2)
        tag_link_id_entry = ttk.Entry(tab)
        tag_link_id_entry.grid(row=0, column=1, pady=2)
        ttk.Label(tab, text="Integer", style='Info.TLabel').grid(row=0, column=2)
        ttk.Label(tab, text="*", style='Info.TLabel').grid(row=0, column=3)

        tag_link_tag_id_label = ttk.Label(tab, text="Tag ID")
        tag_link_tag_id_label.grid(row=1, column=0, sticky='w', pady=2)
        tag_link_tag_id_entry = ttk.Entry(tab)
        tag_link_tag_id_entry.grid(row=1, column=1, pady=2)
        ttk.Label(tab, text="Integer", style='Info.TLabel').grid(row=1, column=2)
        ttk.Label(tab, text="*", style='Info.TLabel').grid(row=1, column=3)
        
        tag_link_main_id_label = ttk.Label(tab, text="Main ID")
        tag_link_main_id_label.grid(row=2, column=0, sticky='w', pady=2)
        tag_link_main_id_entry = ttk.Entry(tab)
        tag_link_main_id_entry.grid(row=2, column=1, pady=2)
        ttk.Label(tab, text="Integer", style='Info.TLabel').grid(row=2, column=2)
        ttk.Label(tab, text="*", style='Info.TLabel').grid(row=2, column=3)

    if key=='Tree':
        tree_id_label = ttk.Label(tab, text="ID")
        tree_id_label.grid(row=0, column=0, sticky='w', pady=2)
        tree_id_entry = ttk.Entry(tab)
        tree_id_entry.grid(row=0, column=1, pady=2)
        ttk.Label(tab, text="Integer", style='Info.TLabel').grid(row=0, column=2)
        ttk.Label(tab, text="*", style='Info.TLabel').grid(row=0, column=3)

        tree_title_label = ttk.Label(tab, text="Title")
        tree_title_label.grid(row=1, column=0, sticky='w', pady=2)
        tree_title_entry = ttk.Entry(tab)
        tree_title_entry.grid(row=1, column=1, pady=2)
        ttk.Label(tab, text="String", style='Info.TLabel').grid(row=1, column=2)
        ttk.Label(tab, text="*", style='Info.TLabel').grid(row=1, column=3)

        tree_code_label = ttk.Label(tab, text="Code")
        tree_code_label.grid(row=2, column=0, sticky='w', pady=2)
        tree_code_entry = ttk.Entry(tab)
        tree_code_entry.grid(row=2, column=1, pady=2)
        ttk.Label(tab, text="String", style='Info.TLabel').grid(row=2, column=2)
        ttk.Label(tab, text="*", style='Info.TLabel').grid(row=2, column=3)

        tree_root_code_label = ttk.Label(tab, text="Root Code")
        tree_root_code_label.grid(row=3, column=0, sticky='w', pady=2)
        tree_root_code_entry = ttk.Entry(tab)
        tree_root_code_entry.grid(row=3, column=1, pady=2)
        ttk.Label(tab, text="String", style='Info.TLabel').grid(row=3, column=2)
        ttk.Label(tab, text="*", style='Info.TLabel').grid(row=3, column=3)

    if key=='User':
        user_id_label = ttk.Label(tab, text="ID")
        user_id_label.grid(row=0, column=0, sticky='w', pady=2)
        user_id_entry = ttk.Entry(tab)
        user_id_entry.grid(row=0, column=1, pady=2)
        ttk.Label(tab, text="Integer", style='Info.TLabel').grid(row=0, column=2)
        ttk.Label(tab, text="*", style='Info.TLabel').grid(row=0, column=3)

        user_first_name_label = ttk.Label(tab, text="First Name")
        user_first_name_label.grid(row=1, column=0, sticky='w', pady=2)
        user_first_name_entry = ttk.Entry(tab)
        user_first_name_entry.grid(row=1, column=1, pady=2)
        ttk.Label(tab, text="String", style='Info.TLabel').grid(row=1, column=2)
        ttk.Label(tab, text="*", style='Info.TLabel').grid(row=1, column=3)

        user_last_name_label = ttk.Label(tab, text="Last Name")
        user_last_name_label.grid(row=2, column=0, sticky='w', pady=2)
        user_last_name_entry = ttk.Entry(tab)
        user_last_name_entry.grid(row=2, column=1, pady=2)
        ttk.Label(tab, text="String", style='Info.TLabel').grid(row=2, column=2)
        ttk.Label(tab, text="*", style='Info.TLabel').grid(row=2, column=3)

        user_national_code_label = ttk.Label(tab, text="National Code")
        user_national_code_label.grid(row=3, column=0, sticky='w', pady=2)
        user_national_code_entry = ttk.Entry(tab)
        user_national_code_entry.grid(row=3, column=1, pady=2)
        ttk.Label(tab, text="Integer", style='Info.TLabel').grid(row=3, column=2)
        ttk.Label(tab, text="*", style='Info.TLabel').grid(row=3, column=3)

        user_phone_label = ttk.Label(tab, text="Phone Number")
        user_phone_label.grid(row=4, column=0, sticky='w', pady=2)
        user_phone_entry = ttk.Entry(tab)
        user_phone_entry.grid(row=4, column=1, pady=2)
        ttk.Label(tab, text="Integer", style='Info.TLabel').grid(row=4, column=2)
        ttk.Label(tab, text="*", style='Info.TLabel').grid(row=4, column=3)
        
        user_username_label = ttk.Label(tab, text="Username")
        user_username_label.grid(row=5, column=0, sticky='w', pady=2)
        user_username_entry = ttk.Entry(tab)
        user_username_entry.grid(row=5, column=1, pady=2)
        ttk.Label(tab, text="String", style='Info.TLabel').grid(row=5, column=2)
        ttk.Label(tab, text="*", style='Info.TLabel').grid(row=5, column=3)
        
        user_password_label = ttk.Label(tab, text="Password")
        user_password_label.grid(row=6, column=0, sticky='w', pady=2)
        user_password_entry = ttk.Entry(tab)
        user_password_entry.grid(row=6, column=1, pady=2)
        ttk.Label(tab, text="String", style='Info.TLabel').grid(row=6, column=2)
        ttk.Label(tab, text="*", style='Info.TLabel').grid(row=6, column=3)
        
        user_evidence_label = ttk.Label(tab, text="Evidence")
        user_evidence_label.grid(row=7, column=0, sticky='w', pady=2)
        user_evidence_entry = ttk.Entry(tab)
        user_evidence_entry.grid(row=7, column=1, pady=2)
        ttk.Label(tab, text="String", style='Info.TLabel').grid(row=7, column=2)
        
        user_email_label = ttk.Label(tab, text="Email")
        user_email_label.grid(row=8, column=0, sticky='w', pady=2)
        user_email_entry = ttk.Entry(tab)
        user_email_entry.grid(row=8, column=1, pady=2)
        ttk.Label(tab, text="String", style='Info.TLabel').grid(row=8, column=2)

    nb.add(tab, text=key)

nb.grid(row=LAST_ROW, column=0, columnspan=4, sticky='nsew')
LAST_ROW =+ 1

insert_button = ttk.Button(window, text="Insert", command=insert_data)
insert_button.grid(row=LAST_ROW, column=0, ipadx=30)

select_button = ttk.Button(window, text="Select", command=select_data)
select_button.grid(row=LAST_ROW, column=1, ipadx=30)

update_button = ttk.Button(window, text="Update", command=update_data)
update_button.grid(row=LAST_ROW, column=2, ipadx=30)

delete_button = ttk.Button(window, text="Delete", command=delete_data)
delete_button.grid(row=LAST_ROW, column=3, ipadx=30)
LAST_ROW += 1

query_box = ttk.Labelframe(window, text="Query")
query_box.grid(row=LAST_ROW, column=0, columnspan=3, sticky='nsew', padx=5, pady=5)
query_entry = ttk.Entry(query_box, font=12)
query_entry.pack(fill='both', expand=True)
ttk.Button(window, text="Submit", command=exe_query).grid(row=LAST_ROW, column=3, ipadx=30, pady=(20,0))
LAST_ROW += 1

message_box = ttk.Labelframe(window, text="Status")
message_box.grid(row=LAST_ROW, column=0, columnspan=4, sticky='nsew', padx=5, pady=5)
ttk.Label(message_box, textvariable=MASSAGE_TEXT).pack()
LAST_ROW += 1

window.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform=1)
window.grid_rowconfigure(0, weight=1)
window.configure(bg='#dcdad3')

window.mainloop()
