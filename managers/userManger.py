from collections import deque

class Users():
    q = deque()
    conn_list = {}

    @classmethod
    def get_total_users(cls):
        return len(cls.conn_list)


            



    
    

