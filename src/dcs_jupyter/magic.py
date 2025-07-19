"""IPython magic commands for DCS integration."""
from IPython.core.magic import line_cell_magic, Magics, magics_class
from IPython.core.magic import output_can_be_silenced, needs_local_scope, no_var_expand

from dcs_jupyter.connection import DCSConnection


@magics_class
class DCSMagics(Magics):
    """Magic commands for DCS integration in Python notebooks."""
    
    def __init__(self, shell, host='127.0.0.1', port=8042, timeout=10.0):
        super().__init__(shell)
        self.dcs = DCSConnection(host=host, port=port, timeout=timeout)
    
    @line_cell_magic
    @output_can_be_silenced
    @needs_local_scope
    @no_var_expand
    def dcs(self, line, cell=None, local_ns=None):
        """
        Execute Lua code in DCS World.
        
        Usage:
        %%dcs
        -- Your Lua code here
        trigger.action.outText("Hello from Python notebook!", 5)
        
        Or single line:
        %dcs return timer.getTime()
        """
        # Use cell content if available, otherwise use line
        lua_code = cell if cell is not None else line
        
        result = self.dcs.execute(lua_code)
        return result


# Store magic instance for cleanup
_magic_instance = None


def load_ipython_extension(ipython, parameter=None):
    """
    Load the DCS magic extension.
    
    Usage:
    %load_ext dcs_jupyter.magic
    %load_ext dcs_jupyter.magic 192.168.1.100:8080
    """
    global _magic_instance
    
    # Parse parameter for host:port
    host = '127.0.0.1'
    port = 8042
    
    if parameter:
        host, sep, port_str = parameter.partition(':')
        if sep and port_str:
            port = int(port_str)
    
    _magic_instance = DCSMagics(ipython, host=host, port=port)
    ipython.register_magics(_magic_instance)


def unload_ipython_extension(ipython):
    """Unload the DCS magic extension."""
    global _magic_instance
    if _magic_instance:
        _magic_instance.dcs.disconnect()
        _magic_instance = None
