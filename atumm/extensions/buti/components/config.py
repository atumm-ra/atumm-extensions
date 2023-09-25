from atumm.extensions.buti.keys import AtummContainerKeys
from atumm.extensions.config import Config, configure
from buti import BootableComponent, ButiStore


class ConfigComponent(BootableComponent):
    def boot(self, object_store: ButiStore):
        config: Config = configure.build()
        object_store.set(AtummContainerKeys.config, config)
