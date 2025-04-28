from pydantic import BaseModel, Field


class EditorConfig(BaseModel):
    """
    Configuration for the editor.
    """

    # The name of the editor
    max_columns: int = Field(
        10,
        description="Maximum number of columns in the editor.",
    )
    max_rows: int = Field(
        5,
        description="Maximum number of rows in the editor.",
    )

    @classmethod
    def default(cls) -> "EditorConfig":
        """
        Returns the default configuration for the editor.
        """
        return cls()  # type: ignore
