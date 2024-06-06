from spyne import Application, rpc, ServiceBase, Unicode, Integer
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import pandas as pd
from wsgiref.simple_server import make_server
from flask import Flask

stored_df_parts = {}
stored_df = None


class DataFrameService(ServiceBase):
    @rpc(Unicode, Integer, Integer, _returns=Unicode)
    def send_dataframe_part(ctx, data, part_index, total_parts):
        if part_index is None or total_parts is None:
            return "Error: part_index and total_parts must be provided"

        global stored_df_parts
        stored_df_parts[part_index] = pd.read_json(data, orient='split')

        if len(stored_df_parts) == total_parts:
            global stored_df
            stored_df = pd.concat([stored_df_parts[i] for i in range(total_parts)])
            stored_df_parts.clear()
            return stored_df.to_json(orient='split')
        return f"Part {part_index + 1}/{total_parts} received"

    @rpc(_returns=Unicode)
    def get_dataframe(ctx):
        global stored_df
        if stored_df is None:
            return "{}"
        return stored_df.to_json(orient='split')


application = Application([DataFrameService], 'spyne.examples.hello.soap',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())
wsgi_application = WsgiApplication(application)

app = Flask(__name__)
app.wsgi_app = wsgi_application
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024 * 1024  # 1GB

if __name__ == '__main__':
    server = make_server('127.0.0.1', 8000, app)
    print("Server is running...")
    server.serve_forever()
