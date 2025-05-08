from mcp_table_editor.handler._base_handler import BaseHandler
from mcp_table_editor.handler._crud_handler import CrudHandler
from mcp_table_editor.handler._delete_content_handler import DeleteContentHandler
from mcp_table_editor.handler._drop_content_handler import DropContentHandler
from mcp_table_editor.handler._get_content_handler import GetContentHandler
from mcp_table_editor.handler._insert_cell_handler import InsertContentHandler
from mcp_table_editor.handler._remove_content_handler import RemoveContentHandler
from mcp_table_editor.handler._sort_by_value_handler import SortByValueHandler
from mcp_table_editor.handler._sort_handler import SortHandler
from mcp_table_editor.handler._update_content_handler import UpdateContentHandler

TOOL_HANDLERS: list[type[BaseHandler]] = [
    CrudHandler,
    GetContentHandler,
    UpdateContentHandler,
    InsertContentHandler,
    DeleteContentHandler,
    RemoveContentHandler,
    DropContentHandler,
    SortHandler,
    SortByValueHandler,
]

TOOL_HANDLERS_DICT: dict[str, type[BaseHandler]] = {
    handler.name: handler for handler in TOOL_HANDLERS
}

__all__ = [
    "BaseHandler",
    "CrudHandler",
    "GetContentHandler",
    "UpdateContentHandler",
    "InsertContentHandler",
    "DeleteContentHandler",
    "RemoveContentHandler",
    "DropContentHandler",
    "SortHandler",
    "SortByValueHandler",
    "TOOL_HANDLERS",
]
