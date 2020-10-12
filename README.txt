Key Value Storage Script(R) Version 1.0 05/10/2020


GENERAL USAGE NOTES:
--------------------

- This script can connect with system of databases, which can
get, set, delete data by keys.

- Databases have limit of items, which stated by second argument
in initialization database.

- Item can't have more than ITEM_MAX_SIZE length.

- Work with databases is performed via http.

- Work with databases is doing via kvs.py and his arguments:
	-h, --help            
		show this help message and exit
	-sa SET_ADDRESS, --set_address SET_ADDRESS 
		set address to connect db
	-sp SET_PORT, --set_port SET_PORT 
		set port to connect db
	-cs, --check_selected 
		check selected address and port
	-c CREATE, --create CREATE 
		create the database
	-dd DELETE_DATABASE, --delete_database DELETE_DATABASE 
		delete the database
	-ld, --list_databases 
		list of existing databases
	-sd SELECT_DATABASE, --select_database SELECT_DATABASE 
		select the database to work with
	-s SET SET, --set SET SET 
		set value with key in selected database
	-g GET [GET ...], --get GET [GET ...] 
		get value by key in selected database
	-d DELETE, --delete DELETE 
		delete item by key in selected database
	-l, --list 
		get list of items in selected database
	-ss START_SERVER, --start_server START_SERVER 
		starts local server with chosen port(write "exit"
					     to shut down server)
----------------------------------------------------------------

This script works under Linux, MacOS, Windows by Python 3.
But after starting server in Windows opens cmd in current cmd.
On other OS after starting server you should open new terminal.
================================================================


Contacts:

Voice: +79527326662
VK: vk.com/xaspy
E-mail: 20kolpakov01@gmail.com