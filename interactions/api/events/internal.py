"""
These are events dispatched by the client. This is intended as a reference so you know what data to expect for each event.

??? Hint "Example Usage:"
    The event classes outlined here are in `CamelCase` to comply with Class naming convention, however the event names
    are actually in `lower_case_with_underscores` so your listeners should be named as following:

    ```python
    @listen()
    def on_ready():
        # ready events pass no data, so dont have params
        print("Im ready!")

    @listen()
    def on_guild_join(event):
        # guild_create events pass a guild object, expect a single param
        print(f"{event.guild.name} created")
    ```
!!! warning
    While all of these events are documented, not all of them are used, currently.

"""
import re
from typing import Any, Optional, TYPE_CHECKING

import attrs

from interactions.api.events.base import BaseEvent, RawGatewayEvent
from interactions.client.utils.attr_utils import docs

__all__ = (
    "ButtonPressed",
    "Component",
    "Connect",
    "Disconnect",
    "Error",
    "ShardConnect",
    "ShardDisconnect",
    "Login",
    "Ready",
    "Resume",
    "Select",
    "Startup",
    "WebsocketReady",
    "CommandError",
    "ComponentError",
    "AutocompleteError",
    "ModalError",
    "CommandCompletion",
    "ComponentCompletion",
    "AutocompleteCompletion",
    "ModalCompletion",
)


if TYPE_CHECKING:
    from interactions.models.internal.context import (
        ComponentContext,
        Context,
        AutocompleteContext,
        ModalContext,
        InteractionContext,
        PrefixedContext,
        HybridContext,
    )

_event_reg = re.compile("(?<!^)(?=[A-Z])")


@attrs.define(eq=False, order=False, hash=False, kw_only=False)
class Login(BaseEvent):
    """The bot has just logged in."""


@attrs.define(eq=False, order=False, hash=False, kw_only=False)
class Connect(BaseEvent):
    """The bot is now connected to the discord Gateway."""


@attrs.define(eq=False, order=False, hash=False, kw_only=False)
class Resume(BaseEvent):
    """The bot has resumed its connection to the discord Gateway."""


@attrs.define(eq=False, order=False, hash=False, kw_only=False)
class Disconnect(BaseEvent):
    """The bot has just disconnected."""


@attrs.define(eq=False, order=False, hash=False, kw_only=False)
class ShardConnect(Connect):
    """A shard just connected to the discord Gateway."""

    shard_id: int = attrs.field(repr=False, metadata=docs("The ID of the shard"))


@attrs.define(eq=False, order=False, hash=False, kw_only=False)
class ShardDisconnect(Disconnect):
    """A shard just disconnected."""

    shard_id: int = attrs.field(repr=False, metadata=docs("The ID of the shard"))


@attrs.define(eq=False, order=False, hash=False, kw_only=False)
class Startup(BaseEvent):
    """
    The client is now ready for the first time.

    Use this for tasks you want to do upon login, instead of ready, as
    this will only be called once.

    """


@attrs.define(eq=False, order=False, hash=False, kw_only=False)
class Ready(BaseEvent):
    """
    The client is now ready.

    !!! note
        Don't use this event for things that must only happen once, on startup, as this event may be called multiple times.
        Instead, use the `Startup` event

    """


@attrs.define(eq=False, order=False, hash=False, kw_only=False)
class WebsocketReady(RawGatewayEvent):
    """The gateway has reported that it is ready."""

    data: dict = attrs.field(repr=False, metadata=docs("The data from the ready event"))


@attrs.define(eq=False, order=False, hash=False, kw_only=False)
class Component(BaseEvent):
    """Dispatched when a user uses a Component."""

    ctx: "ComponentContext" = attrs.field(repr=False, metadata=docs("The context of the interaction"))


@attrs.define(eq=False, order=False, hash=False, kw_only=False)
class ButtonPressed(Component):
    """Dispatched when a user uses a Button."""


@attrs.define(eq=False, order=False, hash=False, kw_only=False)
class Select(Component):
    """Dispatched when a user uses a Select."""


@attrs.define(eq=False, order=False, hash=False, kw_only=True)
class CommandCompletion(BaseEvent):
    """Dispatched after the library ran any command callback."""

    ctx: "InteractionContext | HybridContext" = attrs.field(
        repr=False, metadata=docs("The command context")
    )


@attrs.define(eq=False, order=False, hash=False, kw_only=True)
class ComponentCompletion(BaseEvent):
    """Dispatched after the library ran any component callback."""

    ctx: "ComponentContext" = attrs.field(repr=False, metadata=docs("The component context"))


@attrs.define(eq=False, order=False, hash=False, kw_only=True)
class AutocompleteCompletion(BaseEvent):
    """Dispatched after the library ran any autocomplete callback."""

    ctx: "AutocompleteContext" = attrs.field(repr=False, metadata=docs("The autocomplete context"))


@attrs.define(eq=False, order=False, hash=False, kw_only=True)
class ModalCompletion(BaseEvent):
    """Dispatched after the library ran any modal callback."""

    ctx: "ModalContext" = attrs.field(repr=False, metadata=docs("The modal context"))


@attrs.define(eq=False, order=False, hash=False, kw_only=True)
class _Error(BaseEvent):
    error: Exception = attrs.field(repr=False, metadata=docs("The error that was encountered"))
    args: tuple[Any] = attrs.field(repr=False, factory=tuple)
    kwargs: dict[str, Any] = attrs.field(repr=False, factory=dict)


@attrs.define(eq=False, order=False, hash=False, kw_only=True)
class Error(_Error):
    """Dispatched when the library encounters an error."""

    source: str = attrs.field(repr=False, metadata=docs("The source of the error"))
    ctx: Optional["Context"] = attrs.field(repr=False, default=None, metadata=docs("The Context, if one was active"))


@attrs.define(eq=False, order=False, hash=False, kw_only=True)
class CommandError(_Error):
    """Dispatched when the library encounters an error in a command."""

    ctx: "InteractionContext | PrefixedContext | HybridContext" = attrs.field(
        repr=False, metadata=docs("The command context")
    )


@attrs.define(eq=False, order=False, hash=False, kw_only=True)
class ComponentError(_Error):
    """Dispatched when the library encounters an error in a component."""

    ctx: "ComponentContext" = attrs.field(repr=False, metadata=docs("The component context"))


@attrs.define(eq=False, order=False, hash=False, kw_only=True)
class AutocompleteError(_Error):
    """Dispatched when the library encounters an error in an autocomplete."""

    ctx: "AutocompleteContext" = attrs.field(repr=False, metadata=docs("The autocomplete context"))


@attrs.define(eq=False, order=False, hash=False, kw_only=True)
class ModalError(_Error):
    """Dispatched when the library encounters an error in a modal."""

    ctx: "ModalContext" = attrs.field(repr=False, metadata=docs("The modal context"))
