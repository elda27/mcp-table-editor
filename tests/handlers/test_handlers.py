import pandas as pd
import pytest

from mcp_table_editor.editor import Editor, InsertRule
from mcp_table_editor.editor.config import EditorConfig
from mcp_table_editor.handler.delete_content_handler import DeleteContentHandler
from mcp_table_editor.handler.drop_content_handler import DropContentHandler
from mcp_table_editor.handler.get_content_handler import GetContentHandler
from mcp_table_editor.handler.insert_cell_handler import InsertCellHandler
from mcp_table_editor.handler.remove_content_handler import RemoveContentHandler
from mcp_table_editor.handler.update_content_handler import UpdateContentHandler


@pytest.fixture
def sample_df():
    data = {"A": [1, 2], "B": [3, 4]}
    return pd.DataFrame(data)


@pytest.fixture
def editor_config():
    return EditorConfig(max_columns=10, max_rows=10)


@pytest.fixture
def editor(sample_df, editor_config):
    return Editor(table=sample_df.copy(), config=editor_config)


def test_insert_row_handler_instantiation(editor):
    handler = DropContentHandler(editor)
    assert handler.name == "drop_content"
    assert hasattr(handler, "input_schema")


def test_insert_cell_handler_instantiation(editor):
    handler = InsertCellHandler(editor)
    assert handler.name == "insert_cell"
    assert hasattr(handler, "input_schema")


def test_get_content_handler_instantiation(editor):
    handler = GetContentHandler(editor)
    assert handler.name == "get_content"
    assert hasattr(handler, "input_schema")


def test_update_content_handler_instantiation(editor):
    handler = UpdateContentHandler(editor)
    assert handler.name == "update_content"
    assert hasattr(handler, "input_schema")


def test_delete_content_handler_instantiation(editor):
    handler = DeleteContentHandler(editor)
    assert handler.name == "delete_content"
    assert hasattr(handler, "input_schema")


def test_remove_content_handler_instantiation(editor):
    handler = RemoveContentHandler(editor)
    assert handler.name == "remove_content"
    assert hasattr(handler, "input_schema")
