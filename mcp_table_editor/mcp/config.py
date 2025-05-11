from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class McpSettings(BaseSettings):
    """Settings for the MCP Table Editor."""

    model_config = SettingsConfigDict(env_prefix="MTE_")
    # The URL of the MCP server
    # host: str = Field(
    #     default="http://localhost:8000",
    #     description="The URL of the MCP server.",
    # )

    # Web settings
    host: str = Field(
        default="localhost",
        description="The host for the MCP server.",
    )
    port: int = Field(
        default=8000,
        description="The port for the MCP server.",
    )

    # The path to the MCP table editor
    path: str = Field(
        default="/mcp",
        description="The path to the MCP table editor.",
    )
    debug: bool = Field(
        default=True,
        description="Whether to enable debug mode.",
    )

    json_response: bool = Field(
        False,
        description="Whether to use JSON response format.",
    )
    log_level: str = Field(
        "INFO",
        description="The log level for the MCP server.",
    )
