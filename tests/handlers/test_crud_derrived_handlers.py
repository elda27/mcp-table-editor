import pandas as pd
import pytest

from mcp_table_editor.editor import InMemoryEditor, InsertRule
from mcp_table_editor.editor._config import EditorConfig
from mcp_table_editor.handler._delete_content_handler import DeleteContentHandler
from mcp_table_editor.handler._drop_content_handler import DropContentHandler
from mcp_table_editor.handler._get_content_handler import GetContentHandler
from mcp_table_editor.handler._insert_cell_handler import InsertContentHandler
from mcp_table_editor.handler._remove_content_handler import RemoveContentHandler
from mcp_table_editor.handler._update_content_handler import UpdateContentHandler


@pytest.fixture
def sample_df():
    data = {"A": [1, 2], "B": [3, 4]}
    return pd.DataFrame(data)


@pytest.fixture
def editor_config():
    return EditorConfig(max_columns=10, max_rows=10)


@pytest.fixture
def editor(sample_df, editor_config):
    return InMemoryEditor(table=sample_df.copy(), config=editor_config)


def test_insert_row_handler_instantiation(editor):
    handler = DropContentHandler(editor)
    assert handler.name == "drop_content"


def test_insert_cell_handler_instantiation(editor):
    handler = InsertContentHandler(editor)
    assert handler.name == "insert_cell"


def test_get_content_handler_instantiation(editor):
    handler = GetContentHandler(editor)
    assert handler.name == "get_content"


def test_update_content_handler_instantiation(editor):
    handler = UpdateContentHandler(editor)
    assert handler.name == "update_content"


def test_delete_content_handler_instantiation(editor):
    handler = DeleteContentHandler(editor)
    assert handler.name == "delete_content"


def test_remove_content_handler_instantiation(editor):
    handler = RemoveContentHandler(editor)
    assert handler.name == "remove_content"
