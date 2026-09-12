from __future__ import annotations

import inspect
from typing import Any, Callable


def function_has_argument(func: Callable[..., Any], arg_name: str) -> bool:
    """Returns whether or not the given function has a specific parameter"""
    sig = inspect.signature(func)
    return arg_name in sig.parameters


def assert_signatures_in_sync(
    source_func: Callable[..., Any],
    check_func: Callable[..., Any],
    *,
    exclude_params: set[str] = set(),
    description: str = "",
) -> None:
    """Ensure that the signature of the second function matches the first."""

    check_sig = inspect.signature(check_func)
    source_sig = inspect.signature(source_func)

    errors: list[str] = []

    # Local utility to normalize annotations into a comparable string form.
    def _normalize_annotation(a: Any) -> str:
        # Represent missing annotations consistently
        if a is inspect._empty:
            return "<empty>"
        try:
            from typing import get_origin, get_args
        except Exception:
            # Fallback: string normalization
            s = str(a)
            s = s.replace("typing.", "")
            s = s.replace("SequenceNotStr", "List")
            s = s.replace("NoneType", "None")
            return s.replace(" ", "")

        try:
            # Use str() as a base representation, then normalize common differences
            s = str(a)
        except Exception:
            s = repr(a)

        # Normalize typing module prefixes and known equivalent container names
        s = s.replace("typing.", "")
        s = s.replace("SequenceNotStr", "List")
        s = s.replace("NoneType", "None")
        # Remove extra whitespace for consistent comparison
        s = s.replace(" ", "")

        # For unions, ensure ordering does not affect comparison by sorting parts
        origin = get_origin(a)
        if origin is None:
            return s

        if origin is getattr(__import__("typing"), "Union", None) or (hasattr(origin, "__name__") and origin.__name__ == "Union"):
            parts = get_args(a)
            normalized_parts = sorted(_normalize_annotation(p) for p in parts)
            return "Union[" + ",".join(normalized_parts) + "]"

        # Fallback normalized string for other parametrized types
        args = get_args(a)
        if args:
            normalized_args = ",".join(_normalize_annotation(arg) for arg in args)
            # Replace any SequenceNotStr with List in the outer representation
            base = s.split("[")[0]
            base = base.replace("SequenceNotStr", "List").replace("typing.", "")
            return base + "[" + normalized_args + "]"

        return s

    for name, source_param in source_sig.parameters.items():
        if name in exclude_params:
            continue

        custom_param = check_sig.parameters.get(name)
        if not custom_param:
            errors.append(f"the `{name}` param is missing")
            continue

        if _normalize_annotation(custom_param.annotation) != _normalize_annotation(source_param.annotation):
            errors.append(
                f"types for the `{name}` param do not match; source={repr(source_param.annotation)} checking={repr(custom_param.annotation)}"
            )
            continue

    if errors:
        raise AssertionError(
            f"{len(errors)} errors encountered when comparing signatures{description}:\n\n" + "\n\n".join(errors)
        )
