import json

from plugins.gtts_text_to_speech import GTTSTextToSpeech
from plugins.auto_tts import AutoTextToSpeech
from plugins.dice import DicePlugin
from plugins.youtube_audio_extractor import YouTubeAudioExtractorPlugin
from plugins.ddg_image_search import DDGImageSearchPlugin
from plugins.ddg_translate import DDGTranslatePlugin
from plugins.spotify import SpotifyPlugin
from plugins.crypto import CryptoPlugin
from plugins.weather import WeatherPlugin
from plugins.ddg_web_search import DDGWebSearchPlugin
from plugins.wolfram_alpha import WolframAlphaPlugin
from plugins.deepl import DeeplTranslatePlugin
from plugins.worldtimeapi import WorldTimeApiPlugin
from plugins.whois_ import WhoisPlugin
from plugins.webshot import WebshotPlugin
from plugins.iplocation import IpLocationPlugin


class PluginManager:
    """
    A class to manage the plugins and call the correct functions
    """

    def __init__(self, config):
        # Get the list of enabled plugins from the config
        enabled_plugins = config.get('plugins', [])
        
        # Map of plugin names to their respective classes
        plugin_mapping = {
            'wolfram': WolframAlphaPlugin,
            'weather': WeatherPlugin,
            'crypto': CryptoPlugin,
            'ddg_web_search': DDGWebSearchPlugin,
            'ddg_translate': DDGTranslatePlugin,
            'ddg_image_search': DDGImageSearchPlugin,
            'spotify': SpotifyPlugin,
            'worldtimeapi': WorldTimeApiPlugin,
            'youtube_audio_extractor': YouTubeAudioExtractorPlugin,
            'dice': DicePlugin,
            'deepl_translate': DeeplTranslatePlugin,
            'gtts_text_to_speech': GTTSTextToSpeech,
            'auto_tts': AutoTextToSpeech,
            'whois': WhoisPlugin,
            'webshot': WebshotPlugin,
            'iplocation': IpLocationPlugin,
        }

        # Initialize the plugins by checking which plugins are enabled in the config
        self.plugins = [plugin_mapping[plugin]() for plugin in enabled_plugins if plugin in plugin_mapping]

    def get_functions_specs(self):
        """
        Return the list of function specs that can be called by the model
        """
        # Collect specs from all plugins
        return [spec for specs in map(lambda plugin: plugin.get_spec(), self.plugins) for spec in specs]

    async def call_function(self, function_name, helper, arguments):
        """
        Call a function based on the name and parameters provided
        """
        # Find the plugin corresponding to the function
        plugin = self.__get_plugin_by_function_name(function_name)
        if not plugin:
            return json.dumps({'error': f'Function {function_name} not found'})
        # Call the plugin function asynchronously and return the result as a JSON response
        return json.dumps(await plugin.execute(function_name, helper, **json.loads(arguments)), default=str)

    def get_plugin_source_name(self, function_name) -> str:
        """
        Return the source name of the plugin
        """
        # Find the plugin corresponding to the function
        plugin = self.__get_plugin_by_function_name(function_name)
        if not plugin:
            return ''
        return plugin.get_source_name()

    def __get_plugin_by_function_name(self, function_name):
        """
        Helper method to get plugin by function name
        """
        # Iterate over all plugins and find the one that has the specified function
        return next((plugin for plugin in self.plugins
                    if function_name in map(lambda spec: spec.get('name'), plugin.get_spec())), None)


# Main code execution (for example, you can create a bot or script here)
def main():
    # Sample configuration for the plugins (the plugins you want to enable)
    plugin_config = {
        'plugins': ['wolfram', 'weather', 'crypto', 'spotify', 'dice', 'gtts_text_to_speech']  # Example plugins
    }

    # Initialize the PluginManager with the configuration
    plugin_manager = PluginManager(plugin_config)

    # Example: Get all function specs (functions that the plugins can handle)
    function_specs = plugin_manager.get_functions_specs()
    print("Function specs:", function_specs)

    # Example: Call a function from a plugin (you need to pass correct function_name and arguments)
    # Assuming 'gtts_text_to_speech' plugin has a function 'text_to_speech'
    function_name = "text_to_speech"
    helper = None  # Assume helper is defined
    arguments = json.dumps({"text": "Hello, this is a test message"})  # Example arguments
    result = plugin_manager.call_function(function_name, helper, arguments)
    print("Function result:", result)


if __name__ == "__main__":
    main()
