class Action():    
    def __init__(self, action_name, mode='onboard'):
        self.action_name = action_name
        self.mode = mode

    def exec(self, conn, **kwargs):
        raise NotImplementedError
    def get_name(self):
        return self.action_name
    
    def set_test_input(self, data):
        self.test_msg = data
        return

    def read_input(self, conn, show_str):
        if self.mode == 'onboard':
            ret = conn.send(f'[INPUT]Please enter {show_str}: '.encode('utf-8'))
            recv_msg = conn.recv(100).decode("utf-8")
        else:
            recv_msg = self.test_msg[show_str]
        return recv_msg
    
    def send_table(self, conn, table): 
        # Since the table is too long, buffer size is not enough for client to receive the whole message.
        # Add a [END] tag to mark the end of the message
        conn.sendall(("[TABLE]" + '\n' + table + '\n' + "[END]").encode('utf-8'))

        