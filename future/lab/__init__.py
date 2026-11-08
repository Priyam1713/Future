"""Future Lab v1: discovery, native execution and explicit eligible experiments."""
from .registry import registry,list_techniques,capability
from .invocation import invoke,validate_request
from .experiments import create,forecast,resolve,replay,persist
from .evaluation import evaluate,compare,markdown
__all__=['registry','list_techniques','capability','invoke','validate_request','create','forecast','resolve','replay','persist','evaluate','compare','markdown']
