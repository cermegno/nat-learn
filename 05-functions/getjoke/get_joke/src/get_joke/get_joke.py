import logging

from pydantic import Field

from nat.plugin_api import Builder
from nat.plugin_api import FunctionBaseConfig
from nat.plugin_api import FunctionInfo
from nat.plugin_api import LLMFrameworkEnum
from nat.plugin_api import register_function

logger = logging.getLogger(__name__)


class GetJokeFunctionConfig(FunctionBaseConfig, name="get_joke"):
    #prefix: str = Field(default="Echo:", description="Prefix to add before the echoed text.")
    mood: str = Field(default="bad", description="Bad if not in the mood for jokes.")
    capitalize: bool = Field(default=False, description="Whether to capitalize the response text.")


@register_function(config_type=GetJokeFunctionConfig, framework_wrappers=[LLMFrameworkEnum.LANGCHAIN])
async def get_joke_function(config: GetJokeFunctionConfig, builder: Builder):
    """
    Registers the function. It will be addressable via `get_joke` in the configuration.

    Args:
        config (GetJokeFunctionConfig): The configuration for the function.
        builder (Builder): The builder object.

    Returns:
        FunctionInfo: The function info object for the function.
    """

    # Define the function that will be registered.
    async def _get_joke(mood: str, capitalize: bool) -> str:
        """
        Takes a mood and capitalize flag and returns a joke or a message based on the mood.

        Args:
            mood (str): The user's mood.
            capitalize (bool): Whether to capitalize the response.

        Returns:
            str: The joke or a message based on the mood.
        """
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "What do you call a fake noodle? An impasta!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "How does a penguin build its house? Igloos it together!",
            "Why did the bicycle fall over? Because it was two-tired!"
            ]
        if mood == "bad":
            joke = "I am not in the mood for jokes right now."
        else:
            # pick a random joke from the list
            import random
            joke = random.choice(jokes)

        return joke.upper() if capitalize else joke

    # The callable is wrapped in a FunctionInfo object.
    # The description parameter is used to describe the function.
    yield FunctionInfo.from_fn(_get_joke, description=_get_joke.__doc__)
