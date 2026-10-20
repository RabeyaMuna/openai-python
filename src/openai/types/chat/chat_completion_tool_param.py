# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias

from .chat_completion_custom_tool_param import ChatCompletionCustomToolParam
from .chat_completion_function_tool_param import ChatCompletionFunctionToolParam
from .chat_completion_tool_param import ChatCompletionToolParam

__all__ = ["ChatCompletionToolParam"]

ChatCompletionToolParam: TypeAlias = Union[ChatCompletionFunctionToolParam, ChatCompletionCustomToolParam]
