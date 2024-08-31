import asyncio
import logging
from zigpy.config import CONF_DEVICE, CONF_DEVICE_PATH, CONF_DEVICE_BAUDRATE
from zha.application.gateway import Gateway
from zha.application.helpers import ZHAData, ZHAConfiguration, QuirksConfiguration, CoordinatorConfiguration, DeviceOptions

class GatewayManager:
    def __init__(self, config):
        self.config = config
        self.gateway = None

    async def create(self):
        """Initialize and start the Zigbee gateway."""
        # Prepare the Zigbee gateway configuration
        zigpy_config = {
            CONF_DEVICE: {
                CONF_DEVICE_PATH: self.config['device']['path'],
                CONF_DEVICE_BAUDRATE: self.config['device']['baudrate'],
            }
        }

        # Initialize quirks configuration
        quirks_config = QuirksConfiguration(
            enabled=False,
            custom_quirks_path=None
        )

        # Initialize coordinator configuration
        coordinator_config = CoordinatorConfiguration(
            path=self.config['device']['path'],
            baudrate=self.config['device']['baudrate'],
            flow_control=None,
            radio_type=self.config['device']['radio_type']
        )

        # Initialize device options
        device_options = DeviceOptions(
            enable_identify_on_join=True,
            consider_unavailable_mains=120,
            consider_unavailable_battery=240
        )

        # Create the necessary configuration object
        zha_config = ZHAConfiguration(
            light_options=None,
            device_options=device_options,
            alarm_control_panel_options=None,
            coordinator_configuration=coordinator_config,
            quirks_configuration=quirks_config,
            device_overrides=None,
        )

        # Create an instance of ZHAData with both required arguments
        zha_data = ZHAData(
            zigpy_config=zigpy_config,
            config=zha_config,
        )

        # Initialize the Gateway with the structured config
        self.gateway = await Gateway.async_from_config(zha_data)

        # Initialize the Gateway
        try:
            await self.gateway.async_initialize()
            logging.info("Zigbee gateway successfully initialized.")
        except Exception as e:
            logging.error(f"Failed to start the Zigbee gateway: {e}")
            raise

    async def permit_join(self, enable=True, duration=60):
        """Enable or disable device joining."""
        if enable:
            logging.info(f"Permitting join for {duration} seconds...")
            await self.gateway.application_controller.permit(duration)
        else:
            logging.info("Disabling join.")
            await self.gateway.application_controller.permit(0)
        logging.info("Permit join status updated.")

    async def remove_device(self, ieee_address):
        """Remove a device from the network using its IEEE address."""
        device = self.gateway.devices.get(ieee_address)
        if device:
            logging.info(f"Removing device with IEEE address: {ieee_address}")
            await self.gateway.application_controller.remove(device)
            logging.info(f"Device {ieee_address} removed from the network.")
        else:
            logging.warning(f"Device with IEEE address {ieee_address} not found.")

    def list_devices(self):
        """List all devices currently connected to the Zigbee network."""
        logging.info("Listing all connected devices:")
        for ieee, device in self.gateway.devices.items():
            logging.info(f"Device IEEE: {ieee}, Model: {device.model}, Manufacturer: {device.manufacturer}")
