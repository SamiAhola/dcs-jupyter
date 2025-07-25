import socket

from ipykernel.kernelbase import Kernel

from dcs_jupyter.connection import DCSConnection, LuaExecutionError

# Configuration constants - edit these for custom setups
SOCKET_ADDR = '127.0.0.1'
PORT = 8042


class DcsKernel(Kernel):
    implementation = 'DCS'
    implementation_version = '0.1'
    language_info = {
        'name': 'lua',
        'version': '5.1',
        'mimetype': 'text/plain',
        'file_extension': '.lua',
    }
    banner = 'DCS kernel.'

    def __init__(self, *args, **kwargs):
        self.dcs = DCSConnection(host=SOCKET_ADDR, port=PORT)
        super().__init__(*args, **kwargs)

    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
        try:
            ret_val = self.dcs.execute(code)
            status = 'ok'
        except LuaExecutionError as e:
            ret_val = str(e)
            status = 'error'
        except socket.timeout:
            ret_val = f'<< DCS connection timeout ({SOCKET_ADDR}:{PORT})>>'
            status = 'error'
        except KeyboardInterrupt:
            ret_val = '<< Interrupted >>'
            status = 'aborted'
        except Exception as e:
            ret_val = f'<< Other exception occurred: {type(e).__name__}: {e} >>'
            status = 'error'
        finally:
            if not silent:
                stream_content = {'name': 'stdout', 'text': ret_val}
                self.send_response(self.iopub_socket, 'stream', stream_content)
        
        return {
            'status': status,
            'execution_count': self.execution_count,  # The base class increments the execution count
            'payload': [],
            'user_expressions': {},
        }

    def do_shutdown(self, restart):
        self.dcs.disconnect()
        return {'status': 'ok', 'restart': restart}


if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp

    IPKernelApp.launch_instance(kernel_class=DcsKernel)
